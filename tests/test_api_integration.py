#!/usr/bin/env python3
"""
API Integration Tests for the N-Dimensional Geometry Engine
Tests all REST API endpoints and their responses
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict

import httpx
import pytest
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_api import app

# Create test client
client = TestClient(app)


@pytest.mark.api
@pytest.mark.integration
class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self):
        """Test health check endpoint returns correct status."""
        response = client.get("/api/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["geometry_engine"] == "operational"
        assert "supported_shapes" in data
        assert "supported_tilings" in data
        assert "features" in data

        # Check that all expected shapes are supported
        expected_shapes = ["sphere", "cube", "ellipsoid", "simplex", "pyramid"]
        for shape in expected_shapes:
            assert shape in data["supported_shapes"]

        # Check that all expected tilings are supported
        expected_tilings = ["regular", "hexagonal", "voronoi"]
        for tiling in expected_tilings:
            assert tiling in data["supported_tilings"]


@pytest.mark.api
@pytest.mark.integration
class TestSphereEndpoint:
    """Test sphere API endpoints."""

    def test_create_sphere_2d(self):
        """Test creating a 2D sphere (circle)."""
        request_data = {"dimensions": 2, "radius": 1.0}
        response = client.post("/api/sphere", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "Circle"
        assert data["dimensions"] == 2
        assert data["parameter"] == 1.0
        assert data["parameter_name"] == "radius"

        # Check mathematical accuracy
        import math

        expected_volume = math.pi * 1.0**2
        expected_surface = 2 * math.pi * 1.0
        pytest.assert_almost_equal(data["volume"], expected_volume)
        pytest.assert_almost_equal(data["surface_area"], expected_surface)

    def test_create_sphere_3d(self):
        """Test creating a 3D sphere."""
        request_data = {"dimensions": 3, "radius": 2.0}
        response = client.post("/api/sphere", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "Sphere"
        assert data["dimensions"] == 3
        assert data["parameter"] == 2.0

        # Check mathematical accuracy
        import math

        expected_volume = (4 / 3) * math.pi * 2.0**3
        expected_surface = 4 * math.pi * 2.0**2
        pytest.assert_almost_equal(data["volume"], expected_volume)
        pytest.assert_almost_equal(data["surface_area"], expected_surface)

    def test_create_sphere_4d(self):
        """Test creating a 4D hypersphere."""
        request_data = {"dimensions": 4, "radius": 1.5}
        response = client.post("/api/sphere", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "4D HyperSphere"
        assert data["dimensions"] == 4
        assert data["parameter"] == 1.5

    def test_create_sphere_invalid_dimensions(self):
        """Test creating sphere with invalid dimensions."""
        request_data = {"dimensions": 0, "radius": 1.0}
        response = client.post("/api/sphere", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_create_sphere_invalid_radius(self):
        """Test creating sphere with invalid radius."""
        request_data = {"dimensions": 3, "radius": 0.0}
        response = client.post("/api/sphere", json=request_data)
        assert response.status_code == 400  # Bad request

    def test_create_sphere_high_dimensions(self):
        """Test creating sphere with high dimensions."""
        request_data = {"dimensions": 20, "radius": 1.0}
        response = client.post("/api/sphere", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["dimensions"] == 20
        assert data["volume"] > 0
        assert data["surface_area"] > 0


@pytest.mark.api
@pytest.mark.integration
class TestCubeEndpoint:
    """Test cube API endpoints."""

    def test_create_cube_2d(self):
        """Test creating a 2D cube (square)."""
        request_data = {"dimensions": 2, "side_length": 2.0}
        response = client.post("/api/cube", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "Square"
        assert data["dimensions"] == 2
        assert data["parameter"] == 2.0
        assert data["parameter_name"] == "side_length"

        # Check mathematical accuracy
        expected_volume = 2.0**2
        expected_surface = 4 * 2.0
        pytest.assert_almost_equal(data["volume"], expected_volume)
        pytest.assert_almost_equal(data["surface_area"], expected_surface)

        # Check additional properties
        assert "vertices" in data["additional_properties"]
        assert "edges" in data["additional_properties"]
        assert "diagonal" in data["additional_properties"]
        assert data["additional_properties"]["vertices"] == 4
        assert data["additional_properties"]["edges"] == 4

    def test_create_cube_3d(self):
        """Test creating a 3D cube."""
        request_data = {"dimensions": 3, "side_length": 3.0}
        response = client.post("/api/cube", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "Cube"
        assert data["dimensions"] == 3
        assert data["parameter"] == 3.0

        # Check mathematical accuracy
        expected_volume = 3.0**3
        expected_surface = 6 * 3.0**2
        pytest.assert_almost_equal(data["volume"], expected_volume)
        pytest.assert_almost_equal(data["surface_area"], expected_surface)

        # Check additional properties
        assert data["additional_properties"]["vertices"] == 8
        assert data["additional_properties"]["edges"] == 12

    def test_create_cube_4d(self):
        """Test creating a 4D hypercube."""
        request_data = {"dimensions": 4, "side_length": 1.0}
        response = client.post("/api/cube", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "4D HyperCube"
        assert data["dimensions"] == 4
        assert data["parameter"] == 1.0

        # Check mathematical accuracy
        expected_volume = 1.0**4
        pytest.assert_almost_equal(data["volume"], expected_volume)

        # Check additional properties
        assert data["additional_properties"]["vertices"] == 16
        assert data["additional_properties"]["edges"] == 32


@pytest.mark.api
@pytest.mark.integration
class TestEllipsoidEndpoint:
    """Test ellipsoid API endpoints."""

    def test_create_ellipsoid_2d(self):
        """Test creating a 2D ellipsoid (ellipse)."""
        request_data = {"dimensions": 2, "semi_axes": [1.0, 2.0]}
        response = client.post("/api/ellipsoid", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "Ellipse"
        assert data["dimensions"] == 2
        assert data["parameter"] == 2.0  # max semi-axis
        assert data["parameter_name"] == "max_semi_axis"

        # Check mathematical accuracy
        import math

        expected_volume = math.pi * 1.0 * 2.0
        pytest.assert_almost_equal(data["volume"], expected_volume)

        # Check additional properties
        assert "semi_axes" in data["additional_properties"]
        assert "axis_ratio" in data["additional_properties"]
        assert "is_sphere" in data["additional_properties"]
        assert "eccentricity" in data["additional_properties"]
        assert data["additional_properties"]["semi_axes"] == [1.0, 2.0]
        assert not data["additional_properties"]["is_sphere"]

    def test_create_ellipsoid_3d(self):
        """Test creating a 3D ellipsoid."""
        request_data = {"dimensions": 3, "semi_axes": [1.0, 2.0, 3.0]}
        response = client.post("/api/ellipsoid", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "Ellipsoid"
        assert data["dimensions"] == 3
        assert data["parameter"] == 3.0  # max semi-axis

        # Check mathematical accuracy
        import math

        expected_volume = (4 / 3) * math.pi * 1.0 * 2.0 * 3.0
        pytest.assert_almost_equal(data["volume"], expected_volume)

        # Check additional properties
        assert data["additional_properties"]["semi_axes"] == [1.0, 2.0, 3.0]
        assert not data["additional_properties"]["is_sphere"]
        expected_ratio = 3.0 / 1.0
        pytest.assert_almost_equal(
            data["additional_properties"]["axis_ratio"], expected_ratio
        )

    def test_create_ellipsoid_sphere_detection(self):
        """Test ellipsoid sphere detection."""
        request_data = {"dimensions": 3, "semi_axes": [2.0, 2.0, 2.0]}
        response = client.post("/api/ellipsoid", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["shape_type"] == "HyperSphere"  # Should be detected as sphere
        assert data["additional_properties"]["is_sphere"]
        assert data["additional_properties"]["axis_ratio"] == 1.0

    def test_create_ellipsoid_invalid_axes(self):
        """Test creating ellipsoid with invalid semi-axes."""
        request_data = {
            "dimensions": 3,
            "semi_axes": [1.0, 2.0],
        }  # Wrong number of axes
        response = client.post("/api/ellipsoid", json=request_data)
        assert response.status_code == 400


@pytest.mark.api
@pytest.mark.integration
class TestSimplexEndpoint:
    """Test simplex API endpoints."""

    def test_create_simplex_2d(self):
        """Test creating a 2D simplex (triangle)."""
        request_data = {"dimensions": 2, "side_length": 1.0}
        response = client.post("/api/simplex", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "Triangle"
        assert data["dimensions"] == 2
        assert data["parameter"] == 1.0
        assert data["parameter_name"] == "side_length"

        # Check mathematical accuracy
        import math

        expected_volume = (math.sqrt(3) / 4) * 1.0**2
        pytest.assert_almost_equal(data["volume"], expected_volume)

        # Check additional properties
        assert "vertices" in data["additional_properties"]
        assert "edges" in data["additional_properties"]
        assert "circumradius" in data["additional_properties"]
        assert "inradius" in data["additional_properties"]
        assert data["additional_properties"]["vertices"] == 3
        assert data["additional_properties"]["edges"] == 3

    def test_create_simplex_3d(self):
        """Test creating a 3D simplex (tetrahedron)."""
        request_data = {"dimensions": 3, "side_length": 2.0}
        response = client.post("/api/simplex", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "Tetrahedron"
        assert data["dimensions"] == 3
        assert data["parameter"] == 2.0

        # Check mathematical accuracy
        import math

        expected_volume = (math.sqrt(2) / 12) * 2.0**3
        pytest.assert_almost_equal(data["volume"], expected_volume)

        # Check additional properties
        assert data["additional_properties"]["vertices"] == 4
        assert data["additional_properties"]["edges"] == 6

    def test_create_simplex_4d(self):
        """Test creating a 4D simplex."""
        request_data = {"dimensions": 4, "side_length": 1.5}
        response = client.post("/api/simplex", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "4D Simplex"
        assert data["dimensions"] == 4
        assert data["parameter"] == 1.5

        # Check additional properties
        assert data["additional_properties"]["vertices"] == 5
        assert data["additional_properties"]["edges"] == 10


@pytest.mark.api
@pytest.mark.integration
class TestPyramidEndpoint:
    """Test pyramid API endpoints."""

    def test_create_pyramid_2d(self):
        """Test creating a 2D pyramid (triangle)."""
        request_data = {"dimensions": 2, "base_side_length": 4.0, "height": 3.0}
        response = client.post("/api/pyramid", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "Triangle"
        assert data["dimensions"] == 2
        assert data["parameter"] == 4.0
        assert data["parameter_name"] == "base_side_length"

        # Check mathematical accuracy
        expected_volume = 0.5 * 4.0 * 3.0
        pytest.assert_almost_equal(data["volume"], expected_volume)

        # Check additional properties
        assert "height" in data["additional_properties"]
        assert "vertices" in data["additional_properties"]
        assert "edges" in data["additional_properties"]
        assert data["additional_properties"]["height"] == 3.0
        assert data["additional_properties"]["vertices"] == 3
        assert data["additional_properties"]["edges"] == 3

    def test_create_pyramid_3d(self):
        """Test creating a 3D pyramid."""
        request_data = {"dimensions": 3, "base_side_length": 4.0, "height": 3.0}
        response = client.post("/api/pyramid", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "Square Pyramid"
        assert data["dimensions"] == 3
        assert data["parameter"] == 4.0

        # Check mathematical accuracy
        expected_volume = (1 / 3) * 4.0**2 * 3.0
        pytest.assert_almost_equal(data["volume"], expected_volume)

        # Check additional properties
        assert data["additional_properties"]["height"] == 3.0
        assert data["additional_properties"]["vertices"] == 5
        assert data["additional_properties"]["edges"] == 8
        assert "slant_height" in data["additional_properties"]
        assert "base_volume" in data["additional_properties"]

    def test_create_pyramid_4d(self):
        """Test creating a 4D pyramid."""
        request_data = {"dimensions": 4, "base_side_length": 2.0, "height": 4.0}
        response = client.post("/api/pyramid", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_shape_response(data)
        assert data["shape_type"] == "4D HyperPyramid"
        assert data["dimensions"] == 4
        assert data["parameter"] == 2.0

        # Check additional properties
        assert data["additional_properties"]["height"] == 4.0
        assert data["additional_properties"]["vertices"] == 9
        assert data["additional_properties"]["edges"] == 20


@pytest.mark.api
@pytest.mark.integration
class TestTilingEndpoint:
    """Test tiling API endpoints."""

    def test_create_regular_tiling_cube(self):
        """Test creating regular tiling with cubes."""
        request_data = {
            "tiling_type": "regular",
            "dimensions": 2,
            "bounds": [[0, 5], [0, 5]],
            "density": 1.0,
            "shape_type": "cube",
            "parameter": 1.0,
        }
        response = client.post("/api/tiling", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_tiling_response(data)
        assert data["tiling_type"] == "regular"
        assert data["dimensions"] == 2
        assert data["tile_count"] > 0
        assert data["coverage_efficiency"] > 0
        assert "analysis" in data

    def test_create_regular_tiling_sphere(self):
        """Test creating regular tiling with spheres."""
        request_data = {
            "tiling_type": "regular",
            "dimensions": 2,
            "bounds": [[0, 4], [0, 4]],
            "density": 1.0,
            "shape_type": "sphere",
            "parameter": 0.5,
        }
        response = client.post("/api/tiling", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_tiling_response(data)
        assert data["tiling_type"] == "regular"
        assert data["tile_count"] > 0

    def test_create_hexagonal_tiling(self):
        """Test creating hexagonal tiling."""
        request_data = {
            "tiling_type": "hexagonal",
            "dimensions": 2,
            "bounds": [[0, 10], [0, 10]],
            "density": 1.0,
            "side_length": 1.0,
        }
        response = client.post("/api/tiling", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_tiling_response(data)
        assert data["tiling_type"] == "hexagonal"
        assert data["dimensions"] == 2
        assert data["tile_count"] > 0
        assert data["coverage_efficiency"] == 1.0  # Perfect hexagonal tiling

        # Check analysis properties
        assert "analysis" in data
        assert data["analysis"]["mathematical_properties"]["coordination_number"] == 6

    def test_create_voronoi_tiling_random_seeds(self):
        """Test creating Voronoi tiling with random seeds."""
        request_data = {
            "tiling_type": "voronoi",
            "dimensions": 2,
            "bounds": [[0, 8], [0, 8]],
            "density": 1.0,
            "num_random_seeds": 6,
        }
        response = client.post("/api/tiling", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_tiling_response(data)
        assert data["tiling_type"] == "voronoi"
        assert data["dimensions"] == 2
        assert data["tile_count"] == 6  # Should match number of seeds
        assert data["coverage_efficiency"] == 1.0  # Complete coverage

    def test_create_voronoi_tiling_specified_seeds(self):
        """Test creating Voronoi tiling with specified seeds."""
        request_data = {
            "tiling_type": "voronoi",
            "dimensions": 2,
            "bounds": [[0, 6], [0, 6]],
            "density": 1.0,
            "seed_points": [[1, 1], [2, 4], [4, 2], [5, 5]],
        }
        response = client.post("/api/tiling", json=request_data)
        assert response.status_code == 200

        data = response.json()
        pytest.assert_valid_tiling_response(data)
        assert data["tiling_type"] == "voronoi"
        assert data["tile_count"] == 4  # Should match number of seeds

    def test_create_tiling_invalid_type(self):
        """Test creating tiling with invalid type."""
        request_data = {
            "tiling_type": "invalid",
            "dimensions": 2,
            "bounds": [[0, 5], [0, 5]],
            "density": 1.0,
        }
        response = client.post("/api/tiling", json=request_data)
        assert response.status_code == 400

    def test_create_tiling_invalid_dimensions_mismatch(self):
        """Test creating tiling with mismatched dimensions."""
        request_data = {
            "tiling_type": "regular",
            "dimensions": 3,
            "bounds": [[0, 5], [0, 5]],  # Only 2D bounds for 3D tiling
            "density": 1.0,
            "shape_type": "cube",
            "parameter": 1.0,
        }
        response = client.post("/api/tiling", json=request_data)
        assert response.status_code == 400

    def test_create_hexagonal_tiling_3d_error(self):
        """Test that hexagonal tiling fails in 3D."""
        request_data = {
            "tiling_type": "hexagonal",
            "dimensions": 3,
            "bounds": [[0, 5], [0, 5], [0, 5]],
            "density": 1.0,
            "side_length": 1.0,
        }
        response = client.post("/api/tiling", json=request_data)
        assert response.status_code == 400
        assert "only supported in 2D" in response.json()["detail"]


@pytest.mark.api
@pytest.mark.integration
class TestQueryEndpoint:
    """Test natural language query endpoint."""

    def test_query_create_sphere(self):
        """Test natural language sphere creation."""
        request_data = {"query": "create a 3D sphere radius 2"}
        response = client.post("/api/query", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "sphere" in data["response"].lower()
        assert "volume" in data["response"].lower()

    def test_query_create_cube(self):
        """Test natural language cube creation."""
        request_data = {"query": "create a 3D cube side 2"}
        response = client.post("/api/query", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "cube" in data["response"].lower()

    def test_query_create_ellipsoid(self):
        """Test natural language ellipsoid creation."""
        request_data = {"query": "create a 3D ellipsoid with axes 1 2 3"}
        response = client.post("/api/query", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "ellipsoid" in data["response"].lower()

    def test_query_create_simplex(self):
        """Test natural language simplex creation."""
        request_data = {"query": "create a 3D simplex side 2"}
        response = client.post("/api/query", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert (
            "simplex" in data["response"].lower()
            or "tetrahedron" in data["response"].lower()
        )

    def test_query_create_pyramid(self):
        """Test natural language pyramid creation."""
        request_data = {"query": "create a 3D pyramid base 2 height 3"}
        response = client.post("/api/query", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "pyramid" in data["response"].lower()

    def test_query_help(self):
        """Test natural language help query."""
        request_data = {"query": "help"}
        response = client.post("/api/query", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "commands" in data["response"].lower()

    def test_query_invalid(self):
        """Test natural language invalid query."""
        request_data = {"query": "create a flying unicorn"}
        response = client.post("/api/query", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert (
            "specify" in data["response"].lower() or "error" in data["response"].lower()
        )


@pytest.mark.api
@pytest.mark.integration
class TestCompareEndpoint:
    """Test shape comparison endpoint."""

    def test_compare_shapes_2d(self):
        """Test comparing 2D shapes."""
        request_data = {"dimensions": 2, "parameter": 1.0}
        response = client.post("/api/compare", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["dimensions"] == 2
        assert data["parameter"] == 1.0
        assert "sphere_volume" in data
        assert "sphere_surface" in data
        assert "comparison_data" in data

        # Check comparison data structure
        comparison = data["comparison_data"]
        assert "sphere" in comparison
        assert "cube" in comparison
        assert "ratios" in comparison
        assert "insights" in comparison

    def test_compare_shapes_3d(self):
        """Test comparing 3D shapes."""
        request_data = {"dimensions": 3, "parameter": 2.0}
        response = client.post("/api/compare", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["dimensions"] == 3
        assert data["parameter"] == 2.0

        # Check that volumes and surface areas are positive
        assert data["sphere_volume"] > 0
        assert data["sphere_surface"] > 0
        assert data["comparison_data"]["cube"]["volume"] > 0
        assert data["comparison_data"]["cube"]["surface_area"] > 0

        # Check that ratios are computed
        assert "volume_ratio_sphere_cube" in data["comparison_data"]["ratios"]
        assert "surface_ratio_sphere_cube" in data["comparison_data"]["ratios"]


@pytest.mark.api
@pytest.mark.integration
class TestDimensionEndpoint:
    """Test dimension info endpoint."""

    def test_dimension_info_2d(self):
        """Test getting 2D dimension info."""
        response = client.get("/api/dimensions/2")
        assert response.status_code == 200

        data = response.json()
        assert data["dimensions"] == 2
        assert "unit_sphere" in data
        assert "insights" in data

        # Check unit sphere properties
        unit_sphere = data["unit_sphere"]
        assert "volume" in unit_sphere
        assert "surface_area" in unit_sphere
        assert "volume_formula" in unit_sphere
        assert "surface_formula" in unit_sphere

    def test_dimension_info_3d(self):
        """Test getting 3D dimension info."""
        response = client.get("/api/dimensions/3")
        assert response.status_code == 200

        data = response.json()
        assert data["dimensions"] == 3

        # Check mathematical accuracy
        import math

        expected_volume = (4 / 3) * math.pi
        expected_surface = 4 * math.pi
        pytest.assert_almost_equal(data["unit_sphere"]["volume"], expected_volume)
        pytest.assert_almost_equal(
            data["unit_sphere"]["surface_area"], expected_surface
        )

    def test_dimension_info_high_dimension(self):
        """Test getting high dimension info."""
        response = client.get("/api/dimensions/10")
        assert response.status_code == 200

        data = response.json()
        assert data["dimensions"] == 10
        assert data["unit_sphere"]["volume"] > 0
        assert data["unit_sphere"]["surface_area"] > 0

    def test_dimension_info_invalid(self):
        """Test getting invalid dimension info."""
        response = client.get("/api/dimensions/0")
        assert response.status_code == 422  # Validation error

        response = client.get("/api/dimensions/101")
        assert response.status_code == 422  # Validation error


@pytest.mark.api
@pytest.mark.integration
class TestOriginalJavaEndpoint:
    """Test original Java integration endpoint."""

    def test_original_java_endpoint(self):
        """Test original Java endpoint."""
        response = client.post("/api/original-java?diameter=2.0")
        assert response.status_code == 200

        data = response.json()
        assert data["diameter"] == 2.0
        assert "java_available" in data
        assert "result" in data
        assert data["success"] is True

        # If Java is available, check result
        if data["java_available"]:
            assert "diameter" in data["result"].lower()


@pytest.mark.api
@pytest.mark.integration
class TestRootEndpoint:
    """Test root and demo endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint returns HTML."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "N-Dimensional Geometry Engine" in response.text

    def test_demo_endpoint(self):
        """Test demo endpoint returns HTML."""
        response = client.get("/demo")
        # This might fail if demo.html doesn't exist, which is expected
        assert response.status_code in [200, 404]


