#!/usr/bin/env python3
"""
Test configuration and fixtures for the N-Dimensional Geometry Engine
"""

import asyncio
import os
import sys
# Unused typing imports removed for Flake8 compliance
from unittest.mock import MagicMock

import pytest

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geometry_engine import (
    GeometryAgent,
    HexagonalTiling,
    HyperCube,
    HyperEllipsoid,
    HyperPyramid,
    HyperSphere,
    JavaBridge,
    RegularTiling,
    Simplex,
    VoronoiTiling,
)

# Test configuration
pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def geometry_agent():
    """Create a GeometryAgent instance for testing."""
    return GeometryAgent()


@pytest.fixture
def mock_java_bridge():
    """Create a mock Java bridge for testing when Java is not available."""
    mock = MagicMock(spec=JavaBridge)
    mock.java_available = False
    mock.run_original_sphere.return_value = "Mock Java output"
    mock.run_original_multisphere.return_value = "Mock Java output"
    return mock


@pytest.fixture(params=[1, 2, 3, 4, 5])
def dimension(request):
    """Parametrized fixture for testing different dimensions."""
    return request.param


@pytest.fixture(params=[0.5, 1.0, 2.0, 3.14159])
def radius(request):
    """Parametrized fixture for testing different radii."""
    return request.param


@pytest.fixture(params=[0.5, 1.0, 2.0])
def side_length(request):
    """Parametrized fixture for testing different side lengths."""
    return request.param


@pytest.fixture
def sample_spheres():
    """Create sample spheres for testing."""
    return {
        "unit_2d": HyperSphere(2, 1.0),
        "unit_3d": HyperSphere(3, 1.0),
        "unit_4d": HyperSphere(4, 1.0),
        "large_2d": HyperSphere(2, 5.0),
        "small_3d": HyperSphere(3, 0.1),
    }


@pytest.fixture
def sample_cubes():
    """Create sample cubes for testing."""
    return {
        "unit_2d": HyperCube(2, 1.0),
        "unit_3d": HyperCube(3, 1.0),
        "unit_4d": HyperCube(4, 1.0),
        "large_2d": HyperCube(2, 5.0),
        "small_3d": HyperCube(3, 0.1),
    }


@pytest.fixture
def sample_ellipsoids():
    """Create sample ellipsoids for testing."""
    return {
        "2d_ellipse": HyperEllipsoid(2, 1.0, 2.0),
        "3d_ellipsoid": HyperEllipsoid(3, 1.0, 2.0, 3.0),
        "4d_ellipsoid": HyperEllipsoid(4, 1.0, 1.5, 2.0, 2.5),
    }


@pytest.fixture
def sample_simplices():
    """Create sample simplices for testing."""
    return {
        "2d_triangle": Simplex(2, 1.0),
        "3d_tetrahedron": Simplex(3, 1.0),
        "4d_simplex": Simplex(4, 1.0),
    }


@pytest.fixture
def sample_pyramids():
    """Create sample pyramids for testing."""
    return {
        "2d_triangle": HyperPyramid(2, 2.0, 1.0),
        "3d_pyramid": HyperPyramid(3, 2.0, 3.0),
        "4d_pyramid": HyperPyramid(4, 2.0, 4.0),
    }


@pytest.fixture
def sample_tilings():
    """Create sample tilings for testing."""
    cube = HyperCube(2, 1.0)
    sphere = HyperSphere(2, 0.5)

    return {
        "regular_square": RegularTiling(2, cube),
        "regular_circle": RegularTiling(2, sphere),
        "hexagonal": HexagonalTiling(1.0),
        "voronoi": VoronoiTiling(2, [[1, 1], [2, 2], [3, 1], [1, 3]]),
    }


@pytest.fixture
def test_bounds():
    """Standard test bounds for different dimensions."""
    return {
        1: [(0, 5)],
        2: [(0, 5), (0, 5)],
        3: [(0, 5), (0, 5), (0, 5)],
        4: [(0, 5), (0, 5), (0, 5), (0, 5)],
        5: [(0, 5), (0, 5), (0, 5), (0, 5), (0, 5)],
    }


