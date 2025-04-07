# PASTURE Installation Guide

This guide provides detailed instructions for setting up the PASTURE framework for orchestrating multiple Ollama-based LLMs.

## Prerequisites

- **Python 3.8+**: PASTURE requires Python 3.8 or newer
- **Ollama**: You must have Ollama installed and running locally (or on a specified host)

## Installing Ollama

Before installing PASTURE, you need to set up Ollama:

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### macOS

Download and install from [https://ollama.com](https://ollama.com)

### Windows

Ollama can be run on Windows through WSL2 (Windows Subsystem for Linux). Follow the Linux instructions after setting up WSL2.

## Verify Ollama Installation

After installation, verify that Ollama is running correctly:

```bash
ollama list
```

You should see a list of available models. If not, start the Ollama service:

```bash
ollama serve
```

## Installing PASTURE

### From PyPI

The simplest way to install PASTURE is using pip:

```bash
pip install pasture
```

### From Source

To install from source:

```bash
git clone https://github.com/yourusername/pasture.git
cd pasture
pip install -e .
```

### Installing Optional Dependencies

PASTURE has optional dependencies for distributed processing:

```bash
pip install "pasture[celery]"
```

This will install Celery and Redis, enabling distributed model processing across multiple workers.

## Setting Up Ollama Models

Before using PASTURE, pull the models you want to use:

```bash
# Pull the llama3 model
ollama pull llama3

# Pull the mistral model
ollama pull mistral

# Pull other models you want to use
ollama pull phi3

# Check available models
ollama list
```

## Verifying Installation

Create a simple test script to verify that PASTURE is installed correctly:

```python
import asyncio
from pasture import Config, ModelManager, FileCache

async def test_pasture():
    config = Config()
    cache = FileCache(config.cache_dir)
    model_manager = ModelManager(config, cache)
    
    try:
        models = await model_manager.get_available_models()
        print(f"Available models: {models}")
    finally:
        await model_manager.close()

if __name__ == "__main__":
    asyncio.run(test_pasture())
```

Run the script to see if PASTURE can connect to Ollama and retrieve the list of models.

## Setting Up Distributed Processing

If you want to use PASTURE with Celery for distributed processing, follow these additional steps:

### 1. Install Redis

Redis is required as a message broker for Celery:

#### Linux

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### macOS

```bash
brew install redis
brew services start redis
```

### 2. Verify Redis Installation

Ensure Redis is running:

```bash
redis-cli ping
```

This should return `PONG`.

### 3. Install PASTURE with Celery Support

```bash
pip install "pasture[celery]"
```

### 4. Running Celery Workers

To run Celery workers that will process PASTURE tasks:

```bash
cd your_project_directory
celery -A pasture.pasture_distributed.celery_app worker --loglevel=info
```

For production deployments, consider using a process manager like Supervisor or systemd to keep workers running.

## Troubleshooting

### Common Issues

1. **Connection to Ollama Failed**
   
   Ensure Ollama is running with:
   ```bash
   ollama serve
   ```

2. **Model Not Found**
   
   Ensure you've pulled the models with:
   ```bash
   ollama pull model_name
   ```

3. **Cache Directory Permissions**
   
   Make sure the cache directory is writable by the user running PASTURE.

4. **Celery Workers Not Starting**
   
   Make sure Redis is running and accessible. Check your broker URL configuration.

### Logging

PASTURE uses Python's logging module. To see more detailed logs, set the log level in your configuration:

```python
config = Config(
    log_level="DEBUG",
    debug_mode=True
)
```

## Next Steps

After installation, check out the [API Documentation](API.md) and [example scripts](../examples/) to start using PASTURE for your projects.
