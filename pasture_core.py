#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pasture_core.py

PASTURE Core: Stripped down essential functionality of the PASTURE framework.
Provides the core building blocks for orchestrating Ollama-based LLMs with
robust error handling and caching.

This lightweight version contains the essential components without distributed processing
or other advanced features, making it easier to understand and adapt.
"""

import asyncio
import json
import logging
import time
import traceback
import hashlib
import re
from typing import Any, Dict, List, Optional, Tuple, Union, Type
from enum import Enum
from pathlib import Path

import aiohttp
from pydantic import BaseModel, Field, ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

###########################################
## CORE CONFIGURATION                   ##
###########################################

class LogLevel(str, Enum):
    """Valid log levels for configuration"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class OllamaOptions(BaseModel):
    """Options for the Ollama API"""
    temperature: Optional[float] = Field(default=0.7, description="Sampling temperature")
    top_p: Optional[float] = None
    top_k: Optional[int] = None

class JSONPatchingConfig(BaseModel):
    """Configuration for JSON patching behavior"""
    enabled: bool = Field(default=True, description="Enable JSON patching globally")
    max_attempts: int = Field(default=3, description="Maximum number of patching attempts")
    fallback_to_text: bool = Field(default=True, description="Fallback to text wrapping if patching fails")
    patching_prompt: str = Field(
        default="The previous output was not valid JSON. Please fix it and return only valid JSON that matches the expected schema: {schema}",
        description="Prompt template for requesting fixed JSON from the model"
    )

class Config(BaseModel):
    """Configuration for the PASTURE framework"""
    # Core settings
    cache_dir: str = Field(default="./cache", description="Cache directory")
    json_patching: JSONPatchingConfig = Field(default_factory=JSONPatchingConfig, description="JSON patching configuration")
    simulation_mode: bool = Field(default=False, description="Enable simulation mode")
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    
    # HTTP settings
    request_timeout: float = Field(default=90.0, description="Timeout for API requests in seconds")
    
    # Retry settings
    max_retries: int = Field(default=2, description="Maximum number of retry attempts")
    retry_delay: float = Field(default=2.0, description="Base delay between retries in seconds")
    
    # Model settings
    preload_models: bool = Field(default=True, description="Preload models before using them")
    sequential_execution: bool = Field(default=True, description="Execute models sequentially")
    fallback_threshold: int = Field(default=2, description="Number of failures before using fallback model")
    min_response_length: int = Field(default=10, description="Minimum acceptable response length in characters")
    
    # Misc settings
    verbose_output: bool = Field(default=False, description="Enable verbose output")
    debug_mode: bool = Field(default=False, description="Enable debug mode with additional logging")
    
    # Override default Ollama API URL (http://localhost:11434 is used if not specified)
    api_base: Optional[str] = Field(default=None, description="Base URL for the Ollama API")
    
    def __init__(self, **data):
        super().__init__(**data)
        # Configure logging based on settings
        log_level = getattr(logging, self.log_level.value)
        logger.setLevel(log_level)
        if self.debug_mode and log_level > logging.DEBUG:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled, setting log level to DEBUG")
    
    @classmethod
    def from_file(cls, file_path: str) -> 'Config':
        """
        Load configuration from a JSON file.
        
        Args:
            file_path: Path to the configuration JSON file
            
        Returns:
            Config: Configuration object with merged settings
        """
        try:
            with open(file_path, 'r') as f:
                config_data = json.load(f)
                return cls(**config_data)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {file_path}, using defaults")
            return cls()
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in config file: {file_path}, using defaults")
            return cls()
        except ValidationError as e:
            logger.error(f"Validation error in config file: {e}")
            return cls()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return cls()

###########################################
## CACHING SYSTEM                       ##
###########################################

class CacheEntry(BaseModel):
    """Model for a cache entry"""
    value: Any
    created_at: float
    expires_at: Optional[float] = None

