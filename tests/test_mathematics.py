#!/usr/bin/env python3
"""
Mathematical Accuracy Tests for the N-Dimensional Geometry Engine
Verifies mathematical formulas and calculations are correct
"""

import math
import os
import sys
from typing import Any, Dict, List, Tuple

import numpy as np
import pytest
import scipy.special as sp

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geometry_engine import gamma  # Import gamma function for testing
from geometry_engine import (
    HexagonalTiling,
    HyperCube,
    HyperEllipsoid,
    HyperPyramid,
    HyperSphere,
    RegularTiling,
    Simplex,
    TilingAnalyzer,
    VoronoiTiling,
)


@pytest.mark.mathematical
class TestMathematicalConstants:
    """Test mathematical constants and functions."""

    def test_gamma_function_accuracy(self, mathematical_constants, tolerance):
        """Test gamma function accuracy against known values."""
        # Test integer values: Γ(n) = (n-1)!
        assert abs(gamma(1) - 1.0) < tolerance
        assert abs(gamma(2) - 1.0) < tolerance  # Γ(2) = 1! = 1
        assert abs(gamma(3) - 2.0) < tolerance  # Γ(3) = 2! = 2
        assert abs(gamma(4) - 6.0) < tolerance  # Γ(4) = 3! = 6
        assert abs(gamma(5) - 24.0) < tolerance  # Γ(5) = 4! = 24

        # Test half-integer values: Γ(n + 1/2) = (2n)!√π / (4^n n!)
        assert abs(gamma(0.5) - math.sqrt(math.pi)) < tolerance
        assert abs(gamma(1.5) - 0.5 * math.sqrt(math.pi)) < tolerance
        assert abs(gamma(2.5) - 0.75 * math.sqrt(math.pi)) < tolerance

    def test_pi_accuracy(self, mathematical_constants, tolerance):
        """Test π accuracy in calculations."""
        pi = mathematical_constants["pi"]

        # Test that our π matches math.pi
        assert abs(pi - math.pi) < tolerance

        # Test π in circle calculations
        circle = HyperSphere(2, 1.0)
        expected_area = pi
        assert abs(circle.get_volume() - expected_area) < tolerance

        expected_circumference = 2 * pi
        assert abs(circle.get_surface_area() - expected_circumference) < tolerance

    def test_mathematical_relationships(self, mathematical_constants):
        """Test mathematical relationships and identities."""
        pi = mathematical_constants["pi"]
        e = mathematical_constants["e"]

        # Test Euler's identity: e^(iπ) + 1 = 0
        # Using real form: e^π = -1 + 2πi (approximately)
        # We can test that e^π is close to expected value
        assert abs(math.exp(pi) - 23.14069263) < 1e-6

        # Test that our constants are internally consistent
        assert abs(e - math.e) < 1e-15
        assert abs(pi - math.pi) < 1e-15


