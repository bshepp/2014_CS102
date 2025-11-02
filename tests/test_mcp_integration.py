#!/usr/bin/env python3
"""
MCP Integration Tests for the GeometryOracle MCP Server
Tests MCP protocol functionality and AWS connectivity
"""

import os
import sys
import pytest
import asyncio
from unittest.mock import AsyncMock, patch

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import geometry_oracle_mcp_server
from geometry_engine import HyperSphere, HyperCube


@pytest.mark.mcp
@pytest.mark.integration
class TestMCPServerImports:
    """Test MCP server can be imported and initialized."""

    def test_import_mcp_server(self):
        """Test that MCP server module can be imported."""
        import geometry_oracle_mcp_server
        assert hasattr(geometry_oracle_mcp_server, 'aws_proxy')
        assert hasattr(geometry_oracle_mcp_server, 'mcp')

    def test_aws_proxy_creation(self):
        """Test AWS proxy can be created."""
        from geometry_oracle_mcp_server import AWSMCPProxy
        proxy = AWSMCPProxy("https://example.com/test")
        assert proxy.endpoint == "https://example.com/test"


@pytest.mark.mcp
@pytest.mark.integration 
class TestMCPToolFunctions:
    """Test MCP tool functions can be called locally."""

    @pytest.mark.asyncio
    async def test_calculate_hypersphere_function_exists(self):
        """Test calculate_hypersphere function exists and has correct signature."""
        from geometry_oracle_mcp_server import calculate_hypersphere
        assert callable(calculate_hypersphere)
        
        # Test function signature inspection
        import inspect
        sig = inspect.signature(calculate_hypersphere)
        assert 'dimensions' in sig.parameters
        assert 'radius' in sig.parameters

    @pytest.mark.asyncio
    async def test_calculate_hypercube_function_exists(self):
        """Test calculate_hypercube function exists and has correct signature."""
        from geometry_oracle_mcp_server import calculate_hypercube
        assert callable(calculate_hypercube)
        
        import inspect
        sig = inspect.signature(calculate_hypercube)
        assert 'dimensions' in sig.parameters
        assert 'side_length' in sig.parameters

    @pytest.mark.asyncio
    async def test_compare_shapes_function_exists(self):
        """Test compare_shapes function exists and has correct signature."""
        from geometry_oracle_mcp_server import compare_shapes
        assert callable(compare_shapes)
        
        import inspect
        sig = inspect.signature(compare_shapes)
        assert 'shapes' in sig.parameters

    @pytest.mark.asyncio
    async def test_get_usage_statistics_function_exists(self):
        """Test get_usage_statistics function exists and has correct signature."""
        from geometry_oracle_mcp_server import get_usage_statistics
        assert callable(get_usage_statistics)
        
        import inspect
        sig = inspect.signature(get_usage_statistics)
        assert 'days' in sig.parameters


@pytest.mark.mcp
@pytest.mark.integration
class TestGeometryEngineIntegration:
    """Test core geometry engine works correctly for MCP."""

    def test_hypersphere_creation(self):
        """Test HyperSphere can be created and used."""
        sphere = HyperSphere(3, 1.0)
        assert sphere.dimensions == 3
        assert sphere.radius == 1.0
        
        volume = sphere.get_volume()
        assert isinstance(volume, float)
        assert volume > 0

    def test_hypercube_creation(self):
        """Test HyperCube can be created and used."""
        cube = HyperCube(3, 2.0)
        assert cube.dimensions == 3
        assert cube.side_length == 2.0
        
        volume = cube.get_volume()
        assert isinstance(volume, float)
        assert volume == 8.0  # 2^3

    def test_multiple_dimensions(self):
        """Test calculations work for multiple dimensions."""
        dimensions_to_test = [1, 2, 3, 4, 5, 10]
        
        for dim in dimensions_to_test:
            sphere = HyperSphere(dim, 1.0)
            volume = sphere.get_volume()
            assert volume > 0
            assert isinstance(volume, float)


@pytest.mark.mcp
@pytest.mark.integration
class TestMCPResources:
    """Test MCP resource functions."""

    @pytest.mark.asyncio
    async def test_get_server_status_resource(self):
        """Test server status resource function."""
        from geometry_oracle_mcp_server import get_server_status
        
        # Mock AWS connectivity to avoid actual API calls
        with patch('geometry_oracle_mcp_server.aws_proxy.call_aws_tool') as mock_call:
            mock_call.return_value = {"test": "data"}
            
            result = await get_server_status()
            assert isinstance(result, str)
            assert "status" in result
            assert "aws_endpoint" in result

    @pytest.mark.asyncio
    async def test_get_available_tools_resource(self):
        """Test available tools resource function."""
        from geometry_oracle_mcp_server import get_available_tools
        
        result = await get_available_tools()
        assert isinstance(result, str)
        assert "tools" in result
        assert "calculate_hypersphere" in result
        assert "calculate_hypercube" in result


