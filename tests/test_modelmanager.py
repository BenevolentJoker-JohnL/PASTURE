#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pasture/tests/test_modelmanager.py

Unit tests for the ModelManager class in the PASTURE framework.
"""

import asyncio
import json
from unittest.mock import patch, MagicMock, AsyncMock

import pytest
import aiohttp
from aiohttp import ClientSession, ClientResponse

from pasture import Config, FileCache, ModelManager

class TestModelManager:
    """Test suite for the ModelManager class."""
    
    @pytest.fixture
    def config(self):
        """Create a Config instance with simulation mode."""
        return Config(
            simulation_mode=True,
            cache_dir="./test_cache",
            request_timeout=5.0
        )
    
    @pytest.fixture
    def cache(self, config):
        """Create a FileCache instance with mock implementation."""
        cache = MagicMock(spec=FileCache)
        cache.get = AsyncMock(return_value=None)
        cache.set = AsyncMock()
        return cache
    
    @pytest.fixture
    def model_manager(self, config, cache):
        """Create a ModelManager instance for testing."""
        return ModelManager(config, cache)
    
    @pytest.mark.asyncio
    async def test_get_available_models_simulation(self, model_manager):
        """Test getting available models in simulation mode."""
        models = await model_manager.get_available_models()
        
        assert isinstance(models, list)
        assert len(models) > 0
        assert "llama3" in models
    
    @pytest.mark.asyncio
    async def test_check_model_health_simulation(self, model_manager):
        """Test checking model health in simulation mode."""
        # In simulation mode, all models are considered healthy
        is_healthy = await model_manager.check_model_health("any_model")
        
        assert is_healthy is True
    
    @pytest.mark.asyncio
    async def test_generate_with_model_simulation(self, model_manager):
        """Test generating text in simulation mode."""
        # Test different prompt types
        economic_result = await model_manager.generate_with_model(
            "llama3", "Analyze the economic impact of AI."
        )
        assert "economic_impacts" in economic_result
        
        social_result = await model_manager.generate_with_model(
            "llama3", "Discuss social implications of AI."
        )
        assert "social_impacts" in social_result
        
        ethical_result = await model_manager.generate_with_model(
            "llama3", "Examine ethical considerations of AI."
        )
        assert "ethical_considerations" in ethical_result
        
        integration_result = await model_manager.generate_with_model(
            "llama3", "Combine economic, social, and ethical analyses of AI."
        )
        assert "integrated_response" in integration_result
        
        generic_result = await model_manager.generate_with_model(
            "llama3", "Tell me about AI."
        )
        assert "response" in generic_result
    
    @pytest.mark.asyncio
    async def test_cache_hit(self, model_manager, cache):
        """Test using cached response."""
        # Set up cache to return a mock response
        cached_response = {"response": "Cached response"}
        cache.get.return_value = cached_response
        
        result = await model_manager.generate_with_model("llama3", "Any prompt")
        
        # Should return the cached response
        assert result == cached_response
        
        # Should have checked cache
        cache.get.assert_called_once()
        
        # Should not set cache again
        cache.set.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_generate_with_options(self, model_manager):
        """Test generating text with custom options."""
        options = {"temperature": 0.3, "top_p": 0.9}
        
        result = await model_manager.generate_with_model(
            "llama3", "Test prompt", options
        )
        
        assert "response" in result
    
    @pytest.mark.asyncio
    async def test_real_api_mocked(self, config, cache):
        """Test interaction with the real API using mocks."""
        # Create a non-simulation mode config
        real_config = Config(
            simulation_mode=False,
            cache_dir="./test_cache",
            request_timeout=5.0
        )
        
        # Mock the aiohttp ClientSession
        with patch('aiohttp.ClientSession') as mock_session:
            # Set up the mock response
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                "model": "llama3",
                "response": "This is a mock response from the Ollama API."
            })
            mock_response.__aenter__.return_value = mock_response
            
            # Make the session.post method return our mock response
            session_instance = mock_session.return_value
            session_instance.post = AsyncMock(return_value=mock_response)
            session_instance.get = AsyncMock(return_value=mock_response)
            
            # Create a model manager with the real config but mocked HTTP
            manager = ModelManager(real_config, cache)
            
            # Test various API methods
            models = await manager.get_available_models()
            assert isinstance(models, list)
            
            is_healthy = await manager.check_model_health("llama3")
            assert is_healthy is True
            
            response = await manager.generate_with_model("llama3", "Test prompt")
            assert "response" in response
            assert response["response"] == "This is a mock response from the Ollama API."
    
    @pytest.mark.asyncio
    async def test_api_error_handling(self, config, cache):
        """Test handling of API errors."""
        # Create a non-simulation mode config
        real_config = Config(
            simulation_mode=False,
            cache_dir="./test_cache",
            request_timeout=5.0,
            max_retries=1
        )
        
        # Mock the aiohttp ClientSession for an error case
        with patch('aiohttp.ClientSession') as mock_session:
            # Set up the mock error response
            mock_response = AsyncMock()
            mock_response.status = 500
            mock_response.text = AsyncMock(return_value="Internal Server Error")
            mock_response.__aenter__.return_value = mock_response
            
            # Make the session.post method return our error response
            session_instance = mock_session.return_value
            session_instance.post = AsyncMock(return_value=mock_response)
            
            # Create a model manager with the real config but mocked HTTP
            manager = ModelManager(real_config, cache)
            
            # Test error handling
            response = await manager.generate_with_model("llama3", "Test prompt")
            
            assert "error" in response
            assert response["error"] == "HTTP 500"
    
    @pytest.mark.asyncio
    async def test_get_fallback_model(self, model_manager):
        """Test selection of fallback models."""
        # Setup models with indicator terms that should be prioritized
        available_models = [
            "llama3", 
            "large-model", 
            "small-model-7b", 
            "tiny-model"
        ]
        
        # In simulation mode, all models are healthy
        fallback = await model_manager.get_fallback_model("llama3", available_models)
        
        # Should prefer smaller models based on name indicators
        assert fallback in ["small-model-7b", "tiny-model"]
        
        # When failed model is not in the list, should still find a fallback
        fallback = await model_manager.get_fallback_model("other-model", available_models)
        assert fallback is not None
        
        # Empty list should return None
        fallback = await model_manager.get_fallback_model("llama3", [])
        assert fallback is None
        
        # When only the failed model is available, should return None
        fallback = await model_manager.get_fallback_model("llama3", ["llama3"])
        assert fallback is None