@pytest.mark.mathematical
class TestHyperSphereFormulas:
    """Test hypersphere mathematical formulas."""

    def test_2d_circle_formulas(self, tolerance):
        """Test 2D circle (hypersphere) formulas."""
        radius = 2.0
        circle = HyperSphere(2, radius)

        # Area: πr²
        expected_area = math.pi * radius**2
        assert abs(circle.get_volume() - expected_area) < tolerance

        # Circumference: 2πr
        expected_circumference = 2 * math.pi * radius
        assert abs(circle.get_surface_area() - expected_circumference) < tolerance

    def test_3d_sphere_formulas(self, tolerance):
        """Test 3D sphere formulas."""
        radius = 1.5
        sphere = HyperSphere(3, radius)

        # Volume: (4/3)πr³
        expected_volume = (4.0 / 3.0) * math.pi * radius**3
        assert abs(sphere.get_volume() - expected_volume) < tolerance

        # Surface area: 4πr²
        expected_surface = 4 * math.pi * radius**2
        assert abs(sphere.get_surface_area() - expected_surface) < tolerance

    def test_4d_hypersphere_formulas(self, tolerance):
        """Test 4D hypersphere formulas."""
        radius = 1.0
        hypersphere = HyperSphere(4, radius)

        # Volume: (π²/2)r⁴
        expected_volume = (math.pi**2 / 2.0) * radius**4
        assert abs(hypersphere.get_volume() - expected_volume) < tolerance

        # Surface area: 2π²r³
        expected_surface = 2 * math.pi**2 * radius**3
        assert abs(hypersphere.get_surface_area() - expected_surface) < tolerance

    def test_5d_hypersphere_formulas(self, tolerance):
        """Test 5D hypersphere formulas."""
        radius = 1.0
        hypersphere = HyperSphere(5, radius)

        # Volume: (8π²/15)r⁵
        expected_volume = (8.0 * math.pi**2 / 15.0) * radius**5
        assert abs(hypersphere.get_volume() - expected_volume) < tolerance

        # Surface area: (8π²/3)r⁴
        expected_surface = (8.0 * math.pi**2 / 3.0) * radius**4
        assert abs(hypersphere.get_surface_area() - expected_surface) < tolerance

    def test_general_hypersphere_formulas(self, tolerance):
        """Test general n-dimensional hypersphere formulas."""
        test_cases = [
            (1, 1.0),  # Line segment
            (2, 1.0),  # Circle
            (3, 1.0),  # Sphere
            (6, 1.0),  # 6D hypersphere
            (10, 1.0),  # 10D hypersphere
        ]

        for dim, radius in test_cases:
            sphere = HyperSphere(dim, radius)

            # Volume: V_n = (π^(n/2) / Γ(n/2 + 1)) * r^n
            expected_volume = (
                math.pi ** (dim / 2.0) / gamma(dim / 2.0 + 1)
            ) * radius**dim
            assert abs(sphere.get_volume() - expected_volume) < tolerance

            # Surface area: S_n = n * V_n / r
            expected_surface = dim * expected_volume / radius
            assert abs(sphere.get_surface_area() - expected_surface) < tolerance

    def test_hypersphere_scaling_properties(self, tolerance):
        """Test hypersphere scaling properties."""
        base_radius = 1.0
        scale_factor = 2.0

        for dim in range(1, 8):
            sphere1 = HyperSphere(dim, base_radius)
            sphere2 = HyperSphere(dim, base_radius * scale_factor)

            # Volume should scale as scale_factor^dim
            expected_volume_ratio = scale_factor**dim
            actual_volume_ratio = sphere2.get_volume() / sphere1.get_volume()
            assert abs(actual_volume_ratio - expected_volume_ratio) < tolerance

            # Surface area should scale as scale_factor^(dim-1)
            expected_surface_ratio = scale_factor ** (dim - 1)
            actual_surface_ratio = (
                sphere2.get_surface_area() / sphere1.get_surface_area()
            )
            assert abs(actual_surface_ratio - expected_surface_ratio) < tolerance

    def test_hypersphere_volume_peak(self):
        """Test that hypersphere volume peaks around 5-6 dimensions."""
        radius = 1.0
        volumes = []

        for dim in range(1, 15):
            sphere = HyperSphere(dim, radius)
            volumes.append(sphere.get_volume())

        # Find the dimension with maximum volume
        max_volume = max(volumes)
        max_dim = volumes.index(max_volume) + 1

        # Volume should peak around dimension 5-6
        assert 5 <= max_dim <= 6, f"Volume peak at dimension {max_dim}, expected 5-6"

        # Check that volume decreases after the peak
        peak_index = max_dim - 1
        assert volumes[peak_index + 1] < volumes[peak_index]
        assert volumes[peak_index + 2] < volumes[peak_index + 1]