@pytest.mark.mcp
@pytest.mark.integration 
class TestMCPProtocolMocking:
    """Test MCP functions with mocked AWS responses."""

    @pytest.mark.asyncio
    async def test_mocked_hypersphere_calculation(self):
        """Test hypersphere calculation with mocked AWS response."""
        from geometry_oracle_mcp_server import calculate_hypersphere
        
        # Mock AWS response
        mock_response = {
            "volume": 4.188790204786391,
            "surface_area": 12.566370614359172,
            "diameter": 2.0,
            "formulas": {
                "volume": "π^(n/2) × r^n / Γ(n/2 + 1)",
                "surface_area": "n × π^(n/2) × r^(n-1) / Γ(n/2 + 1)"
            }
        }
        
        with patch('geometry_oracle_mcp_server.aws_proxy.call_aws_tool') as mock_call:
            mock_call.return_value = mock_response
            
            result = await calculate_hypersphere(3, 1.0)
            assert result == mock_response
            
            # Verify the AWS tool was called with correct parameters
            mock_call.assert_called_once_with(
                "calculate_hypersphere", 
                {"dimensions": 3, "radius": 1.0}
            )

    @pytest.mark.asyncio
    async def test_mocked_hypercube_calculation(self):
        """Test hypercube calculation with mocked AWS response."""
        from geometry_oracle_mcp_server import calculate_hypercube
        
        mock_response = {
            "volume": 8.0,
            "surface_area": 24.0,
            "vertices": 8,
            "edges": 12
        }
        
        with patch('geometry_oracle_mcp_server.aws_proxy.call_aws_tool') as mock_call:
            mock_call.return_value = mock_response
            
            result = await calculate_hypercube(3, 2.0)
            assert result == mock_response
            
            mock_call.assert_called_once_with(
                "calculate_hypercube",
                {"dimensions": 3, "side_length": 2.0}
            )

    @pytest.mark.asyncio
    async def test_mocked_usage_statistics(self):
        """Test usage statistics with mocked AWS response."""
        from geometry_oracle_mcp_server import get_usage_statistics
        
        mock_response = {
            "total_queries": 42,
            "unique_sessions": 7,
            "popular_tools": ["calculate_hypersphere", "calculate_hypercube"],
            "popular_dimensions": [2, 3, 4]
        }
        
        with patch('geometry_oracle_mcp_server.aws_proxy.call_aws_tool') as mock_call:
            mock_call.return_value = mock_response
            
            result = await get_usage_statistics(7)
            assert result == mock_response
            
            mock_call.assert_called_once_with(
                "get_usage_statistics",
                {"days": 7}
            )


@pytest.mark.mcp
@pytest.mark.integration
@pytest.mark.slow
class TestErrorHandling:
    """Test MCP error handling scenarios."""

    @pytest.mark.asyncio
    async def test_aws_connection_failure(self):
        """Test behavior when AWS connection fails."""
        from geometry_oracle_mcp_server import calculate_hypersphere
        
        with patch('geometry_oracle_mcp_server.aws_proxy.call_aws_tool') as mock_call:
            mock_call.side_effect = Exception("AWS connection failed")
            
            with pytest.raises(Exception) as exc_info:
                await calculate_hypersphere(3, 1.0)
            
            assert "AWS connection failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_invalid_parameters(self):
        """Test MCP functions handle invalid parameters gracefully."""
        from geometry_oracle_mcp_server import calculate_hypersphere
        
        with patch('geometry_oracle_mcp_server.aws_proxy.call_aws_tool') as mock_call:
            # This should still call AWS, which would handle validation
            mock_call.return_value = {"error": "Invalid dimensions"}
            
            result = await calculate_hypersphere(-1, 1.0)
            assert "error" in result


@pytest.mark.mcp
@pytest.mark.integration
class TestMCPConfiguration:
    """Test MCP server configuration and environment."""

    def test_aws_endpoint_configuration(self):
        """Test AWS endpoint is configured correctly."""
        from geometry_oracle_mcp_server import AWS_ENDPOINT
        
        assert AWS_ENDPOINT is not None
        assert isinstance(AWS_ENDPOINT, str)
        assert "execute-api" in AWS_ENDPOINT or "localhost" in AWS_ENDPOINT

    def test_mcp_server_object_exists(self):
        """Test MCP server object is created."""
        from geometry_oracle_mcp_server import mcp
        
        assert mcp is not None
        # The FastMCP object should have tools registered
        assert hasattr(mcp, '_tools') or hasattr(mcp, 'tools')