class FileCache:
    """File-based cache implementation with hash-based keys"""
    def __init__(self, cache_dir: str) -> None:
        self._cache_dir = Path(cache_dir)
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._lock = asyncio.Lock()  # Asyncio lock for cache operations
    
    def _hash_key(self, key: str) -> str:
        """Create a hash of the key for safe filenames"""
        return hashlib.md5(key.encode('utf-8')).hexdigest()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache with error handling"""
        try:
            async with self._lock:  # Use asyncio lock to prevent concurrent access
                file_path = self._cache_dir / f"{self._hash_key(key)}.json"
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        entry = CacheEntry(**data)
                        
                        # Check if the cached data has expired
                        if entry.expires_at is not None and entry.expires_at < time.time():
                            logger.debug(f"Cache entry for {key} has expired")
                            return None
                            
                        logger.debug(f"Cache hit for {key}")
                        return entry.value
                
                logger.debug(f"Cache miss for {key}")
                return None
        except Exception as e:
            logger.error(f"Error reading from cache: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in cache with optional TTL"""
        try:
            async with self._lock:  # Use asyncio lock to prevent concurrent access
                file_path = self._cache_dir / f"{self._hash_key(key)}.json"
                
                entry = CacheEntry(
                    value=value,
                    created_at=time.time()
                )
                
                # Add expiration if TTL is provided
                if ttl is not None:
                    entry.expires_at = time.time() + ttl
                
                # Serialize the cache entry
                with open(file_path, 'w') as f:
                    json.dump(entry.model_dump(), f)
                    
                logger.debug(f"Cached value for {key}" + (f" with TTL {ttl}s" if ttl else ""))
        except Exception as e:
            logger.error(f"Error writing to cache: {e}")

    async def clear(self, key: Optional[str] = None) -> None:
        """Clear a specific cache entry or all entries"""
        async with self._lock:
            if key:
                file_path = self._cache_dir / f"{self._hash_key(key)}.json"
                if file_path.exists():
                    file_path.unlink()
                    logger.debug(f"Cleared cache entry for {key}")
            else:
                # Clear all cache entries
                for file_path in self._cache_dir.glob("*.json"):
                    file_path.unlink()
                logger.debug("Cleared all cache entries")

    async def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the cache"""
        async with self._lock:
            files = list(self._cache_dir.glob("*.json"))
            
            # Count expired entries
            expired = 0
            active = 0
            for file_path in files:
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if "expires_at" in data and data["expires_at"] < time.time():
                            expired += 1
                        else:
                            active += 1
                except:
                    pass
            
            return {
                "total_entries": len(files),
                "expired_entries": expired,
                "active_entries": active,
                "cache_size_bytes": sum(file_path.stat().st_size for file_path in files)
            }

###########################################
## JSON PROCESSING                      ##
###########################################

class JSONProcessor:
    """JSON processing with validation and repair"""
    
    @staticmethod
    def is_valid_json(json_str: str) -> bool:
        """Check if a string is valid JSON"""
        try:
            json.loads(json_str)
            return True
        except:
            return False
    
    @staticmethod
    def extract_json(text: str) -> Optional[str]:
        """Extract JSON from text that might contain other content"""
        # Look for content wrapped in JSON or code blocks
        json_pattern = r'```(?:json)?\s*({[\s\S]*?})\s*```'
        matches = re.findall(json_pattern, text)
        
        if matches:
            for match in matches:
                if JSONProcessor.is_valid_json(match):
                    return match
        
        # Try to find naked JSON objects
        naked_pattern = r'({[\s\S]*?})'
        matches = re.findall(naked_pattern, text)
        
        if matches:
            for match in matches:
                if JSONProcessor.is_valid_json(match):
                    return match
        
        return None
    
    @staticmethod
    def repair_json(json_str: str) -> str:
        """Attempt to fix common JSON formatting issues"""
        fixed = json_str.strip()
        
        # Extract JSON if wrapped in markdown or other text
        extracted = JSONProcessor.extract_json(fixed)
        if extracted:
            fixed = extracted
            
        # Fix common syntax issues
        fixed = fixed.replace("'", '"')
        fixed = re.sub(r',\s*([\]}])', r'\1', fixed)  # Remove trailing commas
        
        # Ensure property names are double-quoted
        fixed = re.sub(r'(\w+)(?=\s*:)', r'"\1"', fixed)
        
        # If not a JSON object, wrap it
        if not (fixed.startswith("{") and fixed.endswith("}")):
            # Escape double quotes and newlines
            content = fixed.replace('"', '\\"').replace('\n', '\\n')
            fixed = f'{{"response": "{content}"}}'
            
        # Validate the repaired JSON
        try:
            json.loads(fixed)
            return fixed
        except json.JSONDecodeError as e:
            logger.error(f"JSON repair failed: {e}")
            raise
    
    @classmethod
    def parse(cls, input_str: str) -> Dict[str, Any]:
        """Parse JSON with robust error handling and repair"""
        if not input_str or not input_str.strip():
            return {"response": "", "error": "empty_response"}
            
        try:
            return json.loads(input_str)
        except json.JSONDecodeError:
            logger.warning(f"Initial JSON parsing failed, attempting repair...")
            
            try:
                # Try extracting and repairing JSON
                fixed_json = cls.repair_json(input_str)
                return json.loads(fixed_json)
            except Exception as e:
                logger.error(f"JSON repair failed: {e}")
                return {"response": input_str, "error": "json_parsing_failed"}
                
    @staticmethod
    def wrap_text_as_json(text: str) -> Dict[str, Any]:
        """Wrap plain text in a simple JSON structure for pipeline compatibility"""
        if not text:
            return {"response": "", "error": "empty_response"}
        
        return {"response": text.strip()}
        
    @staticmethod
    def schema_to_text(schema: Type[BaseModel]) -> str:
        """Convert a Pydantic schema to a text description for prompting"""
        schema_dict = schema.model_json_schema()
        return json.dumps(schema_dict, indent=2)
    
    @staticmethod
    async def validate_with_schema(data: Dict[str, Any], schema_model: Type[BaseModel]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Validate JSON against a Pydantic schema model"""
        try:
            # Use asyncio to prevent blocking on large validation operations
            loop = asyncio.get_event_loop()
            validated = await loop.run_in_executor(
                None, lambda: schema_model.model_validate(data).model_dump()
            )
            return True, validated
        except ValidationError as e:
            logger.error(f"Schema validation error: {e}")
            return False, {"error": "schema_validation_failed", "details": str(e)}
            
    @classmethod
    async def patch_json_with_model(
        cls, 
        model_manager: 'ModelManager', 
        model_name: str,
        prompt: str,
        input_text: str,
        expected_schema: Optional[Type[BaseModel]] = None,
        patching_prompt: str = "The previous output was not valid JSON. Please fix it and return only valid JSON.",
        options: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """Attempt to patch invalid JSON by asking the model to fix it"""
        if options is None:
            options = {"temperature": 0.2}  # Lower temperature for more precise fixing
            
        schema_text = ""
        if expected_schema:
            schema_text = cls.schema_to_text(expected_schema)
            
        fix_prompt = f"{patching_prompt.format(schema=schema_text)}\n\nPrevious output:\n{input_text}"
        
        # Ask the model to fix the JSON
        try:
            result = await model_manager.generate_with_model(
                model_name, 
                fix_prompt,
                options
            )
            
            # Check if the response contains valid JSON
            if "error" in result:
                logger.error(f"Error when patching JSON with model {model_name}: {result['error']}")
                return False, {"error": "patching_failed", "response": input_text}
                
            fixed_text = result.get("response", "")
            
            # Try to extract and parse the JSON
            try:
                # First try to extract JSON if it's wrapped in text
                json_str = cls.extract_json(fixed_text)
                if json_str:
                    fixed_json = json.loads(json_str)
                else:
                    # Try parsing directly
                    fixed_json = json.loads(fixed_text)
                
                # Validate against schema if provided
                if expected_schema:
                    is_valid, validated_data = await cls.validate_with_schema(fixed_json, expected_schema)
                    if is_valid:
                        return True, validated_data
                    else:
                        logger.warning(f"Patched JSON from {model_name} doesn't match schema")
                        return False, fixed_json
                
                return True, fixed_json
            except json.JSONDecodeError:
                logger.warning(f"Model {model_name} failed to produce valid JSON for patching")
                return False, {"response": fixed_text, "error": "patching_failed"}
        except Exception as e:
            logger.error(f"Exception during JSON patching with model {model_name}: {e}")
            return False, {"error": "patching_exception", "response": input_text, "details": str(e)}

###########################################
## MODEL MANAGEMENT                     ##
###########################################

class ModelStatus(BaseModel):
    """Status of a model in the ModelManager"""
    name: str
    loaded: bool = False
    healthy: bool = True
    failure_count: int = 0
    last_checked: Optional[float] = None
    last_used: Optional[float] = None

class ModelManager:
    """Manages interactions with AI models with resource management"""
    def __init__(
        self, 
        config: Config, 
        cache: FileCache,
        base_url: Optional[str] = None
    ) -> None:
        self.config = config
        self.cache = cache
        self.base_url = base_url or config.api_base or "http://localhost:11434"
        self.timeout = aiohttp.ClientTimeout(total=config.request_timeout)
        self.active_model = None
        self.model_lock = asyncio.Lock()
        self.loaded_models = set()
        self.model_statuses = {}  # Track model statuses
        self.session = None
        
        # Set up logging based on config
        self.logger = logging.getLogger(f"{__name__}.ModelManager")
        self.logger.setLevel(
            logging.DEBUG if self.config.debug_mode else 
            getattr(logging, self.config.log_level.value)
        )
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self.session
        
    async def close(self) -> None:
        """Close resources when done"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def _request(self, endpoint: str, method: str = "GET", json_data: Optional[Dict] = None) -> Dict:
        """Make a request to the Ollama API with proper error handling"""
        url = f"{self.base_url}/api/{endpoint}"
        
        if self.config.debug_mode:
            self.logger.debug(f"API request: {method} {url}")
            if json_data:
                self.logger.debug(f"Request payload: {json.dumps(json_data, indent=2)}")
        
        session = await self._get_session()
        
        try:
            if method == "GET":
                async with session.get(url) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        self.logger.error(f"HTTP {resp.status} from Ollama API: {text}")
                        return {"error": f"HTTP {resp.status}", "details": text}
                    return await resp.json()
            elif method == "POST":
                async with session.post(url, json=json_data) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        self.logger.error(f"HTTP {resp.status} from Ollama API: {text}")
                        return {"error": f"HTTP {resp.status}", "details": text}
                    return await resp.json()
        except asyncio.TimeoutError:
            self.logger.error(f"Request to {endpoint} timed out after {self.config.request_timeout}s")
            return {"error": "timeout", "details": f"Request timed out after {self.config.request_timeout}s"}
        except aiohttp.ClientError as e:
            self.logger.error(f"Client error in request to {endpoint}: {e}")
            return {"error": "connection_error", "details": str(e)}
        except Exception as e:
            self.logger.error(f"Error in request to {endpoint}: {e}")
            traceback.print_exc()
            return {"error": "request_failed", "details": str(e)}
    
    def _get_model_status(self, model_name: str) -> ModelStatus:
        """Get or create status tracking for a model"""
        if model_name not in self.model_statuses:
            self.model_statuses[model_name] = ModelStatus(name=model_name)
        return self.model_statuses[model_name]
    
    def _increment_failure_count(self, model_name: str) -> None:
        """Increment the failure count for a model"""
        status = self._get_model_status(model_name)
        status.failure_count += 1
        
        # Mark as unhealthy if failure count exceeds threshold
        if status.failure_count >= self.config.fallback_threshold:
            status.healthy = False
            self.logger.warning(f"Model {model_name} marked unhealthy after {status.failure_count} failures")
    
    def _update_model_status(self, model_name: str, **kwargs) -> None:
        """Update status fields for a model"""
        status = self._get_model_status(model_name)
        for key, value in kwargs.items():
            setattr(status, key, value)
    
    async def get_available_models(self) -> List[str]:
        """Get list of available models"""
        if self.config.simulation_mode:
            self.logger.info("Simulation mode enabled, using synthetic model list")
            return ["llama3", "mistral", "phi3", "gemma"]
        
        result = await self._request("tags")
        if "error" in result:
            self.logger.error(f"Failed to get models: {result['error']}")
            return []
            
        # Extract model names from the response
        try:
            if "models" in result:
                models = [model["name"] for model in result.get("models", [])]
                
                # Filter out incompatible models if needed
                exclude_terms = {"embed", "whisper"}
                filtered_models = [m for m in models if not any(t in m.lower() for t in exclude_terms)]
                
                self.logger.info(f"Found {len(filtered_models)} compatible models")
                return filtered_models
            else:
                self.logger.error(f"Unexpected response format from Ollama: {result}")
                return []
        except Exception as e:
            self.logger.error(f"Error processing model list: {e}")
            return []
    
    async def check_model_health(self, model_name: str) -> bool:
        """Check if a model is healthy and responsive"""
        if self.config.simulation_mode:
            return True
            
        # Get the model status
        status = self._get_model_status(model_name)
        
        # Check if already marked unhealthy
        if not status.healthy:
            self.logger.warning(f"Model {model_name} is already marked unhealthy")
            return False
            
        # Try a minimal request to the model
        self.logger.info(f"Checking health of model {model_name}...")
        
        result = await self._request("generate", method="POST", json_data={
            "model": model_name,
            "prompt": "Hello",
            "stream": False
        })
        
        # Update status tracking
        status.last_checked = time.time()
        
        if "error" in result:
            self.logger.warning(f"Health check failed for model {model_name}: {result['error']}")
            self._increment_failure_count(model_name)
            return False
            
        # Reset failure count on successful health check
        if status.failure_count > 0:
            self.logger.info(f"Model {model_name} health check passed, resetting failure count")
            status.failure_count = 0
            status.healthy = True
            
        return True
    
    async def preload_model(self, model_name: str) -> bool:
        """Preload a model into memory without generating text"""
        if self.config.simulation_mode or model_name in self.loaded_models:
            return True
            
        self.logger.info(f"Preloading model: {model_name}")
        # Send an empty prompt to load the model
        payload = {"model": model_name, "prompt": ""}
        
        result = await self._request("generate", method="POST", json_data=payload)
        if "error" in result:
            self.logger.error(f"Failed to preload model {model_name}: {result['error']}")
            self._increment_failure_count(model_name)
            return False
            
        self.loaded_models.add(model_name)
        self._update_model_status(model_name, loaded=True)
        return True
    
    async def unload_model(self, model_name: str) -> bool:
        """Explicitly unload a model from memory"""
        if self.config.simulation_mode:
            return True
            
        self.logger.info(f"Unloading model: {model_name}")
        # Setting keep_alive to 0 unloads the model
        payload = {"model": model_name, "prompt": "", "keep_alive": 0}
        
        try:
            result = await self._request("generate", method="POST", json_data=payload)
            if "error" in result:
                self.logger.error(f"Failed to unload model {model_name}: {result['error']}")
                return False
                
            if model_name in self.loaded_models:
                self.loaded_models.remove(model_name)
                self._update_model_status(model_name, loaded=False)
            return True
        except Exception as e:
            self.logger.error(f"Error unloading model {model_name}: {e}")
            return False
    
    def _create_cache_key(self, model_name: str, prompt: str, options: Dict) -> str:
        """Create a cache key for a model request"""
        # Combine model, prompt, and options into a single string
        serialized = f"{model_name}:{prompt}:{json.dumps(options or {})}"
        return serialized

    async def generate_with_model(self, model_name: str, prompt: str, options: Optional[Dict] = None) -> Dict:
        """Generate a response from a model with resource management"""
        # Check cache first
        cache_key = self._create_cache_key(model_name, prompt, options or {})
        cached_result = await self.cache.get(cache_key)
        if cached_result:
            self.logger.info(f"Using cached response for {model_name}")
            return cached_result
        
        if self.config.simulation_mode:
            # Generate a simulated response
            await asyncio.sleep(0.5)  # Simulate a slight delay
            response = {
                "response": f"Simulated response from {model_name} to: {prompt[:50]}..."
            }
            await self.cache.set(cache_key, response, ttl=3600)
            return response
        
        # Sequential processing to avoid overwhelming Ollama
        async with self.model_lock:
            # Update model status
            self._update_model_status(model_name, last_used=time.time())
            
            # Preload the model if needed and not already loaded
            if self.config.preload_models and self.active_model != model_name:
                if self.active_model:
                    # Unload previous model to free resources
                    await self.unload_model(self.active_model)
                preload_success = await self.preload_model(model_name)
                if not preload_success:
                    return {"error": "model_load_failed", "response": f"Failed to load model {model_name}"}
                self.active_model = model_name
            
            # Prepare retry logic
            max_retries = self.config.max_retries
            retry_count = 0
            
            while retry_count <= max_retries:
                self.logger.info(f"Generating response from {model_name} (attempt {retry_count + 1}/{max_retries + 1})...")
                
                # Prepare request
                payload = {
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False
                }
                
                # Add options if provided
                if options:
                    payload["options"] = options
                
                # Make the API request
                start_time = time.time()
                result = await self._request("generate", method="POST", json_data=payload)
                execution_time = time.time() - start_time
                
                if "error" in result:
                    self.logger.error(f"Error generating from {model_name}: {result['error']}")
                    retry_count += 1
                    
                    # Increment failure count
                    self._increment_failure_count(model_name)
                    
                    if retry_count <= max_retries:
                        retry_delay = self.config.retry_delay * (2 ** (retry_count - 1))  # Exponential backoff
                        self.logger.info(f"Retrying in {retry_delay:.2f} seconds...")
                        await asyncio.sleep(retry_delay)
                    else:
                        return {
                            "error": result["error"],
                            "response": f"Error after {max_retries + 1} attempts: {result.get('details', 'No details provided')}",
                            "execution_time": execution_time
                        }
                else:
                    # Process successful response
                    if "response" in result:
                        response_text = result["response"]
                        self.logger.info(f"Received response from {model_name} ({len(response_text)} chars)")
                        
                        # Check for empty or very short responses
                        if not response_text or len(response_text.strip()) < self.config.min_response_length:
                            self.logger.warning(f"Response from {model_name} too short: {len(response_text.strip())} chars")
                            retry_count += 1
                            
                            if retry_count <= max_retries:
                                retry_delay = self.config.retry_delay * (2 ** (retry_count - 1))
                                self.logger.info(f"Retrying in {retry_delay:.2f} seconds...")
                                await asyncio.sleep(retry_delay)
                                continue
                            else:
                                return {
                                    "error": "response_too_short",
                                    "response": response_text or "Empty response from model",
                                    "execution_time": execution_time
                                }
                        
                        if self.config.verbose_output:
                            self.logger.info(f"Response preview: {response_text[:100]}...")
                        
                        # Try to parse response as JSON if it looks like JSON
                        if response_text.strip().startswith("{") and response_text.strip().endswith("}"):
                            try:
                                parsed_json = JSONProcessor.parse(response_text)
                                output = parsed_json
                            except:
                                output = {"response": response_text}
                        else:
                            output = {"response": response_text}
                        
                        # Add execution metadata
                        output["execution_time"] = execution_time
                        
                        # Include metadata from Ollama response
                        for key in ["eval_count", "eval_duration", "total_duration"]:
                            if key in result:
                                output[key] = result[key]
                        
                        # Cache successful response
                        await self.cache.set(cache_key, output, ttl=3600)
                        return output
                    else:
                        self.logger.error(f"Unexpected response format from {model_name}: {result}")
                        retry_count += 1
                        
                        if retry_count <= max_retries:
                            retry_delay = self.config.retry_delay * (2 ** (retry_count - 1))
                            self.logger.info(f"Retrying in {retry_delay:.2f} seconds...")
                            await asyncio.sleep(retry_delay)
                        else:
                            return {
                                "error": "unexpected_format",
                                "response": "Received unexpected response format from model",
                                "execution_time": execution_time
                            }

    async def generate_with_chat(self, model_name: str, messages: List[Dict[str, Any]], 
                              options: Optional[Dict] = None, format: Optional[Dict] = None) -> Dict:
        """Generate a chat response using the Ollama chat API"""
        # Create a cache key from the messages and options
        cache_key = f"chat:{model_name}:{json.dumps(messages)}:{json.dumps(options or {})}:{json.dumps(format or {})}"
        cached_result = await self.cache.get(cache_key)
        if cached_result:
            self.logger.info(f"Using cached chat response for {model_name}")
            return cached_result
            
        if self.config.simulation_mode:
            # Generate a simulated chat response
            await asyncio.sleep(0.5)  # Simulate a slight delay
            
            # Get the last user message
            last_user_msg = next((m for m in reversed(messages) if m.get("role") == "user"), None)
            content = last_user_msg.get("content", "") if last_user_msg else ""
            
            response = {
                "message": {
                    "role": "assistant",
                    "content": f"Simulated chat response from {model_name} to: {content[:50]}..."
                }
            }
            await self.cache.set(cache_key, response, ttl=3600)
            return response
        
        # Sequential processing to avoid overwhelming Ollama
        async with self.model_lock:
            # Update model status
            self._update_model_status(model_name, last_used=time.time())
            
            # Preload the model if needed
            if self.config.preload_models and self.active_model != model_name:
                if self.active_model:
                    await self.unload_model(self.active_model)
                preload_success = await self.preload_model(model_name)
                if not preload_success:
                    return {"error": "model_load_failed", "message": {"content": f"Failed to load model {model_name}"}}
                self.active_model = model_name
            
            # Prepare retry logic
            max_retries = self.config.max_retries
            retry_count = 0
            
            while retry_count <= max_retries:
                self.logger.info(f"Generating chat response from {model_name} (attempt {retry_count + 1}/{max_retries + 1})...")
                
                # Prepare request
                payload = {
                    "model": model_name,
                    "messages": messages,
                    "stream": False
                }
                
                # Add options if provided
                if options:
                    payload["options"] = options
                
                # Add format if provided
                if format:
                    payload["format"] = format
                
                # Make the API request
                start_time = time.time()
                result = await self._request("chat", method="POST", json_data=payload)
                execution_time = time.time() - start_time
                
                if "error" in result:
                    self.logger.error(f"Error in chat with {model_name}: {result['error']}")
                    retry_count += 1
                    
                    # Increment failure count
                    self._increment_failure_count(model_name)
                    
                    if retry_count <= max_retries:
                        retry_delay = self.config.retry_delay * (2 ** (retry_count - 1))
                        self.logger.info(f"Retrying in {retry_delay:.2f} seconds...")
                        await asyncio.sleep(retry_delay)
                    else:
                        return {
                            "error": result["error"],
                            "message": {"content": f"Error after {max_retries + 1} attempts: {result.get('details', 'No details provided')}"},
                            "execution_time": execution_time
                        }
                else:
                    # Process successful response
                    if "message" in result:
                        message = result["message"]
                        content = message.get("content", "")
                        self.logger.info(f"Received chat response from {model_name} ({len(content)} chars)")
                        
                        # Check for empty or very short responses
                        if not content or len(content.strip()) < self.config.min_response_length:
                            self.logger.warning(f"Chat response from {model_name} too short: {len(content.strip())} chars")
                            retry_count += 1
                            
                            if retry_count <= max_retries:
                                retry_delay = self.config.retry_delay * (2 ** (retry_count - 1))
                                self.logger.info(f"Retrying in {retry_delay:.2f} seconds...")
                                await asyncio.sleep(retry_delay)
                                continue
                            else:
                                return {
                                    "error": "response_too_short",
                                    "message": {"content": content or "Empty response from model"},
                                    "execution_time": execution_time
                                }
                        
                        # Add execution metadata
                        result["execution_time"] = execution_time
                        
                        # Extract content for easier access
                        result["response"] = content
                        
                        # Cache successful response
                        await self.cache.set(cache_key, result, ttl=3600)
                        return result
                    else:
                        self.logger.error(f"Unexpected response format from {model_name}: {result}")
                        retry_count += 1
                        
                        if retry_count <= max_retries:
                            retry_delay = self.config.retry_delay * (2 ** (retry_count - 1))
                            self.logger.info(f"Retrying in {retry_delay:.2f} seconds...")
                            await asyncio.sleep(retry_delay)
                        else:
                            return {
                                "error": "unexpected_format",
                                "message": {"content": "Received unexpected response format from model"},
                                "execution_time": execution_time
                            }

    async def get_fallback_model(self, failed_model: str, available_models: List[str]) -> Optional[str]:
        """Get a healthy fallback model"""
        if not available_models:
            return None
            
        # Filter out the failed model
        candidates = [m for m in available_models if m != failed_model]
        if not candidates:
            return None
        
        # First check health of all candidates
        healthy_models = []
        for model in candidates:
            if await self.check_model_health(model):
                healthy_models.append(model)
                
        if not healthy_models:
            self.logger.warning("No healthy fallback models available")
            return None
            
        # Prioritize smaller, faster models for fallbacks
        # This is a simplified version of the ranking logic
        for model in healthy_models:
            if "tiny" in model.lower() or "mini" in model.lower() or "small" in model.lower():
                self.logger.info(f"Selected lightweight fallback model: {model}")
                return model
        
        # If no lightweight model is found, return the first healthy model
        fallback = healthy_models[0]
        self.logger.info(f"Selected fallback model: {fallback}")
        return fallback

###########################################
## PIPELINE COMPONENTS                  ##
###########################################

class AnalysisStep:
    """Base class for analysis pipeline steps"""
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the step with the given data"""
        raise NotImplementedError("Subclasses must implement execute()")
        
    def get_name(self) -> str:
        """Get the name of this step"""
        return self.__class__.__name__
        
    async def get_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute fallback logic when primary execution fails"""
        raise NotImplementedError("Subclasses must implement get_fallback()")

class ModelStep(AnalysisStep):
    """Pipeline step for model-based text generation"""
    def __init__(self, 
                 model_manager: ModelManager, 
                 model_name: str, 
                 prompt_template: str,
                 options: Optional[Dict[str, Any]] = None,
                 fallback_models: Optional[List[str]] = None,
                 output_schema: Optional[Type[BaseModel]] = None,
                 use_patching: Optional[bool] = None,
                 max_patching_attempts: Optional[int] = None,
                 patching_prompt: Optional[str] = None):
        self.model_manager = model_manager
        self.model_name = model_name
        self.prompt_template = prompt_template
        self.options = options or {"temperature": 0.7}
        self.fallback_models = fallback_models or []
        self.output_schema = output_schema
        
        # JSON patching configuration (use global settings if not specified)
        self.use_patching = use_patching if use_patching is not None else model_manager.config.json_patching.enabled
        self.max_patching_attempts = max_patching_attempts or model_manager.config.json_patching.max_attempts
        self.patching_prompt = patching_prompt or model_manager.config.json_patching.patching_prompt
        self.fallback_to_text = model_manager.config.json_patching.fallback_to_text
    
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
                if isinstance(data[key], dict) and "response" in data[key]:
                    prompt_parts.append(f"{key.capitalize()} analysis: {data[key]['response']}")
            
            prompt = "\n\n".join(prompt_parts)
            prompt += "\n\nPlease provide a detailed analysis."
                
            return prompt
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the step by formatting the prompt and calling the model"""
        try:
            # Check model health
            is_healthy = await self.model_manager.check_model_health(self.model_name)
            if not is_healthy and self.fallback_models:
                logger.warning(f"Model {self.model_name} is unhealthy, trying fallbacks")
                return await self.get_fallback(data)
                
            # Format prompt
            prompt = self._format_prompt(data)
            
            # Call the model
            start_time = time.time()
            result = await self.model_manager.generate_with_model(
                self.model_name, prompt, self.options
            )
            execution_time = time.time() - start_time
            
            # Check for errors
            if "error" in result:
                logger.error(f"Error from {self.model_name}: {result['error']}")
                if self.fallback_models:
                    logger.info(f"Trying fallback models for {self.model_name}")
                    return await self.get_fallback(data)
            
            # Process the result - here we handle JSON validation and patching
            if self.output_schema:
                try:
                    # Try to validate against schema
                    response_obj = result.get("response", "")
                    
                    # If response is a string and looks like JSON, try to parse it
                    if isinstance(response_obj, str) and (response_obj.strip().startswith("{") and response_obj.strip().endswith("}")):
                        try:
                            parsed_json = json.loads(response_obj)
                            is_valid, validated_data = await JSONProcessor.validate_with_schema(parsed_json, self.output_schema)
                            
                            if is_valid:
                                # Valid JSON that matches schema
                                result = validated_data
                            elif self.use_patching:
                                # Invalid JSON that doesn't match schema, attempt patching
                                patched = await self._patch_json_output(response_obj)
                                if patched:
                                    result = patched
                                elif self.fallback_to_text:
                                    # If patching failed, wrap as text if configured to do so
                                    result = JSONProcessor.wrap_text_as_json(response_obj)
                            elif self.fallback_to_text:
                                # Patching disabled, but still wrap as text
                                result = JSONProcessor.wrap_text_as_json(response_obj)
                        except json.JSONDecodeError:
                            # Not valid JSON - attempt patching if enabled
                            if self.use_patching:
                                patched = await self._patch_json_output(response_obj)
                                if patched:
                                    result = patched
                                elif self.fallback_to_text:
                                    result = JSONProcessor.wrap_text_as_json(response_obj)
                            elif self.fallback_to_text:
                                result = JSONProcessor.wrap_text_as_json(response_obj)
                    elif self.fallback_to_text:
                        # Not JSON-like, wrap as text
                        result = JSONProcessor.wrap_text_as_json(response_obj)
                except Exception as e:
                    logger.error(f"Error processing JSON output: {e}")
                    if self.fallback_to_text:
                        result = JSONProcessor.wrap_text_as_json(result.get("response", ""))
            
            # Process the result
            status = "success" if "error" not in result else "error"
            
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
                "time": 0,
                "model": self.model_name,
                "status": "error",
                "error_details": str(e)
            }
    
    async def _patch_json_output(self, output_text: str) -> Optional[Dict[str, Any]]:
        """Attempt to patch invalid JSON by asking the model to fix it, with configurable attempts"""
        if not self.use_patching or self.max_patching_attempts <= 0:
            return None
            
        logger.info(f"Attempting to patch JSON output with {self.max_patching_attempts} max attempts")
        
        # Create patching options with lower temperature for more deterministic fixing
        patching_options = dict(self.options)
        patching_options["temperature"] = min(patching_options.get("temperature", 0.7) * 0.5, 0.3)
        
        for attempt in range(self.max_patching_attempts):
            logger.info(f"JSON patching attempt {attempt + 1}/{self.max_patching_attempts}")
            
            success, patched_json = await JSONProcessor.patch_json_with_model(
                model_manager=self.model_manager,
                model_name=self.model_name,
                prompt=f"Fix the following JSON to make it valid and match the expected schema.",
                input_text=output_text,
                expected_schema=self.output_schema,
                patching_prompt=self.patching_prompt,
                options=patching_options
            )
            
            if success:
                logger.info(f"Successfully patched JSON on attempt {attempt + 1}")
                return patched_json
            
            # Use the output from the failed patching attempt as input for the next attempt
            if isinstance(patched_json, dict) and "response" in patched_json:
                output_text = patched_json["response"]
        
        logger.warning(f"Failed to patch JSON after {self.max_patching_attempts} attempts")
        return None
    
    async def get_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Try fallback models when primary model fails"""
        # Try fallback models in order
        for fallback_model in self.fallback_models:
            logger.info(f"Trying fallback model {fallback_model}")
            
            # Check health of fallback model
            is_healthy = await self.model_manager.check_model_health(fallback_model)
            if not is_healthy:
                logger.warning(f"Fallback model {fallback_model} is also unhealthy, skipping")
                continue
                
            # Format prompt
            prompt = self._format_prompt(data)
            
            # Call the fallback model
            start_time = time.time()
            result = await self.model_manager.generate_with_model(
                fallback_model, prompt, self.options
            )
            execution_time = time.time() - start_time
            
            # Check for success
            if "error" not in result:
                logger.info(f"Fallback model {fallback_model} succeeded")
                return {
                    "output": result,
                    "time": execution_time,
                    "model": fallback_model,
                    "status": "success",
                    "prompt": prompt,
                    "fallback": True
                }
        
        # All fallbacks failed
        logger.error(f"All fallback models failed for {self.model_name}")
        return {
            "output": {"response": "All models failed to generate a response", "error": "all_models_failed"},
            "time": 0,
            "model": self.model_name,
            "status": "error",
            "fallback": True
        }

class ChatModelStep(AnalysisStep):
    """Pipeline step for model-based chat interaction"""
    def __init__(self, 
                 model_manager: ModelManager, 
                 model_name: str,
                 system_prompt: Optional[str] = None,
                 options: Optional[Dict[str, Any]] = None,
                 fallback_models: Optional[List[str]] = None,
                 output_schema: Optional[Type[BaseModel]] = None,
                 use_patching: Optional[bool] = None,
                 max_patching_attempts: Optional[int] = None,
                 patching_prompt: Optional[str] = None):
        self.model_manager = model_manager
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.options = options or {"temperature": 0.7}
        self.fallback_models = fallback_models or []
        self.output_schema = output_schema
        
        # JSON patching configuration
        self.use_patching = use_patching if use_patching is not None else model_manager.config.json_patching.enabled
        self.max_patching_attempts = max_patching_attempts or model_manager.config.json_patching.max_attempts
        self.patching_prompt = patching_prompt or model_manager.config.json_patching.patching_prompt
        self.fallback_to_text = model_manager.config.json_patching.fallback_to_text
    
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
        """Execute the step by preparing messages and calling the model"""
        try:
            # Check model health
            is_healthy = await self.model_manager.check_model_health(self.model_name)
            if not is_healthy and self.fallback_models:
                logger.warning(f"Model {self.model_name} is unhealthy, trying fallbacks")
                return await self.get_fallback(data)
                
            # Prepare messages
            messages = self._prepare_messages(data)
            
            # Format options
            format_options = None
            if self.output_schema:
                # Convert output schema to Ollama format field
                format_options = self.output_schema.model_json_schema()
            
            # Call the model
            start_time = time.time()
            result = await self.model_manager.generate_with_chat(
                self.model_name, messages, self.options, format_options
            )
            execution_time = time.time() - start_time
            
            # Check for errors
            if "error" in result:
                logger.error(f"Error from {self.model_name}: {result['error']}")
                if self.fallback_models:
                    logger.info(f"Trying fallback models for {self.model_name}")
                    return await self.get_fallback(data)
            
            # Process the result with JSON validation and patching if needed
            if self.output_schema and "response" in result:
                response_text = result["response"]
                
                # If response is a string and looks like JSON, try to parse it
                if isinstance(response_text, str) and (response_text.strip().startswith("{") and response_text.strip().endswith("}")):
                    try:
                        parsed_json = json.loads(response_text)
                        is_valid, validated_data = await JSONProcessor.validate_with_schema(parsed_json, self.output_schema)
                        
                        if is_valid:
                            # Valid JSON that matches schema
                            result["parsed_output"] = validated_data
                        elif self.use_patching:
                            # Invalid JSON that doesn't match schema, attempt patching
                            patched = await self._patch_json_output(response_text)
                            if patched:
                                result["parsed_output"] = patched
                    except json.JSONDecodeError:
                        # Not valid JSON - attempt patching if enabled
                        if self.use_patching:
                            patched = await self._patch_json_output(response_text)
                            if patched:
                                result["parsed_output"] = patched
            
            status = "success" if "error" not in result else "error"
            
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
                "time": 0,
                "model": self.model_name,
                "status": "error",
                "error_details": str(e)
            }
    
    async def _patch_json_output(self, output_text: str) -> Optional[Dict[str, Any]]:
        """Attempt to patch invalid JSON by asking the model to fix it, with configurable attempts"""
        if not self.use_patching or self.max_patching_attempts <= 0:
            return None
            
        logger.info(f"Attempting to patch JSON output with {self.max_patching_attempts} max attempts")
        
        # Create patching options with lower temperature for more deterministic fixing
        patching_options = dict(self.options)
        patching_options["temperature"] = min(patching_options.get("temperature", 0.7) * 0.5, 0.3)
        
        for attempt in range(self.max_patching_attempts):
            logger.info(f"JSON patching attempt {attempt + 1}/{self.max_patching_attempts}")
            
            success, patched_json = await JSONProcessor.patch_json_with_model(
                model_manager=self.model_manager,
                model_name=self.model_name,
                prompt=f"Fix the following JSON to make it valid and match the expected schema.",
                input_text=output_text,
                expected_schema=self.output_schema,
                patching_prompt=self.patching_prompt,
                options=patching_options
            )
            
            if success:
                logger.info(f"Successfully patched JSON on attempt {attempt + 1}")
                return patched_json
            
            # Use the output from the failed patching attempt as input for the next attempt
            if isinstance(patched_json, dict) and "response" in patched_json:
                output_text = patched_json["response"]
        
        logger.warning(f"Failed to patch JSON after {self.max_patching_attempts} attempts")
        return None
    
    async def get_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Try fallback models when primary model fails"""
        for fallback_model in self.fallback_models:
            logger.info(f"Trying fallback model {fallback_model}")
            
            # Check health of fallback model
            is_healthy = await self.model_manager.check_model_health(fallback_model)
            if not is_healthy:
                logger.warning(f"Fallback model {fallback_model} is also unhealthy, skipping")
                continue
                
            # Prepare messages
            messages = self._prepare_messages(data)
            
            # Format options for schema if available
            format_options = None
            if self.output_schema:
                format_options = self.output_schema.model_json_schema()
            
            # Call the fallback model
            start_time = time.time()
            result = await self.model_manager.generate_with_chat(
                fallback_model, messages, self.options, format_options
            )
            execution_time = time.time() - start_time
            
            # Check for success
            if "error" not in result:
                logger.info(f"Fallback model {fallback_model} succeeded")
                return {
                    "output": result,
                    "time": execution_time,
                    "model": fallback_model,
                    "status": "success",
                    "messages": messages,
                    "fallback": True
                }
        
        # All fallbacks failed
        logger.error(f"All fallback models failed for {self.model_name}")
        return {
            "output": {
                "message": {"content": "All models failed to generate a response"},
                "error": "all_models_failed"
            },
            "time": 0,
            "model": self.model_name,
            "status": "error",
            "fallback": True
        }