@pytest.mark.mathematical
class TestHyperCubeFormulas:
    """Test hypercube mathematical formulas."""

    def test_2d_square_formulas(self, tolerance):
        """Test 2D square (hypercube) formulas."""
        side = 3.0
        square = HyperCube(2, side)

        # Area: s²
        expected_area = side**2
        assert abs(square.get_volume() - expected_area) < tolerance

        # Perimeter: 4s
        expected_perimeter = 4 * side
        assert abs(square.get_surface_area() - expected_perimeter) < tolerance

    def test_3d_cube_formulas(self, tolerance):
        """Test 3D cube formulas."""
        side = 2.5
        cube = HyperCube(3, side)

        # Volume: s³
        expected_volume = side**3
        assert abs(cube.get_volume() - expected_volume) < tolerance

        # Surface area: 6s²
        expected_surface = 6 * side**2
        assert abs(cube.get_surface_area() - expected_surface) < tolerance

    def test_4d_hypercube_formulas(self, tolerance):
        """Test 4D hypercube formulas."""
        side = 1.5
        hypercube = HyperCube(4, side)

        # Volume: s⁴
        expected_volume = side**4
        assert abs(hypercube.get_volume() - expected_volume) < tolerance

        # Surface area: 8s³
        expected_surface = 8 * side**3
        assert abs(hypercube.get_surface_area() - expected_surface) < tolerance

    def test_general_hypercube_formulas(self, tolerance):
        """Test general n-dimensional hypercube formulas."""
        test_cases = [
            (1, 2.0),  # Line segment
            (2, 2.0),  # Square
            (3, 2.0),  # Cube
            (5, 2.0),  # 5D hypercube
            (10, 2.0),  # 10D hypercube
        ]

        for dim, side in test_cases:
            cube = HyperCube(dim, side)

            # Volume: s^n
            expected_volume = side**dim
            assert abs(cube.get_volume() - expected_volume) < tolerance

            # Surface area: 2n * s^(n-1)
            expected_surface = 2 * dim * side ** (dim - 1)
            assert abs(cube.get_surface_area() - expected_surface) < tolerance

    def test_hypercube_vertex_count(self):
        """Test hypercube vertex count formula."""
        test_cases = [
            (1, 2),  # Line: 2 vertices
            (2, 4),  # Square: 4 vertices
            (3, 8),  # Cube: 8 vertices
            (4, 16),  # 4D hypercube: 16 vertices
            (5, 32),  # 5D hypercube: 32 vertices
        ]

        for dim, expected_vertices in test_cases:
            cube = HyperCube(dim, 1.0)
            assert cube.get_vertex_count() == expected_vertices
            assert cube.get_vertex_count() == 2**dim

    def test_hypercube_edge_count(self):
        """Test hypercube edge count formula."""
        test_cases = [
            (1, 1),  # Line: 1 edge
            (2, 4),  # Square: 4 edges
            (3, 12),  # Cube: 12 edges
            (4, 32),  # 4D hypercube: 32 edges
            (5, 80),  # 5D hypercube: 80 edges
        ]

        for dim, expected_edges in test_cases:
            cube = HyperCube(dim, 1.0)
            assert cube.get_edge_count() == expected_edges
            assert cube.get_edge_count() == dim * (2 ** (dim - 1))

    def test_hypercube_diagonal_length(self, tolerance):
        """Test hypercube diagonal length formula."""
        test_cases = [
            (2, 1.0, math.sqrt(2)),  # Square diagonal
            (3, 1.0, math.sqrt(3)),  # Cube diagonal
            (4, 1.0, math.sqrt(4)),  # 4D hypercube diagonal
            (5, 2.0, 2.0 * math.sqrt(5)),  # 5D hypercube with side 2
        ]

        for dim, side, expected_diagonal in test_cases:
            cube = HyperCube(dim, side)
            assert abs(cube.get_diagonal_length() - expected_diagonal) < tolerance
            assert abs(cube.get_diagonal_length() - side * math.sqrt(dim)) < tolerance


