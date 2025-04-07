#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pasture/tests/test_pipeline.py

Unit tests for the Pipeline and ModelStep classes in the PASTURE framework.
"""

import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from pasture import Config, FileCache, ModelManager, AnalysisStep, ModelStep, Pipeline

class MockStep(AnalysisStep):
    """Mock implementation of AnalysisStep for testing."""
    
    def __init__(self, name, success=True, output=None, execution_time=0.1):
        self.name = name
        self.success = success
        self.mock_output = output or {"response": f"Response from {name}"}
        self.execution_time = execution_time
        self.execute_called = False
        self.fallback_called = False
    
    async def execute(self, data):
        """Mock execute implementation."""
        self.execute_called = True
        self.execute_data = data
        
        await asyncio.sleep(self.execution_time)
        
        if not self.success:
            return {
                "output": {"response": f"Error from {self.name}", "error": "mock_error"},
                "time": self.execution_time,
                "model": self.name,
                "status": "error",
                "error_details": "Mock error for testing"
            }
        
        return {
            "output": self.mock_output,
            "time": self.execution_time,
            "model": self.name,
            "status": "success"
        }
    
    async def get_fallback(self, data):
        """Mock fallback implementation."""
        self.fallback_called = True
        self.fallback_data = data
        
        return {
            "output": {"response": f"Fallback response from {self.name}"},
            "time": self.execution_time / 2,
            "model": f"{self.name}_fallback",
            "status": "success",
            "fallback": True
        }

class TestPipeline:
    """Test suite for the Pipeline class."""
    
    @pytest.fixture
    def config(self):
        """Create a Config instance for testing."""
        return Config(simulation_mode=True)
    
    @pytest.mark.asyncio
    async def test_simple_pipeline(self, config):
        """Test a simple pipeline with one step."""
        # Create a single successful step
        step = MockStep("test_step")
        
        # Create a pipeline with the step
        pipeline = Pipeline(
            steps=[("test_step", step, [])],
            config=config
        )
        
        # Run the pipeline with some input data
        input_data = {"query": "Test query"}
        results = await pipeline.run(input_data)
        
        # Check that the step was executed
        assert step.execute_called
        
        # Check the pipeline results
        assert "results" in results
        assert "test_step" in results["results"]
        assert results["results"]["test_step"]["status"] == "success"
        assert results["success_count"] == 1
        assert results["total_count"] == 1
        assert results["success_rate"] == "1/1"
    
    @pytest.mark.asyncio
    async def test_multi_step_pipeline(self, config):
        """Test a pipeline with multiple steps."""
        # Create steps
        step1 = MockStep("step1")
        step2 = MockStep("step2")
        step3 = MockStep("step3")
        
        # Create a pipeline with dependencies
        pipeline = Pipeline(
            steps=[
                ("step1", step1, []),
                ("step2", step2, ["step1"]),  # Depends on step1
                ("step3", step3, ["step1", "step2"])  # Depends on step1 and step2
            ],
            config=config
        )
        
        # Run the pipeline
        results = await pipeline.run({"query": "Test query"})
        
        # Check that all steps were executed
        assert step1.execute_called
        assert step2.execute_called
        assert step3.execute_called
        
        # Check the pipeline results
        assert results["success_count"] == 3
        assert results["total_count"] == 3
        assert all(r["status"] == "success" for r in results["results"].values())
        
        # Check that step2 had access to step1's output
        assert "step1" in step2.execute_data
        
        # Check that step3 had access to both step1 and step2's outputs
        assert "step1" in step3.execute_data
        assert "step2" in step3.execute_data
    
    @pytest.mark.asyncio
    async def test_pipeline_with_failing_step(self, config):
        """Test pipeline behavior when a step fails."""
        # Create steps with the middle one failing
        step1 = MockStep("step1")
        failing_step = MockStep("failing_step", success=False)
        step3 = MockStep("step3")
        
        # Create a pipeline with the failing step in the middle
        pipeline = Pipeline(
            steps=[
                ("step1", step1, []),
                ("failing_step", failing_step, ["step1"]),
                ("step3", step3, ["step1", "failing_step"])  # Depends on both
            ],
            config=config
        )
        
        # Run the pipeline
        results = await pipeline.run({"query": "Test query"})
        
        # First two steps should have been executed
        assert step1.execute_called
        assert failing_step.execute_called
        assert step3.execute_called
        
        # Check the pipeline results
        assert results["success_count"] == 1  # Only step1 succeeded
        assert results["total_count"] == 3
        assert results["results"]["step1"]["status"] == "success"
        assert results["results"]["failing_step"]["status"] == "error"
        
        # step3 should still run but have error data for failing_step
        assert "failing_step" in step3.execute_data
        assert "error" in step3.execute_data["failing_step"]
    
    @pytest.mark.asyncio
    async def test_pipeline_with_missing_dependency(self, config):
        """Test pipeline behavior with missing dependencies."""
        # Create a step with a non-existent dependency
        step = MockStep("orphan_step")
        
        # Create a pipeline with a missing dependency
        pipeline = Pipeline(
            steps=[
                ("orphan_step", step, ["non_existent_step"])
            ],
            config=config
        )
        
        # Run the pipeline
        results = await pipeline.run({"query": "Test query"})
        
        # Step should not have been executed due to missing dependency
        assert not step.execute_called
        
        # Check the pipeline results
        assert results["success_count"] == 0
        assert results["total_count"] == 1
        assert "error" in results["results"]["orphan_step"]["output"]
        assert "missing_dependencies" in results["results"]["orphan_step"]["output"]["error"]

class TestModelStep:
    """Test suite for the ModelStep class."""
    
    @pytest.fixture
    def model_manager(self):
        """Create a mocked ModelManager."""
        manager = MagicMock(spec=ModelManager)
        manager.check_model_health = AsyncMock(return_value=True)
        manager.generate_with_model = AsyncMock(return_value={
            "response": "Mock model response"
        })
        return manager
    
    @pytest.mark.asyncio
    async def test_model_step_execution(self, model_manager):
        """Test basic ModelStep execution."""
        # Create a model step
        step = ModelStep(
            model_manager=model_manager,
            model_name="test-model",
            prompt_template="Answer this: {query}",
            options={"temperature": 0.7}
        )
        
        # Execute the step
        result = await step.execute({"query": "What is AI?"})
        
        # Check the result
        assert result["status"] == "success"
        assert result["model"] == "test-model"
        assert "output" in result
        assert "prompt" in result
        
        # Verify the model manager was called correctly
        model_manager.check_model_health.assert_called_once_with("test-model")
        model_manager.generate_with_model.assert_called_once()
        # Check the prompt was formatted correctly
        args, kwargs = model_manager.generate_with_model.call_args
        assert "Answer this: What is AI?" in args
    
    @pytest.mark.asyncio
    async def test_model_step_with_unhealthy_model(self, model_manager):
        """Test ModelStep with an unhealthy model."""
        # Make the model unhealthy
        model_manager.check_model_health.return_value = False
        
        # Create a model step with fallbacks
        step = ModelStep(
            model_manager=model_manager,
            model_name="unhealthy-model",
            prompt_template="Answer this: {query}",
            fallback_models=["fallback-model"]
        )
        
        # Mock the fallback method
        step.get_fallback = AsyncMock(return_value={
            "output": {"response": "Fallback response"},
            "time": 0.1,
            "model": "fallback-model",
            "status": "success",
            "fallback": True
        })
        
        # Execute the step
        result = await step.execute({"query": "What is AI?"})
        
        # Should have used the fallback
        assert result["status"] == "success"
        assert result["fallback"] is True
        assert result["model"] == "fallback-model"
        
        # Verify fallback was called
        step.get_fallback.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_model_step_template_formatting(self, model_manager):
        """Test template formatting in ModelStep."""
        # Create a model step with a complex template
        step = ModelStep(
            model_manager=model_manager,
            model_name="test-model",
            prompt_template="""
            Query: {query}
            Previous Analysis: {previous[response]}
            """
        )
        
        # Execute with data that matches the template
        data = {
            "query": "What is ML?",
            "previous": {"response": "AI stands for Artificial Intelligence."}
        }
        result = await step.execute(data)
        
        # Verify the prompt was formatted correctly
        args, kwargs = model_manager.generate_with_model.call_args
        assert "Query: What is ML?" in args[1]
        assert "Previous Analysis: AI stands for Artificial Intelligence." in args[1]
    
    @pytest.mark.asyncio
    async def test_model_step_template_error_handling(self, model_manager):
        """Test handling of template formatting errors."""
        # Create a model step with a template requiring fields
        step = ModelStep(
            model_manager=model_manager,
            model_name="test-model",
            prompt_template="Query: {query}\nContext: {context}"
        )
        
        # Execute with missing data (no context)
        data = {"query": "What is ML?"}
        result = await step.execute(data)
        
        # Should still succeed but use fallback formatting
        assert result["status"] == "success"
        
        # Verify the prompt contains the available data
        args, kwargs = model_manager.generate_with_model.call_args
        assert "Query: What is ML?" in args[1]
    
    @pytest.mark.asyncio
    async def test_get_fallback(self, model_manager):
        """Test the fallback mechanism in ModelStep."""
        # Set up model manager behavior for fallbacks
        model_manager.check_model_health = AsyncMock(side_effect=[
            False,  # First fallback is unhealthy
            True    # Second fallback is healthy
        ])
        
        # Set up response for the successful fallback
        model_manager.generate_with_model = AsyncMock(return_value={
            "response": "Response from fallback model"
        })
        
        # Create a model step with multiple fallbacks
        step = ModelStep(
            model_manager=model_manager,
            model_name="primary-model",
            prompt_template="Answer: {query}",
            fallback_models=["fallback1", "fallback2"]
        )
        
        # Execute the fallback directly
        result = await step.get_fallback({"query": "Test query"})
        
        # Should have skipped the unhealthy fallback and used the healthy one
        assert result["status"] == "success"
        assert result["fallback"] is True
        assert result["model"] == "fallback2"  # Second fallback
        
        # Verify generate_with_model was called with the right model
        model_manager.generate_with_model.assert_called_once_with(
            "fallback2", 
            "Answer: Test query", 
            {"temperature": 0.7}  # Default options
        )
