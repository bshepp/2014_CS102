# N-Dimensional Geometry

A tiny Python library for n-dimensional shape calculations.

## Origin Story

This started as an 84-line Java assignment in CS102 (Fall 2014) to calculate sphere volume and surface area. Eleven years and much over-engineering later, we've returned to simplicity: a few hundred lines of Python that actually do something useful — in any number of dimensions.

The original Java is preserved in `src/java/original/` for historical purposes.

The `master` branch is the repository as it originally was — my first repo. It's kept purely for nostalgia; all development happens on `main`.

## Installation

```bash
# The library itself needs nothing - pure Python 3.8+ (CI tests 3.10-3.14)
# For MCP server integration with Claude Desktop (mcp 1.x and 2.x both work):
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

# Any dimension works. Floats saturate to 0.0/inf outside the double range,
# log_volume never does, and precise() gives as many correct digits as you ask for.
s = Sphere(dimensions=1000, radius=10.0)
print(s.volume)                   # 3.0798e+114
print(s.log_volume)               # 263.619... (natural log)
print(s.precise(40)["volume"])    # Decimal('3.079837565955026912398408692851318677844E+114')
print(Cube(2000, 2.0).volume)     # inf  (2^2000 ≈ 1.1e602)
print(Cube(2000, 2.0).precise(12)["volume"])  # Decimal('1.14813069527E+602')
```

### As an MCP Server (Claude Desktop)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "geometry": {
      "command": "python",
      "args": ["/path/to/2014_CS102/mcp_server.py"]
    }
  }
}
```

Then ask Claude things like:
- "What's the volume of a 7-dimensional sphere with radius 3?"
- "What's the exact formula for the volume of a 9-ball?"
- "Give me the volume of a 1000-dimensional sphere with radius 10 to 50 digits"
- "Compare a 4D sphere to a 4D cube with the same 'size'"
- "Show me how sphere volume changes from 1D to 15D"

## Available Shapes

| Shape | Class | Key Properties |
|-------|-------|----------------|
| N-sphere | `Sphere(dimensions, radius)` | volume, surface_area, diameter |
| N-cube | `Cube(dimensions, side)` | volume, surface_area, diagonal, vertices, edges |
| N-ellipsoid | `Ellipsoid(semi_axes)` | volume, is_sphere |
| N-simplex | `Simplex(dimensions, side)` | volume, surface_area, vertices, edges |

Every shape also has `log_volume` (natural log, finite in any dimension) and
`precise(digits)` (a dict of the same quantities as `Decimal`s, correct to `digits`
significant digits). `unit_ball_coefficient(n)` returns the exact rational `c` with
unit n-ball volume `c · π^(n//2)` — e.g. `8/15` for n = 5.

## The Math

### Sphere Volume
The volume of an n-dimensional unit ball is:

$$V_n = \frac{\pi^{n/2}}{\Gamma(n/2 + 1)}$$

For a sphere of radius r: $V = V_n \cdot r^n$

### Cube Volume  
Simply: $V = s^n$ where s is the side length.

### The Curse of Dimensionality
A fascinating result: for a unit sphere, volume *increases* up to about 5D, then *decreases* toward zero as dimensions increase. This is why machine learning in high dimensions is hard - most of the "space" is near the edges.

## Dimensions and Accuracy

Every formula is closed-form, so every shape works in any number of dimensions. What
limits the answer is the number type, and the library offers three:

| Level | How | Range | Accuracy |
|-------|-----|-------|----------|
| `volume`, `surface_area`, ... | IEEE double | ~1e-308 to 1e308; saturates to `0.0` / `inf` outside it, never raises | ~1e-15 relative in low dimensions, degrading roughly as n × 1e-16 (float π is itself rounded) |
| `log_volume` | double, computed with `lgamma` | finite in any dimension | relative error ~1e-13 in the log |
| `precise(digits)` | `decimal` module, π from the Gauss–Legendre AGM | any magnitude | every digit shown is correct; inputs are read as the decimal numbers they print as, so `radius=0.1` means exactly 0.1 |

Before this, `math.gamma` overflowed at 342 dimensions, `171!` would not fit in a float,
and `2.0 ** 1024` raised `OverflowError`. Now the float path switches to log-space
where the direct formula over/underflows, and `precise()` evaluates the same closed
forms with arbitrary precision (`Sphere(100_000, 1.5).precise(1000)` takes about a second).

The MCP server reports all three levels on every result, plus `float_relative_error`
— the measured error of the float answer against the precise one — and, up to 100
dimensions, the exact closed form of sphere and ellipsoid volumes (`8/15 * pi^2 * r^5`).
It accepts dimensions up to 100,000 and `digits` up to 1,000.

## Running Tests

```bash
python -m pytest -v    # test_mcp_server.py is skipped unless mcp is installed
```

## Files

```
ndgeometry.py          # The library (~360 lines, stdlib only)
mcp_server.py          # MCP server for Claude Desktop (~300 lines)
test_ndgeometry.py     # Library tests against closed-form formulas
test_mcp_server.py     # MCP tool tests (need the mcp package)
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

Now we have about 650 lines of library and server that actually work — in any dimension, to any precision.

## License

MIT - see LICENSE

---

*"Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."* — Antoine de Saint-Exupéry