@pytest.mark.mathematical
class TestHyperEllipsoidFormulas:
    """Test hyperellipsoid mathematical formulas."""

    def test_2d_ellipse_formulas(self, tolerance):
        """Test 2D ellipse formulas."""
        a, b = 3.0, 2.0
        ellipse = HyperEllipsoid(2, a, b)

        # Area: πab
        expected_area = math.pi * a * b
        assert abs(ellipse.get_volume() - expected_area) < tolerance

    def test_3d_ellipsoid_formulas(self, tolerance):
        """Test 3D ellipsoid formulas."""
        a, b, c = 2.0, 3.0, 1.5
        ellipsoid = HyperEllipsoid(3, a, b, c)

        # Volume: (4/3)πabc
        expected_volume = (4.0 / 3.0) * math.pi * a * b * c
        assert abs(ellipsoid.get_volume() - expected_volume) < tolerance

    def test_hyperellipsoid_sphere_case(self, tolerance):
        """Test hyperellipsoid with equal axes (sphere case)."""
        radius = 2.0
        ellipsoid = HyperEllipsoid(3, radius, radius, radius)
        sphere = HyperSphere(3, radius)

        # Should match sphere calculations
        assert abs(ellipsoid.get_volume() - sphere.get_volume()) < tolerance
        assert abs(ellipsoid.get_surface_area() - sphere.get_surface_area()) < tolerance
        assert ellipsoid.is_sphere()

    def test_ellipse_eccentricity(self, tolerance):
        """Test ellipse eccentricity calculation."""
        test_cases = [
            (1.0, 1.0, 0.0),  # Circle: e = 0
            (2.0, 1.0, math.sqrt(3) / 2),  # e = √(1 - b²/a²)
            (3.0, 2.0, math.sqrt(5) / 3),  # e = √(1 - (2/3)²)
        ]

        for a, b, expected_e in test_cases:
            ellipse = HyperEllipsoid(2, a, b)
            actual_e = ellipse.get_eccentricity()
            assert abs(actual_e - expected_e) < tolerance

    def test_ellipsoid_axis_ratio(self, tolerance):
        """Test ellipsoid axis ratio calculation."""
        test_cases = [
            ([1.0, 1.0, 1.0], 1.0),  # Sphere: ratio = 1
            ([1.0, 2.0, 3.0], 3.0),  # Ratio = max/min
            ([5.0, 2.0, 8.0], 4.0),  # Ratio = 8/2 = 4
        ]

        for axes, expected_ratio in test_cases:
            ellipsoid = HyperEllipsoid(len(axes), *axes)
            actual_ratio = ellipsoid.get_axis_ratio()
            assert abs(actual_ratio - expected_ratio) < tolerance


@pytest.mark.mathematical
class TestSimplexFormulas:
    """Test simplex mathematical formulas."""

    def test_2d_triangle_formulas(self, tolerance):
        """Test 2D triangle (simplex) formulas."""
        side = 2.0
        triangle = Simplex(2, side)

        # Area: (√3/4)s²
        expected_area = (math.sqrt(3) / 4.0) * side**2
        assert abs(triangle.get_volume() - expected_area) < tolerance

        # Perimeter: 3s
        expected_perimeter = 3 * side
        assert abs(triangle.get_surface_area() - expected_perimeter) < tolerance

    def test_3d_tetrahedron_formulas(self, tolerance):
        """Test 3D tetrahedron formulas."""
        side = 3.0
        tetrahedron = Simplex(3, side)

        # Volume: (√2/12)s³
        expected_volume = (math.sqrt(2) / 12.0) * side**3
        assert abs(tetrahedron.get_volume() - expected_volume) < tolerance

        # Surface area: √3 * s²
        expected_surface = math.sqrt(3) * side**2
        assert abs(tetrahedron.get_surface_area() - expected_surface) < tolerance

    def test_simplex_vertex_count(self):
        """Test simplex vertex count formula."""
        test_cases = [
            (1, 2),  # Line: 2 vertices
            (2, 3),  # Triangle: 3 vertices
            (3, 4),  # Tetrahedron: 4 vertices
            (4, 5),  # 4D simplex: 5 vertices
            (10, 11),  # 10D simplex: 11 vertices
        ]

        for dim, expected_vertices in test_cases:
            simplex = Simplex(dim, 1.0)
            assert simplex.get_vertex_count() == expected_vertices
            assert simplex.get_vertex_count() == dim + 1

    def test_simplex_edge_count(self):
        """Test simplex edge count formula."""
        test_cases = [
            (1, 1),  # Line: 1 edge
            (2, 3),  # Triangle: 3 edges
            (3, 6),  # Tetrahedron: 6 edges
            (4, 10),  # 4D simplex: 10 edges
            (5, 15),  # 5D simplex: 15 edges
        ]

        for dim, expected_edges in test_cases:
            simplex = Simplex(dim, 1.0)
            assert simplex.get_edge_count() == expected_edges
            # Formula: n(n+1)/2
            assert simplex.get_edge_count() == dim * (dim + 1) // 2

    def test_triangle_circumradius(self, tolerance):
        """Test triangle circumradius formula."""
        side = 6.0
        triangle = Simplex(2, side)

        # Circumradius: s/√3
        expected_circumradius = side / math.sqrt(3)
        assert abs(triangle.get_circumradius() - expected_circumradius) < tolerance

    def test_triangle_inradius(self, tolerance):
        """Test triangle inradius formula."""
        side = 6.0
        triangle = Simplex(2, side)

        # Inradius: s/(2√3)
        expected_inradius = side / (2 * math.sqrt(3))
        assert abs(triangle.get_inradius() - expected_inradius) < tolerance

    def test_triangle_height(self, tolerance):
        """Test triangle height formula."""
        side = 4.0
        triangle = Simplex(2, side)

        # Height: (√3/2)s
        expected_height = (math.sqrt(3) / 2.0) * side
        assert abs(triangle.get_height() - expected_height) < tolerance