class Pipeline:
    """Orchestrates the execution of analysis steps"""
    def __init__(self, steps: List[Tuple[str, AnalysisStep, List[str]]], config: Config):
        """
        Initialize the pipeline with steps.
        
        Args:
            steps: List of (name, step, dependencies) tuples
            config: Configuration object
        """
        self.steps = steps
        self.config = config
        
        # Set up logging
        self.logger = logging.getLogger(f"{__name__}.Pipeline")
        self.logger.setLevel(
            logging.DEBUG if self.config.debug_mode else 
            getattr(logging, self.config.log_level.value)
        )
        
        # Validate steps
        self._validate_steps()
    
    def _validate_steps(self) -> None:
        """Validate the pipeline configuration for circular dependencies"""
        # Build a dependency graph
        graph = {}
        for name, _, deps in self.steps:
            graph[name] = deps
        
        # Check for circular dependencies
        visited = set()
        path = []
        
        def dfs(node):
            if node in path:
                cycle = path[path.index(node):] + [node]
                raise ValueError(f"Circular dependency detected: {' -> '.join(cycle)}")
            
            if node in visited:
                return
                
            visited.add(node)
            path.append(node)
            
            for dep in graph.get(node, []):
                if dep not in graph:
                    self.logger.warning(f"Step {node} depends on undefined step {dep}")
                else:
                    dfs(dep)
                    
            path.pop()
        
        # Run DFS from each node
        for node in graph:
            dfs(node)
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the pipeline with the given input data"""
        results = {}
        data = input_data.copy()
        
        start_time = time.time()
        
        # Create execution plan based on dependencies
        execution_plan = []
        remaining_steps = {name: deps for name, _, deps in self.steps}
        
        # Keep adding steps until we've processed all or can't proceed
        while remaining_steps:
            # Find steps that have all dependencies satisfied
            ready_steps = [
                name for name, deps in remaining_steps.items() 
                if all(dep in results for dep in deps)
            ]
            
            if not ready_steps:
                # If no steps are ready but we have remaining steps, we have a problem
                missing_deps = {}
                for name, deps in remaining_steps.items():
                    unsatisfied = [dep for dep in deps if dep not in results]
                    if unsatisfied:
                        missing_deps[name] = unsatisfied
                
                self.logger.error(f"Cannot proceed with pipeline execution. Missing dependencies: {missing_deps}")
                break
            
            # Add ready steps to the execution plan
            execution_plan.extend(ready_steps)
            
            # Remove processed steps
            for name in ready_steps:
                del remaining_steps[name]
        
        self.logger.info(f"Pipeline execution plan: {' -> '.join(execution_plan)}")
        
        # Execute steps according to the plan
        for step_name in execution_plan:
            # Find the step
            step_info = next((s for s in self.steps if s[0] == step_name), None)
            if not step_info:
                self.logger.error(f"Step {step_name} not found in pipeline")
                continue
                
            name, step, dependencies = step_info
            self.logger.info(f"Running step: {name}")
            
            # Check dependencies (should be satisfied due to execution plan)
            missing_deps = [dep for dep in dependencies if dep not in results]
            if missing_deps:
                self.logger.error(f"Step {name} missing dependencies: {missing_deps}")
                results[name] = {
                    "output": {"response": f"Missing dependencies: {missing_deps}", "error": "missing_dependencies"},
                    "time": 0,
                    "status": "error",
                    "model": getattr(step, "model_name", "unknown")
                }
                continue
            
            # Execute the step with proper error handling
            try:
                # Create a robust version of the data
                robust_data = input_data.copy()
                
                # Add results from previous steps
                for prev_name, prev_result in results.items():
                    prev_output = prev_result.get("output", {})
                    if not isinstance(prev_output, dict):
                        prev_output = {"response": str(prev_output)}
                    robust_data[prev_name] = prev_output
                
                # Execute step with timeout protection
                step_timeout = 300  # 5 minute default timeout
                try:
                    task = asyncio.create_task(step.execute(robust_data))
                    result = await asyncio.wait_for(task, timeout=step_timeout)
                except asyncio.TimeoutError:
                    self.logger.error(f"Step {name} execution timed out after {step_timeout}s")
                    result = {
                        "output": {"response": f"Execution timed out after {step_timeout}s", "error": "timeout"},
                        "time": step_timeout,
                        "model": getattr(step, "model_name", "unknown"),
                        "status": "error"
                    }
                
                results[name] = result
                
                # Update data with successful results
                if result.get("status") == "success":
                    data[name] = result["output"]
                else:
                    # Add placeholder for failed steps
                    data[name] = {"response": f"Step {name} failed", "error": "step_failed"}
                
                self.logger.info(f"Completed step {name} with status: {result.get('status', 'unknown')}")
            except Exception as e:
                self.logger.error(f"Error executing step {name}: {e}")
                traceback.print_exc()
                results[name] = {
                    "output": {"response": f"Error: {str(e)}", "error": "execution_error"},
                    "time": 0,
                    "status": "error"
                }
        
        # Count successful steps and total execution time
        success_count = sum(1 for r in results.values() if r.get("status") == "success")
        total_time = time.time() - start_time
        
        self.logger.info(f"Pipeline completed in {total_time:.2f}s with {success_count}/{len(results)} successful steps")
        
        # Return formatted results
        return {
            "results": results,
            "total_time": total_time,
            "success_count": success_count,
            "total_count": len(results),
            "success_rate": f"{success_count}/{len(results)}"
        }
