#!/usr/bin/env python3
"""
GeometryOracle MCP Server

A simple MCP server for n-dimensional geometry calculations.
Uses local computation - no AWS, no proxies, just math.

Setup for Claude Desktop (add to claude_desktop_config.json):
{
  "mcpServers": {
    "geometry": {
      "command": "python",
      "args": ["/path/to/2014_CS102/mcp_server.py"]
    }
  }
}
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

from ndgeometry import Cube, Ellipsoid, Simplex, Sphere

mcp = FastMCP("GeometryOracle")


@mcp.tool()
def sphere(dimensions: int, radius: float) -> Dict[str, Any]:
    """
    Calculate n-dimensional sphere properties.

    Args:
        dimensions: Number of dimensions
        radius: Radius of the sphere
    
    Returns:
        Volume, surface area, and other properties
    """
    s = Sphere(dimensions, radius)
    return {
        "shape": s.name,
        "dimensions": dimensions,
        "radius": radius,
        "volume": s.volume,
        "surface_area": s.surface_area,
        "diameter": s.diameter,
    }


@mcp.tool()
def cube(dimensions: int, side: float) -> Dict[str, Any]:
    """
    Calculate n-dimensional hypercube properties.

    Args:
        dimensions: Number of dimensions
        side: Side length
    
    Returns:
        Volume, surface area, vertices, edges, diagonal
    """
    c = Cube(dimensions, side)
    return {
        "shape": c.name,
        "dimensions": dimensions,
        "side": side,
        "volume": c.volume,
        "surface_area": c.surface_area,
        "vertices": c.vertices,
        "edges": c.edges,
        "diagonal": c.diagonal,
    }


@mcp.tool()
def ellipsoid(semi_axes: List[float]) -> Dict[str, Any]:
    """
    Calculate n-dimensional ellipsoid properties.
    
    Args:
        semi_axes: List of semi-axis lengths (one per dimension)
    
    Returns:
        Volume and shape classification
    """
    e = Ellipsoid(tuple(semi_axes))
    return {
        "shape": e.name,
        "dimensions": e.dimensions,
        "semi_axes": semi_axes,
        "volume": e.volume,
        "is_sphere": e.is_sphere,
    }


@mcp.tool()
def simplex(dimensions: int, side: float) -> Dict[str, Any]:
    """
    Calculate n-dimensional regular simplex properties.

    Args:
        dimensions: Number of dimensions
        side: Edge length
    
    Returns:
        Volume, vertices, edges
    """
    s = Simplex(dimensions, side)
    return {
        "shape": s.name,
        "dimensions": dimensions,
        "side": side,
        "volume": s.volume,
        "vertices": s.vertices,
        "edges": s.edges,
    }


@mcp.tool()
def compare(
    shape1_type: str,
    shape1_dim: int,
    shape1_size: float,
    shape2_type: str,
    shape2_dim: int,
    shape2_size: float,
) -> Dict[str, Any]:
    """
    Compare two shapes.
    
    Args:
        shape1_type: "sphere" or "cube"
        shape1_dim: Dimensions for shape 1
        shape1_size: Radius (sphere) or side (cube) for shape 1
        shape2_type: "sphere" or "cube"
        shape2_dim: Dimensions for shape 2
        shape2_size: Radius (sphere) or side (cube) for shape 2
    
    Returns:
        Comparison of volumes and surface areas
    """
    def make_shape(stype: str, dim: int, size: float):
        if stype.lower() == "sphere":
            return Sphere(dim, size)
        elif stype.lower() == "cube":
            return Cube(dim, size)
        else:
            raise ValueError(f"Unknown shape type: {stype}")
    
    s1 = make_shape(shape1_type, shape1_dim, shape1_size)
    s2 = make_shape(shape2_type, shape2_dim, shape2_size)
    
    return {
        "shape1": {"name": s1.name, "volume": s1.volume, "surface_area": s1.surface_area},
        "shape2": {"name": s2.name, "volume": s2.volume, "surface_area": s2.surface_area},
        "volume_ratio": s1.volume / s2.volume,
        "surface_ratio": s1.surface_area / s2.surface_area,
    }


@mcp.tool()
def volume_by_dimension(
    shape_type: str, size: float, max_dim: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Show how volume changes across dimensions (demonstrates the "curse of dimensionality").
    
    Args:
        shape_type: "sphere" or "cube"
        size: Radius (sphere) or side (cube)
        max_dim: Maximum dimension to calculate (default 10)
    
    Returns:
        Volumes for dimensions 1 through max_dim
    """
    max_dim = min(max_dim or 10, 50)  # Cap at 50
    stype = shape_type.lower()
    if stype not in ("sphere", "cube"):
        raise ValueError(f"shape_type must be 'sphere' or 'cube', got: {shape_type}")

    volumes = {}
    for d in range(1, max_dim + 1):
        if stype == "sphere":
            volumes[d] = Sphere(d, size).volume
        else:
            volumes[d] = Cube(d, size).volume

    peak_dim = max(volumes, key=volumes.get)

    return {
        "shape_type": shape_type,
        "size": size,
        "volumes_by_dimension": volumes,
        "peak_dimension": peak_dim if stype == "sphere" else None,
        "note": "For unit spheres, volume peaks around 5D then decreases!" if stype == "sphere" else None,
    }


if __name__ == "__main__":
    mcp.run()