@pytest.mark.mathematical
class TestHyperPyramidFormulas:
    """Test hyperpyramid mathematical formulas."""

    def test_2d_triangle_pyramid_formulas(self, tolerance):
        """Test 2D triangle (pyramid) formulas."""
        base = 4.0
        height = 3.0
        triangle = HyperPyramid(2, base, height)

        # Area: (1/2) * base * height
        expected_area = 0.5 * base * height
        assert abs(triangle.get_volume() - expected_area) < tolerance

    def test_3d_square_pyramid_formulas(self, tolerance):
        """Test 3D square pyramid formulas."""
        base = 4.0
        height = 3.0
        pyramid = HyperPyramid(3, base, height)

        # Volume: (1/3) * base² * height
        expected_volume = (1.0 / 3.0) * base**2 * height
        assert abs(pyramid.get_volume() - expected_volume) < tolerance

    def test_pyramid_base_volume(self, tolerance):
        """Test pyramid base volume calculation."""
        base = 3.0
        height = 4.0

        test_cases = [
            (2, base),  # Line segment
            (3, base**2),  # Square
            (4, base**3),  # Cube
        ]

        for dim, expected_base_volume in test_cases:
            pyramid = HyperPyramid(dim, base, height)
            assert abs(pyramid.get_base_volume() - expected_base_volume) < tolerance

    def test_pyramid_slant_height(self, tolerance):
        """Test pyramid slant height calculation."""
        base = 4.0
        height = 3.0
        pyramid = HyperPyramid(3, base, height)

        # Slant height: √(h² + (s/2)²)
        expected_slant = math.sqrt(height**2 + (base / 2) ** 2)
        assert abs(pyramid.get_slant_height() - expected_slant) < tolerance

    def test_pyramid_lateral_edge_length(self, tolerance):
        """Test pyramid lateral edge length calculation."""
        base = 4.0
        height = 3.0
        pyramid = HyperPyramid(3, base, height)

        # Lateral edge: √(h² + (s√2/2)²)
        expected_lateral = math.sqrt(height**2 + (base * math.sqrt(2) / 2) ** 2)
        assert abs(pyramid.get_lateral_edge_length() - expected_lateral) < tolerance

    def test_pyramid_vertex_count(self):
        """Test pyramid vertex count formula."""
        test_cases = [
            (1, 2),  # Line: 2 vertices
            (2, 3),  # Triangle: 3 vertices
            (3, 5),  # Square pyramid: 5 vertices
            (4, 9),  # 4D pyramid: 9 vertices
        ]

        for dim, expected_vertices in test_cases:
            pyramid = HyperPyramid(dim, 2.0, 3.0)
            assert pyramid.get_vertex_count() == expected_vertices

    def test_pyramid_edge_count(self):
        """Test pyramid edge count formula."""
        test_cases = [
            (1, 1),  # Line: 1 edge
            (2, 3),  # Triangle: 3 edges
            (3, 8),  # Square pyramid: 8 edges
            (4, 20),  # 4D pyramid: 20 edges
        ]

        for dim, expected_edges in test_cases:
            pyramid = HyperPyramid(dim, 2.0, 3.0)
            assert pyramid.get_edge_count() == expected_edges


