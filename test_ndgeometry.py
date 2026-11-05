"""Tests for ndgeometry.py"""

import math
from decimal import Decimal, localcontext
from fractions import Fraction

import pytest
from ndgeometry import Sphere, Cube, Ellipsoid, Simplex, unit_ball_coefficient
from ndgeometry import _pi

# Known digits of pi, independent of the library's own computation.
PI_50 = Decimal("3.14159265358979323846264338327950288419716939937510")


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

    def test_surface_area(self):
        """Triangle perimeter 3s; tetrahedron 4 faces of (√3/4)s² = √3 s²; segment: 2 endpoints"""
        assert abs(Simplex(2, 2.0).surface_area - 6.0) < 1e-10
        assert abs(Simplex(3, 2.0).surface_area - math.sqrt(3) * 4.0) < 1e-10
        assert abs(Simplex(1, 5.0).surface_area - 2.0) < 1e-10

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

    def test_sphere_beyond_gamma_overflow(self):
        """math.gamma overflows past ~340D; the log-space path must take over seamlessly."""
        s = Sphere(400, 3.0)
        assert 0 < s.volume < math.inf
        expected_log = 200 * math.log(math.pi) - math.lgamma(201) + 400 * math.log(3.0)
        assert math.isclose(math.log(s.volume), expected_log, rel_tol=1e-12)
        assert math.isclose(s.log_volume, expected_log, rel_tol=1e-12)

    def test_log_volume_when_volume_underflows(self):
        """ln V = (n/2) ln π − lnΓ(n/2+1) + n ln r stays finite after the float hits 0.0"""
        s = Sphere(500, 1.0)
        assert s.volume == 0.0  # true value ~1e-300-something, below the double range
        assert math.isclose(s.log_volume, 250 * math.log(math.pi) - math.lgamma(251))

    def test_simplex_beyond_factorial_float_range(self):
        """171! does not fit in a float; the log-space path must take over."""
        s = Simplex(200, 20.0)
        assert 0 < s.volume < math.inf
        expected_log = 200 * math.log(20.0) - math.lgamma(201) + (math.log(201) - 200 * math.log(2)) / 2
        assert math.isclose(math.log(s.volume), expected_log, rel_tol=1e-12)

    def test_cube_saturates_instead_of_raising(self):
        assert Cube(2000, 2.0).volume == math.inf
        assert Cube(2000, 0.5).volume == 0.0
        assert math.isclose(Cube(2000, 2.0).log_volume, 2000 * math.log(2))
        assert math.isclose(Cube(2000, 2.0).diagonal, 2 * math.sqrt(2000))

    def test_ellipsoid_many_axes(self):
        e = Ellipsoid((2.0,) * 400)
        assert 0 < e.volume < math.inf
        assert math.isclose(math.log(e.volume), e.log_volume, rel_tol=1e-12)
        assert math.isclose(e.log_volume, Sphere(400, 2.0).log_volume)

    def test_million_dimensions(self):
        """Float properties never raise, whatever the dimension."""
        n = 1_000_000
        assert Sphere(n, 1.0).volume == 0.0 and math.isfinite(Sphere(n, 1.0).log_volume)
        assert Cube(n, 1.0).volume == 1.0
        assert Simplex(n, 1.0).volume == 0.0 and math.isfinite(Simplex(n, 1.0).log_volume)


