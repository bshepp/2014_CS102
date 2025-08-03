#!/usr/bin/env python3
"""
Tiling Tests for the N-Dimensional Geometry Engine
Tests tiling patterns and tessellation functionality
"""

import os
import sys

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geometry_engine import (
    HexagonalTiling,
    HyperCube,
    RegularTiling,
    TilingAnalyzer,
    VoronoiTiling,
)


@pytest.mark.tiling
class TestRegularTiling:
    """Test regular tiling patterns."""

    def test_square_tiling_creation(self):
        """Test creation of square tiling pattern."""
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)
        assert tiling.dimensions == 2
        assert tiling.base_shape.dimensions == 2

    def test_square_tiling_pattern_generation(self):
        """Test square tiling pattern generation."""
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)
        bounds = [(0, 5), (0, 5)]
        tiling.generate_pattern(bounds, density=1.0)

        # Should generate tiles
        assert len(tiling.tiles) > 0

        # Test get_tile_count method
        tile_count = tiling.get_tile_count()
        assert tile_count == len(tiling.tiles)


@pytest.mark.tiling
class TestHexagonalTiling:
    """Test hexagonal tiling patterns."""

    def test_hexagonal_tiling_creation(self):
        """Test creation of hexagonal tiling pattern."""
        tiling = HexagonalTiling(1.0)
        assert tiling.side_length == 1.0
        assert tiling.dimensions == 2

    def test_hexagonal_tiling_pattern_generation(self):
        """Test hexagonal tiling pattern generation."""
        tiling = HexagonalTiling(1.0)
        bounds = [(0, 10), (0, 10)]
        tiling.generate_pattern(bounds, density=1.0)

        # Should generate tiles
        assert len(tiling.tiles) > 0

        # Coverage should be 100% for hexagonal tiling
        efficiency = tiling.get_coverage_efficiency()
        assert efficiency == 1.0


@pytest.mark.tiling
class TestVoronoiTiling:
    """Test Voronoi tiling patterns."""

    def test_voronoi_tiling_creation(self):
        """Test creation of Voronoi tiling pattern."""
        seed_points = [[1, 1], [3, 2], [2, 4]]
        tiling = VoronoiTiling(2, seed_points)
        assert len(tiling.seed_points) == 3
        assert tiling.dimensions == 2

    def test_voronoi_pattern_generation(self):
        """Test Voronoi pattern generation."""
        seed_points = [[1, 1], [3, 2], [2, 4], [5, 5]]
        tiling = VoronoiTiling(2, seed_points)
        bounds = [(0, 6), (0, 6)]
        tiling.generate_pattern(bounds, density=1.0)

        # Should generate tiles
        assert len(tiling.tiles) > 0


@pytest.mark.tiling
class TestTilingAnalyzer:
    """Test tiling analysis functionality."""

    def test_tiling_analyzer_creation(self):
        """Test creation of tiling analyzer."""
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)
        analyzer = TilingAnalyzer(tiling)
        assert analyzer.pattern == tiling

    def test_pattern_analysis(self):
        """Test pattern analysis functionality."""
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)
        bounds = [(0, 5), (0, 5)]
        tiling.generate_pattern(bounds, density=1.0)

        analyzer = TilingAnalyzer(tiling)
        properties = analyzer.analyze_pattern()

        # Should return a dictionary with analysis results
        assert isinstance(properties, dict)


@pytest.mark.tiling
class TestTilingProperties:
    """Test basic tiling properties."""

    def test_tiling_pattern_properties(self):
        """Test getting pattern properties."""
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)

        properties = tiling.get_pattern_properties()

        # Should have basic properties
        assert "dimensions" in properties
        assert "pattern_type" in properties
        assert properties["dimensions"] == 2
        assert properties["pattern_type"] == "regular"

    def test_hexagonal_properties(self):
        """Test hexagonal tiling properties."""
        tiling = HexagonalTiling(1.0)

        properties = tiling.get_pattern_properties()

        assert properties["dimensions"] == 2
        assert properties["pattern_type"] == "hexagonal"


# Simple performance tests
@pytest.mark.tiling
@pytest.mark.performance
class TestTilingPerformance:
    """Test basic tiling performance."""

    def test_regular_tiling_performance(self):
        """Test regular tiling generation performance."""
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)
        bounds = [(0, 5), (0, 5)]

        # Should complete without timeout
        tiling.generate_pattern(bounds, density=1.0)
        assert len(tiling.tiles) > 0

    def test_hexagonal_tiling_performance(self):
        """Test hexagonal tiling generation performance."""
        tiling = HexagonalTiling(1.0)
        bounds = [(0, 10), (0, 10)]

        # Should complete without timeout
        tiling.generate_pattern(bounds, density=1.0)
        assert len(tiling.tiles) > 0


# Fixtures for tiling tests
@pytest.fixture
def sample_square_tiling():
    """Create a sample square tiling for testing."""
    cube = HyperCube(2, 1.0)
    tiling = RegularTiling(2, cube)
    bounds = [(0, 5), (0, 5)]
    tiling.generate_pattern(bounds, density=1.0)
    return tiling


@pytest.fixture
def sample_hexagonal_tiling():
    """Create a sample hexagonal tiling for testing."""
    tiling = HexagonalTiling(1.0)
    bounds = [(0, 8), (0, 8)]
    tiling.generate_pattern(bounds, density=1.0)
    return tiling


@pytest.fixture
def sample_voronoi_tiling():
    """Create a sample Voronoi tiling for testing."""
    seed_points = [[1, 1], [3, 2], [2, 4], [5, 3], [4, 5]]
    tiling = VoronoiTiling(2, seed_points)
    bounds = [(0, 6), (0, 6)]
    tiling.generate_pattern(bounds, density=1.0)
    return tiling
