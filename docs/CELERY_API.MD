# PASTURE Celery Integration API Reference

This document provides a detailed reference for PASTURE's Celery integration, which enables distributed processing across multiple workers.

## Prerequisites

Before using these features, ensure you have installed PASTURE with Celery support:

```bash
pip install "pasture[celery]"
```

You will also need Redis installed and running as a message broker and result backend.

## Architecture Overview

The distributed processing architecture in PASTURE consists of:

1. **Celery Application**: A singleton Celery application used for task definition and management
2. **Task Definitions**: Pre-defined Celery tasks for model processing and pipeline step execution
3. **Distributed Step Classes**: Pipeline step implementations that delegate work to Celery workers
4. **Distributed Pipeline**: A pipeline implementation that coordinates distributed step execution

## Celery Application

### `celery_app`

The `celery_app` is a Celery application instance available from the `pasture.pasture_distributed` module. It is configured with sensible defaults but can be customized as needed.

```python
from pasture.pasture_distributed import celery_app

# Update Celery configuration
celery_app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    worker_send_task_events=True
)
```

## Pre-defined Tasks

### `process_model`

The `process_model` task handles model invocation on a Celery worker.

```python
from pasture.pasture_distributed import process_model

# Submit a task to process a model
task = process_model.delay(
    model_name="llama3",
    prompt="What is artificial intelligence?",
    options={"temperature": 0.7},
    config_dict=config.model_dump()  # Pass configuration as a dictionary
)

# Get the result
result = task.get(timeout=180)
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_name` | `str` | Name of the model to use |
| `prompt` | `str` | Prompt to send to the model |
| `options` | `Optional[Dict[str, Any]]` | Model generation options |
| `config_dict` | `Optional[Dict[str, Any]]` | Configuration dictionary |

#### Return Value

A dictionary containing the model's response and metadata, including:
- `response`: The model's generated text
- `execution_time`: Time taken to generate the response
- Other metadata from the model

### `run_pipeline_step`

The `run_pipeline_step` task executes a pipeline step on a Celery worker.

```python
from pasture.pasture_distributed import run_pipeline_step

# Submit a task to run a pipeline step
task = run_pipeline_step.delay(
    step_name="analysis",
    step_config={
        "model_name": "llama3",
        "prompt_template": "Analyze this: {query}",
        "options": {"temperature": 0.7}
    },
    data={"query": "What is artificial intelligence?"},
    config_dict=config.model_dump()
)

# Get the result
result = task.get(timeout=240)
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `step_name` | `str` | Name of the step |
| `step_config` | `Dict[str, Any]` | Configuration for the step |
| `data` | `Dict[str, Any]` | Input data for the step |
| `config_dict` | `Optional[Dict[str, Any]]` | Configuration dictionary |

#### Return Value

A dictionary containing the step execution results, including:
- `output`: The step's output (including model response)
- `time`: Execution time
- `model`: Model used
- `status`: Execution status
- Other metadata

## Distributed Step Classes

### `CeleryModelStep` Class

`CeleryModelStep` is a pipeline step that delegates model processing to a Celery worker.

```python
from pasture import Config, FileCache, ModelManager
from pasture.pasture_distributed import CeleryModelStep

config = Config()
cache = FileCache(config.cache_dir)
model_manager = ModelManager(config, cache)

# Create a Celery model step
step = CeleryModelStep(
    model_manager=model_manager,
    model_name="llama3",
    prompt_template="Answer this question: {query}",
    options={"temperature": 0.7},
    fallback_models=["mistral", "phi3"],
    task_timeout=180
)

# Execute the step
result = await step.execute({"query": "What is artificial intelligence?"})
```

#### Constructor Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_manager` | `ModelManager` | Model manager instance |
| `model_name` | `str` | Name of the model to use |
| `prompt_template` | `str` | Template string for the prompt |
| `options` | `Optional[Dict[str, Any]]` | Model generation options |
| `fallback_models` | `Optional[List[str]]` | List of fallback models to try if primary model fails |
| `task_timeout` | `int` | Timeout in seconds for task completion (default: 180) |
| `use_patching` | `Optional[bool]` | Whether to attempt JSON patching |
| `max_patching_attempts` | `Optional[int]` | Maximum number of patching attempts |
| `patching_prompt` | `Optional[str]` | Custom prompt for patching requests |

#### Methods

| Method | Parameters | Return Type | Description |
|--------|------------|-------------|-------------|
| `execute(data)` | `data: Dict[str, Any]` | `Dict[str, Any]` | Execute the step by submitting a task to Celery |
| `get_fallback(data)` | `data: Dict[str, Any]` | `Dict[str, Any]` | Try fallback models when primary model fails |

### `CeleryChatModelStep` Class

`CeleryChatModelStep` is a pipeline step for chat-based interaction using Celery.

```python
from pasture import Config, FileCache, ModelManager
from pasture.pasture_distributed import CeleryChatModelStep

config = Config()
cache = FileCache(config.cache_dir)
model_manager = ModelManager(config, cache)

# Create a Celery chat model step
step = CeleryChatModelStep(
    model_manager=model_manager,
    model_name="llama3",
    system_prompt="You are a helpful assistant.",
    options={"temperature": 0.7},
    task_timeout=180
)

# Execute the step
result = await step.execute({
    "messages": [
        {"role": "user", "content": "What is AI?"}
    ]
})
```

