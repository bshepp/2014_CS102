"""Tests for mcp_server.py (skipped when the optional mcp package is not installed)."""

import asyncio
import json
import math

import pytest

pytest.importorskip("mcp")

from mcp_server import mcp  # noqa: E402


def call(name, **args):
    """Call a tool the way a client would and parse its JSON text (strict: no NaN/Infinity)."""
    result = asyncio.run(mcp.call_tool(name, args))
    content = result[0] if isinstance(result, tuple) else result.content  # mcp 1.x returns a tuple
    return json.loads(content[0].text)


def test_tools_listed():
    names = {t.name for t in asyncio.run(mcp.list_tools())}
    assert names == {"sphere", "cube", "ellipsoid", "simplex", "compare", "volume_by_dimension"}


def test_sphere_three_accuracy_levels():
    r = call("sphere", dimensions=5, radius=2.0, digits=20)
    assert math.isclose(r["volume"], 8 / 15 * math.pi ** 2 * 32)
    assert r["precise"]["digits"] == 20
    assert r["precise"]["volume"].startswith("168.4412484452583")
    assert r["exact_volume"] == "8/15 * pi^2 * r^5"
    assert 0 <= r["float_relative_error"] < 1e-14
    assert math.isclose(r["log10_volume"], math.log10(r["volume"]))


def test_exact_forms():
    assert call("sphere", dimensions=1, radius=1.0)["exact_volume"] == "2 * r"
    assert call("sphere", dimensions=2, radius=1.0)["exact_volume"] == "pi * r^2"
    assert call("sphere", dimensions=3, radius=1.0)["exact_volume"] == "4/3 * pi * r^3"
    assert call("ellipsoid", semi_axes=[1.0, 2.0, 3.0])["exact_volume"] == "4/3 * pi * (product of semi-axes)"
    assert "exact_volume" not in call("sphere", dimensions=101, radius=1.0)


def test_outside_float_range_is_null_not_infinity():
    r = call("sphere", dimensions=1000, radius=1.0, digits=12)
    assert r["volume"] is None and r["surface_area"] is None
    assert r["float_relative_error"] is None
    assert "note" in r
    assert r["precise"]["volume"] == "3.07983756596E-886"
    assert math.isclose(r["log10_volume"], -885.5114721880675)

    r = call("cube", dimensions=2000, side=2.0, digits=8)
    assert r["volume"] is None
    assert r["precise"]["volume"] == "1.1481307E+602"
    assert r["vertices"] == "1.1481307E+602"  # too big for a JSON number
    assert call("cube", dimensions=4, side=1.0)["vertices"] == 16


def test_simplex_past_old_factorial_limit():
    r = call("simplex", dimensions=300, side=10.0, digits=10)
    assert r["vertices"] == 301 and r["edges"] == 45150
    assert r["precise"]["volume"].endswith("E-359")
    assert r["volume"] is None


def test_compare_in_log_space():
    r = call("compare", shape1_type="cube", shape1_dim=5000, shape1_size=2.0,
             shape2_type="sphere", shape2_dim=5000, shape2_size=2.0)
    assert r["volume_ratio"] is None  # ~1e6168
    assert math.isclose(r["log10_volume_ratio"], 6168.3372, rel_tol=1e-6)
    r = call("compare", shape1_type="sphere", shape1_dim=4, shape1_size=1.0,
             shape2_type="simplex", shape2_dim=4, shape2_size=1.0)
    assert math.isclose(r["volume_ratio"], r["shape1"]["volume"] / r["shape2"]["volume"])
    assert "note" not in r


def test_volume_by_dimension_peak():
    r = call("volume_by_dimension", shape_type="sphere", size=1.0, max_dim=600)
    assert r["peak_dimension"] == 5
    assert r["volumes_by_dimension"]["500"] is None
    assert math.isfinite(r["log10_volumes_by_dimension"]["600"])
    assert call("volume_by_dimension", shape_type="sphere", size=3.0, max_dim=100)["peak_dimension"] == 56


@pytest.mark.parametrize("args", [
    dict(dimensions=0, radius=1.0),
    dict(dimensions=100_001, radius=1.0),
    dict(dimensions=3, radius=0.0),
    dict(dimensions=3, radius=1.0, digits=1001),
])
def test_rejects_out_of_range(args):
    with pytest.raises(Exception):
        call("sphere", **args)
