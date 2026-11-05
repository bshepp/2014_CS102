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

import math
from decimal import Context, Decimal
from typing import Annotated, Any, Dict, List, Optional

from pydantic import Field

try:  # mcp >= 2.0 renamed FastMCP to MCPServer; the parts used here are unchanged
    from mcp.server.mcpserver import MCPServer as FastMCP
except ModuleNotFoundError:
    from mcp.server.fastmcp import FastMCP

from ndgeometry import Cube, Ellipsoid, Simplex, Sphere, unit_ball_coefficient

MAX_DIMENSIONS = 100_000  # arbitrary-precision results take ~1s at this size
MAX_DIGITS = 1000
DEFAULT_DIGITS = 30
EXACT_FORM_MAX_DIMENSIONS = 100  # beyond this the exact rational coefficient is too long to be useful

INSTRUCTIONS = f"""
GeometryOracle computes properties of n-dimensional shapes (spheres, cubes, ellipsoids,
regular simplices) from closed-form formulas, in any dimension from 1 to {MAX_DIMENSIONS:,}.

Every shape result reports three levels of accuracy:
- Float values (IEEE doubles): ~15 correct digits in low dimensions, degrading roughly as
  n x 1e-16 in dimension n. They are null when the true value lies outside the double
  range (about 1e-308 to 1e308), which happens quickly in high dimensions.
- log10_volume: always finite, for magnitudes beyond the float range.
- precise: the same quantities to `digits` significant digits (default {DEFAULT_DIGITS},
  max {MAX_DIGITS}), computed with arbitrary-precision decimal arithmetic and correct in
  every digit shown. Inputs are taken as the decimal numbers given (radius 0.1 means
  exactly 0.1), and values are strings, in scientific notation when large or small.
- float_relative_error: the measured relative error of the float volume against the
  precise value, so the float's accuracy is known rather than assumed.

For spheres and ellipsoids in up to {EXACT_FORM_MAX_DIMENSIONS} dimensions, exact_volume gives the exact
closed form: a rational number times a power of pi (e.g. "8/15 * pi^2 * r^5").
"""

mcp = FastMCP("GeometryOracle", instructions=INSTRUCTIONS.strip())

Dimensions = Annotated[int, Field(ge=1, le=MAX_DIMENSIONS, description="Number of dimensions")]
Digits = Annotated[int, Field(ge=1, le=MAX_DIGITS,
                              description="Significant digits for the arbitrary-precision results")]
Positive = Annotated[float, Field(gt=0)]


def _float(x: float) -> Optional[float]:
    """A float for JSON, or None when it over/underflowed the double range."""
    return x if math.isfinite(x) and x != 0 else None


def _report(shape, digits: int, **properties: float) -> Dict[str, Any]:
    """Float properties, log10 volume, the same values to `digits` digits, and the float's error."""
    precise = shape.precise(digits)
    reference = precise["volume"] if digits >= 20 else shape.precise(20)["volume"]
    volume = properties["volume"]
    out: Dict[str, Any] = {key: _float(value) for key, value in properties.items()}
    out["log10_volume"] = shape.log_volume / math.log(10)
    out["precise"] = {"digits": digits, **{key: str(value) for key, value in precise.items()}}
    out["float_relative_error"] = (
        float(abs(Decimal(volume) / reference - 1)) if _float(volume) is not None else None
    )
    if out["volume"] is None:
        out["note"] = ("The volume is outside double-precision float range; "
                       "use log10_volume or the precise values.")
    return out


def _count(x: int, digits: int):
    """An exact int when JSON clients can hold it (< 2^53), else a string in scientific notation."""
    return x if x < 2 ** 53 else str(Context(prec=digits).create_decimal(x))


def _exact_volume(n: int, size: str) -> str:
    """Closed form of an n-ball volume: rational coefficient * pi^k * size, e.g. '8/15 * pi^2 * r^5'."""
    c, k = unit_ball_coefficient(n), n // 2
    parts = [str(c)] if (c != 1 or k == 0) else []
    if k:
        parts.append("pi" if k == 1 else f"pi^{k}")
    return " * ".join(parts + [size])


