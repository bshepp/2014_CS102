#!/usr/bin/env python3
"""
Core unit tests for the N-Dimensional Geometry Engine
Tests all fundamental geometry classes and their methods
"""

import math
import os
import sys
from typing import Dict, List

import numpy as np
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geometry_engine import (
    GeometryAgent,
    HyperCube,
    HyperEllipsoid,
    HyperPyramid,
    HyperSphere,
    JavaBridge,
    NDShape,
    OriginalSphere,
    Simplex,
)


@pytest.mark.unit
class TestNDShape:
    """Test the abstract NDShape base class."""

    def test_ndshape_is_abstract(self):
        """Test that NDShape cannot be instantiated directly."""
        with pytest.raises(TypeError):
            NDShape(3, 1.0)


@pytest.mark.unit
class TestHyperSphere:
    """Test HyperSphere class functionality."""

    def test_hypersphere_creation(self, dimension, radius):
        """Test creating hyperspheres with various dimensions and radii."""
        sphere = HyperSphere(dimension, radius)
        assert sphere.dimensions == dimension
        assert sphere.radius == radius
        assert sphere.get_diameter() == 2 * radius

    def test_hypersphere_volume(self, sample_spheres, tolerance):
        """Test hypersphere volume calculations."""
        # 2D circle: π * r²
        expected_2d = math.pi * 1.0**2
        assert abs(sample_spheres["unit_2d"].get_volume() - expected_2d) < tolerance

        # 3D sphere: (4/3) * π * r³
        expected_3d = (4 / 3) * math.pi * 1.0**3
        assert abs(sample_spheres["unit_3d"].get_volume() - expected_3d) < tolerance

    def test_hypersphere_surface_area(self, sample_spheres, tolerance):
        """Test hypersphere surface area calculations."""
        # 2D circle: 2 * π * r
        expected_2d = 2 * math.pi * 1.0
        assert (
            abs(sample_spheres["unit_2d"].get_surface_area() - expected_2d) < tolerance
        )

        # 3D sphere: 4 * π * r²
        expected_3d = 4 * math.pi * 1.0**2
        assert (
            abs(sample_spheres["unit_3d"].get_surface_area() - expected_3d) < tolerance
        )

    def test_hypersphere_scaling(self):
        """Test that hypersphere properties scale correctly."""
        sphere1 = HyperSphere(3, 1.0)
        sphere2 = HyperSphere(3, 2.0)

        # Volume should scale as r³ in 3D
        assert abs(sphere2.get_volume() / sphere1.get_volume() - 8.0) < 1e-10

        # Surface area should scale as r² in 3D
        assert (
            abs(sphere2.get_surface_area() / sphere1.get_surface_area() - 4.0) < 1e-10
        )

    def test_hypersphere_contains_point(self):
        """Test point containment in hypersphere."""
        sphere = HyperSphere(3, 1.0)

        # Points inside sphere
        assert sphere.contains_point([0, 0, 0])
        assert sphere.contains_point([0.5, 0.5, 0.5])

        # Points outside sphere
        assert not sphere.contains_point([1.5, 0, 0])
        assert not sphere.contains_point([1, 1, 1])

    def test_hypersphere_invalid_inputs(self):
        """Test error handling for invalid inputs."""
        with pytest.raises(ValueError):
            HyperSphere(0, 1.0)  # Zero dimensions

        with pytest.raises(ValueError):
            HyperSphere(3, 0.0)  # Zero radius

        with pytest.raises(ValueError):
            HyperSphere(3, -1.0)  # Negative radius

    def test_hypersphere_formulas(self):
        """Test that formula strings are returned correctly."""
        sphere = HyperSphere(3, 1.0)
        vol_formula = sphere.get_volume_formula()
        surf_formula = sphere.get_surface_area_formula()

        assert "π" in vol_formula
        assert "r³" in vol_formula
        assert "π" in surf_formula
        assert "r²" in surf_formula

    def test_hypersphere_shape_type(self):
        """Test shape type identification."""
        sphere2d = HyperSphere(2, 1.0)
        sphere3d = HyperSphere(3, 1.0)
        sphere4d = HyperSphere(4, 1.0)

        assert sphere2d.get_shape_type() == "Circle"
        assert sphere3d.get_shape_type() == "Sphere"
        assert sphere4d.get_shape_type() == "4D HyperSphere"


