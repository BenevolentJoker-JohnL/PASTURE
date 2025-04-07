#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pasture/pasture_distributed.py

PASTURE Framework: Pipeline for Analytical Synthesis of Textual Unification and Resource Enhancement
Distributed Processing Extension with Celery and Redis

This extension module provides distributed processing capabilities for PASTURE:
- Celery-based task processing for horizontal scaling
- Redis-backed result storage and task queue management
- Distributed pipeline execution across multiple workers
"""

import asyncio
import importlib.util
import json
import logging
import os
import sys
import time
import traceback
from typing import Any, Dict, List, Optional, Tuple, Union, Callable

from . import Config, FileCache, ModelManager, AnalysisStep, Pipeline

# Check if Celery is installed
celery_installed = importlib.util.find_spec("celery") is not None
redis_installed = importlib.util.find_spec("redis") is not None

if not celery_installed or not redis_installed:
    logging.warning(
        "Distributed extensions require Celery and Redis. "
        "Install with: pip install 'pasture[celery]'"
    )

# Configure logging
logger = logging.getLogger(__name__)

# Only define Celery-dependent code if it's installed
if celery_installed and redis_installed:
    import celery
    from celery import Celery
    from celery.result import AsyncResult
    
    ###########################################
    ## CELERY APPLICATION                   ##
    ###########################################
    
    class PastureTaskApp:
        """Singleton for the Celery application used by PASTURE tasks"""
        _instance = None
        _app = None
        
        def __new__(cls, broker_url=None, backend_url=None):
            if cls._instance is None:
                cls._instance = super(PastureTaskApp, cls).__new__(cls)
                cls._instance._init_app(broker_url, backend_url)
            return cls._instance
        
        def _init_app(self, broker_url=None, backend_url=None):
            """Initialize the Celery application"""
            broker = broker_url or os.environ.get('BROKER_URL', 'redis://localhost:6379/0')
            backend = backend_url or os.environ.get('RESULT_BACKEND', broker)
            
            self._app = Celery(
                'pasture_tasks',
                broker=broker,
                backend=backend
            )
            
            self._app.conf.update(
                task_serializer='json',
                accept_content=['json'],
                result_serializer='json',
                timezone='UTC',
                enable_utc=True,
                task_track_started=True,
                worker_send_task_events=True
            )
            
            # Register basic tasks
            self._register_tasks()
        
        def _register_tasks(self):
            """Register PASTURE tasks with Celery"""
            # Tasks are defined below using the app decorator
            pass
        
        @property
        def app(self):
            """Get the Celery application"""
            return self._app
    
    # Create default Celery app
    celery_app = PastureTaskApp().app
    
    ###########################################
    ## CELERY TASKS                         ##
    ###########################################
    
    @celery_app.task(bind=True, name='pasture.process_model')
    def process_model(self, model_name, prompt, options=None, config_dict=None):
        """
        Process a model request as a Celery task.
        
        Args:
            model_name: Name of the model to use
            prompt: Prompt string to send to the model
            options: Model generation options
            config_dict: Configuration dictionary
            
        Returns:
            Dict: Model output and metadata
        """
        # Need to use asyncio.run because Celery tasks are synchronous
        # but our PASTURE code is asynchronous
        try:
            return asyncio.run(_process_model_async(
                model_name, prompt, options, config_dict
            ))
        except Exception as e:
            logger.error(f"Error in Celery task: {e}")
            traceback.print_exc()
            return {
                "error": "celery_task_error",
                "response": f"Error in Celery task: {str(e)}",
                "execution_time": 0
            }
    
    async def _process_model_async(
        model_name: str, 
        prompt: str, 
        options: Optional[Dict] = None,
        config_dict: Optional[Dict] = None
    ) -> Dict:
        """Async implementation for the process_model Celery task"""
        start_time = time.time()
        
        # Create config from dict or use defaults
        config = Config(**(config_dict or {}))
        
        # Initialize cache and model manager
        cache = FileCache(config.cache_dir)
        model_manager = ModelManager(config, cache)
        
        try:
            # Generate response from model
            result = await model_manager.generate_with_model(
                model_name=model_name,
                prompt=prompt,
                options=options
            )
            
            execution_time = time.time() - start_time
            
            # Add execution metadata
            if "execution_time" not in result:
                result["execution_time"] = execution_time
                
            return result
        finally:
            # Clean up resources
            await model_manager.close()
    
    @celery_app.task(bind=True, name='pasture.run_pipeline_step')
    def run_pipeline_step(self, step_name, step_config, data, config_dict=None):
        """
        Run a single pipeline step as a Celery task.
        
        Args:
            step_name: Name of the step
            step_config: Configuration for the step (model, prompt template, etc.)
            data: Input data for the step
            config_dict: Configuration dictionary
            
        Returns:
            Dict: Step output and metadata
        """
        return asyncio.run(_run_pipeline_step_async(
            step_name, step_config, data, config_dict
        ))
    
    async def _run_pipeline_step_async(
        step_name: str,
        step_config: Dict,
        data: Dict,
        config_dict: Optional[Dict] = None
    ) -> Dict:
        """Async implementation for the run_pipeline_step Celery task"""
        start_time = time.time()
        
        # Create config from dict or use defaults
        config = Config(**(config_dict or {}))
        
        # Initialize cache and model manager
        cache = FileCache(config.cache_dir)
        model_manager = ModelManager(config, cache)
        
        try:
            # Create and execute the step
            step = CeleryModelStep(
                model_manager=model_manager,
                model_name=step_config.get("model_name"),
                prompt_template=step_config.get("prompt_template"),
                options=step_config.get("options", {"temperature": 0.7}),
                fallback_models=step_config.get("fallback_models", []),
                use_patching=step_config.get("use_patching"),
                max_patching_attempts=step_config.get("max_patching_attempts"),
                patching_prompt=step_config.get("patching_prompt")
            )
            
            result = await step.execute(data)
            
            execution_time = time.time() - start_time
            
            # Add total execution time (including Celery overhead)
            result["total_time"] = execution_time
            if "time" in result:
                result["queue_time"] = execution_time - result["time"]
                
            return result
        finally:
            # Clean up resources
            await model_manager.close()
    
    ###########################################
    ## DISTRIBUTED PIPELINE COMPONENTS      ##
    ###########################################
    
    class CeleryModelStep(AnalysisStep):
        """Pipeline step that delegates processing to a Celery worker"""
        
        def __init__(self, 
                    model_manager: ModelManager,
                    model_name: str, 
                    prompt_template: str,
                    options: Optional[Dict[str, Any]] = None,
                    fallback_models: Optional[List[str]] = None,
                    task_timeout: int = 180,
                    use_patching: Optional[bool] = None,
                    max_patching_attempts: Optional[int] = None,
                    patching_prompt: Optional[str] = None):
            self.model_manager = model_manager
            self.model_name = model_name
            self.prompt_template = prompt_template
            self.options = options or {"temperature": 0.7}
            self.fallback_models = fallback_models or []
            self.task_timeout = task_timeout
            
            # JSON patching configuration
            self.use_patching = use_patching if use_patching is not None else model_manager.config.json_patching.enabled
            self.max_patching_attempts = max_patching_attempts or model_manager.config.json_patching.max_attempts
            self.patching_prompt = patching_prompt or model_manager.config.json_patching.patching_prompt
        
        def _format_prompt(self, data: Dict[str, Any]) -> str:
            """Format prompt template with data, handling errors"""
            try:
                return self.prompt_template.format(**data)
            except KeyError as e:
                logger.error(f"Error formatting prompt: missing key {e}")
                # Create a safe fallback prompt
                prompt_parts = []
                if "query" in data:
                    prompt_parts.append(f"Query: {data['query']}")
                
                # Add previous analysis results if available
                for key in data:
                    if key in ["economic", "social", "ethical"]:
                        if isinstance(data[key], dict) and "response" in data[key]:
                            prompt_parts.append(f"{key.capitalize()} analysis: {data[key]['response']}")
                
                prompt = "\n\n".join(prompt_parts)
                
                # Add integration request if this seems to be an integration step
                if "combine" in self.prompt_template.lower() or "integrat" in self.prompt_template.lower():
                    prompt += "\n\nPlease integrate these analyses into a cohesive response."
                    
                return prompt
        
        async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
            """Execute the step by submitting a task to Celery"""
            start_time = time.time()
            
            try:
                # Check model health
                is_healthy = await self.model_manager.check_model_health(self.model_name)
                if not is_healthy and self.fallback_models:
                    logger.warning(f"Model {self.model_name} is unhealthy, trying fallbacks")
                    return await self.get_fallback(data)
                
                # Format the prompt
                prompt = self._format_prompt(data)
                
                logger.info(f"Submitting Celery task for model {self.model_name}")
                
                # Submit task to Celery
                task: AsyncResult = process_model.delay(
                    self.model_name,
                    prompt,
                    self.options,
                    self.model_manager.config.__dict__ if not hasattr(self.model_manager.config, 'model_dump') else self.model_manager.config.model_dump()
                )
                
                # Wait for the task to complete with timeout
                try:
                    result = task.get(timeout=self.task_timeout)
                except celery.exceptions.TimeoutError:
                    logger.error(f"Celery task timed out after {self.task_timeout}s")
                    if self.fallback_models:
                        logger.info(f"Trying fallback models for {self.model_name}")
                        return await self.get_fallback(data)
                    return {
                        "output": {"response": "Task timed out", "error": "celery_timeout"},
                        "time": self.task_timeout,
                        "model": self.model_name,
                        "status": "error",
                        "error_details": f"Task timed out after {self.task_timeout}s"
                    }
                    
                execution_time = time.time() - start_time
                
                # Check for errors
                if "error" in result:
                    logger.error(f"Error from {self.model_name}: {result['error']}")
                    if self.fallback_models:
                        logger.info(f"Trying fallback models for {self.model_name}")
                        return await self.get_fallback(data)
                
                # Process the result
                status = "success" if "error" not in result else "error"
                
                # For JSON patching, we could patch the output here if use_patching is enabled
                # This would require sending the output back to the model for fixing
                # We'll keep this simple for now and leave JSON patching to the user's code
                
                return {
                    "output": result,
                    "time": execution_time,
                    "model": self.model_name,
                    "status": status,
                    "prompt": prompt
                }
            
            except Exception as e:
                logger.error(f"Error in {self.model_name} step: {e}")
                traceback.print_exc()
                
                if self.fallback_models:
                    logger.info(f"Trying fallback models after exception in {self.model_name}")
                    return await self.get_fallback(data)
                    
                return {
                    "output": {"response": f"Error: {str(e)}", "error": "execution_error"},
                    "time": time.time() - start_time,
                    "model": self.model_name,
                    "status": "error",
                    "error_details": str(e)
                }
        
        async def get_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
            """Try fallback models when primary model fails"""
            for fallback_model in self.fallback_models:
                logger.info(f"Trying fallback model {fallback_model}")
                
                # Format prompt
                prompt = self._format_prompt(data)
                
                try:
                    # Check health of fallback model
                    is_healthy = await self.model_manager.check_model_health(fallback_model)
                    if not is_healthy:
                        logger.warning(f"Fallback model {fallback_model} is unhealthy, skipping")
                        continue
                    
                    # Submit task to Celery with fallback model
                    task: AsyncResult = process_model.delay(
                        fallback_model,
                        prompt,
                        self.options,
                        self.model_manager.config.__dict__ if not hasattr(self.model_manager.config, 'model_dump') else self.model_manager.config.model_dump()
                    )
                    
                    # Wait for the task to complete
                    result = task.get(timeout=self.task_timeout)
                    
                    # Check for success
                    if "error" not in result:
                        logger.info(f"Fallback model {fallback_model} succeeded")
                        return {
                            "output": result,
                            "time": result.get("execution_time", 0),
                            "model": fallback_model,
                            "status": "success",
                            "prompt": prompt,
                            "fallback": True
                        }
                except Exception as e:
                    logger.error(f"Fallback {fallback_model} failed: {e}")
                    continue
            
            # All fallbacks failed
            logger.error(f"All fallback models failed for {self.model_name}")
            return {
                "output": {"response": "All models failed to generate a response", "error": "all_models_failed"},
                "time": 0,
                "model": self.model_name,
                "status": "error",
                "fallback": True
            }
    
    class DistributedPipeline:
        """Pipeline implementation that distributes steps across Celery workers"""
        
        def __init__(self, steps: List[Tuple[str, Union[Dict, CeleryModelStep], List[str]]], config: Config):
            """
            Initialize a distributed pipeline.
            
            Args:
                steps: List of (name, step_config_or_instance, dependencies) tuples
                       where step_config is a dictionary with model_name, prompt_template, etc.
                       or a CeleryModelStep instance
                config: Configuration settings
            """
            self.steps = steps
            self.config = config
        
        async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
            """
            Run the pipeline with the given input data.
            
            This distributes each step to a Celery worker.
            """
            results = {}
            data = input_data.copy()
            
            # Sequential execution of steps (could be parallelized in the future)
            for name, step_config_or_instance, dependencies in self.steps:
                logger.info(f"Running distributed step: {name}")
                
                # Check dependencies
                missing_deps = [dep for dep in dependencies if dep not in results]
                if missing_deps:
                    logger.error(f"Step {name} missing dependencies: {missing_deps}")
                    results[name] = {
                        "output": {"response": f"Missing dependencies: {missing_deps}", "error": "missing_dependencies"},
                        "time": 0,
                        "status": "error",
                        "model": step_config_or_instance.get("model_name", "unknown") if isinstance(step_config_or_instance, dict) else step_config_or_instance.model_name
                    }
                    continue
                
                # Execute the step
                try:
                    # Create a robust version of the data
                    robust_data = input_data.copy()
                    
                    # Add results from previous steps
                    for prev_name, prev_result in results.items():
                        prev_output = prev_result.get("output", {})
                        if not isinstance(prev_output, dict):
                            prev_output = {"response": str(prev_output)}
                        robust_data[prev_name] = prev_output
                    
                    # If step_config_or_instance is already a CeleryModelStep instance, use it directly
                    if isinstance(step_config_or_instance, CeleryModelStep):
                        result = await step_config_or_instance.execute(robust_data)
                        results[name] = result
                    else:
                        # Otherwise, it's a config dict - submit task to Celery
                        step_config = step_config_or_instance
                        
                        task: AsyncResult = run_pipeline_step.delay(
                            name,
                            step_config,
                            robust_data,
                            self.config.__dict__ if not hasattr(self.config, 'model_dump') else self.config.model_dump()
                        )
                        
                        # Wait for completion with timeout
                        try:
                            task_timeout = step_config.get("task_timeout", 180)
                            result = task.get(timeout=task_timeout)
                            results[name] = result
                        except celery.exceptions.TimeoutError:
                            logger.error(f"Step {name} timed out after {task_timeout}s")
                            results[name] = {
                                "output": {"response": "Task timed out", "error": "celery_timeout"},
                                "time": task_timeout,
                                "model": step_config.get("model_name", "unknown"),
                                "status": "error"
                            }
                    
                    # Update data with successful results
                    if results[name].get("status") == "success":
                        data[name] = results[name]["output"]
                    else:
                        # Add placeholder for failed steps
                        data[name] = {"response": f"Step {name} failed", "error": "step_failed"}
                    
                    logger.info(f"Completed step {name} with status: {results[name].get('status', 'unknown')}")
                
                except Exception as e:
                    logger.error(f"Error executing step {name}: {e}")
                    traceback.print_exc()
                    results[name] = {
                        "output": {"response": f"Error: {str(e)}", "error": "execution_error"},
                        "time": 0,
                        "status": "error"
                    }
            
            # Count successful steps
            success_count = sum(1 for r in results.values() if r.get("status") == "success")
            
            return {
                "results": results,
                "total_time": sum(r.get("time", 0) for r in results.values()),
                "success_count": success_count,
                "total_count": len(results),
                "success_rate": f"{success_count}/{len(results)}"
            }
    
    class CelerychatModelStep(CeleryModelStep):
        """Pipeline step for chat-based interaction using Celery"""
        
        def __init__(self, 
                    model_manager: ModelManager,
                    model_name: str,
                    system_prompt: Optional[str] = None,
                    options: Optional[Dict[str, Any]] = None,
                    fallback_models: Optional[List[str]] = None,
                    task_timeout: int = 180,
                    use_patching: Optional[bool] = None,
                    max_patching_attempts: Optional[int] = None,
                    patching_prompt: Optional[str] = None):
            super().__init__(
                model_manager=model_manager,
                model_name=model_name,
                prompt_template="",  # Not used for chat
                options=options,
                fallback_models=fallback_models,
                task_timeout=task_timeout,
                use_patching=use_patching,
                max_patching_attempts=max_patching_attempts,
                patching_prompt=patching_prompt
            )
            self.system_prompt = system_prompt
        
        def _prepare_messages(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
            """Prepare messages for the chat API"""
            messages = []
            
            # Add system message if provided
            if self.system_prompt:
                messages.append({"role": "system", "content": self.system_prompt})
            
            # If data contains a 'messages' field, use that directly
            if "messages" in data and isinstance(data["messages"], list):
                # Filter out system messages if we already added one
                if self.system_prompt:
                    user_assistant_messages = [m for m in data["messages"] if m.get("role") != "system"]
                    messages.extend(user_assistant_messages)
                else:
                    messages.extend(data["messages"])
                return messages
            
            # Create a user message from the query
            if "query" in data:
                messages.append({"role": "user", "content": data["query"]})
            
            # Add context from previous steps if available
            context_parts = []
            for key in data:
                if key != "query" and isinstance(data[key], dict):
                    if "response" in data[key]:
                        context_parts.append(f"{key.capitalize()} analysis: {data[key]['response']}")
            
            if context_parts and not self.system_prompt:
                # Add context as a system message if we don't already have one
                context = "\n\n".join(context_parts)
                messages.insert(0, {"role": "system", "content": f"Context:\n{context}"})
            
            return messages
        
        async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
            """Execute the step by submitting a chat task to Celery"""
            start_time = time.time()
            
            try:
                # Check model health
                is_healthy = await self.model_manager.check_model_health(self.model_name)
                if not is_healthy and self.fallback_models:
                    logger.warning(f"Model {self.model_name} is unhealthy, trying fallbacks")
                    return await self.get_fallback(data)
                
                # Prepare messages
                messages = self._prepare_messages(data)
                
                logger.info(f"Submitting Celery chat task for model {self.model_name}")
                
                # TODO: Implement a specific chat task for Celery
                # For now, we'll implement a simple version by converting chat to a prompt
                
                # Convert chat messages to a formatted prompt
                prompt = self._messages_to_prompt(messages)
                
                # Submit task to Celery
                task: AsyncResult = process_model.delay(
                    self.model_name,
                    prompt,
                    self.options,
                    self.model_manager.config.__dict__ if not hasattr(self.model_manager.config, 'model_dump') else self.model_manager.config.model_dump()
                )
                
                # Wait for the task to complete with timeout
                try:
                    result = task.get(timeout=self.task_timeout)
                except celery.exceptions.TimeoutError:
                    logger.error(f"Celery chat task timed out after {self.task_timeout}s")
                    if self.fallback_models:
                        logger.info(f"Trying fallback models for {self.model_name}")
                        return await self.get_fallback(data)
                    return {
                        "output": {"message": {"content": "Task timed out"}, "error": "celery_timeout"},
                        "time": self.task_timeout,
                        "model": self.model_name,
                        "status": "error",
                        "error_details": f"Task timed out after {self.task_timeout}s"
                    }
                    
                execution_time = time.time() - start_time
                
                # Check for errors
                if "error" in result:
                    logger.error(f"Error from {self.model_name} chat: {result['error']}")
                    if self.fallback_models:
                        logger.info(f"Trying fallback models for {self.model_name}")
                        return await self.get_fallback(data)
                
                # Process the result
                status = "success" if "error" not in result else "error"
                
                # Convert to chat response format
                if "response" in result:
                    chat_result = {
                        "message": {
                            "role": "assistant",
                            "content": result["response"]
                        }
                    }
                    for key in result:
                        if key != "response":
                            chat_result[key] = result[key]
                    result = chat_result
                
                return {
                    "output": result,
                    "time": execution_time,
                    "model": self.model_name,
                    "status": status,
                    "messages": messages
                }
            
            except Exception as e:
                logger.error(f"Error in {self.model_name} chat step: {e}")
                traceback.print_exc()
                
                if self.fallback_models:
                    logger.info(f"Trying fallback models after exception in {self.model_name}")
                    return await self.get_fallback(data)
                    
                return {
                    "output": {"message": {"content": f"Error: {str(e)}"}, "error": "execution_error"},
                    "time": time.time() - start_time,
                    "model": self.model_name,
                    "status": "error",
                    "error_details": str(e)
                }
        
        def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
            """Convert chat messages to a formatted prompt"""
            prompt_parts = []
            
            for message in messages:
                role = message.get("role", "")
                content = message.get("content", "")
                
                if role == "system":
                    prompt_parts.append(f"System: {content}")
                elif role == "user":
                    prompt_parts.append(f"User: {content}")
                elif role == "assistant":
                    prompt_parts.append(f"Assistant: {content}")
                else:
                    prompt_parts.append(f"{role.capitalize()}: {content}")
            
            return "\n\n".join(prompt_parts) + "\n\nAssistant:"
        
        async def get_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
            """Try fallback models when primary chat model fails"""
            for fallback_model in self.fallback_models:
                logger.info(f"Trying fallback model {fallback_model}")
                
                # Prepare messages
                messages = self._prepare_messages(data)
                
                # Convert to prompt for now
                prompt = self._messages_to_prompt(messages)
                
                try:
                    # Check health of fallback model
                    is_healthy = await self.model_manager.check_model_health(fallback_model)
                    if not is_healthy:
                        logger.warning(f"Fallback model {fallback_model} is also unhealthy, skipping")
                        continue
                    
                    # Submit task to Celery with fallback model
                    task: AsyncResult = process_model.delay(
                        fallback_model,
                        prompt,
                        self.options,
                        self.model_manager.config.__dict__ if not hasattr(self.model_manager.config, 'model_dump') else self.model_manager.config.model_dump()
                    )
                    
                    # Wait for the task to complete
                    result = task.get(timeout=self.task_timeout)
                    
                    # Check for success
                    if "error" not in result:
                        logger.info(f"Fallback model {fallback_model} succeeded")
                        
                        # Convert to chat response format
                        if "response" in result:
                            chat_result = {
                                "message": {
                                    "role": "assistant",
                                    "content": result["response"]
                                }
                            }
                            for key in result:
                                if key != "response":
                                    chat_result[key] = result[key]
                            result = chat_result
                        
                        return {
                            "output": result,
                            "time": result.get("execution_time", 0),
                            "model": fallback_model,
                            "status": "success",
                            "messages": messages,
                            "fallback": True
                        }
                except Exception as e:
                    logger.error(f"Fallback {fallback_model} chat failed: {e}")
                    continue
            
            # All fallbacks failed
            logger.error(f"All fallback models failed for {self.model_name} chat")
            return {
                "output": {
                    "message": {"content": "All models failed to generate a chat response"},
                    "error": "all_models_failed"
                },
                "time": 0,
                "model": self.model_name,
                "status": "error",
                "fallback": True
            }

else:
    # Provide placeholder classes for code that might import them
    class CeleryModelStep:
        """Placeholder for CeleryModelStep when Celery is not installed"""
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "CeleryModelStep requires Celery and Redis. "
                "Install with: pip install 'pasture[celery]'"
            )
    
    class DistributedPipeline:
        """Placeholder for DistributedPipeline when Celery is not installed"""
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "DistributedPipeline requires Celery and Redis. "
                "Install with: pip install 'pasture[celery]'"
            )
    
    class CelerychatModelStep:
        """Placeholder for CelerychatModelStep when Celery is not installed"""
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "CelerychatModelStep requires Celery and Redis. "
                "Install with: pip install 'pasture[celery]'"
            )
    
    celery_app = None
    process_model = None
    run_pipeline_step = None
