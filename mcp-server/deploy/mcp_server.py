"""
GeometryOracle MCP Server
Model Context Protocol server for N-dimensional geometry calculations with data collection
"""

import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
import traceback

from mcp.server.fastmcp import FastMCP
from mcp.server import NotificationOptions
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from database import DatabaseManager, PerformanceMonitor
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from geometry_engine import HyperSphere, HyperCube, HyperEllipsoid, Simplex, HyperPyramid


class GeometryOracleMCP:
    def __init__(self):
        self.db = DatabaseManager()
        self.app = FastMCP("GeometryOracle")
        self._setup_tools()
        self._setup_resources()
    
    def _setup_tools(self):
        """Register MCP tools for geometry calculations"""
        
        @self.app.tool()
        async def calculate_hypersphere(
            dimensions: int,
            radius: float,
            session_id: str = None,
            client_info: str = None
        ) -> Dict[str, Any]:
            """Calculate volume and surface area of N-dimensional hypersphere"""
            
            monitor = PerformanceMonitor()
            monitor.start_monitoring()
            
            input_params = {
                "dimensions": dimensions,
                "radius": radius,
                "tool": "calculate_hypersphere"
            }
            
            try:
                # Create hypersphere and calculate properties
                sphere = HyperSphere(dimensions, radius)
                
                results = {
                    "shape_type": "hypersphere",
                    "dimensions": dimensions,
                    "radius": radius,
                    "volume": sphere.get_volume(),
                    "surface_area": sphere.get_surface_area(),
                    "diameter": sphere.get_diameter(),
                    "volume_formula": sphere.get_volume_formula(),
                    "surface_area_formula": sphere.get_surface_area_formula()
                }
                
                # Get performance metrics
                metrics = monitor.get_metrics()
                
                # Log to database
                await self.db.log_query(
                    tool_name="calculate_hypersphere",
                    input_parameters=input_params,
                    output_results=results,
                    success=True,
                    session_id=session_id,
                    client_info=client_info,
                    dimensions=dimensions,
                    shape_type="hypersphere",
                    **metrics
                )
                
                # Update stats
                await self.db.update_tool_stats("calculate_hypersphere", metrics["execution_time_ms"], True, session_id)
                await self.db.update_dimension_stats(dimensions, "hypersphere", metrics["execution_time_ms"])
                
                return results
                
            except Exception as e:
                error_msg = str(e)
                metrics = monitor.get_metrics()
                
                # Log error
                await self.db.log_query(
                    tool_name="calculate_hypersphere",
                    input_parameters=input_params,
                    success=False,
                    error_message=error_msg,
                    session_id=session_id,
                    client_info=client_info,
                    **metrics
                )
                
                await self.db.log_error(
                    tool_name="calculate_hypersphere",
                    error_type=type(e).__name__,
                    error_message=error_msg,
                    input_parameters=input_params,
                    stack_trace=traceback.format_exc()
                )
                
                raise
        
        @self.app.tool()
        async def calculate_hypercube(
            dimensions: int,
            side_length: float,
            session_id: str = None,
            client_info: str = None
        ) -> Dict[str, Any]:
            """Calculate volume and surface area of N-dimensional hypercube"""
            
            monitor = PerformanceMonitor()
            monitor.start_monitoring()
            
            input_params = {
                "dimensions": dimensions,
                "side_length": side_length,
                "tool": "calculate_hypercube"
            }
            
            try:
                cube = HyperCube(dimensions, side_length)
                
                results = {
                    "shape_type": "hypercube",
                    "dimensions": dimensions,
                    "side_length": side_length,
                    "volume": cube.get_volume(),
                    "surface_area": cube.get_surface_area(),
                    "vertices": 2 ** dimensions,
                    "edges": dimensions * (2 ** (dimensions - 1)) if dimensions > 0 else 0,
                    "diagonal": cube.get_diagonal_length() if hasattr(cube, 'get_diagonal_length') else None
                }
                
                metrics = monitor.get_metrics()
                
                await self.db.log_query(
                    tool_name="calculate_hypercube",
                    input_parameters=input_params,
                    output_results=results,
                    success=True,
                    session_id=session_id,
                    client_info=client_info,
                    dimensions=dimensions,
                    shape_type="hypercube",
                    **metrics
                )
                
                await self.db.update_tool_stats("calculate_hypercube", metrics["execution_time_ms"], True, session_id)
                await self.db.update_dimension_stats(dimensions, "hypercube", metrics["execution_time_ms"])
                
                return results
                
            except Exception as e:
                error_msg = str(e)
                metrics = monitor.get_metrics()
                
                await self.db.log_query(
                    tool_name="calculate_hypercube",
                    input_parameters=input_params,
                    success=False,
                    error_message=error_msg,
                    session_id=session_id,
                    client_info=client_info,
                    **metrics
                )
                
                await self.db.log_error(
                    tool_name="calculate_hypercube",
                    error_type=type(e).__name__,
                    error_message=error_msg,
                    input_parameters=input_params,
                    stack_trace=traceback.format_exc()
                )
                
                raise
        
        @self.app.tool()
        async def compare_shapes(
            shapes: List[Dict[str, Any]],
            session_id: str = None,
            client_info: str = None
        ) -> Dict[str, Any]:
            """Compare volumes and properties of multiple N-dimensional shapes"""
            
            monitor = PerformanceMonitor()
            monitor.start_monitoring()
            
            input_params = {
                "shapes": shapes,
                "tool": "compare_shapes"
            }
            
            try:
                comparisons = []
                
                for shape_config in shapes:
                    shape_type = shape_config.get("type")
                    dimensions = shape_config.get("dimensions")
                    
                    if shape_type == "hypersphere":
                        radius = shape_config.get("radius", 1.0)
                        shape = HyperSphere(dimensions, radius)
                        comparisons.append({
                            "type": "hypersphere",
                            "dimensions": dimensions,
                            "radius": radius,
                            "volume": shape.get_volume(),
                            "surface_area": shape.get_surface_area()
                        })
                    elif shape_type == "hypercube":
                        side = shape_config.get("side_length", 1.0)
                        shape = HyperCube(dimensions, side)
                        comparisons.append({
                            "type": "hypercube",
                            "dimensions": dimensions,
                            "side_length": side,
                            "volume": shape.get_volume(),
                            "surface_area": shape.get_surface_area()
                        })
                
                # Calculate ratios and relationships
                if len(comparisons) >= 2:
                    volume_ratios = []
                    for i in range(len(comparisons) - 1):
                        ratio = comparisons[i]["volume"] / comparisons[i + 1]["volume"]
                        volume_ratios.append({
                            "shape_1": comparisons[i]["type"],
                            "shape_2": comparisons[i + 1]["type"],
                            "volume_ratio": ratio
                        })
                else:
                    volume_ratios = []
                
                results = {
                    "shapes": comparisons,
                    "volume_ratios": volume_ratios,
                    "largest_volume": max(comparisons, key=lambda x: x["volume"]) if comparisons else None,
                    "comparison_count": len(comparisons)
                }
                
                metrics = monitor.get_metrics()
                
                await self.db.log_query(
                    tool_name="compare_shapes",
                    input_parameters=input_params,
                    output_results=results,
                    success=True,
                    session_id=session_id,
                    client_info=client_info,
                    dimensions=shapes[0].get("dimensions") if shapes else None,
                    shape_type="comparison",
                    **metrics
                )
                
                await self.db.update_tool_stats("compare_shapes", metrics["execution_time_ms"], True, session_id)
                
                return results
                
            except Exception as e:
                error_msg = str(e)
                metrics = monitor.get_metrics()
                
                await self.db.log_query(
                    tool_name="compare_shapes",
                    input_parameters=input_params,
                    success=False,
                    error_message=error_msg,
                    session_id=session_id,
                    client_info=client_info,
                    **metrics
                )
                
                await self.db.log_error(
                    tool_name="compare_shapes",
                    error_type=type(e).__name__,
                    error_message=error_msg,
                    input_parameters=input_params,
                    stack_trace=traceback.format_exc()
                )
                
                raise
        
        @self.app.tool()
        async def get_usage_statistics(days: int = 7) -> Dict[str, Any]:
            """Get usage statistics for the MCP server (meta tool!)"""
            
            monitor = PerformanceMonitor()
            monitor.start_monitoring()
            
            try:
                stats = await self.db.get_usage_stats(days)
                
                metrics = monitor.get_metrics()
                
                await self.db.log_query(
                    tool_name="get_usage_statistics",
                    input_parameters={"days": days},
                    output_results=stats,
                    success=True,
                    **metrics
                )
                
                return stats
                
            except Exception as e:
                error_msg = str(e)
                await self.db.log_error(
                    tool_name="get_usage_statistics",
                    error_type=type(e).__name__,
                    error_message=error_msg,
                    input_parameters={"days": days}
                )
                raise
    
    def _setup_resources(self):
        """Setup MCP resources"""
        
        @self.app.resource("geometry://stats/usage")
        async def get_usage_stats() -> str:
            """Get current usage statistics"""
            stats = await self.db.get_usage_stats(30)
            return json.dumps(stats, indent=2)
        
        @self.app.resource("geometry://data/export")
        async def export_data() -> str:
            """Export all collected data (for research)"""
            # This would return the full dataset
            return json.dumps({"message": "Data export endpoint - implement as needed"})
    
    def get_app(self):
        """Get the FastMCP app"""
        return self.app


# Create the MCP server instance
server = GeometryOracleMCP()
app = server.get_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)