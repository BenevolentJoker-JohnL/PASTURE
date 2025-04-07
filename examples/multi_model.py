#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
examples/multi_model.py

Advanced example demonstrating how to use PASTURE with multiple models in a pipeline.
PASTURE: Pipeline for Analytical Synthesis of Textual Unification and Resource Enhancement

This script creates a pipeline where different models analyze economic, social, and ethical
implications of a topic, then a final model integrates these analyses.
"""

import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field
from pasture import Config, FileCache, ModelManager, ModelStep, Pipeline, JSONProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Define schemas for structured outputs
class EconomicAnalysis(BaseModel):
    """Schema for economic analysis output"""
    short_term_impacts: List[str] = Field(description="Short-term economic impacts, within 1-2 years")
    medium_term_impacts: List[str] = Field(description="Medium-term economic impacts, within 3-5 years")
    long_term_impacts: List[str] = Field(description="Long-term economic impacts, 5+ years")
    key_sectors_affected: List[str] = Field(description="Key economic sectors that will be affected")
    confidence_level: float = Field(ge=0, le=1, description="Confidence level in this analysis (0-1)")

class SocialAnalysis(BaseModel):
    """Schema for social analysis output"""
    primary_social_effects: List[str] = Field(description="Primary social effects")
    affected_demographics: List[str] = Field(description="Demographics most affected")
    potential_benefits: List[str] = Field(description="Potential social benefits")
    potential_challenges: List[str] = Field(description="Potential social challenges")
    confidence_level: float = Field(ge=0, le=1, description="Confidence level in this analysis (0-1)")

class EthicalAnalysis(BaseModel):
    """Schema for ethical analysis output"""
    ethical_considerations: List[str] = Field(description="Key ethical considerations")
    value_conflicts: List[str] = Field(description="Potential conflicts between values")
    ethical_guidelines: List[str] = Field(description="Proposed ethical guidelines")
    areas_for_oversight: List[str] = Field(description="Areas that may require ethical oversight")
    confidence_level: float = Field(ge=0, le=1, description="Confidence level in this analysis (0-1)")

class IntegratedAnalysis(BaseModel):
    """Schema for the integrated analysis"""
    summary: str = Field(description="Executive summary of the integrated analysis")
    key_findings: List[str] = Field(description="Key findings from all analyses")
    recommendations: List[str] = Field(description="Recommendations based on the analyses")
    areas_for_further_research: List[str] = Field(description="Areas that need further research")
    overall_confidence: float = Field(ge=0, le=1, description="Overall confidence in the integrated analysis")

async def main():
    """Main function that sets up and runs a multi-model PASTURE pipeline."""
    # Create configuration with JSON patching enabled
    config = Config(
        cache_dir="./cache",
        verbose_output=True,
        debug_mode=True,
        json_patching={
            "enabled": True,
            "max_attempts": 3,
            "fallback_to_text": True
        }
    )
    
    # Initialize cache and model manager
    cache = FileCache(config.cache_dir)
    model_manager = ModelManager(config, cache)
    
    # Get available models from Ollama
    available_models = await model_manager.get_available_models()
    logger.info(f"Available models: {available_models}")
    
    # For this example, we'll use different models for different analysis types
    # Adjust based on your available models
    models = {
        "economic": "llama3",
        "social": "mistral",
        "ethical": "phi3",
        "integration": "llama3"
    }
    
    # Define prompt templates for different analysis types
    prompt_templates = {
        "economic": """
        Analyze the economic implications of the following topic:
        
        Topic: {query}
        
        Focus on market impacts, financial considerations, and economic trends.
        Provide a detailed economic analysis with:
        - Short-term impacts (1-2 years)
        - Medium-term impacts (3-5 years)
        - Long-term impacts (5+ years)
        - Key sectors affected
        - Your confidence level (0-1)
        
        Format your response as a JSON object with these fields:
        {
          "short_term_impacts": ["impact1", "impact2", ...],
          "medium_term_impacts": ["impact1", "impact2", ...],
          "long_term_impacts": ["impact1", "impact2", ...],
          "key_sectors_affected": ["sector1", "sector2", ...],
          "confidence_level": 0.8  // number between 0-1
        }
        """,
        
        "social": """
        Analyze the social implications of the following topic:
        
        Topic: {query}
        
        Focus on societal impacts, cultural considerations, and community effects.
        Provide a detailed social analysis with:
        - Primary social effects
        - Demographics most affected
        - Potential benefits
        - Potential challenges
        - Your confidence level (0-1)
        
        Format your response as a JSON object with these fields:
        {
          "primary_social_effects": ["effect1", "effect2", ...],
          "affected_demographics": ["demographic1", "demographic2", ...],
          "potential_benefits": ["benefit1", "benefit2", ...],
          "potential_challenges": ["challenge1", "challenge2", ...],
          "confidence_level": 0.8  // number between 0-1
        }
        """,
        
        "ethical": """
        Analyze the ethical implications of the following topic:
        
        Topic: {query}
        
        Focus on moral considerations, ethical dilemmas, and philosophical perspectives.
        Provide a detailed ethical analysis with:
        - Key ethical considerations
        - Potential value conflicts
        - Ethical guidelines
        - Areas requiring oversight
        - Your confidence level (0-1)
        
        Format your response as a JSON object with these fields:
        {
          "ethical_considerations": ["consideration1", "consideration2", ...],
          "value_conflicts": ["conflict1", "conflict2", ...],
          "ethical_guidelines": ["guideline1", "guideline2", ...],
          "areas_for_oversight": ["area1", "area2", ...],
          "confidence_level": 0.8  // number between 0-1
        }
        """,
        
        "integration": """
        Integrate the following analyses into a cohesive response:
        
        Topic: {query}
        
        Economic Analysis:
        {economic}
        
        Social Analysis:
        {social}
        
        Ethical Analysis:
        {ethical}
        
        Create an integrated analysis that synthesizes these perspectives.
        Include:
        - An executive summary
        - Key findings from all analyses
        - Recommendations based on all analyses
        - Areas that need further research
        - Overall confidence level (0-1)
        
        Format your response as a JSON object with these fields:
        {
          "summary": "Executive summary text here...",
          "key_findings": ["finding1", "finding2", ...],
          "recommendations": ["recommendation1", "recommendation2", ...],
          "areas_for_further_research": ["area1", "area2", ...],
          "overall_confidence": 0.8  // number between 0-1
        }
        """
    }
    
    # Create pipeline steps
    steps = []
    
    # Economic analysis step
    economic_step = ModelStep(
        model_manager=model_manager,
        model_name=models["economic"],
        prompt_template=prompt_templates["economic"],
        options={"temperature": 0.7},
        fallback_models=available_models[:2],  # Use first two models as fallbacks
        output_schema=EconomicAnalysis,
        use_patching=True,  # Enable JSON patching
        max_patching_attempts=3
    )
    steps.append(("economic", economic_step, []))
    
    # Social analysis step
    social_step = ModelStep(
        model_manager=model_manager,
        model_name=models["social"],
        prompt_template=prompt_templates["social"],
        options={"temperature": 0.7},
        fallback_models=available_models[:2],
        output_schema=SocialAnalysis,
        use_patching=True,
        max_patching_attempts=3
    )
    steps.append(("social", social_step, []))
    
    # Ethical analysis step
    ethical_step = ModelStep(
        model_manager=model_manager,
        model_name=models["ethical"],
        prompt_template=prompt_templates["ethical"],
        options={"temperature": 0.7},
        fallback_models=available_models[:2],
        output_schema=EthicalAnalysis,
        use_patching=True,
        max_patching_attempts=3
    )
    steps.append(("ethical", ethical_step, []))
    
    # Integration step (depends on all previous analyses)
    integration_step = ModelStep(
        model_manager=model_manager,
        model_name=models["integration"],
        prompt_template=prompt_templates["integration"],
        options={"temperature": 0.5},  # Lower temperature for more focused integration
        fallback_models=available_models[:2],
        output_schema=IntegratedAnalysis,
        use_patching=True,
        max_patching_attempts=3
    )
    steps.append(("integration", integration_step, ["economic", "social", "ethical"]))
    
    # Create the pipeline with all steps
    pipeline = Pipeline(steps=steps, config=config)
    
    try:
        # Define input data
        input_data = {
            "query": "The impact of artificial intelligence on modern society."
        }
        
        logger.info(f"Running multi-model pipeline for query: {input_data['query']}")
        
        # Execute the pipeline
        results = await pipeline.run(input_data)
        
        # Display results from each step
        for step_name, step_result in results["results"].items():
            model_used = step_result.get("model", "unknown")
            status = step_result.get("status", "unknown")
            execution_time = step_result.get("time", 0)
            
            logger.info(f"Step '{step_name}' used model '{model_used}' with status '{status}'")
            logger.info(f"  Execution time: {execution_time:.2f} seconds")
            
            # Display the structured output if available
            output = step_result.get("output", {})
            
            # Check if patching was used
            if step_result.get("patched", False):
                logger.info(f"  JSON was patched for this step.")
            
            # Display the integrated response 
            if status == "success" and step_name == "integration":
                logger.info("Integrated Analysis:")
                print("\n" + "="*80)
                
                # Display summary
                summary = output.get("summary", "No summary available")
                print(f"SUMMARY: {summary}\n")
                
                # Display key findings
                findings = output.get("key_findings", [])
                if findings:
                    print("KEY FINDINGS:")
                    for i, finding in enumerate(findings, 1):
                        print(f"  {i}. {finding}")
                    print()
                
                # Display recommendations
                recommendations = output.get("recommendations", [])
                if recommendations:
                    print("RECOMMENDATIONS:")
                    for i, rec in enumerate(recommendations, 1):
                        print(f"  {i}. {rec}")
                    print()
                
                # Display confidence
                confidence = output.get("overall_confidence", "not specified")
                print(f"OVERALL CONFIDENCE: {confidence}")
                
                print("="*80 + "\n")
        
        # Display pipeline stats
        logger.info(f"Pipeline stats: {results['success_rate']} steps successful")
        logger.info(f"Total execution time: {results['total_time']:.2f} seconds")
    
    finally:
        # Clean up resources
        await model_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
