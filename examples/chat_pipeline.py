#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
examples/chat_pipeline.py

Example demonstrating how to use PASTURE with chat-based Ollama models.
PASTURE: Pipeline for Analytical Synthesis of Textual Unification and Resource Enhancement

This script shows how to implement a pipeline using the Ollama chat API
with multiple specialized roles for different parts of analysis.
"""

import asyncio
import logging
from typing import Dict, Any, List
import json

from pasture import Config, FileCache, ModelManager, Pipeline, JSONProcessor
from pasture.pasture import ChatModelStep

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ChatHistory:
    """Helper class to manage chat history"""
    def __init__(self):
        self.full_history = []
        self.histories = {}
    
    def add_system_message(self, role_name: str, content: str):
        """Add a system message to a specific role's history"""
        if role_name not in self.histories:
            self.histories[role_name] = []
        
        message = {"role": "system", "content": content}
        self.histories[role_name].append(message)
    
    def add_user_message(self, role_name: str, content: str):
        """Add a user message to a specific role's history"""
        if role_name not in self.histories:
            self.histories[role_name] = []
        
        message = {"role": "user", "content": content}
        self.histories[role_name].append(message)
        self.full_history.append(message)
    
    def add_assistant_message(self, role_name: str, content: str):
        """Add an assistant message to a specific role's history"""
        if role_name not in self.histories:
            self.histories[role_name] = []
        
        message = {"role": "assistant", "content": content}
        self.histories[role_name].append(message)
        self.full_history.append(message)
    
    def get_history(self, role_name: str) -> List[Dict[str, str]]:
        """Get the message history for a specific role"""
        return self.histories.get(role_name, [])
    
    def get_full_history(self) -> List[Dict[str, str]]:
        """Get the combined message history"""
        return self.full_history

