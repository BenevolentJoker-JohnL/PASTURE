#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pasture/tests/test_filecache.py

Unit tests for the FileCache class in the PASTURE framework.
"""

import asyncio
import os
import time
import tempfile
from pathlib import Path

import pytest

from pasture import FileCache

class TestFileCache:
    """Test suite for the FileCache class."""
    
    @pytest.fixture
    def cache_dir(self):
        """Create a temporary directory for cache files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    @pytest.fixture
    def cache(self, cache_dir):
        """Create a FileCache instance with the temporary directory."""
        return FileCache(cache_dir)
    
    @pytest.mark.asyncio
    async def test_set_and_get(self, cache):
        """Test setting and retrieving a value from cache."""
        key = "test_key"
        value = {"data": "test_value"}
        
        # Set a value in cache
        await cache.set(key, value)
        
        # Get the value from cache
        result = await cache.get(key)
        
        assert result == value
    
    @pytest.mark.asyncio
    async def test_missing_key(self, cache):
        """Test retrieving a non-existent key."""
        key = "non_existent_key"
        
        # Try to get a value that doesn't exist
        result = await cache.get(key)
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_ttl_expiration(self, cache):
        """Test that values expire after TTL."""
        key = "expiring_key"
        value = {"data": "temporary_value"}
        
        # Set a value with 1 second TTL
        await cache.set(key, value, ttl=1)
        
        # Verify it exists initially
        result = await cache.get(key)
        assert result == value
        
        # Wait for TTL to expire
        await asyncio.sleep(1.5)
        
        # Verify it's gone after expiration
        result = await cache.get(key)
        assert result is None
    
    @pytest.mark.asyncio
    async def test_overwrite(self, cache):
        """Test overwriting an existing key."""
        key = "overwrite_key"
        value1 = {"data": "first_value"}
        value2 = {"data": "second_value"}
        
        # Set initial value
        await cache.set(key, value1)
        
        # Overwrite with new value
        await cache.set(key, value2)
        
        # Verify new value is retrieved
        result = await cache.get(key)
        assert result == value2
    
    @pytest.mark.asyncio
    async def test_complex_values(self, cache):
        """Test caching complex nested structures."""
        key = "complex_key"
        value = {
            "string": "text",
            "number": 42,
            "boolean": True,
            "null": None,
            "array": [1, 2, 3],
            "nested": {
                "a": "nested value",
                "b": [{"x": 1}, {"y": 2}]
            }
        }
        
        # Set complex value
        await cache.set(key, value)
        
        # Retrieve complex value
        result = await cache.get(key)
        
        assert result == value
    
    def test_hash_key(self, cache):
        """Test the hash_key method creates consistent hashes."""
        key1 = "test_key"
        key2 = "different_key"
        
        hash1 = cache._hash_key(key1)
        hash2 = cache._hash_key(key2)
        hash1_again = cache._hash_key(key1)
        
        # Same key should produce same hash
        assert hash1 == hash1_again
        
        # Different keys should produce different hashes
        assert hash1 != hash2
        
        # Hashes should be valid filenames (check for invalid chars)
        assert all(c.isalnum() or c == '-' for c in hash1)