@pytest.mark.unit
class TestHyperCube:
    """Test HyperCube class functionality."""

    def test_hypercube_creation(self, dimension, side_length):
        """Test creating hypercubes with various dimensions and side lengths."""
        cube = HyperCube(dimension, side_length)
        assert cube.dimensions == dimension
        assert cube.side_length == side_length

    def test_hypercube_volume(self, sample_cubes, tolerance):
        """Test hypercube volume calculations."""
        # 2D square: s²
        expected_2d = 1.0**2
        assert abs(sample_cubes["unit_2d"].get_volume() - expected_2d) < tolerance

        # 3D cube: s³
        expected_3d = 1.0**3
        assert abs(sample_cubes["unit_3d"].get_volume() - expected_3d) < tolerance

        # 4D hypercube: s⁴
        expected_4d = 1.0**4
        assert abs(sample_cubes["unit_4d"].get_volume() - expected_4d) < tolerance

    def test_hypercube_surface_area(self, sample_cubes, tolerance):
        """Test hypercube surface area calculations."""
        # 2D square: 4 * s
        expected_2d = 4 * 1.0
        assert abs(sample_cubes["unit_2d"].get_surface_area() - expected_2d) < tolerance

        # 3D cube: 6 * s²
        expected_3d = 6 * 1.0**2
        assert abs(sample_cubes["unit_3d"].get_surface_area() - expected_3d) < tolerance

    def test_hypercube_vertex_count(self):
        """Test hypercube vertex count calculations."""
        cube2d = HyperCube(2, 1.0)
        cube3d = HyperCube(3, 1.0)
        cube4d = HyperCube(4, 1.0)

        assert cube2d.get_vertex_count() == 4  # 2²
        assert cube3d.get_vertex_count() == 8  # 2³
        assert cube4d.get_vertex_count() == 16  # 2⁴

    def test_hypercube_edge_count(self):
        """Test hypercube edge count calculations."""
        cube2d = HyperCube(2, 1.0)
        cube3d = HyperCube(3, 1.0)
        cube4d = HyperCube(4, 1.0)

        assert cube2d.get_edge_count() == 4  # 2 * 2¹
        assert cube3d.get_edge_count() == 12  # 3 * 2²
        assert cube4d.get_edge_count() == 32  # 4 * 2³

    def test_hypercube_diagonal_length(self):
        """Test hypercube diagonal length calculations."""
        cube = HyperCube(3, 1.0)
        expected_diagonal = math.sqrt(3)  # √3 for unit cube
        assert abs(cube.get_diagonal_length() - expected_diagonal) < 1e-10

    def test_hypercube_contains_point(self):
        """Test point containment in hypercube."""
        cube = HyperCube(3, 2.0)  # 2x2x2 cube

        # Points inside cube
        assert cube.contains_point([0.5, 0.5, 0.5])
        assert cube.contains_point([1.9, 1.9, 1.9])

        # Points outside cube
        assert not cube.contains_point([2.1, 0.5, 0.5])
        assert not cube.contains_point([-0.1, 0.5, 0.5])

    def test_hypercube_cross_section(self):
        """Test hypercube cross-section calculations."""
        cube = HyperCube(3, 2.0)

        # Cross-section at center
        cross_section = cube.get_cross_section(1.0)
        expected = 2.0**2  # 2D square cross-section
        assert abs(cross_section - expected) < 1e-10

        # Cross-section at edge
        cross_section = cube.get_cross_section(2.0)
        assert cross_section == 0.0  # No cross-section at edge