async def main():
    """Main function that sets up and runs a chat-based PASTURE pipeline."""
    # Create configuration
    config = Config(
        cache_dir="./cache",
        verbose_output=True,
        debug_mode=True,
        json_patching={
            "enabled": True,
            "max_attempts": 2,
            "fallback_to_text": True
        }
    )
    
    # Initialize cache and model manager
    cache = FileCache(config.cache_dir)
    model_manager = ModelManager(config, cache)
    
    # Get available models from Ollama
    available_models = await model_manager.get_available_models()
    logger.info(f"Available models: {available_models}")
    
    # Use the same model for all roles, but with different system prompts
    model_name = "llama3"  # Change to any model available in your Ollama installation
    
    # Create chat history manager
    chat_history = ChatHistory()
    
    # Define system prompts for different roles
    system_prompts = {
        "economic_advisor": """You are an economic advisor with expertise in macroeconomics, finance, and market trends.
Your task is to analyze topics from an economic perspective, focusing on market impacts, financial considerations, 
and economic trends. Provide detailed economic analysis with concrete examples and data-driven insights.
Be specific, balanced, and objective in your assessment.
""",
        
        "social_analyst": """You are a social analyst with expertise in sociology, demographics, and cultural studies.
Your task is to analyze topics from a social perspective, focusing on societal impacts, cultural considerations, 
and community effects. Provide detailed social analysis with specific examples and evidence-based insights.
Be specific, balanced, and objective in your assessment.
""",
        
        "integration_specialist": """You are an integration specialist who excels at synthesizing diverse perspectives 
into coherent, balanced analyses. Your task is to combine economic and social analyses into comprehensive overviews 
that acknowledge the complexity and interconnections between different domains. Provide balanced perspective that
integrates diverse viewpoints effectively. Offer conclusions based on the combined input you receive.
"""
    }
    
    # Add system messages to each role's history
    for role, prompt in system_prompts.items():
        chat_history.add_system_message(role, prompt)
    
    # Create chat steps
    steps = []
    
    # Economic analysis step using chat
    economic_step = ChatModelStep(
        model_manager=model_manager,
        model_name=model_name,
        system_prompt=system_prompts["economic_advisor"],
        options={"temperature": 0.7},
        fallback_models=available_models[:2] if len(available_models) >= 2 else []
    )
    steps.append(("economic", economic_step, []))
    
    # Social analysis step using chat
    social_step = ChatModelStep(
        model_manager=model_manager,
        model_name=model_name,
        system_prompt=system_prompts["social_analyst"],
        options={"temperature": 0.7},
        fallback_models=available_models[:2] if len(available_models) >= 2 else []
    )
    steps.append(("social", social_step, []))
    
    # Integration step using chat (depends on economic and social analyses)
    integration_step = ChatModelStep(
        model_manager=model_manager,
        model_name=model_name,
        system_prompt=system_prompts["integration_specialist"],
        options={"temperature": 0.5},  # Lower temperature for more focused integration
        fallback_models=available_models[:2] if len(available_models) >= 2 else []
    )
    steps.append(("integration", integration_step, ["economic", "social"]))
    
    # Create pipeline with all steps
    pipeline = Pipeline(steps=steps, config=config)
    
    try:
        # Define the query/topic to analyze
        query = "The impact of artificial intelligence on modern society."
        
        # Add the query as a user message to all roles
        for role in system_prompts.keys():
            chat_history.add_user_message(role, f"Please analyze: {query}")
        
        # Prepare input data with message histories
        input_data = {
            "query": query,
            "messages": {
                "economic": chat_history.get_history("economic_advisor"),
                "social": chat_history.get_history("social_analyst"),
                "integration": chat_history.get_history("integration_specialist")
            }
        }
        
        logger.info(f"Running chat pipeline for query: {query}")
        
        # Execute the pipeline
        results = await pipeline.run(input_data)
        
        # Process and display results
        for step_name, step_result in results["results"].items():
            model_used = step_result.get("model", "unknown")
            status = step_result.get("status", "unknown")
            execution_time = step_result.get("time", 0)
            
            logger.info(f"Step '{step_name}' used model '{model_used}' with status '{status}'")
            logger.info(f"  Execution time: {execution_time:.2f} seconds")
            
            # Extract response content and add to chat history
            if status == "success":
                output = step_result.get("output", {})
                if "message" in output and "content" in output["message"]:
                    response_content = output["message"]["content"]
                    role_name = {
                        "economic": "economic_advisor",
                        "social": "social_analyst",
                        "integration": "integration_specialist"
                    }.get(step_name, step_name)
                    
                    chat_history.add_assistant_message(role_name, response_content)
                    
                    # Display the response
                    print(f"\n[{role_name.upper()}]\n")
                    print("-" * 80)
                    print(response_content)
                    print("-" * 80)
        
        # Display pipeline stats
        logger.info(f"Pipeline stats: {results['success_rate']} steps successful")
        logger.info(f"Total execution time: {results['total_time']:.2f} seconds")
        
        # Demonstrate interactive follow-up (optional)
        do_followup = input("\nDo you want to ask a follow-up question? (y/n): ")
        if do_followup.lower() == 'y':
            followup_question = input("\nYour follow-up question: ")
            
            # Add follow-up to integration specialist only
            chat_history.add_user_message("integration_specialist", followup_question)
            
            # Create a simpler pipeline with just the integration step
            followup_step = ChatModelStep(
                model_manager=model_manager,
                model_name=model_name,
                options={"temperature": 0.7}
            )
            followup_pipeline = Pipeline(
                steps=[("followup", followup_step, [])],
                config=config
            )
            
            # Run the follow-up
            followup_input = {
                "messages": chat_history.get_history("integration_specialist")
            }
            
            followup_results = await followup_pipeline.run(followup_input)
            
            # Display follow-up response
            if "followup" in followup_results["results"]:
                step_result = followup_results["results"]["followup"]
                if step_result.get("status") == "success":
                    output = step_result.get("output", {})
                    if "message" in output and "content" in output["message"]:
                        response_content = output["message"]["content"]
                        
                        print("\n[FOLLOW-UP RESPONSE]\n")
                        print("-" * 80)
                        print(response_content)
                        print("-" * 80)
    
    finally:
        # Clean up resources
        await model_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