@mcp.tool()
def sphere(dimensions: Dimensions, radius: Positive, digits: Digits = DEFAULT_DIGITS) -> Dict[str, Any]:
    """
    Calculate n-dimensional sphere properties in any dimension (1 to 100,000).

    Args:
        dimensions: Number of dimensions
        radius: Radius of the sphere
        digits: Significant digits for the arbitrary-precision results (default 30, max 1000)

    Returns:
        Float volume and surface area (null outside the double range), log10 of the
        volume (always finite), the same values correct to `digits` digits under
        "precise", the measured relative error of the float volume, and for
        dimensions <= 100 the exact closed form (rational * pi^k * r^n).
    """
    s = Sphere(dimensions, radius)
    out: Dict[str, Any] = {"shape": s.name, "dimensions": dimensions, "radius": radius,
                           "diameter": s.diameter}
    out.update(_report(s, digits, volume=s.volume, surface_area=s.surface_area))
    out["formula"] = "volume = pi^(n/2) / Gamma(n/2 + 1) * r^n;  surface_area = n * volume / r"
    if dimensions <= EXACT_FORM_MAX_DIMENSIONS:
        out["exact_volume"] = _exact_volume(dimensions, "r" if dimensions == 1 else f"r^{dimensions}")
    return out


@mcp.tool()
def cube(dimensions: Dimensions, side: Positive, digits: Digits = DEFAULT_DIGITS) -> Dict[str, Any]:
    """
    Calculate n-dimensional hypercube properties in any dimension (1 to 100,000).

    Args:
        dimensions: Number of dimensions
        side: Side length
        digits: Significant digits for the arbitrary-precision results (default 30, max 1000)

    Returns:
        Float volume, surface area and diagonal (null outside the double range),
        log10 of the volume, the same values correct to `digits` digits under
        "precise", the measured float error, and the vertex and edge counts (exact
        integers below 2^53, otherwise strings in scientific notation).
    """
    c = Cube(dimensions, side)
    out: Dict[str, Any] = {"shape": c.name, "dimensions": dimensions, "side": side,
                           "vertices": _count(c.vertices, digits), "edges": _count(c.edges, digits)}
    out.update(_report(c, digits, volume=c.volume, surface_area=c.surface_area, diagonal=c.diagonal))
    out["formula"] = "volume = s^n;  surface_area = 2n * s^(n-1);  diagonal = s * sqrt(n)"
    return out


@mcp.tool()
def ellipsoid(semi_axes: List[Positive], digits: Digits = DEFAULT_DIGITS) -> Dict[str, Any]:
    """
    Calculate n-dimensional ellipsoid properties (one semi-axis per dimension, up to 100,000).

    Args:
        semi_axes: List of semi-axis lengths (one per dimension)
        digits: Significant digits for the arbitrary-precision results (default 30, max 1000)

    Returns:
        Float volume (null outside the double range), log10 of the volume, the volume
        correct to `digits` digits under "precise", the measured float error, shape
        classification, and for dimensions <= 100 the exact closed form.
    """
    if not 1 <= len(semi_axes) <= MAX_DIMENSIONS:
        raise ValueError(f"semi_axes must have between 1 and {MAX_DIMENSIONS} entries")
    e = Ellipsoid(tuple(semi_axes))
    out: Dict[str, Any] = {"shape": e.name, "dimensions": e.dimensions, "semi_axes": semi_axes,
                           "is_sphere": e.is_sphere}
    out.update(_report(e, digits, volume=e.volume))
    out["formula"] = "volume = pi^(n/2) / Gamma(n/2 + 1) * (a_1 * a_2 * ... * a_n)"
    if e.dimensions <= EXACT_FORM_MAX_DIMENSIONS:
        out["exact_volume"] = _exact_volume(e.dimensions, "(product of semi-axes)")
    return out


@mcp.tool()
def simplex(dimensions: Dimensions, side: Positive, digits: Digits = DEFAULT_DIGITS) -> Dict[str, Any]:
    """
    Calculate n-dimensional regular simplex properties in any dimension (1 to 100,000).

    Args:
        dimensions: Number of dimensions
        side: Edge length
        digits: Significant digits for the arbitrary-precision results (default 30, max 1000)

    Returns:
        Float volume and surface area (null outside the double range), log10 of the
        volume, the same values correct to `digits` digits under "precise", the
        measured float error, and the exact vertex and edge counts.
    """
    s = Simplex(dimensions, side)
    out: Dict[str, Any] = {"shape": s.name, "dimensions": dimensions, "side": side,
                           "vertices": s.vertices, "edges": s.edges}
    out.update(_report(s, digits, volume=s.volume, surface_area=s.surface_area))
    out["formula"] = ("volume = s^n / n! * sqrt((n+1) / 2^n);  "
                      "surface_area = (n+1) facets, each a regular (n-1)-simplex")
    return out