@pytest.mark.unit
class TestHyperEllipsoid:
    """Test HyperEllipsoid class functionality."""

    def test_hyperellipsoid_creation(self, sample_ellipsoids):
        """Test creating hyperellipsoids with various dimensions."""
        ellipse = sample_ellipsoids["2d_ellipse"]
        assert ellipse.dimensions == 2
        assert np.array_equal(ellipse.semi_axes, [1.0, 2.0])

    def test_hyperellipsoid_volume(self, sample_ellipsoids, tolerance):
        """Test hyperellipsoid volume calculations."""
        # 2D ellipse: π * a * b
        ellipse = sample_ellipsoids["2d_ellipse"]
        expected_2d = math.pi * 1.0 * 2.0
        assert abs(ellipse.get_volume() - expected_2d) < tolerance

    def test_hyperellipsoid_is_sphere(self):
        """Test sphere detection in hyperellipsoid."""
        # Equal axes should be detected as sphere
        sphere_ellipsoid = HyperEllipsoid(3, 1.0, 1.0, 1.0)
        assert sphere_ellipsoid.is_sphere()

        # Unequal axes should not be sphere
        ellipsoid = HyperEllipsoid(3, 1.0, 2.0, 3.0)
        assert not ellipsoid.is_sphere()

    def test_hyperellipsoid_axis_ratio(self):
        """Test axis ratio calculations."""
        ellipsoid = HyperEllipsoid(3, 1.0, 2.0, 3.0)
        ratio = ellipsoid.get_axis_ratio()
        expected_ratio = 3.0 / 1.0  # max / min
        assert abs(ratio - expected_ratio) < 1e-10

    def test_hyperellipsoid_eccentricity(self):
        """Test eccentricity calculation for 2D ellipse."""
        ellipse = HyperEllipsoid(2, 1.0, 2.0)
        eccentricity = ellipse.get_eccentricity()

        # e = √(1 - (b²/a²)) where a > b
        expected = math.sqrt(1 - (1.0**2 / 2.0**2))
        assert abs(eccentricity - expected) < 1e-10

    def test_hyperellipsoid_invalid_inputs(self):
        """Test error handling for invalid inputs."""
        with pytest.raises(ValueError):
            HyperEllipsoid(2, 1.0, 0.0)  # Zero semi-axis

        with pytest.raises(ValueError):
            HyperEllipsoid(2, 1.0, -1.0)  # Negative semi-axis


@pytest.mark.unit
class TestSimplex:
    """Test Simplex class functionality."""

    def test_simplex_creation(self, sample_simplices):
        """Test creating simplices with various dimensions."""
        triangle = sample_simplices["2d_triangle"]
        assert triangle.dimensions == 2
        assert triangle.side_length == 1.0

    def test_simplex_volume(self, sample_simplices, tolerance):
        """Test simplex volume calculations."""
        # 2D triangle: (√3/4) * s²
        triangle = sample_simplices["2d_triangle"]
        expected_2d = (math.sqrt(3) / 4) * 1.0**2
        assert abs(triangle.get_volume() - expected_2d) < tolerance

        # 3D tetrahedron: (√2/12) * s³
        tetrahedron = sample_simplices["3d_tetrahedron"]
        expected_3d = (math.sqrt(2) / 12) * 1.0**3
        assert abs(tetrahedron.get_volume() - expected_3d) < tolerance

    def test_simplex_vertex_count(self):
        """Test simplex vertex count calculations."""
        triangle = Simplex(2, 1.0)
        tetrahedron = Simplex(3, 1.0)
        simplex_4d = Simplex(4, 1.0)

        assert triangle.get_vertex_count() == 3
        assert tetrahedron.get_vertex_count() == 4
        assert simplex_4d.get_vertex_count() == 5

    def test_simplex_edge_count(self):
        """Test simplex edge count calculations."""
        triangle = Simplex(2, 1.0)
        tetrahedron = Simplex(3, 1.0)
        simplex_4d = Simplex(4, 1.0)

        assert triangle.get_edge_count() == 3
        assert tetrahedron.get_edge_count() == 6
        assert simplex_4d.get_edge_count() == 10

    def test_simplex_circumradius(self):
        """Test simplex circumradius calculations."""
        triangle = Simplex(2, 1.0)
        circumradius = triangle.get_circumradius()

        # For equilateral triangle: R = s / √3
        expected = 1.0 / math.sqrt(3)
        assert abs(circumradius - expected) < 1e-10

    def test_simplex_inradius(self):
        """Test simplex inradius calculations."""
        triangle = Simplex(2, 1.0)
        inradius = triangle.get_inradius()

        # For equilateral triangle: r = s / (2√3)
        expected = 1.0 / (2 * math.sqrt(3))
        assert abs(inradius - expected) < 1e-10

    def test_simplex_height(self):
        """Test simplex height calculations."""
        triangle = Simplex(2, 1.0)
        height = triangle.get_height()

        # For equilateral triangle: h = (√3/2) * s
        expected = (math.sqrt(3) / 2) * 1.0
        assert abs(height - expected) < 1e-10


