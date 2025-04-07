# PASTURE Framework

**Protocol for AI System Text Understanding and Response Enhancement**

![PASTURE Logo](https://via.placeholder.com/150x150.png?text=PASTURE)

## Overview

PASTURE is a powerful middleware framework for orchestrating multiple AI models hosted on Ollama, designed with a focus on reliability, error handling, and resource efficiency.

## Quick Links

- [📚 Documentation](docs/README.md)
- [🚀 Installation Guide](docs/INSTALL.md)
- [📖 API Reference](docs/API.md)
- [💻 Examples](examples/)

## Key Features

- **Multi-Model Orchestration**: Chain LLMs in sequential pipelines
- **Error Resilience**: Automatic retries and fallbacks
- **Response Validation**: Ensure quality outputs
- **Resource Management**: Efficient model loading/unloading
- **Caching System**: Performance optimization with TTL support

## Installation

```bash
# Install from PyPI
pip install pasture

# Or install from source
git clone https://github.com/yourusername/pasture.git
cd pasture
pip install -e .
```

## Quick Example

```python
import asyncio
from pasture import Config, FileCache, ModelManager, ModelStep, Pipeline

async def main():
    # Initialize components
    config = Config()
    cache = FileCache(config.cache_dir)
    model_manager = ModelManager(config, cache)
    
    # Create a step that uses a model
    step = ModelStep(
        model_manager=model_manager,
        model_name="llama3",
        prompt_template="Answer this question: {query}"
    )
    
    # Create a pipeline with the step
    pipeline = Pipeline(steps=[("answer", step, [])], config=config)
    
    # Run the pipeline
    results = await pipeline.run({"query": "What is artificial intelligence?"})
    
    # Print the answer
    print(results["results"]["answer"]["output"]["response"])

if __name__ == "__main__":
    asyncio.run(main())
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
