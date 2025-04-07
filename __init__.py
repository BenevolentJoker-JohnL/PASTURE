#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pasture/__init__.py

PASTURE: Pipeline for Analytical Synthesis of Textual Unification and Resource Enhancement

A middleware framework for orchestrating multiple Ollama-based LLMs,
enabling effective communication between models while providing robust
error handling, caching, and fallback mechanisms.

Core dependencies:
- Pydantic: For data validation and configuration
- Asyncio: For asynchronous processing
- Tenacity: For robust retry logic with exponential backoff

Optional dependencies:
- Celery + Redis: For distributed processing (install with pip install "pasture[celery]")
"""

import importlib.util
import logging

__version__ = "1.0.0"

# Export core classes from pasture.py
from .pasture import (
    Config, 
    FileCache,
    JSONProcessor,
    ModelManager,
    AnalysisStep,
    ModelStep,
    Pipeline
)

# Define core exports
__all__ = [
    'Config', 
    'FileCache',
    'JSONProcessor',
    'ModelManager',
    'AnalysisStep',
    'ModelStep',
    'Pipeline'
]

# Check if Celery and Redis are installed
celery_installed = importlib.util.find_spec("celery") is not None
redis_installed = importlib.util.find_spec("redis") is not None

# Try to import distributed components if Celery and Redis are available
if celery_installed and redis_installed:
    try:
        from .pasture_distributed import (
            CeleryModelStep,
            DistributedPipeline,
            celery_app,
            process_model,
            run_pipeline_step
        )
        
        # Add distributed components to exports
        __all__.extend([
            'CeleryModelStep',
            'DistributedPipeline',
            'celery_app',
            'process_model',
            'run_pipeline_step'
        ])
    except ImportError as e:
        logging.warning(
            f"Celery and Redis are installed, but distributed components could not be imported: {e}"
        )
elif celery_installed or redis_installed:
    # One dependency is missing
    missing = "Redis" if celery_installed else "Celery"
    logging.info(
        f"{missing} is missing. For distributed processing capabilities, "
        f"install with: pip install 'pasture[celery]'"
    )