@pytest.mark.unit
class TestHyperPyramid:
    """Test HyperPyramid class functionality."""

    def test_hyperpyramid_creation(self, sample_pyramids):
        """Test creating hyperpyramids with various dimensions."""
        pyramid = sample_pyramids["3d_pyramid"]
        assert pyramid.dimensions == 3
        assert pyramid.base_side_length == 2.0
        assert pyramid.height == 3.0

    def test_hyperpyramid_volume(self, sample_pyramids, tolerance):
        """Test hyperpyramid volume calculations."""
        # 2D triangle: (1/2) * base * height
        triangle = sample_pyramids["2d_triangle"]
        expected_2d = 0.5 * 2.0 * 1.0
        assert abs(triangle.get_volume() - expected_2d) < tolerance

        # 3D pyramid: (1/3) * base_area * height
        pyramid = sample_pyramids["3d_pyramid"]
        expected_3d = (1 / 3) * (2.0**2) * 3.0
        assert abs(pyramid.get_volume() - expected_3d) < tolerance

    def test_hyperpyramid_base_volume(self):
        """Test hyperpyramid base volume calculations."""
        pyramid = HyperPyramid(3, 2.0, 3.0)
        base_volume = pyramid.get_base_volume()
        expected = 2.0**2  # Square base
        assert abs(base_volume - expected) < 1e-10

    def test_hyperpyramid_slant_height(self):
        """Test hyperpyramid slant height calculations."""
        pyramid = HyperPyramid(3, 4.0, 3.0)
        slant_height = pyramid.get_slant_height()

        # For square pyramid: slant_height = √(h² + (s/2)²)
        expected = math.sqrt(3.0**2 + (4.0 / 2) ** 2)
        assert abs(slant_height - expected) < 1e-10

    def test_hyperpyramid_lateral_edge_length(self):
        """Test hyperpyramid lateral edge length calculations."""
        pyramid = HyperPyramid(3, 4.0, 3.0)
        lateral_edge = pyramid.get_lateral_edge_length()

        # For square pyramid: lateral_edge = √(h² + (s√2/2)²)
        expected = math.sqrt(3.0**2 + (4.0 * math.sqrt(2) / 2) ** 2)
        assert abs(lateral_edge - expected) < 1e-10

    def test_hyperpyramid_vertex_count(self):
        """Test hyperpyramid vertex count calculations."""
        pyramid2d = HyperPyramid(2, 2.0, 1.0)
        pyramid3d = HyperPyramid(3, 2.0, 3.0)
        pyramid4d = HyperPyramid(4, 2.0, 4.0)

        assert pyramid2d.get_vertex_count() == 3  # Triangle
        assert pyramid3d.get_vertex_count() == 5  # Square pyramid
        assert pyramid4d.get_vertex_count() == 9  # 4D pyramid

    def test_hyperpyramid_edge_count(self):
        """Test hyperpyramid edge count calculations."""
        pyramid2d = HyperPyramid(2, 2.0, 1.0)
        pyramid3d = HyperPyramid(3, 2.0, 3.0)
        pyramid4d = HyperPyramid(4, 2.0, 4.0)

        assert pyramid2d.get_edge_count() == 3  # Triangle
        assert pyramid3d.get_edge_count() == 8  # Square pyramid
        assert pyramid4d.get_edge_count() == 20  # 4D pyramid

    def test_hyperpyramid_cross_section(self):
        """Test hyperpyramid cross-section calculations."""
        pyramid = HyperPyramid(3, 4.0, 3.0)

        # Cross-section at base
        cross_section = pyramid.get_cross_section(0.0)
        expected = 4.0**2  # Full base area
        assert abs(cross_section - expected) < 1e-10

        # Cross-section at apex
        cross_section = pyramid.get_cross_section(3.0)
        assert cross_section == 0.0  # Point at apex

    def test_hyperpyramid_shape_type(self):
        """Test shape type identification."""
        pyramid2d = HyperPyramid(2, 2.0, 1.0)
        pyramid3d = HyperPyramid(3, 2.0, 3.0)
        pyramid4d = HyperPyramid(4, 2.0, 4.0)

        assert pyramid2d.get_shape_type() == "Triangle"
        assert pyramid3d.get_shape_type() == "Square Pyramid"
        assert pyramid4d.get_shape_type() == "4D HyperPyramid"


