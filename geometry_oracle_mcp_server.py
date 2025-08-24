#!/usr/bin/env python3
"""
GeometryOracle MCP Server - AWS Proxy
Bridges MCP protocol to AWS GeometryOracle infrastructure

Usage:
  Add to Claude Desktop config:
  {
    "mcpServers": {
      "geometry-oracle": {
        "command": "python",
        "args": ["/path/to/geometry_oracle_mcp_server.py"]
      }
    }
  }
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Optional

import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr (required for MCP servers)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,  # Never write to stdout in MCP servers
)
logger = logging.getLogger("geometry-oracle-mcp")

# AWS API Gateway endpoint
AWS_ENDPOINT = os.environ.get(
    "AWS_ENDPOINT", "https://s6ngc23inj.execute-api.us-east-1.amazonaws.com/prod/mcp"
)

# Initialize MCP server
mcp = FastMCP("GeometryOracle")


class AWSMCPProxy:
    """Proxy class to handle AWS API calls"""

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.client = httpx.AsyncClient(timeout=30.0)

    async def call_aws_tool(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> dict[str, Any]:
        """Call AWS MCP server and return result"""
        request_data = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
            "id": 1,
        }

        try:
            logger.info(f"Calling AWS tool: {tool_name} with args: {arguments}")
            response = await self.client.post(
                self.endpoint,
                json=request_data,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            result = response.json()
            logger.info(f"AWS response: {result}")

            if "error" in result:
                raise Exception(f"AWS API error: {result['error']}")

            return result.get("result", {})

        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling AWS: {e}")
            raise Exception(f"Failed to call AWS API: {str(e)}")
        except Exception as e:
            logger.error(f"Error calling AWS tool {tool_name}: {e}")
            raise


# Initialize AWS proxy
aws_proxy = AWSMCPProxy(AWS_ENDPOINT)


@mcp.tool()
async def calculate_hypersphere(
    dimensions: int,
    radius: float,
    session_id: Optional[str] = None,
    client_info: Optional[str] = None,
) -> dict[str, Any]:
    """
    Calculate volume and surface area of N-dimensional hypersphere.

    Args:
        dimensions: Number of dimensions (1D to 100D+)
        radius: Radius of the hypersphere
        session_id: Optional session identifier
        client_info: Optional client information

    Returns:
        Dictionary with volume, surface_area, diameter, and formulas
    """
    arguments = {"dimensions": dimensions, "radius": radius}

    if session_id:
        arguments["session_id"] = session_id
    if client_info:
        arguments["client_info"] = client_info

    return await aws_proxy.call_aws_tool("calculate_hypersphere", arguments)


@mcp.tool()
async def calculate_hypercube(
    dimensions: int,
    side_length: float,
    session_id: Optional[str] = None,
    client_info: Optional[str] = None,
) -> dict[str, Any]:
    """
    Calculate volume and surface area of N-dimensional hypercube.

    Args:
        dimensions: Number of dimensions (1D to 100D+)
        side_length: Length of each side of the hypercube
        session_id: Optional session identifier
        client_info: Optional client information

    Returns:
        Dictionary with volume, surface_area, vertices, edges, and diagonal
    """
    arguments = {"dimensions": dimensions, "side_length": side_length}

    if session_id:
        arguments["session_id"] = session_id
    if client_info:
        arguments["client_info"] = client_info

    return await aws_proxy.call_aws_tool("calculate_hypercube", arguments)


@mcp.tool()
async def compare_shapes(
    shapes: list[dict[str, Any]],
    session_id: Optional[str] = None,
    client_info: Optional[str] = None,
) -> dict[str, Any]:
    """
    Compare volumes and properties of multiple N-dimensional shapes.

    Args:
        shapes: List of shape definitions with type, dimensions, and parameters
        session_id: Optional session identifier
        client_info: Optional client information

    Example shapes format:
        [
            {"type": "hypersphere", "dimensions": 3, "radius": 1.0},
            {"type": "hypercube", "dimensions": 3, "side_length": 2.0}
        ]

    Returns:
        Dictionary with shape comparisons, volume ratios, and analysis
    """
    arguments = {"shapes": shapes}

    if session_id:
        arguments["session_id"] = session_id
    if client_info:
        arguments["client_info"] = client_info

    return await aws_proxy.call_aws_tool("compare_shapes", arguments)


@mcp.tool()
async def get_usage_statistics(days: int = 7) -> dict[str, Any]:
    """
    Get usage statistics for the GeometryOracle MCP server.

    Args:
        days: Number of days to include in statistics (1-365)

    Returns:
        Dictionary with usage statistics, popular dimensions, tool usage, etc.
    """
    arguments = {"days": days}
    return await aws_proxy.call_aws_tool("get_usage_statistics", arguments)


@mcp.resource("geometry://status")
async def get_server_status() -> str:
    """Get current server status and health"""
    try:
        # Test AWS connectivity
        await aws_proxy.call_aws_tool("get_usage_statistics", {"days": 1})
        status = {
            "status": "healthy",
            "aws_endpoint": AWS_ENDPOINT,
            "connection": "active",
            "tools_available": 4,
        }
    except Exception as e:
        status = {
            "status": "unhealthy",
            "aws_endpoint": AWS_ENDPOINT,
            "connection": "failed",
            "error": str(e),
        }

    return json.dumps(status, indent=2)


@mcp.resource("geometry://tools")
async def get_available_tools() -> str:
    """Get list of available geometry calculation tools"""
    tools_info = {
        "tools": [
            {
                "name": "calculate_hypersphere",
                "description": "Calculate volume and surface area of N-dimensional hypersphere",
                "dimensions": "1D to 100D+",
                "example": "dimensions=3, radius=1.0 → volume=4.189",
            },
            {
                "name": "calculate_hypercube",
                "description": "Calculate volume and surface area of N-dimensional hypercube",
                "dimensions": "1D to 100D+",
                "example": "dimensions=3, side_length=2.0 → volume=8.0",
            },
            {
                "name": "compare_shapes",
                "description": "Compare multiple geometric shapes",
                "usage": "Accepts list of shapes with types and parameters",
            },
            {
                "name": "get_usage_statistics",
                "description": "Get server usage analytics",
                "usage": "Returns statistics for specified number of days",
            },
        ],
        "aws_backend": {
            "endpoint": AWS_ENDPOINT,
            "lambda_function": "geometry-oracle-mcp",
            "database": "geometry-oracle-mcp-prod-queries",
        },
    }

    return json.dumps(tools_info, indent=2)


def main():
    """Main entry point for MCP server"""
    logger.info("Starting GeometryOracle MCP Server")
    logger.info(f"AWS Endpoint: {AWS_ENDPOINT}")

    # Test AWS connectivity on startup
    async def test_connectivity():
        try:
            await aws_proxy.call_aws_tool("get_usage_statistics", {"days": 1})
            logger.info("✅ AWS connectivity verified")
        except Exception as e:
            logger.error(f"❌ AWS connectivity failed: {e}")
            logger.error("Server will start but AWS calls will fail")

    # Run connectivity test
    asyncio.run(test_connectivity())

    # Run the MCP server via stdio (this handles its own event loop)
    mcp.run()


if __name__ == "__main__":
    main()