@pytest.mark.mathematical
class TestTilingMathematics:
    """Test tiling mathematical properties."""

    def test_regular_tiling_coverage_efficiency(self, tolerance):
        """Test regular tiling coverage efficiency."""
        # Square tiling should have 100% coverage
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)
        bounds = [(0, 10), (0, 10)]
        tiling.generate_pattern(bounds, density=1.0)

        efficiency = tiling.get_coverage_efficiency()
        assert abs(efficiency - 1.0) < tolerance

    def test_hexagonal_tiling_efficiency(self, tolerance):
        """Test hexagonal tiling efficiency."""
        # Hexagonal tiling should have 100% coverage
        tiling = HexagonalTiling(1.0)
        bounds = [(0, 10), (0, 10)]
        tiling.generate_pattern(bounds, density=1.0)

        efficiency = tiling.get_coverage_efficiency()
        assert abs(efficiency - 1.0) < tolerance

    def test_circle_packing_efficiency(self, tolerance):
        """Test circle packing efficiency."""
        # Circle packing should have π/(2√3) ≈ 0.9069 efficiency
        sphere = HyperSphere(2, 0.5)
        tiling = RegularTiling(2, sphere)
        bounds = [(0, 10), (0, 10)]
        tiling.generate_pattern(bounds, density=1.0)

        efficiency = tiling.get_coverage_efficiency()
        expected_efficiency = math.pi / (2 * math.sqrt(3))
        assert (
            abs(efficiency - expected_efficiency) < 0.1
        )  # Allow some tolerance for discrete approximation

    def test_tiling_density_calculations(self, tolerance):
        """Test tiling density calculations."""
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)
        bounds = [(0, 5), (0, 5)]
        tiles = tiling.generate_pattern(bounds, density=1.0)

        analyzer = TilingAnalyzer(tiling)
        analysis = analyzer.analyze_pattern()

        # Tile density should be number of tiles per unit area
        expected_density = len(tiles) / (5 * 5)
        assert abs(analysis["tile_density"] - expected_density) < tolerance

    def test_hexagonal_coordination_number(self):
        """Test hexagonal tiling coordination number."""
        tiling = HexagonalTiling(1.0)
        bounds = [(0, 10), (0, 10)]
        tiling.generate_pattern(bounds, density=1.0)

        analyzer = TilingAnalyzer(tiling)
        analysis = analyzer.analyze_pattern()

        # Hexagonal tiling should have coordination number 6
        assert analysis["mathematical_properties"]["coordination_number"] == 6

    def test_square_tiling_coordination_number(self):
        """Test square tiling coordination number."""
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)
        bounds = [(0, 10), (0, 10)]
        tiling.generate_pattern(bounds, density=1.0)

        analyzer = TilingAnalyzer(tiling)
        analysis = analyzer.analyze_pattern()

        # Square tiling should have coordination number 4
        assert analysis["mathematical_properties"]["coordination_number"] == 4

    def test_tiling_scaling_properties(self, tolerance):
        """Test tiling scaling properties."""
        # Test that tiling scales correctly with density
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)
        bounds = [(0, 10), (0, 10)]

        # Generate with different densities
        tiles_1x = tiling.generate_pattern(bounds, density=1.0)
        tiles_2x = tiling.generate_pattern(bounds, density=2.0)

        # Higher density should produce more tiles
        assert len(tiles_2x) > len(tiles_1x)

        # Coverage efficiency should remain the same
        efficiency_1x = tiling.get_coverage_efficiency()
        tiling.generate_pattern(bounds, density=2.0)  # Regenerate for efficiency calc
        efficiency_2x = tiling.get_coverage_efficiency()

        assert abs(efficiency_1x - efficiency_2x) < tolerance


