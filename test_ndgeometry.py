"""Tests for ndgeometry.py"""

import math
import pytest
from ndgeometry import Sphere, Cube, Ellipsoid, Simplex


class TestSphere:
    def test_3d_sphere_volume(self):
        """Classic formula: V = (4/3)πr³"""
        s = Sphere(3, 2.0)
        expected = (4/3) * math.pi * 2.0**3
        assert abs(s.volume - expected) < 1e-10
    
    def test_3d_sphere_surface(self):
        """Classic formula: A = 4πr²"""
        s = Sphere(3, 2.0)
        expected = 4 * math.pi * 2.0**2
        assert abs(s.surface_area - expected) < 1e-10
    
    def test_2d_circle(self):
        """2D sphere is a circle: A = πr²"""
        s = Sphere(2, 3.0)
        assert abs(s.volume - math.pi * 9) < 1e-10
        assert abs(s.surface_area - 2 * math.pi * 3) < 1e-10
    
    def test_4d_hypersphere(self):
        """4D: V = (π²/2)r⁴"""
        s = Sphere(4, 1.0)
        expected = math.pi**2 / 2
        assert abs(s.volume - expected) < 1e-10
    
    def test_unit_sphere_volume_peak(self):
        """Famous result: unit sphere volume peaks around 5D"""
        volumes = [Sphere(n, 1.0).volume for n in range(1, 15)]
        peak_idx = volumes.index(max(volumes))
        assert 4 <= peak_idx <= 5  # 0-indexed, so 5D or 6D
    
    def test_scaling(self):
        """Volume scales as r^n"""
        s1 = Sphere(4, 1.0)
        s2 = Sphere(4, 2.0)
        assert abs(s2.volume / s1.volume - 16.0) < 1e-10  # 2^4
    
    def test_invalid_inputs(self):
        with pytest.raises(ValueError):
            Sphere(0, 1.0)  # Zero dimensions
        with pytest.raises(ValueError):
            Sphere(3, 0.0)  # Zero radius
        with pytest.raises(ValueError):
            Sphere(3, -1.0)  # Negative radius
    
    def test_names(self):
        assert Sphere(2, 1).name == "circle"
        assert Sphere(3, 1).name == "sphere"
        assert "hypersphere" in Sphere(5, 1).name


class TestCube:
    def test_3d_cube_volume(self):
        c = Cube(3, 2.0)
        assert c.volume == 8.0
    
    def test_3d_cube_surface(self):
        c = Cube(3, 2.0)
        assert c.surface_area == 24.0  # 6 faces × 4
    
    def test_diagonal(self):
        c = Cube(3, 1.0)
        assert abs(c.diagonal - math.sqrt(3)) < 1e-10
    
    def test_vertices_and_edges(self):
        c = Cube(4, 1.0)
        assert c.vertices == 16  # 2^4
        assert c.edges == 32     # 4 × 2^3
    
    def test_names(self):
        assert Cube(2, 1).name == "square"
        assert Cube(3, 1).name == "cube"
        assert Cube(4, 1).name == "tesseract"

    def test_invalid_inputs(self):
        with pytest.raises(ValueError):
            Cube(0, 1.0)
        with pytest.raises(ValueError):
            Cube(3, 0.0)
        with pytest.raises(ValueError):
            Cube(3, -1.0)


class TestEllipsoid:
    def test_3d_ellipsoid_volume(self):
        """V = (4/3)π × a × b × c"""
        e = Ellipsoid((1.0, 2.0, 3.0))
        expected = (4/3) * math.pi * 1.0 * 2.0 * 3.0
        assert abs(e.volume - expected) < 1e-10
    
    def test_sphere_detection(self):
        e1 = Ellipsoid((2.0, 2.0, 2.0))
        e2 = Ellipsoid((1.0, 2.0, 3.0))
        assert e1.is_sphere
        assert not e2.is_sphere
    
    def test_matches_sphere(self):
        """Ellipsoid with equal axes should match sphere"""
        e = Ellipsoid((2.0, 2.0, 2.0))
        s = Sphere(3, 2.0)
        assert abs(e.volume - s.volume) < 1e-10

    def test_invalid_inputs(self):
        with pytest.raises(ValueError):
            Ellipsoid(())
        with pytest.raises(ValueError):
            Ellipsoid((1.0, 0.0, 2.0))
        with pytest.raises(ValueError):
            Ellipsoid((1.0, -1.0))


class TestSimplex:
    def test_2d_triangle(self):
        """Equilateral triangle: A = (√3/4)s²"""
        s = Simplex(2, 2.0)
        expected = (math.sqrt(3) / 4) * 4.0
        assert abs(s.volume - expected) < 1e-10
    
    def test_3d_tetrahedron(self):
        """Regular tetrahedron: V = (√2/12)s³"""
        s = Simplex(3, 2.0)
        expected = (math.sqrt(2) / 12) * 8.0
        assert abs(s.volume - expected) < 1e-10
    
    def test_vertex_count(self):
        assert Simplex(2, 1).vertices == 3   # Triangle
        assert Simplex(3, 1).vertices == 4   # Tetrahedron
        assert Simplex(4, 1).vertices == 5   # 4-simplex
    
    def test_edge_count(self):
        assert Simplex(2, 1).edges == 3   # Triangle: 3 edges
        assert Simplex(3, 1).edges == 6   # Tetrahedron: 6 edges
    
    def test_names(self):
        assert Simplex(2, 1).name == "triangle"
        assert Simplex(3, 1).name == "tetrahedron"

    def test_invalid_inputs(self):
        with pytest.raises(ValueError):
            Simplex(0, 1.0)
        with pytest.raises(ValueError):
            Simplex(3, 0.0)
        with pytest.raises(ValueError):
            Simplex(3, -1.0)


class TestHighDimensions:
    """Verify numerical stability at extreme dimensions."""
    
    def test_high_dimension_sphere(self):
        s = Sphere(50, 1.0)
        assert s.volume > 0
        assert math.isfinite(s.volume)
        assert math.isfinite(s.surface_area)
    
    def test_high_dimension_cube(self):
        c = Cube(50, 1.0)
        assert c.volume == 1.0  # s^n = 1^50 = 1
        assert c.vertices == 2**50
    
    def test_very_small_radius(self):
        s = Sphere(3, 1e-10)
        assert s.volume > 0
        assert math.isfinite(s.volume)
    
    def test_very_large_radius(self):
        s = Sphere(3, 1e10)
        assert math.isfinite(s.volume)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