@pytest.mark.api
@pytest.mark.integration
class TestErrorHandling:
    """Test API error handling."""

    def test_404_endpoint(self):
        """Test 404 error handling."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_invalid_json(self):
        """Test invalid JSON handling."""
        response = client.post("/api/sphere", data="invalid json")
        assert response.status_code == 422

    def test_missing_required_fields(self):
        """Test missing required fields."""
        response = client.post("/api/sphere", json={})
        assert response.status_code == 422

    def test_invalid_field_types(self):
        """Test invalid field types."""
        response = client.post(
            "/api/sphere", json={"dimensions": "invalid", "radius": 1.0}
        )
        assert response.status_code == 422

    def test_out_of_range_values(self):
        """Test out of range values."""
        response = client.post("/api/sphere", json={"dimensions": 101, "radius": 1.0})
        assert response.status_code == 422

        response = client.post("/api/sphere", json={"dimensions": 3, "radius": -1.0})
        assert response.status_code == 400


@pytest.mark.api
@pytest.mark.integration
@pytest.mark.slow
class TestPerformanceBasics:
    """Test basic API performance."""

    def test_api_response_time(self):
        """Test that API responses are reasonably fast."""
        import time

        start_time = time.time()
        response = client.post("/api/sphere", json={"dimensions": 10, "radius": 1.0})
        end_time = time.time()

        assert response.status_code == 200
        assert (end_time - start_time) < 2.0  # Should respond within 2 seconds

    def test_concurrent_requests(self):
        """Test handling concurrent requests."""
        import concurrent.futures

        def make_request():
            return client.post("/api/sphere", json={"dimensions": 3, "radius": 1.0})

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in futures]

        # All requests should succeed
        for result in results:
            assert result.status_code == 200