@pytest.mark.mathematical
class TestGeometricRelationships:
    """Test geometric relationships and theorems."""

    def test_isoperimetric_inequality(self, tolerance):
        """Test isoperimetric inequality for circles."""
        # Among all shapes with the same perimeter, the circle has the largest area
        perimeter = 2 * math.pi  # Circle with radius 1
        circle = HyperSphere(2, 1.0)

        # Circle area for given perimeter
        circle_area = circle.get_volume()

        # Square with same perimeter
        square_side = perimeter / 4
        square = HyperCube(2, square_side)
        square_area = square.get_volume()

        # Circle should have larger area
        assert circle_area > square_area

        # Test the inequality: A ≤ P²/(4π)
        assert circle_area <= (perimeter**2) / (4 * math.pi) + tolerance

    def test_packing_density_theorem(self, tolerance):
        """Test sphere packing density relationships."""
        # In 2D, the optimal packing density is π/(2√3)
        sphere = HyperSphere(2, 0.5)
        tiling = RegularTiling(2, sphere)
        bounds = [(0, 20), (0, 20)]  # Large area for better approximation
        tiling.generate_pattern(bounds, density=1.0)

        efficiency = tiling.get_coverage_efficiency()
        expected_efficiency = math.pi / (2 * math.sqrt(3))

        # Allow some tolerance for discrete approximation
        assert abs(efficiency - expected_efficiency) < 0.1

    def test_euler_characteristic(self):
        """Test Euler characteristic for polyhedra."""
        # For 3D polyhedra: V - E + F = 2
        test_cases = [
            # (vertices, edges, faces)
            (4, 6, 4),  # Tetrahedron
            (8, 12, 6),  # Cube
        ]

        for vertices, edges, faces in test_cases:
            euler_char = vertices - edges + faces
            assert euler_char == 2

    def test_volume_surface_area_relationships(self, tolerance):
        """Test relationships between volume and surface area."""
        # For spheres: dV/dr = S (surface area)
        radius = 2.0
        delta_r = 0.001

        sphere1 = HyperSphere(3, radius)
        sphere2 = HyperSphere(3, radius + delta_r)

        dV_dr = (sphere2.get_volume() - sphere1.get_volume()) / delta_r
        surface_area = sphere1.get_surface_area()

        # Should be approximately equal
        assert abs(dV_dr - surface_area) < 0.1

    def test_dimensional_scaling_laws(self, tolerance):
        """Test dimensional scaling laws."""
        base_size = 1.0
        scale_factor = 2.0

        for dim in range(1, 6):
            # Test sphere scaling
            sphere1 = HyperSphere(dim, base_size)
            sphere2 = HyperSphere(dim, base_size * scale_factor)

            # Volume should scale as scale_factor^dim
            volume_ratio = sphere2.get_volume() / sphere1.get_volume()
            expected_ratio = scale_factor**dim
            assert abs(volume_ratio - expected_ratio) < tolerance

            # Surface area should scale as scale_factor^(dim-1)
            surface_ratio = sphere2.get_surface_area() / sphere1.get_surface_area()
            expected_ratio = scale_factor ** (dim - 1)
            assert abs(surface_ratio - expected_ratio) < tolerance