_SHAPES = {"sphere": Sphere, "cube": Cube, "simplex": Simplex}


def _make_shape(shape_type: str, dimensions: int, size: float):
    try:
        cls = _SHAPES[shape_type.lower()]
    except KeyError:
        raise ValueError(f"shape type must be one of {sorted(_SHAPES)}, got: {shape_type}") from None
    return cls(dimensions, size)


def _ratio(a: float, b: float) -> Optional[float]:
    return _float(a / b) if b else None


@mcp.tool()
def compare(
    shape1_type: str,
    shape1_dim: Dimensions,
    shape1_size: Positive,
    shape2_type: str,
    shape2_dim: Dimensions,
    shape2_size: Positive,
) -> Dict[str, Any]:
    """
    Compare two shapes.

    Args:
        shape1_type: "sphere", "cube" or "simplex"
        shape1_dim: Dimensions for shape 1
        shape1_size: Radius (sphere) or side (cube, simplex) for shape 1
        shape2_type: "sphere", "cube" or "simplex"
        shape2_dim: Dimensions for shape 2
        shape2_size: Radius (sphere) or side (cube, simplex) for shape 2

    Returns:
        Volumes, surface areas and their ratios. The log10 ratio is always finite,
        even when the volumes themselves are outside the float range. Note: ratios
        between shapes of different dimensionality compare an n-volume to an
        m-volume, which is not dimensionally meaningful — a note is included when
        this happens.
    """
    s1 = _make_shape(shape1_type, shape1_dim, shape1_size)
    s2 = _make_shape(shape2_type, shape2_dim, shape2_size)
    log_ratio = s1.log_volume - s2.log_volume

    def describe(s):
        return {"name": s.name, "volume": _float(s.volume), "surface_area": _float(s.surface_area),
                "log10_volume": s.log_volume / math.log(10)}

    result: Dict[str, Any] = {
        "shape1": describe(s1),
        "shape2": describe(s2),
        "volume_ratio": _float(math.exp(log_ratio)) if log_ratio < 709 else None,
        "log10_volume_ratio": log_ratio / math.log(10),
        "surface_ratio": _ratio(s1.surface_area, s2.surface_area),
    }
    if shape1_dim != shape2_dim:
        result["note"] = (
            f"Shapes have different dimensionality ({shape1_dim}D vs {shape2_dim}D); "
            "the ratios compare volumes of different dimension and are not directly meaningful."
        )
    return result


@mcp.tool()
def volume_by_dimension(
    shape_type: str,
    size: Positive,
    max_dim: Annotated[int, Field(ge=1, le=1000, description="Highest dimension to include")] = 10,
) -> Dict[str, Any]:
    """
    Show how volume changes across dimensions (demonstrates the "curse of dimensionality").

    Args:
        shape_type: "sphere", "cube" or "simplex"
        size: Radius (sphere) or side (cube, simplex)
        max_dim: Maximum dimension to calculate (default 10, max 1000)

    Returns:
        Float volumes for dimensions 1 through max_dim (null outside the double
        range) and their log10 values, which stay finite, plus the dimension
        where the volume peaks.
    """
    shapes = [_make_shape(shape_type, d, size) for d in range(1, max_dim + 1)]
    log10_volumes = {s.dimensions: s.log_volume / math.log(10) for s in shapes}
    peak_dim = max(log10_volumes, key=log10_volumes.get)
    if peak_dim in (1, max_dim):
        note = f"Volume is monotonic from 1D to {max_dim}D for this size (largest at {peak_dim}D)."
    else:
        note = (f"Volume peaks at {peak_dim}D for this size, then decreases toward zero "
                "(for a unit sphere the peak is at 5D).")

    return {
        "shape_type": shape_type,
        "size": size,
        "volumes_by_dimension": {s.dimensions: _float(s.volume) for s in shapes},
        "log10_volumes_by_dimension": log10_volumes,
        "peak_dimension": peak_dim,
        "note": note,
    }


if __name__ == "__main__":
    mcp.run()
