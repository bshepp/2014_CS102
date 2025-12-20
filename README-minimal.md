# N-Dimensional Geometry

A tiny Python library for n-dimensional shape calculations.

## Origin Story

This started as an 84-line Java assignment in CS102 (Fall 2014) to calculate sphere volume and surface area. Eleven years and much over-engineering later, we've returned to simplicity: ~150 lines of Python that actually do something useful.

The original Java is preserved in `src/java/original/` for historical purposes.

## Installation

```bash
# The library itself needs nothing - pure Python 3.8+
# For MCP server integration with Claude Desktop:
pip install "mcp[cli]"
```

## Usage

### As a Library

```python
from ndgeometry import Sphere, Cube, Ellipsoid, Simplex

# 4D sphere
s = Sphere(dimensions=4, radius=2.0)
print(f"Volume: {s.volume}")        # 39.478...
print(f"Surface: {s.surface_area}") # 78.956...

# 3D cube
c = Cube(dimensions=3, side=2.0)
print(f"Volume: {c.volume}")    # 8.0
print(f"Diagonal: {c.diagonal}") # 3.464...

# Ellipsoid with different axes
e = Ellipsoid(semi_axes=(1.0, 2.0, 3.0))
print(f"Volume: {e.volume}")  # 25.132...

# Fun fact: unit sphere volume peaks at 5D!
for n in range(1, 10):
    print(f"{n}D: {Sphere(n, 1.0).volume:.4f}")
```

### As an MCP Server (Claude Desktop)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "geometry": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}
```

Then ask Claude things like:
- "What's the volume of a 7-dimensional sphere with radius 3?"
- "Compare a 4D sphere to a 4D cube with the same 'size'"
- "Show me how sphere volume changes from 1D to 15D"

## Available Shapes

| Shape | Class | Key Properties |
|-------|-------|----------------|
| N-sphere | `Sphere(dimensions, radius)` | volume, surface_area, diameter |
| N-cube | `Cube(dimensions, side)` | volume, surface_area, diagonal, vertices, edges |
| N-ellipsoid | `Ellipsoid(semi_axes)` | volume, is_sphere |
| N-simplex | `Simplex(dimensions, side)` | volume, vertices, edges |

## The Math

### Sphere Volume
The volume of an n-dimensional unit ball is:

$$V_n = \frac{\pi^{n/2}}{\Gamma(n/2 + 1)}$$

For a sphere of radius r: $V = V_n \cdot r^n$

### Cube Volume  
Simply: $V = s^n$ where s is the side length.

### The Curse of Dimensionality
A fascinating result: for a unit sphere, volume *increases* up to about 5D, then *decreases* toward zero as dimensions increase. This is why machine learning in high dimensions is hard - most of the "space" is near the edges.

## Running Tests

```bash
python -m pytest test_ndgeometry.py -v
```

## Files

```
ndgeometry.py          # The library (~150 lines)
mcp_server.py          # MCP server for Claude Desktop (~160 lines)
src/java/original/     # The original 2014 CS102 Java code
  Sphere.java
  MultiSphere.java
```

## What We Threw Away

The previous version had:
- 2,300+ lines of geometry engine
- AWS Lambda + API Gateway + DynamoDB
- A regex-based "natural language" parser
- Runtime Java compilation
- 12 specialized ignore files
- 338-line .gitignore
- Incomplete Voronoi diagrams
- Documentation for features that didn't exist

Now we have ~300 lines total that actually work.

## License

MIT - see LICENSE

---

*"Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."* — Antoine de Saint-Exupéry