@pytest.fixture
def api_test_data():
    """Test data for API endpoints."""
    return {
        "sphere_requests": [
            {"dimensions": 2, "radius": 1.0},
            {"dimensions": 3, "radius": 2.0},
            {"dimensions": 4, "radius": 0.5},
        ],
        "cube_requests": [
            {"dimensions": 2, "side_length": 1.0},
            {"dimensions": 3, "side_length": 2.0},
            {"dimensions": 4, "side_length": 0.5},
        ],
        "ellipsoid_requests": [
            {"dimensions": 2, "semi_axes": [1.0, 2.0]},
            {"dimensions": 3, "semi_axes": [1.0, 2.0, 3.0]},
            {"dimensions": 4, "semi_axes": [1.0, 1.5, 2.0, 2.5]},
        ],
        "simplex_requests": [
            {"dimensions": 2, "side_length": 1.0},
            {"dimensions": 3, "side_length": 2.0},
            {"dimensions": 4, "side_length": 0.5},
        ],
        "pyramid_requests": [
            {"dimensions": 2, "base_side_length": 2.0, "height": 1.0},
            {"dimensions": 3, "base_side_length": 2.0, "height": 3.0},
            {"dimensions": 4, "base_side_length": 2.0, "height": 4.0},
        ],
        "tiling_requests": [
            {
                "tiling_type": "regular",
                "dimensions": 2,
                "bounds": [[0, 5], [0, 5]],
                "density": 1.0,
                "shape_type": "cube",
                "parameter": 1.0,
            },
            {
                "tiling_type": "hexagonal",
                "dimensions": 2,
                "bounds": [[0, 10], [0, 10]],
                "density": 1.0,
                "side_length": 1.0,
            },
            {
                "tiling_type": "voronoi",
                "dimensions": 2,
                "bounds": [[0, 8], [0, 8]],
                "density": 1.0,
                "num_random_seeds": 6,
            },
        ],
    }


@pytest.fixture
def mathematical_constants():
    """Mathematical constants for accuracy testing."""
    import math

    return {
        "pi": math.pi,
        "e": math.e,
        "sqrt_2": math.sqrt(2),
        "sqrt_3": math.sqrt(3),
        "sqrt_pi": math.sqrt(math.pi),
        "golden_ratio": (1 + math.sqrt(5)) / 2,
        "euler_gamma": 0.5772156649015329,  # Euler-Mascheroni constant
    }


@pytest.fixture
def performance_limits():
    """Performance limits for benchmark testing."""
    return {
        "max_dimension": 20,
        "max_response_time": 1.0,  # seconds
        "max_memory_usage": 100,  # MB
        "max_tile_count": 10000,
        "min_accuracy": 1e-10,
    }


@pytest.fixture
def tolerance():
    """Numerical tolerance for floating-point comparisons."""
    return 1e-10


@pytest.fixture(scope="session")
def temp_dir():
    """Create a temporary directory for test files."""
    import shutil
    import tempfile

    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


# Custom markers for different test categories
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "performance: mark test as a performance test")
    config.addinivalue_line(
        "markers", "mathematical: mark test as a mathematical accuracy test"
    )
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "requires_java: mark test as requiring Java")
    config.addinivalue_line("markers", "api: mark test as an API test")
    config.addinivalue_line("markers", "tiling: mark test as a tiling test")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add markers based on test file names
        if "test_performance" in item.nodeid:
            item.add_marker(pytest.mark.performance)
        if "test_mathematics" in item.nodeid:
            item.add_marker(pytest.mark.mathematical)
        if "test_api" in item.nodeid:
            item.add_marker(pytest.mark.api)
        if "test_tiling" in item.nodeid:
            item.add_marker(pytest.mark.tiling)
        if "java" in item.name.lower():
            item.add_marker(pytest.mark.requires_java)


# Helper functions for tests
def assert_almost_equal(actual, expected, tolerance=1e-10):
    """Assert that two floating-point numbers are almost equal."""
    assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"


def assert_valid_shape_response(response_data):
    """Assert that a shape response has all required fields."""
    required_fields = [
        "dimensions",
        "parameter",
        "parameter_name",
        "volume",
        "surface_area",
        "volume_formula",
        "surface_area_formula",
        "shape_type",
    ]
    for field in required_fields:
        assert field in response_data, f"Missing field: {field}"

    # Check that numeric fields are valid
    assert response_data["dimensions"] > 0
    assert response_data["parameter"] > 0
    assert response_data["volume"] >= 0
    assert response_data["surface_area"] >= 0


def assert_valid_tiling_response(response_data):
    """Assert that a tiling response has all required fields."""
    required_fields = [
        "tiling_type",
        "dimensions",
        "tile_count",
        "coverage_efficiency",
        "pattern_properties",
        "tiles",
    ]
    for field in required_fields:
        assert field in response_data, f"Missing field: {field}"

    # Check that numeric fields are valid
    assert response_data["dimensions"] > 0
    assert response_data["tile_count"] >= 0
    assert 0 <= response_data["coverage_efficiency"] <= 1
    assert isinstance(response_data["tiles"], list)


# Make helper functions available to all tests
pytest.assert_almost_equal = assert_almost_equal
pytest.assert_valid_shape_response = assert_valid_shape_response
pytest.assert_valid_tiling_response = assert_valid_tiling_response