@pytest.mark.unit
class TestOriginalSphere:
    """Test OriginalSphere class functionality."""

    def test_original_sphere_creation(self):
        """Test creating original sphere with diameter."""
        sphere = OriginalSphere(4.0)
        assert sphere.diameter == 4.0
        assert sphere.radius == 2.0

    def test_original_sphere_volume(self, tolerance):
        """Test original sphere volume calculation."""
        sphere = OriginalSphere(2.0)  # diameter = 2, radius = 1
        volume = sphere.get_volume()
        expected = (4 / 3) * math.pi * 1.0**3
        assert abs(volume - expected) < tolerance

    def test_original_sphere_surface_area(self, tolerance):
        """Test original sphere surface area calculation."""
        sphere = OriginalSphere(2.0)  # diameter = 2, radius = 1
        surface_area = sphere.get_surface_area()
        expected = 4 * math.pi * 1.0**2
        assert abs(surface_area - expected) < tolerance

    def test_original_sphere_diameter_setter(self):
        """Test original sphere diameter setter."""
        sphere = OriginalSphere(2.0)
        sphere.set_diameter(6.0)
        assert sphere.diameter == 6.0
        assert sphere.radius == 3.0


@pytest.mark.unit
class TestGeometryAgent:
    """Test GeometryAgent class functionality."""

    def test_geometry_agent_creation(self, geometry_agent):
        """Test creating geometry agent."""
        assert geometry_agent is not None
        assert hasattr(geometry_agent, "process_query")

    def test_geometry_agent_sphere_query(self, geometry_agent):
        """Test geometry agent sphere queries."""
        result = geometry_agent.process_query("create a 3D sphere radius 2")
        assert "sphere" in result.lower()
        assert "volume" in result.lower()

    def test_geometry_agent_cube_query(self, geometry_agent):
        """Test geometry agent cube queries."""
        result = geometry_agent.process_query("create a 3D cube side 2")
        assert "cube" in result.lower()
        assert "volume" in result.lower()

    def test_geometry_agent_ellipsoid_query(self, geometry_agent):
        """Test geometry agent ellipsoid queries."""
        result = geometry_agent.process_query("create a 3D ellipsoid axes 1 2 3")
        assert "ellipsoid" in result.lower()
        assert "volume" in result.lower()

    def test_geometry_agent_simplex_query(self, geometry_agent):
        """Test geometry agent simplex queries."""
        result = geometry_agent.process_query("create a 3D simplex side 2")
        assert "simplex" in result.lower() or "tetrahedron" in result.lower()

    def test_geometry_agent_pyramid_query(self, geometry_agent):
        """Test geometry agent pyramid queries."""
        result = geometry_agent.process_query("create a 3D pyramid base 2 height 3")
        assert "pyramid" in result.lower()
        assert "volume" in result.lower()

    def test_geometry_agent_invalid_query(self, geometry_agent):
        """Test geometry agent with invalid queries."""
        result = geometry_agent.process_query("create a flying unicorn")
        assert "specify" in result.lower() or "error" in result.lower()

    def test_geometry_agent_help_query(self, geometry_agent):
        """Test geometry agent help functionality."""
        result = geometry_agent.process_query("help")
        assert "commands" in result.lower()
        assert "sphere" in result.lower()
        assert "cube" in result.lower()