@pytest.mark.mathematical
class TestNumericalStability:
    """Test numerical stability and precision."""

    def test_small_values_stability(self, tolerance):
        """Test stability with very small values."""
        small_radius = 1e-10
        sphere = HyperSphere(3, small_radius)

        volume = sphere.get_volume()
        surface_area = sphere.get_surface_area()

        # Should still be positive and finite
        assert volume > 0
        assert surface_area > 0
        assert math.isfinite(volume)
        assert math.isfinite(surface_area)

    def test_large_values_stability(self, tolerance):
        """Test stability with very large values."""
        large_radius = 1e6
        sphere = HyperSphere(3, large_radius)

        volume = sphere.get_volume()
        surface_area = sphere.get_surface_area()

        # Should be positive and finite
        assert volume > 0
        assert surface_area > 0
        assert math.isfinite(volume)
        assert math.isfinite(surface_area)

    def test_high_precision_calculations(self, tolerance):
        """Test high precision calculations."""
        # Test with values that require high precision
        radius = math.pi
        sphere = HyperSphere(3, radius)

        # Calculate expected volume with high precision
        expected_volume = (4.0 / 3.0) * math.pi * radius**3
        actual_volume = sphere.get_volume()

        # Should match to high precision
        relative_error = abs(actual_volume - expected_volume) / expected_volume
        assert relative_error < tolerance

    def test_extreme_dimensions_stability(self):
        """Test stability with extreme dimensions."""
        # Test with dimension 1 (edge case)
        sphere_1d = HyperSphere(1, 1.0)
        assert sphere_1d.get_volume() == 2.0  # Length of line segment
        assert sphere_1d.get_surface_area() == 2.0  # Two endpoints

        # Test with high dimension
        sphere_20d = HyperSphere(20, 1.0)
        volume = sphere_20d.get_volume()
        surface_area = sphere_20d.get_surface_area()

        # Should be positive and finite
        assert volume > 0
        assert surface_area > 0
        assert math.isfinite(volume)
        assert math.isfinite(surface_area)


@pytest.mark.mathematical
class TestMathematicalEdgeCases:
    """Test mathematical edge cases and boundary conditions."""

    def test_unit_values(self, tolerance):
        """Test calculations with unit values."""
        # Test unit sphere in various dimensions
        for dim in range(1, 8):
            sphere = HyperSphere(dim, 1.0)
            volume = sphere.get_volume()
            surface_area = sphere.get_surface_area()

            # Volume should match theoretical formula
            expected_volume = (math.pi ** (dim / 2.0)) / gamma(dim / 2.0 + 1)
            assert abs(volume - expected_volume) < tolerance

            # Surface area should match theoretical formula
            expected_surface = dim * expected_volume
            assert abs(surface_area - expected_surface) < tolerance

    def test_rational_values(self, tolerance):
        """Test calculations with rational values."""
        # Test with simple fractions
        test_values = [0.5, 1.5, 2.5, 3.5]

        for value in test_values:
            sphere = HyperSphere(3, value)
            cube = HyperCube(3, value)

            # Calculations should be exact for rational inputs
            sphere_volume = sphere.get_volume()
            cube_volume = cube.get_volume()

            assert math.isfinite(sphere_volume)
            assert math.isfinite(cube_volume)
            assert sphere_volume > 0
            assert cube_volume > 0

    def test_irrational_values(self, tolerance):
        """Test calculations with irrational values."""
        # Test with π, e, √2, etc.
        irrational_values = [math.pi, math.e, math.sqrt(2), math.sqrt(3)]

        for value in irrational_values:
            sphere = HyperSphere(3, value)
            volume = sphere.get_volume()
            surface_area = sphere.get_surface_area()

            # Should handle irrational values correctly
            assert math.isfinite(volume)
            assert math.isfinite(surface_area)
            assert volume > 0
            assert surface_area > 0

    def test_zero_boundary_conditions(self):
        """Test behavior near zero boundary."""
        # Test with very small but non-zero values
        epsilon = 1e-15

        # Should not create shapes with zero or negative parameters
        with pytest.raises(ValueError):
            HyperSphere(3, 0.0)

        with pytest.raises(ValueError):
            HyperCube(3, 0.0)

        # Should handle very small positive values
        tiny_sphere = HyperSphere(3, epsilon)
        assert tiny_sphere.get_volume() > 0
        assert tiny_sphere.get_surface_area() > 0
