"""
GeometryOracle MCP Server
Model Context Protocol server for N-dimensional geometry calculations with data collection
"""

import json
import math
import os
import sys
import traceback
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from database import DatabaseManager, PerformanceMonitor
from mcp.server import NotificationOptions
from mcp.server.fastmcp import FastMCP
from mcp.types import (
    EmbeddedResource,
    ImageContent,
    Resource,
    TextContent,
    Tool,
)

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from geometry_engine import (
    HyperCube,
    HyperEllipsoid,
    HyperPyramid,
    HyperSphere,
    Simplex,
)


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
            client_info: str = None,
        ) -> Dict[str, Any]:
            """Calculate volume and surface area of N-dimensional hypersphere"""

            monitor = PerformanceMonitor()
            monitor.start_monitoring()

            input_params = {
                "dimensions": dimensions,
                "radius": radius,
                "tool": "calculate_hypersphere",
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
                    "surface_area_formula": sphere.get_surface_area_formula(),
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
                    **metrics,
                )

                # Update stats
                await self.db.update_tool_stats(
                    "calculate_hypersphere",
                    metrics["execution_time_ms"],
                    True,
                    session_id,
                )
                await self.db.update_dimension_stats(
                    dimensions, "hypersphere", metrics["execution_time_ms"]
                )

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
                    **metrics,
                )

                await self.db.log_error(
                    tool_name="calculate_hypersphere",
                    error_type=type(e).__name__,
                    error_message=error_msg,
                    input_parameters=input_params,
                    stack_trace=traceback.format_exc(),
                )

                raise

        @self.app.tool()
        async def calculate_hypercube(
            dimensions: int,
            side_length: float,
            session_id: str = None,
            client_info: str = None,
        ) -> Dict[str, Any]:
            """Calculate volume and surface area of N-dimensional hypercube"""

            monitor = PerformanceMonitor()
            monitor.start_monitoring()

            input_params = {
                "dimensions": dimensions,
                "side_length": side_length,
                "tool": "calculate_hypercube",
            }

            try:
                cube = HyperCube(dimensions, side_length)

                results = {
                    "shape_type": "hypercube",
                    "dimensions": dimensions,
                    "side_length": side_length,
                    "volume": cube.get_volume(),
                    "surface_area": cube.get_surface_area(),
                    "vertices": 2**dimensions,
                    "edges": (
                        dimensions * (2 ** (dimensions - 1)) if dimensions > 0 else 0
                    ),
                    "diagonal": (
                        cube.get_diagonal_length()
                        if hasattr(cube, "get_diagonal_length")
                        else None
                    ),
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
                    **metrics,
                )

                await self.db.update_tool_stats(
                    "calculate_hypercube",
                    metrics["execution_time_ms"],
                    True,
                    session_id,
                )
                await self.db.update_dimension_stats(
                    dimensions, "hypercube", metrics["execution_time_ms"]
                )

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
                    **metrics,
                )

                await self.db.log_error(
                    tool_name="calculate_hypercube",
                    error_type=type(e).__name__,
                    error_message=error_msg,
                    input_parameters=input_params,
                    stack_trace=traceback.format_exc(),
                )

                raise

        @self.app.tool()
        async def compare_shapes(
            shapes: List[Dict[str, Any]],
            session_id: str = None,
            client_info: str = None,
        ) -> Dict[str, Any]:
            """Compare volumes and properties of multiple N-dimensional shapes"""

            monitor = PerformanceMonitor()
            monitor.start_monitoring()

            input_params = {"shapes": shapes, "tool": "compare_shapes"}

            try:
                comparisons = []

                for shape_config in shapes:
                    shape_type = shape_config.get("type")
                    dimensions = shape_config.get("dimensions")

                    if shape_type == "hypersphere":
                        radius = shape_config.get("radius", 1.0)
                        shape = HyperSphere(dimensions, radius)
                        comparisons.append(
                            {
                                "type": "hypersphere",
                                "dimensions": dimensions,
                                "radius": radius,
                                "volume": shape.get_volume(),
                                "surface_area": shape.get_surface_area(),
                            }
                        )
                    elif shape_type == "hypercube":
                        side = shape_config.get("side_length", 1.0)
                        shape = HyperCube(dimensions, side)
                        comparisons.append(
                            {
                                "type": "hypercube",
                                "dimensions": dimensions,
                                "side_length": side,
                                "volume": shape.get_volume(),
                                "surface_area": shape.get_surface_area(),
                            }
                        )

                # Calculate ratios and relationships
                if len(comparisons) >= 2:
                    volume_ratios = []
                    for i in range(len(comparisons) - 1):
                        ratio = comparisons[i]["volume"] / comparisons[i + 1]["volume"]
                        volume_ratios.append(
                            {
                                "shape_1": comparisons[i]["type"],
                                "shape_2": comparisons[i + 1]["type"],
                                "volume_ratio": ratio,
                            }
                        )
                else:
                    volume_ratios = []

                results = {
                    "shapes": comparisons,
                    "volume_ratios": volume_ratios,
                    "largest_volume": (
                        max(comparisons, key=lambda x: x["volume"])
                        if comparisons
                        else None
                    ),
                    "comparison_count": len(comparisons),
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
                    **metrics,
                )

                await self.db.update_tool_stats(
                    "compare_shapes", metrics["execution_time_ms"], True, session_id
                )

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
                    **metrics,
                )

                await self.db.log_error(
                    tool_name="compare_shapes",
                    error_type=type(e).__name__,
                    error_message=error_msg,
                    input_parameters=input_params,
                    stack_trace=traceback.format_exc(),
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
                    **metrics,
                )

                return stats

            except Exception as e:
                error_msg = str(e)
                await self.db.log_error(
                    tool_name="get_usage_statistics",
                    error_type=type(e).__name__,
                    error_message=error_msg,
                    input_parameters={"days": days},
                )
                raise

        @self.app.tool()
        async def batch_geometry_calculations(
            shapes: List[Dict[str, Any]],
            operations: List[str] = ["volume", "surface_area"],
            session_id: str = None,
            client_info: str = None,
        ) -> Dict[str, Any]:
            """Calculate multiple shapes in one request - perfect for AI agents analyzing datasets"""

            monitor = PerformanceMonitor()
            monitor.start_monitoring()

            input_params = {
                "shapes": shapes,
                "operations": operations,
                "tool": "batch_geometry_calculations",
            }

            try:
                results = []
                for shape_def in shapes:
                    shape_type = shape_def.get("type")
                    dimensions = shape_def.get("dimensions")
                    parameter = shape_def.get("parameter")

                    if shape_type == "hypersphere":
                        shape = HyperSphere(dimensions, parameter)
                        shape_result = {
                            "shape_type": "hypersphere",
                            "dimensions": dimensions,
                            "radius": parameter,
                        }
                    elif shape_type == "hypercube":
                        shape = HyperCube(dimensions, parameter)
                        shape_result = {
                            "shape_type": "hypercube",
                            "dimensions": dimensions,
                            "side_length": parameter,
                        }
                    else:
                        continue

                    # Extract requested properties
                    if "volume" in operations:
                        shape_result["volume"] = shape.get_volume()
                    if "surface_area" in operations:
                        shape_result["surface_area"] = shape.get_surface_area()
                    if "properties" in operations:
                        shape_result["properties"] = {
                            "formulas": {
                                "volume": getattr(
                                    shape, "get_volume_formula", lambda: "N/A"
                                )(),
                                "surface_area": getattr(
                                    shape, "get_surface_area_formula", lambda: "N/A"
                                )(),
                            }
                        }

                    results.append(shape_result)

                metrics = monitor.get_metrics()
                batch_result = {
                    "success": True,
                    "total_shapes": len(results),
                    "operations_performed": operations,
                    "results": results,
                }

                # Log to database
                await self.db.log_query(
                    tool_name="batch_geometry_calculations",
                    input_parameters=input_params,
                    output_results=batch_result,
                    success=True,
                    session_id=session_id,
                    client_info=client_info,
                    **metrics,
                )

                return batch_result

            except Exception as e:
                error_msg = str(e)
                metrics = monitor.get_metrics()

                await self.db.log_query(
                    tool_name="batch_geometry_calculations",
                    input_parameters=input_params,
                    success=False,
                    error_message=error_msg,
                    session_id=session_id,
                    client_info=client_info,
                    **metrics,
                )

                await self.db.log_error(
                    tool_name="batch_geometry_calculations",
                    error_type=type(e).__name__,
                    error_message=error_msg,
                    input_parameters=input_params,
                    stack_trace=traceback.format_exc(),
                )
                raise

        @self.app.tool()
        async def analyze_dimension_scaling(
            shape_type: str,
            property_name: str = "volume",
            dimension_range: Dict[str, int] = {"start": 1, "end": 10},
            parameter_value: float = 1.0,
            session_id: str = None,
            client_info: str = None,
        ) -> Dict[str, Any]:
            """Show how properties change with dimensions - fascinating for AI analysis"""

            monitor = PerformanceMonitor()
            monitor.start_monitoring()

            input_params = {
                "shape_type": shape_type,
                "property": property_name,
                "dimension_range": dimension_range,
                "parameter_value": parameter_value,
                "tool": "analyze_dimension_scaling",
            }

            try:
                start_dim = dimension_range.get("start", 1)
                end_dim = min(dimension_range.get("end", 10), 20)  # Limit to 20D max

                scaling_data = []

                for dim in range(start_dim, end_dim + 1):
                    try:
                        if shape_type == "hypersphere":
                            shape = HyperSphere(dim, parameter_value)
                        elif shape_type == "hypercube":
                            shape = HyperCube(dim, parameter_value)
                        else:
                            continue

                        if property_name == "volume":
                            value = shape.get_volume()
                        elif property_name == "surface_area":
                            value = shape.get_surface_area()
                        elif (
                            property_name == "diameter" and shape_type == "hypersphere"
                        ):
                            value = shape.get_diameter()
                        else:
                            continue

                        scaling_data.append(
                            {
                                "dimensions": dim,
                                "value": value,
                                "log_value": math.log10(max(value, 1e-10)),
                            }
                        )

                    except Exception:
                        continue

                # Find peak dimension
                peak_dim = None
                peak_value = 0
                for data_point in scaling_data:
                    if data_point["value"] > peak_value:
                        peak_value = data_point["value"]
                        peak_dim = data_point["dimensions"]

                results = {
                    "success": True,
                    "shape_type": shape_type,
                    "property": property_name,
                    "parameter_value": parameter_value,
                    "dimension_range": f"{start_dim}D to {end_dim}D",
                    "scaling_data": scaling_data,
                    "insights": {
                        "peak_dimension": peak_dim,
                        "peak_value": peak_value,
                        "total_data_points": len(scaling_data),
                        "scaling_pattern": (
                            "Volume peaks around 5-7D for unit hyperspheres"
                            if shape_type == "hypersphere" and property_name == "volume"
                            else "Monotonic growth"
                        ),
                    },
                }

                metrics = monitor.get_metrics()

                # Log to database
                await self.db.log_query(
                    tool_name="analyze_dimension_scaling",
                    input_parameters=input_params,
                    output_results=results,
                    success=True,
                    session_id=session_id,
                    client_info=client_info,
                    **metrics,
                )

                return results

            except Exception as e:
                error_msg = str(e)
                metrics = monitor.get_metrics()

                await self.db.log_query(
                    tool_name="analyze_dimension_scaling",
                    input_parameters=input_params,
                    success=False,
                    error_message=error_msg,
                    session_id=session_id,
                    client_info=client_info,
                    **metrics,
                )

                await self.db.log_error(
                    tool_name="analyze_dimension_scaling",
                    error_type=type(e).__name__,
                    error_message=error_msg,
                    input_parameters=input_params,
                    stack_trace=traceback.format_exc(),
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