#### Constructor Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_manager` | `ModelManager` | Model manager instance |
| `model_name` | `str` | Name of the model to use |
| `system_prompt` | `Optional[str]` | System message to use |
| `options` | `Optional[Dict[str, Any]]` | Model generation options |
| `fallback_models` | `Optional[List[str]]` | List of fallback models to try if primary model fails |
| `task_timeout` | `int` | Timeout in seconds for task completion (default: 180) |
| `use_patching` | `Optional[bool]` | Whether to attempt JSON patching |
| `max_patching_attempts` | `Optional[int]` | Maximum number of patching attempts |
| `patching_prompt` | `Optional[str]` | Custom prompt for patching requests |

## Distributed Pipeline

### `DistributedPipeline` Class

`DistributedPipeline` is a pipeline implementation that distributes steps across Celery workers.

```python
from pasture import Config
from pasture.pasture_distributed import DistributedPipeline

config = Config()

# Create a distributed pipeline
pipeline = DistributedPipeline(
    steps=[
        # Option 1: Use step configuration dictionaries
        ("step1", {
            "model_name": "llama3",
            "prompt_template": "Answer this: {query}",
            "options": {"temperature": 0.7},
            "fallback_models": ["mistral"],
            "task_timeout": 180
        }, []),
        
        # Option 2: Use CeleryModelStep instances
        ("step2", celery_step_instance, ["step1"])
    ],
    config=config
)

# Run the pipeline
results = await pipeline.run({"query": "What is artificial intelligence?"})
```

#### Constructor Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `steps` | `List[Tuple[str, Union[Dict, CeleryModelStep], List[str]]]` | List of (name, step_config_or_instance, dependencies) tuples |
| `config` | `Config` | Configuration settings |

#### Methods

| Method | Parameters | Return Type | Description |
|--------|------------|-------------|-------------|
| `run(input_data)` | `input_data: Dict[str, Any]` | `Dict[str, Any]` | Run the pipeline with the given input data |

## Running Celery Workers

To process PASTURE tasks, you need to run Celery workers that will pull tasks from the message broker.

```bash
# Start a Celery worker
celery -A pasture.pasture_distributed.celery_app worker --loglevel=info
```

For production deployments, consider using a process manager like Supervisor or systemd to keep workers running.

## Configuration

### Broker and Result Backend URLs

By default, PASTURE uses Redis running on localhost for both the broker and result backend. You can customize these settings:

```python
import os
from pasture.pasture_distributed import celery_app

# Define broker and backend URLs (use environment variables or defaults)
broker_url = os.environ.get('BROKER_URL', 'redis://localhost:6379/0')
result_backend = os.environ.get('RESULT_BACKEND', broker_url)

# Update Celery configuration
celery_app.conf.update(
    broker_url=broker_url,
    result_backend=result_backend
)
```

### Worker Concurrency

By default, Celery will start as many worker processes as you have CPU cores. You can control this with the `--concurrency` option:

```bash
# Start a worker with 4 processes
celery -A pasture.pasture_distributed.celery_app worker --concurrency=4 --loglevel=info
```

## Best Practices

### 1. Distributed Task Sizing

Distribute work at an appropriate granularity:
- **Too Fine-Grained**: Overhead of task distribution outweighs benefits
- **Too Coarse-Grained**: Doesn't fully leverage distributed processing

For PASTURE, the ideal unit is usually a single model invocation or pipeline step.

### 2. Memory Management

Monitor memory usage on worker machines, especially when using multiple large models. Consider:
- Dedicating specific workers to specific models
- Setting memory limits for workers
- Configuring worker concurrency based on available memory

### 3. Error Handling

Build robustness against worker failures:
- Set appropriate timeouts for tasks
- Implement fallback mechanisms
- Monitor task failures through Celery's monitoring tools

### 4. Monitoring

Monitor your Celery workers and tasks using tools like:
- Flower: `celery -A pasture.pasture_distributed.celery_app flower`
- Celery's built-in monitoring: `celery -A pasture.pasture_distributed.celery_app events`

## Example: Complete Distributed Pipeline

Here's a complete example of a distributed pipeline:

```python
import asyncio
import os
from pasture import Config, FileCache, ModelManager
from pasture.pasture_distributed import (
    CeleryModelStep, DistributedPipeline, celery_app
)

async def main():
    # Create configuration
    config = Config(cache_dir="./cache")
    
    # Define broker and backend URLs
    broker_url = os.environ.get('BROKER_URL', 'redis://localhost:6379/0')
    result_backend = os.environ.get('RESULT_BACKEND', broker_url)
    
    # Update Celery configuration
    celery_app.conf.update(
        broker_url=broker_url,
        result_backend=result_backend
    )
    
    # Initialize resources
    cache = FileCache(config.cache_dir)
    model_manager = ModelManager(config, cache)
    
    # Create steps
    analysis_step = CeleryModelStep(
        model_manager=model_manager,
        model_name="llama3",
        prompt_template="Analyze this topic: {query}",
        task_timeout=180
    )
    
    summary_step = CeleryModelStep(
        model_manager=model_manager,
        model_name="mistral",
        prompt_template="Summarize this analysis: {analysis[response]}",
        task_timeout=120
    )
    
    # Create pipeline
    pipeline = DistributedPipeline(
        steps=[
            ("analysis", analysis_step, []),
            ("summary", summary_step, ["analysis"])
        ],
        config=config
    )
    
    # Run pipeline
    results = await pipeline.run({"query": "The impact of AI on healthcare"})
    
    # Process results
    for step_name, result in results["results"].items():
        if result["status"] == "success":
            print(f"\n--- {step_name.upper()} ---")
            print(result["output"]["response"])
    
    # Clean up
    await model_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
```

For more examples, see the [examples/celery_pipeline.py](../examples/celery_pipeline.py) file in the repository.
