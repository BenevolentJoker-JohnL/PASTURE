#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
examples/simple_pipeline.py

A simple example demonstrating how to use the PASTURE framework with a single model.
PASTURE: Pipeline for Analytical Synthesis of Textual Unification and Resource Enhancement

This script creates a basic pipeline that uses one model to generate a creative response
to a user query.
"""

import asyncio
import logging
from pathlib import Path

from pasture import Config, FileCache, ModelManager, ModelStep, Pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    """Main function that sets up and runs a simple PASTURE pipeline."""
    # Create configuration
    config = Config(
        cache_dir="./cache",
        verbose_output=True,
        debug_mode=False
    )
    
    # Initialize cache and model manager
    cache = FileCache(config.cache_dir)
    model_manager = ModelManager(config, cache)
    
    # Create a simple prompt template
    prompt_template = """
    Generate a creative response to the following query:
    
    Query: {query}
    
    Provide a detailed and thoughtful response.
    """
    
    # Create a model step using the specified model
    model_step = ModelStep(
        model_manager=model_manager,
        model_name="llama3", # Change to any model available in your Ollama installation
        prompt_template=prompt_template,
        options={
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40
        }
    )
    
    # Create a pipeline with a single step
    # Format: (step_name, step_object, dependencies)
    pipeline = Pipeline(
        steps=[("creative_response", model_step, [])],
        config=config
    )
    
    try:
        # Define input data
        input_data = {
            "query": "Explain the concept of artificial intelligence to a 10-year-old child."
        }
        
        logger.info(f"Running pipeline with query: {input_data['query']}")
        
        # Execute the pipeline
        results = await pipeline.run(input_data)
        
        # Extract and display the response
        if "creative_response" in results["results"]:
            step_result = results["results"]["creative_response"]
            if step_result["status"] == "success":
                response = step_result["output"]["response"]
                logger.info("Generated Response:")
                print("\n" + "="*80)
                print(response)
                print("="*80 + "\n")
            else:
                logger.error(f"Step failed: {step_result.get('error_details', 'Unknown error')}")
        else:
            logger.error("No results from the creative_response step")
            
        # Display pipeline stats
        logger.info(f"Pipeline stats: {results['success_rate']} steps successful")
        logger.info(f"Total execution time: {results['total_time']:.2f} seconds")
    
    finally:
        # Clean up resources
        await model_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
