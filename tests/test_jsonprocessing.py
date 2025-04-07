#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pasture/tests/test_jsonprocessor.py

Unit tests for the JSONProcessor class in the PASTURE framework.
"""

import json
import pytest

from pasture import JSONProcessor

class TestJSONProcessor:
    """Test suite for the JSONProcessor class."""
    
    def test_is_valid_json(self):
        """Test JSON validation."""
        # Valid JSON cases
        assert JSONProcessor.is_valid_json('{"key": "value"}')
        assert JSONProcessor.is_valid_json('{"nested": {"key": 42}}')
        assert JSONProcessor.is_valid_json('[]')
        assert JSONProcessor.is_valid_json('[1, 2, 3]')
        assert JSONProcessor.is_valid_json('{"array": [1, 2, 3]}')
        
        # Invalid JSON cases
        assert not JSONProcessor.is_valid_json('{key: "value"}')  # Missing quotes
        assert not JSONProcessor.is_valid_json('{"key": value}')  # Missing quotes
        assert not JSONProcessor.is_valid_json('{"key": "value"')  # Missing closing brace
        assert not JSONProcessor.is_valid_json('Not JSON at all')
        assert not JSONProcessor.is_valid_json('')
    
    def test_extract_json(self):
        """Test extracting JSON from text with other content."""
        # JSON in code blocks
        text = "Here's some JSON:\n```json\n{\"key\": \"value\"}\n```\nMore text."
        assert JSONProcessor.extract_json(text) == '{\"key\": \"value\"}'
        
        # JSON in code blocks without language specifier
        text = "Here's some JSON:\n```\n{\"key\": \"value\"}\n```\nMore text."
        assert JSONProcessor.extract_json(text) == '{\"key\": \"value\"}'
        
        # Naked JSON
        text = "Here's some JSON: {\"key\": \"value\"} and more text."
        assert JSONProcessor.extract_json(text) == '{\"key\": \"value\"}'
        
        # Multiple JSON objects - should extract first valid one
        text = "First: {\"first\": true} Second: {\"second\": true}"
        assert JSONProcessor.extract_json(text) == '{\"first\": true}'
        
        # No valid JSON
        text = "No JSON here at all."
        assert JSONProcessor.extract_json(text) is None
        
        # Invalid JSON
        text = "Bad JSON: {key: value}"
        assert JSONProcessor.extract_json(text) is None
    
    def test_repair_json(self):
        """Test repairing common JSON formatting issues."""
        # Fix single quotes
        assert json.loads(JSONProcessor.repair_json("{'key': 'value'}"))
        
        # Fix unquoted property names
        assert json.loads(JSONProcessor.repair_json("{key: \"value\"}"))
        
        # Fix trailing commas
        assert json.loads(JSONProcessor.repair_json("{\"key\": \"value\",}"))
        
        # Extract from markdown
        fixed = JSONProcessor.repair_json("```json\n{\"key\": \"value\"}\n```")
        assert json.loads(fixed)
        
        # Wrap non-object in a response object
        fixed = JSONProcessor.repair_json("This is just text")
        assert "response" in json.loads(fixed)
        
        # Fix nested issues
        complex_case = "{'outer': {inner: 'value', 'nested': [1, 2, 3,]}}"
        fixed = JSONProcessor.repair_json(complex_case)
        parsed = json.loads(fixed)
        assert parsed["outer"]["inner"] == "value"
        assert parsed["outer"]["nested"] == [1, 2, 3]
    
    def test_parse(self):
        """Test the parse method."""
        # Valid JSON
        result = JSONProcessor.parse('{"key": "value"}')
        assert result == {"key": "value"}
        
        # Empty input
        result = JSONProcessor.parse('')
        assert "error" in result
        assert result["error"] == "empty_response"
        
        # Repairable JSON
        result = JSONProcessor.parse("{'key': 'value'}")
        assert result == {"key": "value"}
        
        # Unrepairable JSON
        result = JSONProcessor.parse("This is not even close to JSON {{{")
        assert "error" in result
        assert result["error"] == "json_parsing_failed"
    
    def test_is_quality_response(self):
        """Test quality checking of responses."""
        # Good quality response
        data = {"response": "This is a good quality response."}
        assert JSONProcessor.is_quality_response(data)
        
        # Response with error
        data = {"response": "Error occurred", "error": "some_error"}
        assert not JSONProcessor.is_quality_response(data)
        
        # Missing response field
        data = {"something_else": "Not a response"}
        assert not JSONProcessor.is_quality_response(data)
        
        # Too short response
        data = {"response": "Short"}
        assert not JSONProcessor.is_quality_response(data)
        
        # Non-string response
        data = {"response": {"nested": "object"}}
        assert JSONProcessor.is_quality_response(data)
        
        # Custom minimum length
        data = {"response": "Short response"}
        assert not JSONProcessor.is_quality_response(data, min_length=20)
        assert JSONProcessor.is_quality_response(data, min_length=5)
