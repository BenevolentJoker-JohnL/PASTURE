#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
examples/celery_pipeline.py

Example demonstrating how to use PASTURE with Celery for distributed processing.
PASTURE: Pipeline for Analytical Synthesis of Textual Unification and Resource Enhancement

This script shows how to implement a distributed pipeline using Celery workers
to process different steps of analysis across multiple machines or processes.

Note: This example requires installing PASTURE with Celery support:
      pip install "pasture[celery]"
"""

import asyncio
import logging
import os
from pathlib import Path

# Check if Celery is installed
try:
    import celery
    from pasture import (
        Config, 
        FileCache, 
        ModelManager
    )
    from pasture.pasture_distributed import (
        CeleryModelStep, 
        DistributedPipeline,
        celery_app
    )
    CELERY_INSTALLED = True
except ImportError:
    CELERY_INSTALLED = False
    from pasture import Config
    logging.error(
        "Celery components not available. Install with: pip install 'pasture[celery]'"
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def run_distributed_pipeline():
    """Run a distributed pipeline using Celery workers."""
    if not CELERY_INSTALLED:
        logger.error("Cannot run distributed pipeline without Celery")
        return
    
    # Create configuration
    config = Config(
        cache_dir="./cache",
        verbose_output=True,
        debug_mode=True,
        request_timeout=180.0  # Longer timeout for distributed processing
    )
    
    # Define broker and backend URLs (use environment variables or defaults)
    broker_url = os.environ.get('BROKER_URL', 'redis://localhost:6379/0')
    result_backend = os.environ.get('RESULT_BACKEND', broker_url)
    
    # Update Celery configuration (optional)
    celery_app.conf.update(
        broker_url=broker_url,
        result_backend=result_backend,
        task_track_started=True,
        worker_send_task_events=True,
        task_send_sent_event=True
    )
    
    # Initialize cache and model manager for local tasks
    cache = FileCache(config.cache_dir)
    model_manager = ModelManager(config, cache)
    
    # Define steps for distributed pipeline with CeleryModelStep instances
    
    # Economic analysis step
    economic_step = CeleryModelStep(
        model_manager=model_manager,
        model_name="llama3",
        prompt_template="""
        Analyze the economic implications of the following topic:
        
        Topic: {query}
        
        Focus on market impacts, financial considerations, and economic trends.
        Provide a detailed economic analysis.
        """,
        options={"temperature": 0.7},
        task_timeout=180
    )
    
    # Social analysis step (runs in parallel with economic)
    social_step = CeleryModelStep(
        model_manager=model_manager,
        model_name="mistral",
        prompt_template="""
        Analyze the social implications of the following topic:
        
        Topic: {query}
        
        Focus on societal impacts, cultural considerations, and community effects.
        Provide a detailed social analysis.
        """,
        options={"temperature": 0.7},
        task_timeout=180
    )
    
    # Integration step (depends on both analyses)
    integration_step = CeleryModelStep(
        model_manager=model_manager,
        model_name="llama3",
        prompt_template="""
        Integrate the following analyses into a cohesive response:
        
        Topic: {query}
        
        Economic Analysis: {economic[response]}
        
        Social Analysis: {social[response]}
        
        Provide a balanced, comprehensive integration of these perspectives.
        """,
        options={"temperature": 0.5},
        task_timeout=240
    )
    
    # Create distributed pipeline with steps and dependencies
    pipeline = DistributedPipeline(
        steps=[
            ("economic", economic_step, []),
            ("social", social_step, []),
            ("integration", integration_step, ["economic", "social"])
        ],
        config=config
    )
    
    try:
        # Define input data
        input_data = {
            "query": "The impact of artificial intelligence on modern society."
        }
        
        logger.info(f"Running distributed pipeline for query: {input_data['query']}")
        logger.info(f"Using broker: {broker_url}")
        
        # Execute the pipeline
        results = await pipeline.run(input_data)
        
        # Display results from each step
        for step_name, step_result in results["results"].items():
            model_used = step_result.get("model", "unknown")
            status = step_result.get("status", "unknown")
            execution_time = step_result.get("time", 0)
            
            logger.info(f"Step '{step_name}' used model '{model_used}' with status '{status}'")
            logger.info(f"  Execution time: {execution_time:.2f} seconds")
            
            # Display the integrated response
            if status == "success" and step_name == "integration":
                response = step_result["output"]["response"]
                logger.info("Integrated Response:")
                print("\n" + "="*80)
                print(response)
                print("="*80 + "\n")
        
        # Display pipeline stats
        logger.info(f"Pipeline stats: {results['success_rate']} steps successful")
        logger.info(f"Total execution time: {results['total_time']:.2f} seconds")
    
    except Exception as e:
        logger.error(f"Error running distributed pipeline: {e}")
        raise
    
    finally:
        # Clean up resources
        await model_manager.close()

async def run_distributed_pipeline_with_config_dict():
    """Run a distributed pipeline using configuration dictionaries."""
    if not CELERY_INSTALLED:
        logger.error("Cannot run distributed pipeline without Celery")
        return
    
    # Create configuration
    config = Config(
        cache_dir="./cache",
        verbose_output=True,
        debug_mode=True,
        request_timeout=180.0
    )
    
    # In this approach, we define steps as configuration dictionaries
    # rather than instantiating CeleryModelStep objects
    steps = [
        # Economic analysis step
        ("economic", {
            "model_name": "llama3",
            "prompt_template": """
            Analyze the economic implications of the following topic:
            
            Topic: {query}
            
            Focus on market impacts, financial considerations, and economic trends.
            Provide a detailed economic analysis.
            """,
            "options": {"temperature": 0.7},
            "task_timeout": 180
        }, []),
        
        # Social analysis step
        ("social", {
            "model_name": "mistral",
            "prompt_template": """
            Analyze the social implications of the following topic:
            
            Topic: {query}
            
            Focus on societal impacts, cultural considerations, and community effects.
            Provide a detailed social analysis.
            """,
            "options": {"temperature": 0.7},
            "task_timeout": 180
        }, []),
        
        # Integration step
        ("integration", {
            "model_name": "llama3",
            "prompt_template": """
            Integrate the following analyses into a cohesive response:
            
            Topic: {query}
            
            Economic Analysis: {economic[response]}
            
            Social Analysis: {social[response]}
            
            Provide a balanced, comprehensive integration of these perspectives.
            """,
            "options": {"temperature": 0.5},
            "task_timeout": 240
        }, ["economic", "social"])
    ]
    
    # Create the distributed pipeline
    pipeline = DistributedPipeline(steps=steps, config=config)
    
    try:
        # Define input data
        input_data = {
            "query": "The impact of artificial intelligence on modern society."
        }
        
        logger.info(f"Running distributed pipeline with config dicts for query: {input_data['query']}")
        
        # Execute the pipeline
        results = await pipeline.run(input_data)
        
        # Display results (similar to previous example)
        for step_name, step_result in results["results"].items():
            if step_result.get("status") == "success" and step_name == "integration":
                response = step_result["output"]["response"]
                logger.info("Integrated Response:")
                print("\n" + "="*80)
                print(response)
                print("="*80 + "\n")
        
        logger.info(f"Pipeline stats: {results['success_rate']} steps successful")
        logger.info(f"Total execution time: {results['total_time']:.2f} seconds")
    
    except Exception as e:
        logger.error(f"Error running distributed pipeline: {e}")
        raise

def print_celery_worker_instructions():
    """Print instructions for running Celery workers."""
    if not CELERY_INSTALLED:
        logger.error("Celery not installed")
        return
    
    print("\nTo run Celery workers for this example:")
    print("1. Start Redis (if not already running):")
    print("   redis-server")
    print("\n2. Start Celery workers (in separate terminal):")
    print("   celery -A pasture.pasture_distributed.celery_app worker --loglevel=info")
    print("\n3. Run this script to submit tasks to the workers:")
    print("   python celery_pipeline.py")
    print("\nOptional: Monitor tasks with Flower:")
    print("   pip install flower")
    print("   celery -A pasture.pasture_distributed.celery_app flower")
    print("   Then open http://localhost:5555 in your browser\n")

async def main():
    """Main function to demonstrate different Celery usage patterns."""
    if not CELERY_INSTALLED:
        logger.error(
            "This example requires Celery and Redis. "
            "Install with: pip install 'pasture[celery]'"
        )
        return
    
    # Print instructions for running workers
    print_celery_worker_instructions()
    
    # Ask user if they want to continue
    response = input("Do you want to run the distributed pipeline example? (y/n): ")
    if response.lower() != 'y':
        logger.info("Example aborted")
        return
    
    # Run the distributed pipeline using CeleryModelStep instances
    await run_distributed_pipeline()
    
    # Optionally, run the distributed pipeline using config dictionaries
    run_second = input("Do you want to run the example with configuration dictionaries? (y/n): ")
    if run_second.lower() == 'y':
        await run_distributed_pipeline_with_config_dict()

if __name__ == "__main__":
    asyncio.run(main())
