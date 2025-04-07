# PASTURE API Reference

This document provides a comprehensive reference to the PASTURE framework API for orchestrating multiple Ollama-based LLMs.

## Table of Contents

- [Configuration](#configuration)
- [Caching](#caching)
- [Model Management](#model-management)
- [Pipeline Components](#pipeline-components)
- [JSON Processing](#json-processing)
- [Distributed Processing](#distributed-processing)
- [Complete Examples](#complete-examples)

## Configuration

### `Config` Class

The `Config` class defines the configuration options for the PASTURE framework.

```python
from pasture import Config

# Create config with default values
config = Config()

# Create config with custom values
config = Config(
    cache_dir="./my_cache",
    request_timeout=120.0,
    verbose_output=True,
    debug_mode=True,
    json_patching={
        "enabled": True, 
        "max_attempts": 3,
        "fallback_to_text": True
    }
)

# Load config from a JSON file
config = Config.from_file("path/to/config.json")
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `cache_dir` | `str` | `"./cache"` | Directory for caching responses |
| `json_patching.enabled` | `bool` | `True` | Enable automatic JSON patching |
| `json_patching.max_attempts` | `int` | `3` | Maximum patching attempts |
| `json_patching.fallback_to_text` | `bool` | `True` | Fallback to text wrapping if patching fails |
| `simulation_mode` | `bool` | `False` | Enable simulation mode (no actual API calls) |
| `log_level` | `LogLevel` | `LogLevel.INFO` | Logging level |
| `request_timeout` | `float` | `90.0` | Timeout for API requests in seconds |
| `max_retries` | `int` | `2` | Maximum number of retry attempts |
| `retry_delay` | `float` | `2.0` | Base delay between retries in seconds |
| `preload_models` | `bool` | `True` | Preload models before using them |
| `sequential_execution` | `bool` | `True` | Execute models sequentially |
| `fallback_threshold` | `int` | `2` | Number of failures before using fallback model |
| `min_response_length` | `int` | `10` | Minimum acceptable response length in characters |
| `verbose_output` | `bool` | `False` | Enable verbose output |
| `debug_mode` | `bool` | `False` | Enable debug mode with additional logging |

## Caching

### `FileCache` Class

The `FileCache` class provides a file-based caching mechanism for storing model responses.

```python
from pasture import Config, FileCache

config = Config()
cache = FileCache(config.cache_dir)

# Get a value from cache
cached_result = await cache.get("cache_key")

# Set a value in cache with optional TTL
await cache.set("cache_key", {"response": "Cached response"}, ttl=3600)

# Clear a specific cache entry
await cache.clear("cache_key")

# Clear all cache entries
await cache.clear()

# Get cache statistics
stats = await cache.get_stats()
```

#### Methods

| Method | Arguments | Returns | Description |
|--------|-----------|---------|-------------|
| `get(key)` | `key: str` | `Optional[Any]` | Get a value from cache |
| `set(key, value, ttl=None)` | `key: str, value: Any, ttl: Optional[int]` | `None` | Set a value in cache with optional TTL |
| `clear(key=None)` | `key: Optional[str]` | `None` | Clear a specific cache entry or all entries |
| `get_stats()` | - | `Dict[str, Any]` | Get statistics about the cache |

## Model Management

### `ModelManager` Class

The `ModelManager` class handles interactions with AI models, including resource management.

```python
from pasture import Config, FileCache, ModelManager

config = Config()
cache = FileCache(config.cache_dir)
model_manager = ModelManager(config, cache)

# Get available models
models = await model_manager.get_available_models()

# Check if a model is healthy
is_healthy = await model_manager.check_model_health("llama3")

# Preload a model
success = await model_manager.preload_model("llama3")

# Generate a response
response = await model_manager.generate_with_model(
    model_name="llama3",
    prompt="What is artificial intelligence?",
    options={"temperature": 0.7}
)

# Generate a chat response
chat_response = await model_manager.generate_with_chat(
    model_name="llama3",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is AI?"}
    ],
    options={"temperature": 0.7}
)

# Get a fallback model
fallback = await model_manager.get_fallback_model("failed_model", available_models)

# Close resources when done
await model_manager.close()
```

#### Methods

| Method | Arguments | Returns | Description |
|--------|-----------|---------|-------------|
| `get_available_models()` | - | `List[str]` | Get list of available models |
| `check_model_health(model_name)` | `model_name: str` | `bool` | Check if a model is healthy and responsive |
| `preload_model(model_name)` | `model_name: str` | `bool` | Preload a model into memory |
| `unload_model(model_name)` | `model_name: str` | `bool` | Explicitly unload a model from memory |
| `generate_with_model(model_name, prompt, options=None)` | `model_name: str, prompt: str, options: Optional[Dict]` | `Dict` | Generate a response from a model |
| `generate_with_chat(model_name, messages, options=None, format=None)` | `model_name: str, messages: List[Dict], options: Optional[Dict], format: Optional[Dict]` | `Dict` | Generate a chat response |
| `get_fallback_model(failed_model, available_models)` | `failed_model: str, available_models: List[str]` | `Optional[str]` | Get a healthy fallback model |
| `close()` | - | `None` | Close resources when done |

## Pipeline Components

### `ModelStep` Class

`ModelStep` is a pipeline step for model-based text generation.

```python
from pasture import Config, FileCache, ModelManager, ModelStep

config = Config()
cache = FileCache(config.cache_dir)
model_manager = ModelManager(config, cache)

# Create a model step
step = ModelStep(
    model_manager=model_manager,
    model_name="llama3",
    prompt_template="Answer the following question: {query}",
    options={"temperature": 0.7},
    fallback_models=["mistral", "phi3"],
    output_schema=MyResponseSchema,
    use_patching=True,
    max_patching_attempts=3
)

# Execute the step
result = await step.execute({"query": "What is artificial intelligence?"})
```

#### Constructor Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `model_manager` | `ModelManager` | Model manager instance |
| `model_name` | `str` | Name of the model to use |
| `prompt_template` | `str` | Template string for the prompt |
| `options` | `Optional[Dict[str, Any]]` | Model generation options |
| `fallback_models` | `Optional[List[str]]` | List of fallback models to try if primary model fails |
| `output_schema` | `Optional[Type[BaseModel]]` | Pydantic schema for validating output |
| `use_patching` | `Optional[bool]` | Whether to attempt JSON patching |
| `max_patching_attempts` | `Optional[int]` | Maximum number of patching attempts |
| `patching_prompt` | `Optional[str]` | Custom prompt for patching requests |

### `ChatModelStep` Class

`ChatModelStep` is a pipeline step for chat-based interaction.

```python
from pasture import Config, FileCache, ModelManager
from pasture.pasture import ChatModelStep

config = Config()
cache = FileCache(config.cache_dir)
model_manager = ModelManager(config, cache)

# Create a chat model step
step = ChatModelStep(
    model_manager=model_manager,
    model_name="llama3",
    system_prompt="You are a helpful assistant.",
    options={"temperature": 0.7},
    fallback_models=["mistral", "phi3"]
)

# Execute the step with messages
result = await step.execute({
    "messages": [
        {"role": "user", "content": "What is AI?"}
    ]
})
```

#### Constructor Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `model_manager` | `ModelManager` | Model manager instance |
| `model_name` | `str` | Name of the model to use |
| `system_prompt` | `Optional[str]` | System message to use |
| `options` | `Optional[Dict[str, Any]]` | Model generation options |
| `fallback_models` | `Optional[List[str]]` | List of fallback models to try if primary model fails |
| `output_schema` | `Optional[Type[BaseModel]]` | Pydantic schema for validating output |
| `use_patching` | `Optional[bool]` | Whether to attempt JSON patching |
| `max_patching_attempts` | `Optional[int]` | Maximum number of patching attempts |
| `patching_prompt` | `Optional[str]` | Custom prompt for patching requests |

### `Pipeline` Class

`Pipeline` orchestrates the execution of analysis steps.

```python
from pasture import Config, Pipeline

config = Config()

# Create pipeline with steps
pipeline = Pipeline(
    steps=[
        ("step1", step1, []),  # No dependencies
        ("step2", step2, ["step1"]),  # Depends on step1
        ("step3", step3, ["step1", "step2"])  # Depends on step1 and step2
    ],
    config=config
)

# Run the pipeline
results = await pipeline.run({"query": "What is artificial intelligence?"})
```

#### Constructor Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `steps` | `List[Tuple[str, AnalysisStep, List[str]]]` | List of (name, step, dependencies) tuples |
| `config` | `Config` | Configuration settings |

#### Methods

| Method | Arguments | Returns | Description |
|--------|-----------|---------|-------------|
| `run(input_data)` | `input_data: Dict[str, Any]` | `Dict[str, Any]` | Run the pipeline with the given input data |

## JSON Processing

### `JSONProcessor` Class

`JSONProcessor` provides advanced JSON processing with validation and repair.

```python
from pasture import JSONProcessor

# Check if a string is valid JSON
is_valid = JSONProcessor.is_valid_json('{"key": "value"}')

# Extract JSON from text
json_str = JSONProcessor.extract_json("Here's some JSON: {\"key\": \"value\"}")

# Repair malformed JSON
fixed_json = JSONProcessor.repair_json("{'key': 'value'}")

# Parse JSON with robust error handling
parsed = JSONProcessor.parse('{"key": "value"}')

# Wrap text as JSON
json_obj = JSONProcessor.wrap_text_as_json("This is plain text")

# Validate against a Pydantic schema
from pydantic import BaseModel
class MySchema(BaseModel):
    key: str
valid, validated = await JSONProcessor.validate_with_schema(parsed, MySchema)

# Patch JSON with a model
patched = await JSONProcessor.patch_json_with_model(
    model_manager, "llama3", "Fix this JSON", broken_json,
    expected_schema=MySchema
)
```

#### Methods

| Method | Arguments | Returns | Description |
|--------|-----------|---------|-------------|
| `is_valid_json(json_str)` | `json_str: str` | `bool` | Check if a string is valid JSON |
| `extract_json(text)` | `text: str` | `Optional[str]` | Extract JSON from text that might contain other content |
| `repair_json(json_str)` | `json_str: str` | `str` | Attempt to fix common JSON formatting issues |
| `parse(input_str)` | `input_str: str` | `Dict[str, Any]` | Parse JSON with robust error handling and repair |
| `wrap_text_as_json(text)` | `text: str` | `Dict[str, Any]` | Wrap plain text in a simple JSON structure |
| `validate_with_schema(data, schema_model)` | `data: Dict[str, Any], schema_model: Type[BaseModel]` | `Tuple[bool, Optional[Dict[str, Any]]]` | Validate JSON against a Pydantic schema model |
| `patch_json_with_model(model_manager, model_name, prompt, input_text, expected_schema, patching_prompt, options)` | Various | `Tuple[bool, Dict[str, Any]]` | Attempt to patch invalid JSON by asking the model to fix it |

## Distributed Processing

These components are available when PASTURE is installed with Celery support.

### `CeleryModelStep` Class

`CeleryModelStep` is a pipeline step that delegates processing to a Celery worker.

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
    prompt_template="Answer the following question: {query}",
    options={"temperature": 0.7},
    fallback_models=["mistral", "phi3"],
    task_timeout=180
)
```

#### Constructor Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `model_manager` | `ModelManager` | Model manager instance |
| `model_name` | `str` | Name of the model to use |
| `prompt_template` | `str` | Template string for the prompt |
| `options` | `Optional[Dict[str, Any]]` | Model generation options |
| `fallback_models` | `Optional[List[str]]` | List of fallback models to try if primary model fails |
| `task_timeout` | `int` | Timeout in seconds for task completion |
| `use_patching` | `Optional[bool]` | Whether to attempt JSON patching |
| `max_patching_attempts` | `Optional[int]` | Maximum number of patching attempts |
| `patching_prompt` | `Optional[str]` | Custom prompt for patching requests |

### `DistributedPipeline` Class

`DistributedPipeline` is a pipeline implementation that distributes steps across Celery workers.

```python
from pasture import Config
from pasture.pasture_distributed import DistributedPipeline

config = Config()

# Create a distributed pipeline with step configurations
pipeline = DistributedPipeline(
    steps=[
        ("step1", {
            "model_name": "llama3",
            "prompt_template": "Answer this: {query}",
            "options": {"temperature": 0.7},
            "fallback_models": ["mistral"]
        }, []),
        ("step2", {
            "model_name": "mistral",
            "prompt_template": "Analyze this: {step1[response]}",
            "options": {"temperature": 0.5}
        }, ["step1"])
    ],
    config=config
)

# Run the pipeline
results = await pipeline.run({"query": "What is artificial intelligence?"})
```

#### Constructor Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `steps` | `List[Tuple[str, Union[Dict, CeleryModelStep], List[str]]]` | List of (name, step_config_or_instance, dependencies) tuples |
| `config` | `Config` | Configuration settings |

For more details on the Celery integration, see the [CELERY_API.md](CELERY_API.md) documentation.

## Complete Examples

### Simple Pipeline

```python
import asyncio
from pasture import Config, FileCache, ModelManager, ModelStep, Pipeline

async def main():
    # Initialize components
    config = Config(cache_dir="./cache")
    cache = FileCache(config.cache_dir)
    model_manager = ModelManager(config, cache)
    
    # Create a model step
    step = ModelStep(
        model_manager=model_manager,
        model_name="llama3",
        prompt_template="Answer this question: {query}"
    )
    
    # Create a pipeline
    pipeline = Pipeline(
        steps=[("answer", step, [])],
        config=config
    )
    
    # Run the pipeline
    results = await pipeline.run({"query": "What is artificial intelligence?"})
    
    # Print the answer
    print(results["results"]["answer"]["output"]["response"])
    
    # Close resources
    await model_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Multi-Model Pipeline with JSON Validation

```python
import asyncio
from pydantic import BaseModel, Field
from typing import List
from pasture import Config, FileCache, ModelManager, ModelStep, Pipeline

# Define output schemas
class EconomicAnalysis(BaseModel):
    impacts: List[str] = Field(description="Economic impacts")
    confidence: float = Field(ge=0, le=1, description="Confidence score")

class SocialAnalysis(BaseModel):
    impacts: List[str] = Field(description="Social impacts")
    confidence: float = Field(ge=0, le=1, description="Confidence score")

class IntegratedAnalysis(BaseModel):
    key_findings: List[str] = Field(description="Key findings")
    recommendations: List[str] = Field(description="Recommendations")

async def main():
    config = Config(
        json_patching={"enabled": True, "max_attempts": 3}
    )
    cache = FileCache(config.cache_dir)
    model_manager = ModelManager(config, cache)
    
    # Create steps with schema validation
    economic_step = ModelStep(
        model_manager=model_manager,
        model_name="llama3",
        prompt_template="Analyze economic impact of {query}",
        output_schema=EconomicAnalysis
    )
    
    social_step = ModelStep(
        model_manager=model_manager,
        model_name="mistral",
        prompt_template="Analyze social impact of {query}",
        output_schema=SocialAnalysis
    )
    
    integration_step = ModelStep(
        model_manager=model_manager,
        model_name="llama3",
        prompt_template="""
        Integrate these analyses:
        Economic: {economic}
        Social: {social}
        """,
        output_schema=IntegratedAnalysis
    )
    
    # Create pipeline
    pipeline = Pipeline(
        steps=[
            ("economic", economic_step, []),
            ("social", social_step, []),
            ("integration", integration_step, ["economic", "social"])
        ],
        config=config
    )
    
    # Run pipeline
    results = await pipeline.run({"query": "AI automation"})
    
    # Print results
    print(results["results"]["integration"]["output"])

if __name__ == "__main__":
    asyncio.run(main())
```

For additional examples, see the [examples/](../examples/) directory in the repository.
