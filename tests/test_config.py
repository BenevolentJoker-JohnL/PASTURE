#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pasture/tests/test_config.py

Unit tests for the Config class in the PASTURE framework.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from pasture import Config

class TestConfig:
    """Test suite for the Config class."""
    
    def test_default_values(self):
        """Test that default values are set correctly."""
        config = Config()
        
        assert config.cache_dir == "./cache"
        assert config.simulation_mode is False
        assert config.request_timeout == 90.0
        assert config.max_retries == 2
        assert config.retry_delay == 2.0
        assert config.preload_models is True
        assert config.sequential_execution is True
        assert config.fallback_threshold == 2
        assert config.min_response_length == 10
        assert config.verbose_output is False
        assert config.debug_mode is False
    
    def test_custom_values(self):
        """Test that custom values override defaults."""
        config = Config(
            cache_dir="/custom/cache",
            request_timeout=120.0,
            verbose_output=True,
            debug_mode=True
        )
        
        assert config.cache_dir == "/custom/cache"
        assert config.request_timeout == 120.0
        assert config.verbose_output is True
        assert config.debug_mode is True
        
        # Check that unspecified values use defaults
        assert config.simulation_mode is False
        assert config.max_retries == 2
    
    def test_validation(self):
        """Test that validation rules are enforced."""
        # Test invalid request_timeout (negative)
        with pytest.raises(ValidationError):
            Config(request_timeout=-10.0)
        
        # Test invalid max_retries (negative)
        with pytest.raises(ValidationError):
            Config(max_retries=-1)
    
    def test_from_file(self):
        """Test loading configuration from a file."""
        # Create a temporary config file
        config_data = {
            "cache_dir": "/temp/cache",
            "request_timeout": 150.0,
            "debug_mode": True
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as temp_file:
            json.dump(config_data, temp_file)
            temp_file.flush()
            
            # Load config from the file
            config = Config.from_file(temp_file.name)
            
            # Check loaded values
            assert config.cache_dir == "/temp/cache"
            assert config.request_timeout == 150.0
            assert config.debug_mode is True
            
            # Check default values for unspecified fields
            assert config.simulation_mode is False
    
    def test_from_file_not_found(self):
        """Test behavior when config file is not found."""
        # This should not raise an exception, but log a warning and use defaults
        non_existent_file = "/path/that/does/not/exist/config.json"
        config = Config.from_file(non_existent_file)
        
        # Should use defaults
        assert config.cache_dir == "./cache"
        assert config.request_timeout == 90.0
    
    def test_from_file_invalid_json(self):
        """Test behavior with invalid JSON in config file."""
        # Create a temporary file with invalid JSON
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as temp_file:
            temp_file.write("This is not valid JSON")
            temp_file.flush()
            
            # Should not raise an exception, but log an error and use defaults
            config = Config.from_file(temp_file.name)
            
            # Should use defaults
            assert config.cache_dir == "./cache"
            assert config.request_timeout == 90.0