class TestExactCoefficient:
    """Unit n-ball volume is a rational multiple of π^(n//2)."""

    def test_known_coefficients(self):
        # 2r, πr², (4/3)πr³, (π²/2)r⁴, (8/15)π²r⁵, (π³/6)r⁶, (16/105)π³r⁷
        expected = [Fraction(2), Fraction(1), Fraction(4, 3), Fraction(1, 2),
                    Fraction(8, 15), Fraction(1, 6), Fraction(16, 105)]
        assert [unit_ball_coefficient(n) for n in range(1, 8)] == expected

    def test_recurrence(self):
        """V_n = V_(n-2) · 2π/n, so c_n = c_(n-2) · 2/n"""
        for n in range(3, 300):
            assert unit_ball_coefficient(n) == unit_ball_coefficient(n - 2) * Fraction(2, n)

    def test_matches_float_volume(self):
        for n in range(1, 100):
            exact = float(unit_ball_coefficient(n)) * math.pi ** (n // 2)
            assert math.isclose(exact, Sphere(n, 1.0).volume, rel_tol=1e-13)


class TestPrecise:
    """Arbitrary-precision results from the decimal module."""

    def test_pi(self):
        assert str(_pi(50)) == "3.1415926535897932384626433832795028841971693993751"
        assert str(_pi(5)) == "3.1416"

    def test_3d_sphere_closed_form(self):
        """V = (4/3)πr³ and A = 4πr², evaluated against independently known digits of π"""
        p = Sphere(3, 2.0).precise(40)
        with localcontext() as ctx:
            ctx.prec = 50
            assert abs(p["volume"] - Decimal(4) / 3 * PI_50 * 8) < Decimal("1e-37")
            assert abs(p["surface_area"] - 4 * PI_50 * 4) < Decimal("1e-37")

    def test_tetrahedron_closed_form(self):
        """V = (√2/12)s³; surface = √3 s²"""
        p = Simplex(3, 2.0).precise(40)
        with localcontext() as ctx:
            ctx.prec = 50
            assert abs(p["volume"] - Decimal(2).sqrt() / 12 * 8) < Decimal("1e-38")
            assert abs(p["surface_area"] - Decimal(3).sqrt() * 4) < Decimal("1e-38")

    def test_cube_closed_form(self):
        p = Cube(3, Decimal("1.5")).precise(20)
        assert p["volume"] == Decimal("3.375")
        assert p["surface_area"] == Decimal("13.5")
        with localcontext() as ctx:
            ctx.prec = 30
            assert abs(p["diagonal"] - Decimal("1.5") * Decimal(3).sqrt()) < Decimal("1e-19")

    def test_ellipsoid_closed_form(self):
        """V = (4/3)π·a·b·c"""
        v = Ellipsoid((1.0, 2.0, 3.0)).precise(40)["volume"]
        with localcontext() as ctx:
            ctx.prec = 50
            assert abs(v - Decimal(4) / 3 * PI_50 * 6) < Decimal("1e-37")

    def test_far_outside_float_range(self):
        """2^2000 ≈ 1.1e602 cannot be a float, but is exact in Decimal"""
        with localcontext() as ctx:
            ctx.prec = 20
            assert Cube(2000, 2.0).precise(20)["volume"] == +Decimal(2 ** 2000)
        v = Sphere(1000, 1.0).precise(10)["volume"]
        assert v.adjusted() == -886  # i.e. 3.08e-886
        assert math.isclose(float(v.ln()), Sphere(1000, 1.0).log_volume, rel_tol=1e-9)

    def test_requested_digits(self):
        for digits in (1, 5, 15, 30, 100):
            v = Sphere(7, 0.1).precise(digits)["volume"]
            assert len(v.as_tuple().digits) <= digits

    def test_more_digits_refine_but_never_change(self):
        """precise(100) rounded to 30 digits must equal precise(30): every digit shown is correct"""
        with localcontext() as ctx:
            ctx.prec = 30
            for shape in (Sphere(123, 0.1), Cube(999, 1.01), Simplex(77, 2.5),
                          Ellipsoid((1.1, 2.2, 3.3, 4.4)), Sphere(5000, 7.0)):
                hi, lo = shape.precise(100), shape.precise(30)
                assert all(+hi[key] == lo[key] for key in lo), shape

    def test_inputs_are_taken_as_decimal(self):
        """radius 0.1 means exactly 0.1, not the nearest binary float"""
        assert Cube(3, 0.1).precise(20)["volume"] == Decimal("0.001")

    def test_float_agrees_with_precise(self):
        """Float path is correct to ~n × 1e-16, in both the direct and log-space regions"""
        for n in (1, 5, 50, 340, 341, 1000):
            for shape in (Sphere(n, 1.1), Cube(n, 1.1), Ellipsoid((1.1,) * n), Simplex(n, 3.0)):
                v = shape.volume
                if 0 < v < math.inf:
                    error = abs(float(Decimal(v) / shape.precise(30)["volume"]) - 1)
                    assert error < 1e-12, (shape, error)

    def test_invalid_digits(self):
        with pytest.raises(ValueError):
            Sphere(3, 1.0).precise(0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

