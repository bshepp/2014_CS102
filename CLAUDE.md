# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run tests
python -m pytest test_ndgeometry.py -v

# Run a single test
python -m pytest test_ndgeometry.py::TestSphere::test_3d_sphere_volume -v

# Library demo (prints unit-sphere volume by dimension)
python ndgeometry.py

# Start the MCP server (stdio transport, for Claude Desktop)
python mcp_server.py

# Install MCP dependency (only needed for mcp_server.py; the library itself is stdlib-only)
pip install "mcp[cli]>=1.0.0"
```

## Architecture

Two files do all the real work:

- **`ndgeometry.py`** — the library. Four `@dataclass` shape classes (`Sphere`, `Cube`, `Ellipsoid`, `Simplex`), each with computed properties (`volume`, `surface_area`, etc.). Pure stdlib, ~180 lines, no external deps. `_unit_ball_volume(n)` is the shared primitive — `Sphere` and `Ellipsoid` both build on it.
- **`mcp_server.py`** — thin FastMCP wrapper that exposes the library as MCP tools (`sphere`, `cube`, `ellipsoid`, `simplex`, `compare`, `volume_by_dimension`). Each tool just constructs a shape and returns a dict. No state, no I/O beyond MCP stdio.

`src/java/original/` holds the 2014 CS102 Java assignment (`Sphere.java`, `MultiSphere.java`) preserved as historical artifact — **do not modify or build from it.**

The `master` branch (local and on origin) is the repository's original pre-rewrite history — the author's first repo, kept purely for nostalgia. **Never delete, rebase, or merge it.** All development happens on `main`.

## Design philosophy — read before adding features

This repo was deliberately rewritten from a ~2,300-line over-engineered version (AWS Lambda, DynamoDB, regex NLP parser, runtime Java compilation, incomplete Voronoi code) down to under 400 lines that work. The README's "What We Threw Away" section is load-bearing context.

Implications for changes:
- Prefer extending an existing dataclass over introducing new abstractions, infrastructure, or layers.
- Don't reintroduce web servers, cloud services, persistence, or NL parsing. The MCP server is the user-facing interface; the library stays pure.
- New shapes should follow the existing pattern: a `@dataclass` with validation in `__post_init__` and `@property` accessors. Add a matching `@mcp.tool()` only if the shape is useful through Claude Desktop.
- Tests live in `test_ndgeometry.py` and assert against known closed-form formulas (e.g., `(4/3)πr³` for the 3D sphere) rather than golden values — keep that style.
