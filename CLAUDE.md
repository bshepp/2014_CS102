# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run tests (test_mcp_server.py skips itself unless mcp is installed)
python -m pytest -v

# Run a single test
python -m pytest test_ndgeometry.py::TestSphere::test_3d_sphere_volume -v

# Library demo (prints unit-sphere volume by dimension)
python ndgeometry.py

# Start the MCP server (stdio transport, for Claude Desktop)
python mcp_server.py

# Install MCP dependency (only needed for mcp_server.py and its tests; the library itself is stdlib-only)
pip install "mcp[cli]>=1.0.0"
```

## Architecture

Two files do all the real work:

- **`ndgeometry.py`** — the library. Four `@dataclass` shape classes (`Sphere`, `Cube`, `Ellipsoid`, `Simplex`), each with computed properties (`volume`, `surface_area`, etc.). Pure stdlib (`math`, `decimal`, `fractions`), ~360 lines, no external deps. Every shape works in any dimension at three accuracy levels: float properties (saturate to `0.0`/`inf` via `_float_or_log`, which retries in log-space when the direct formula over/underflows), `log_volume` (always finite, via `lgamma`), and `precise(digits)` (the same closed forms in `decimal`, with π from `_pi()`, run through `_precise()` which adds guard digits and rounds to the requested count). `_unit_ball_volume(n)` / `_unit_ball_volume_decimal(n, pi)` are the shared primitives — `Sphere` and `Ellipsoid` both build on them; `unit_ball_coefficient(n)` is the exact rational form.
- **`mcp_server.py`** — thin MCP wrapper that exposes the library as tools (`sphere`, `cube`, `ellipsoid`, `simplex`, `compare`, `volume_by_dimension`). Imports `MCPServer` from mcp 2.x and falls back to `FastMCP` from 1.x; the tool API is the same. Each tool constructs a shape and returns a dict via `_report()`, which adds `log10_volume`, the `precise` block, and the measured `float_relative_error`; non-finite floats become `null`. Inputs are bounded with pydantic `Field` constraints (`MAX_DIMENSIONS`, `MAX_DIGITS`) so a request can't run for more than a second or two. No state, no I/O beyond MCP stdio.
- **`test_mcp_server.py`** — calls the tools through `mcp.call_tool()` and parses the JSON text strictly; skipped when `mcp` isn't installed.

`src/java/original/` holds the 2014 CS102 Java assignment (`Sphere.java`, `MultiSphere.java`) preserved as historical artifact — **do not modify or build from it.**

The `master` branch (local and on origin) is the repository's original pre-rewrite history — the author's first repo, kept purely for nostalgia. **Never delete, rebase, or merge it.** All development happens on `main`.

## Design philosophy — read before adding features

This repo was deliberately rewritten from a ~2,300-line over-engineered version (AWS Lambda, DynamoDB, regex NLP parser, runtime Java compilation, incomplete Voronoi code) down to under 400 lines that work (now ~650 lines of library and server after the any-dimension and arbitrary-precision work). The README's "What We Threw Away" section is load-bearing context.

Implications for changes:
- Prefer extending an existing dataclass over introducing new abstractions, infrastructure, or layers.
- Don't reintroduce web servers, cloud services, persistence, or NL parsing. The MCP server is the user-facing interface; the library stays pure.
- New shapes should follow the existing pattern: a `@dataclass` with validation in `__post_init__` and `@property` accessors. Add a matching `@mcp.tool()` only if the shape is useful through Claude Desktop.
- Tests live in `test_ndgeometry.py` and assert against known closed-form formulas (e.g., `(4/3)πr³` for the 3D sphere) rather than golden values — keep that style. Precision tests compare against an independently known π literal, not the library's own `_pi()`.
- Keep the float path a plain float path: don't route `volume` through `decimal` for accuracy. The float's error is measured and reported by the MCP server; users who need more call `precise()`.
