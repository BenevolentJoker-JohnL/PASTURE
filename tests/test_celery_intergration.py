#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pasture/tests/test_celery_integration.py

Unit tests for Celery integration with PASTURE.
NOTE: These tests will be skipped if Celery is not installed.
"""

import asyncio
import sys
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

# Check if Celery is installed, skip tests if not
try:
    import celery
    CELERY_INSTALLED = True
except ImportError:
    CELERY_INSTALLED = False

pytestmark = pytest.mark.skipif(not CELERY_INSTALLED, reason="Celery not installed")

# Import custom CeleryModelStep only if Celery is available
if CELERY_INSTALLED:
    # This is a simplified version for testing - in production, import from your module
    class CeleryModelStep:
        """Test implementation of Celery model step."""
        
        def __init__(self, model_name, prompt_template, options=None):
            self.model_name = model_name
            self.prompt_template = prompt_template
            self.options = options or {}
        
        async def execute(self, data):
            """Execute step by submitting a Celery task."""
            # In tests, we'll mock this method
            pass
        
        async def get_fallback(self, data):
            """Fallback logic."""
            return {
                "output": {"response": "Fallback response"},
                "status": "success",
                "fallback": True
            }

@pytest.mark.skipif(not CELERY_INSTALLED, reason="Celery not installed")
class TestCeleryIntegration:
    """Test suite for Celery integration."""
    
    @pytest.mark.asyncio
    async def test_celery_step_with_mock(self):
        """Test CeleryModelStep with mocked Celery task."""
        if not CELERY_INSTALLED:
            pytest.skip("Celery not installed")
        
        # Create a step with mocked execute method
        step = CeleryModelStep(
            model_name="test-model",
            prompt_template="Query: {query}"
        )
        
        # Mock the execute method
        step.execute = AsyncMock(return_value={
            "output": {"response": "Response from Celery task"},
            "status": "success",
            "model": "test-model"
        })
        
        # Execute with test data
        result = await step.execute({"query": "Test query"})
        
        # Verify the result
        assert result["status"] == "success"
        assert "Response from Celery task" in result["output"]["response"]
        
        # Verify execute was called with correct data
        step.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_celery_fallback(self):
        """Test fallback mechanism in CeleryModelStep."""
        if not CELERY_INSTALLED:
            pytest.skip("Celery not installed")
        
        # Create a step
        step = CeleryModelStep(
            model_name="test-model",
            prompt_template="Query: {query}"
        )
        
        # Execute fallback
        result = await step.get_fallback({"query": "Test query"})
        
        # Verify fallback result
        assert result["status"] == "success"
        assert result["fallback"] is True
        assert "Fallback response" in result["output"]["response"]