@pytest.mark.unit
@pytest.mark.requires_java
class TestJavaBridge:
    """Test JavaBridge class functionality."""

    def test_java_bridge_creation(self):
        """Test creating Java bridge."""
        bridge = JavaBridge()
        assert hasattr(bridge, "java_available")

    def test_java_bridge_availability(self):
        """Test Java availability detection."""
        bridge = JavaBridge()
        # Should detect whether Java is available
        assert isinstance(bridge.java_available, bool)

    @pytest.mark.skipif(
        not os.path.exists("Sphere.java"), reason="Sphere.java not found"
    )
    def test_java_bridge_sphere_execution(self):
        """Test executing original Java sphere code."""
        bridge = JavaBridge()
        if bridge.java_available:
            result = bridge.run_original_sphere(2.0)
            assert "diameter" in result.lower()

    @pytest.mark.skipif(
        not os.path.exists("MultiSphere.java"), reason="MultiSphere.java not found"
    )
    def test_java_bridge_multisphere_execution(self):
        """Test executing original Java multisphere code."""
        bridge = JavaBridge()
        if bridge.java_available:
            result = bridge.run_original_multisphere(2.0)
            assert "diameter" in result.lower()


# Additional utility function tests
@pytest.mark.unit
class TestUtilityFunctions:
    """Test utility functions and edge cases."""

    def test_gamma_function_accuracy(self):
        """Test gamma function accuracy for volume calculations."""
        import math

        # Test known values using math.gamma
        assert abs(math.gamma(1) - 1.0) < 1e-10
        assert abs(math.gamma(2) - 1.0) < 1e-10
        assert abs(math.gamma(3) - 2.0) < 1e-10
        assert abs(math.gamma(4) - 6.0) < 1e-10

    def test_high_dimensional_sphere_volume_peak(self):
        """Test that sphere volume peaks around 5-6 dimensions."""
        volumes = []
        for dim in range(1, 11):
            sphere = HyperSphere(dim, 1.0)
            volumes.append(sphere.get_volume())

        # Find the maximum volume
        max_volume = max(volumes)
        max_index = volumes.index(max_volume)

        # Volume should peak around dimension 5-6
        assert 4 <= max_index <= 6

    def test_dimensional_consistency(self):
        """Test that all shapes maintain dimensional consistency."""
        for dim in range(1, 8):
            sphere = HyperSphere(dim, 1.0)
            cube = HyperCube(dim, 1.0)

            # All shapes should have the same dimension
            assert sphere.dimensions == dim
            assert cube.dimensions == dim

            # All shapes should return positive volumes
            assert sphere.get_volume() > 0
            assert cube.get_volume() > 0

    def test_parameter_validation(self):
        """Test parameter validation across all shapes."""
        # Test invalid dimensions
        with pytest.raises(ValueError):
            HyperSphere(0, 1.0)

        with pytest.raises(ValueError):
            HyperCube(-1, 1.0)

        # Test invalid parameters
        with pytest.raises(ValueError):
            HyperSphere(3, 0.0)

        with pytest.raises(ValueError):
            HyperCube(3, -1.0)

        with pytest.raises(ValueError):
            HyperEllipsoid(3, 1.0, 2.0, 0.0)  # Zero semi-axis

    def test_formula_strings(self):
        """Test that all shapes return proper formula strings."""
        shapes = [
            HyperSphere(3, 1.0),
            HyperCube(3, 1.0),
            HyperEllipsoid(3, 1.0, 2.0, 3.0),
            Simplex(3, 1.0),
            HyperPyramid(3, 2.0, 3.0),
        ]

        for shape in shapes:
            vol_formula = shape.get_volume_formula()
            surf_formula = shape.get_surface_area_formula()

            # Formulas should be non-empty strings
            assert isinstance(vol_formula, str)
            assert len(vol_formula) > 0
            assert isinstance(surf_formula, str)
            assert len(surf_formula) > 0

    def test_shape_type_identification(self):
        """Test that all shapes correctly identify their type."""
        shapes = [
            (HyperSphere(2, 1.0), "Circle"),
            (HyperSphere(3, 1.0), "Sphere"),
            (HyperCube(2, 1.0), "Square"),
            (HyperCube(3, 1.0), "Cube"),
            (Simplex(2, 1.0), "Triangle"),
            (Simplex(3, 1.0), "Tetrahedron"),
            (HyperPyramid(2, 2.0, 1.0), "Triangle"),
            (HyperPyramid(3, 2.0, 3.0), "Square Pyramid"),
        ]

        for shape, expected_type in shapes:
            assert shape.get_shape_type() == expected_type
