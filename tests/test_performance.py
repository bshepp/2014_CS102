#!/usr/bin/env python3
"""
Performance Tests for the N-Dimensional Geometry Engine
Benchmarks computational performance and scalability
"""

import gc
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

import psutil
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geometry_engine import (
    GeometryAgent,
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


@pytest.mark.performance
@pytest.mark.benchmark
class TestGeometryPerformance:
    """Test performance of geometry calculations."""

    def test_hypersphere_creation_performance(self, benchmark):
        """Benchmark hypersphere creation performance."""

        def create_hypersphere():
            return HyperSphere(10, 1.0)

        result = benchmark(create_hypersphere)
        assert result.dimensions == 10
        assert result.radius == 1.0

    def test_hypersphere_volume_performance(self, benchmark):
        """Benchmark hypersphere volume calculation performance."""
        sphere = HyperSphere(10, 1.0)

        def calculate_volume():
            return sphere.get_volume()

        result = benchmark(calculate_volume)
        assert result > 0

    def test_hypersphere_surface_area_performance(self, benchmark):
        """Benchmark hypersphere surface area calculation performance."""
        sphere = HyperSphere(10, 1.0)

        def calculate_surface_area():
            return sphere.get_surface_area()

        result = benchmark(calculate_surface_area)
        assert result > 0

    def test_hypercube_creation_performance(self, benchmark):
        """Benchmark hypercube creation performance."""

        def create_hypercube():
            return HyperCube(10, 1.0)

        result = benchmark(create_hypercube)
        assert result.dimensions == 10
        assert result.side_length == 1.0

    def test_hypercube_volume_performance(self, benchmark):
        """Benchmark hypercube volume calculation performance."""
        cube = HyperCube(10, 1.0)

        def calculate_volume():
            return cube.get_volume()

        result = benchmark(calculate_volume)
        assert result > 0

    def test_hyperellipsoid_creation_performance(self, benchmark):
        """Benchmark hyperellipsoid creation performance."""

        def create_hyperellipsoid():
            return HyperEllipsoid(10, *[float(i + 1) for i in range(10)])

        result = benchmark(create_hyperellipsoid)
        assert result.dimensions == 10

    def test_simplex_creation_performance(self, benchmark):
        """Benchmark simplex creation performance."""

        def create_simplex():
            return Simplex(10, 1.0)

        result = benchmark(create_simplex)
        assert result.dimensions == 10

    def test_hyperpyramid_creation_performance(self, benchmark):
        """Benchmark hyperpyramid creation performance."""

        def create_hyperpyramid():
            return HyperPyramid(10, 2.0, 3.0)

        result = benchmark(create_hyperpyramid)
        assert result.dimensions == 10


@pytest.mark.performance
@pytest.mark.benchmark
class TestTilingPerformance:
    """Test performance of tiling operations."""

    def test_regular_tiling_performance(self, benchmark):
        """Benchmark regular tiling generation performance."""
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)
        bounds = [(0, 10), (0, 10)]

        def generate_tiling():
            return tiling.generate_pattern(bounds, density=1.0)

        result = benchmark(generate_tiling)
        assert len(result) > 0

    def test_hexagonal_tiling_performance(self, benchmark):
        """Benchmark hexagonal tiling generation performance."""
        tiling = HexagonalTiling(1.0)
        bounds = [(0, 20), (0, 20)]

        def generate_tiling():
            return tiling.generate_pattern(bounds, density=1.0)

        result = benchmark(generate_tiling)
        assert len(result) > 0

    def test_voronoi_tiling_performance(self, benchmark):
        """Benchmark Voronoi tiling generation performance."""
        seed_points = [[i, j] for i in range(0, 10, 2) for j in range(0, 10, 2)]
        tiling = VoronoiTiling(2, seed_points)
        bounds = [(0, 10), (0, 10)]

        def generate_tiling():
            return tiling.generate_pattern(bounds, density=1.0)

        result = benchmark(generate_tiling)
        assert len(result) > 0

    def test_tiling_analyzer_performance(self, benchmark):
        """Benchmark tiling analysis performance."""
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)
        bounds = [(0, 10), (0, 10)]
        tiling.generate_pattern(bounds, density=1.0)

        analyzer = TilingAnalyzer(tiling)

        def analyze_tiling():
            return analyzer.analyze_pattern()

        result = benchmark(analyze_tiling)
        assert "coverage_efficiency" in result
        assert "mathematical_properties" in result


@pytest.mark.performance
@pytest.mark.benchmark
class TestAgentPerformance:
    """Test performance of geometry agent operations."""

    def test_agent_creation_performance(self, benchmark):
        """Benchmark geometry agent creation performance."""

        def create_agent():
            return GeometryAgent()

        result = benchmark(create_agent)
        assert result is not None

    def test_agent_query_performance(self, benchmark):
        """Benchmark geometry agent query processing performance."""
        agent = GeometryAgent()

        def process_query():
            return agent.process_query("create a 3D sphere radius 1")

        result = benchmark(process_query)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_agent_complex_query_performance(self, benchmark):
        """Benchmark complex geometry agent queries."""
        agent = GeometryAgent()

        def process_complex_query():
            return agent.process_query("create a 5D ellipsoid with axes 1 2 3 4 5")

        result = benchmark(process_complex_query)
        assert isinstance(result, str)
        assert len(result) > 0


@pytest.mark.performance
@pytest.mark.slow
class TestScalabilityLimits:
    """Test scalability limits of the geometry engine."""

    def test_high_dimensional_sphere_performance(self, performance_limits):
        """Test performance with high-dimensional spheres."""
        max_dim = performance_limits["max_dimension"]
        max_time = performance_limits["max_response_time"]

        for dim in range(1, max_dim + 1):
            start_time = time.time()
            sphere = HyperSphere(dim, 1.0)
            volume = sphere.get_volume()
            surface_area = sphere.get_surface_area()
            end_time = time.time()

            elapsed_time = end_time - start_time
            assert (
                elapsed_time < max_time
            ), f"Dimension {dim} took {elapsed_time:.3f}s > {max_time}s"
            assert volume > 0
            assert surface_area > 0

    def test_high_dimensional_cube_performance(self, performance_limits):
        """Test performance with high-dimensional cubes."""
        max_dim = performance_limits["max_dimension"]
        max_time = performance_limits["max_response_time"]

        for dim in range(1, max_dim + 1):
            start_time = time.time()
            cube = HyperCube(dim, 1.0)
            volume = cube.get_volume()
            surface_area = cube.get_surface_area()
            vertex_count = cube.get_vertex_count()
            edge_count = cube.get_edge_count()
            end_time = time.time()

            elapsed_time = end_time - start_time
            assert (
                elapsed_time < max_time
            ), f"Dimension {dim} took {elapsed_time:.3f}s > {max_time}s"
            assert volume > 0
            assert surface_area > 0
            assert vertex_count > 0
            assert edge_count > 0

    def test_large_tiling_performance(self, performance_limits):
        """Test performance with large tiling patterns."""
        max_tiles = performance_limits["max_tile_count"]
        max_time = performance_limits["max_response_time"]

        cube = HyperCube(2, 0.5)  # Small cubes for more tiles
        tiling = RegularTiling(2, cube)
        bounds = [(0, 50), (0, 50)]  # Large area

        start_time = time.time()
        tiles = tiling.generate_pattern(bounds, density=1.0)
        end_time = time.time()

        elapsed_time = end_time - start_time
        assert (
            elapsed_time < max_time
        ), f"Large tiling took {elapsed_time:.3f}s > {max_time}s"
        assert len(tiles) > 0
        assert len(tiles) <= max_tiles  # Should not exceed reasonable limits

    def test_many_voronoi_seeds_performance(self, performance_limits):
        """Test performance with many Voronoi seeds."""
        max_time = performance_limits["max_response_time"]

        # Create many seed points
        seed_points = [[i, j] for i in range(0, 20, 1) for j in range(0, 20, 1)]
        tiling = VoronoiTiling(2, seed_points)
        bounds = [(0, 20), (0, 20)]

        start_time = time.time()
        tiles = tiling.generate_pattern(bounds, density=1.0)
        end_time = time.time()

        elapsed_time = end_time - start_time
        assert (
            elapsed_time < max_time * 2
        ), f"Many seeds took {elapsed_time:.3f}s > {max_time * 2}s"
        assert len(tiles) == len(seed_points)


@pytest.mark.performance
@pytest.mark.slow
class TestMemoryUsage:
    """Test memory usage of the geometry engine."""

    def get_memory_usage(self):
        """Get current memory usage in MB."""
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # Convert to MB

    def test_sphere_memory_usage(self, performance_limits):
        """Test memory usage of sphere operations."""
        max_memory = performance_limits["max_memory_usage"]

        gc.collect()
        initial_memory = self.get_memory_usage()

        # Create many spheres
        spheres = []
        for i in range(1000):
            sphere = HyperSphere(10, 1.0)
            spheres.append(sphere)

        current_memory = self.get_memory_usage()
        memory_increase = current_memory - initial_memory

        assert (
            memory_increase < max_memory
        ), f"Memory increase {memory_increase:.1f}MB > {max_memory}MB"

        # Clean up
        del spheres
        gc.collect()

    def test_tiling_memory_usage(self, performance_limits):
        """Test memory usage of tiling operations."""
        max_memory = performance_limits["max_memory_usage"]

        gc.collect()
        initial_memory = self.get_memory_usage()

        # Create large tiling
        cube = HyperCube(2, 0.5)
        tiling = RegularTiling(2, cube)
        bounds = [(0, 30), (0, 30)]
        tiles = tiling.generate_pattern(bounds, density=1.0)

        current_memory = self.get_memory_usage()
        memory_increase = current_memory - initial_memory

        assert (
            memory_increase < max_memory
        ), f"Memory increase {memory_increase:.1f}MB > {max_memory}MB"

        # Clean up
        del tiles
        del tiling
        gc.collect()

    def test_agent_memory_usage(self, performance_limits):
        """Test memory usage of geometry agent."""
        max_memory = performance_limits["max_memory_usage"]

        gc.collect()
        initial_memory = self.get_memory_usage()

        # Create agent and process many queries
        agent = GeometryAgent()
        for i in range(100):
            result = agent.process_query(
                f"create a {i % 10 + 1}D sphere radius {i % 5 + 1}"
            )

        current_memory = self.get_memory_usage()
        memory_increase = current_memory - initial_memory

        assert (
            memory_increase < max_memory
        ), f"Memory increase {memory_increase:.1f}MB > {max_memory}MB"

        # Clean up
        del agent
        gc.collect()


@pytest.mark.performance
@pytest.mark.slow
class TestConcurrency:
    """Test concurrent operations performance."""

    def test_concurrent_sphere_creation(self):
        """Test concurrent sphere creation."""

        def create_sphere(dim):
            sphere = HyperSphere(dim, 1.0)
            return sphere.get_volume()

        dimensions = list(range(1, 21))
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(create_sphere, dim) for dim in dimensions]
            results = [future.result() for future in as_completed(futures)]

        end_time = time.time()
        elapsed_time = end_time - start_time

        assert len(results) == len(dimensions)
        assert all(result > 0 for result in results)
        assert elapsed_time < 10.0  # Should complete within 10 seconds

    def test_concurrent_tiling_generation(self):
        """Test concurrent tiling generation."""

        def generate_tiling(size):
            cube = HyperCube(2, 0.5)
            tiling = RegularTiling(2, cube)
            bounds = [(0, size), (0, size)]
            return tiling.generate_pattern(bounds, density=1.0)

        sizes = [5, 10, 15, 20]
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(generate_tiling, size) for size in sizes]
            results = [future.result() for future in as_completed(futures)]

        end_time = time.time()
        elapsed_time = end_time - start_time

        assert len(results) == len(sizes)
        assert all(len(result) > 0 for result in results)
        assert elapsed_time < 20.0  # Should complete within 20 seconds

    def test_concurrent_agent_queries(self):
        """Test concurrent geometry agent queries."""

        def process_query(query):
            agent = GeometryAgent()
            return agent.process_query(query)

        queries = [
            "create a 3D sphere radius 1",
            "create a 4D cube side 2",
            "create a 2D ellipse axes 1 2",
            "create a 3D tetrahedron side 1.5",
            "create a 3D pyramid base 2 height 3",
        ]

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(process_query, query) for query in queries]
            results = [future.result() for future in as_completed(futures)]

        end_time = time.time()
        elapsed_time = end_time - start_time

        assert len(results) == len(queries)
        assert all(isinstance(result, str) and len(result) > 0 for result in results)
        assert elapsed_time < 15.0  # Should complete within 15 seconds


@pytest.mark.performance
@pytest.mark.slow
class TestStressTests:
    """Stress tests for the geometry engine."""

    def test_rapid_sphere_creation(self):
        """Test rapid creation of many spheres."""
        start_time = time.time()

        spheres = []
        for i in range(10000):
            sphere = HyperSphere(i % 10 + 1, (i % 5 + 1) * 0.1)
            spheres.append(sphere)

        end_time = time.time()
        elapsed_time = end_time - start_time

        assert len(spheres) == 10000
        assert elapsed_time < 10.0  # Should complete within 10 seconds

        # Clean up
        del spheres
        gc.collect()

    def test_rapid_volume_calculations(self):
        """Test rapid volume calculations."""
        spheres = [HyperSphere(i % 10 + 1, 1.0) for i in range(1000)]

        start_time = time.time()

        volumes = []
        for sphere in spheres:
            volume = sphere.get_volume()
            volumes.append(volume)

        end_time = time.time()
        elapsed_time = end_time - start_time

        assert len(volumes) == 1000
        assert all(volume > 0 for volume in volumes)
        assert elapsed_time < 5.0  # Should complete within 5 seconds

    def test_rapid_tiling_operations(self):
        """Test rapid tiling operations."""
        start_time = time.time()

        tilings = []
        for i in range(100):
            cube = HyperCube(2, 0.5)
            tiling = RegularTiling(2, cube)
            bounds = [(0, 5), (0, 5)]
            tiles = tiling.generate_pattern(bounds, density=1.0)
            tilings.append(tiles)

        end_time = time.time()
        elapsed_time = end_time - start_time

        assert len(tilings) == 100
        assert all(len(tiling) > 0 for tiling in tilings)
        assert elapsed_time < 30.0  # Should complete within 30 seconds

        # Clean up
        del tilings
        gc.collect()

    def test_mixed_operations_stress(self):
        """Test mixed operations under stress."""
        start_time = time.time()

        operations = 0
        for i in range(1000):
            if i % 4 == 0:
                sphere = HyperSphere(i % 10 + 1, 1.0)
                volume = sphere.get_volume()
                operations += 1
            elif i % 4 == 1:
                cube = HyperCube(i % 10 + 1, 1.0)
                surface = cube.get_surface_area()
                operations += 1
            elif i % 4 == 2:
                ellipsoid = HyperEllipsoid(3, 1.0, 2.0, 3.0)
                ratio = ellipsoid.get_axis_ratio()
                operations += 1
            else:
                simplex = Simplex(i % 5 + 1, 1.0)
                vertices = simplex.get_vertex_count()
                operations += 1

        end_time = time.time()
        elapsed_time = end_time - start_time

        assert operations == 1000
        assert elapsed_time < 15.0  # Should complete within 15 seconds


@pytest.mark.performance
@pytest.mark.benchmark
class TestComputationalComplexity:
    """Test computational complexity of operations."""

    def test_sphere_volume_complexity(self, benchmark):
        """Test computational complexity of sphere volume calculation."""
        # Test with different dimensions to check if complexity scales reasonably
        dimensions = [1, 5, 10, 15, 20]
        times = []

        for dim in dimensions:
            sphere = HyperSphere(dim, 1.0)

            def calculate_volume():
                return sphere.get_volume()

            result = benchmark.pedantic(calculate_volume, iterations=100, rounds=5)
            times.append(benchmark.stats["mean"])

        # Check that time doesn't grow exponentially
        # Allow for some variation but ensure reasonable scaling
        for i in range(1, len(times)):
            ratio = times[i] / times[i - 1]
            assert ratio < 10.0, f"Time complexity too high: {ratio:.2f}x increase"

    def test_tiling_complexity(self, benchmark):
        """Test computational complexity of tiling generation."""
        # Test with different area sizes
        sizes = [5, 10, 15, 20]
        times = []

        for size in sizes:
            cube = HyperCube(2, 0.5)
            tiling = RegularTiling(2, cube)
            bounds = [(0, size), (0, size)]

            def generate_tiling():
                return tiling.generate_pattern(bounds, density=1.0)

            result = benchmark.pedantic(generate_tiling, iterations=10, rounds=3)
            times.append(benchmark.stats["mean"])

        # Check that time scales reasonably with area
        for i in range(1, len(times)):
            area_ratio = (sizes[i] / sizes[i - 1]) ** 2
            time_ratio = times[i] / times[i - 1]
            # Time should scale roughly with area, but allow for overhead
            assert (
                time_ratio < area_ratio * 5
            ), f"Time complexity too high: {time_ratio:.2f}x vs {area_ratio:.2f}x area"


@pytest.mark.performance
@pytest.mark.slow
class TestRegressionPerformance:
    """Test for performance regressions."""

    def test_baseline_sphere_performance(self):
        """Test baseline sphere performance to catch regressions."""
        # These benchmarks should be stable over time
        sphere = HyperSphere(10, 1.0)

        # Volume calculation should be fast
        start_time = time.time()
        for _ in range(10000):
            volume = sphere.get_volume()
        end_time = time.time()

        elapsed_time = end_time - start_time
        assert elapsed_time < 1.0, f"Volume calculation too slow: {elapsed_time:.3f}s"

        # Surface area calculation should be fast
        start_time = time.time()
        for _ in range(10000):
            surface_area = sphere.get_surface_area()
        end_time = time.time()

        elapsed_time = end_time - start_time
        assert (
            elapsed_time < 1.0
        ), f"Surface area calculation too slow: {elapsed_time:.3f}s"

    def test_baseline_tiling_performance(self):
        """Test baseline tiling performance to catch regressions."""
        cube = HyperCube(2, 1.0)
        tiling = RegularTiling(2, cube)
        bounds = [(0, 10), (0, 10)]

        # Tiling generation should be reasonably fast
        start_time = time.time()
        for _ in range(100):
            tiles = tiling.generate_pattern(bounds, density=1.0)
        end_time = time.time()

        elapsed_time = end_time - start_time
        assert elapsed_time < 5.0, f"Tiling generation too slow: {elapsed_time:.3f}s"

    def test_baseline_agent_performance(self):
        """Test baseline agent performance to catch regressions."""
        agent = GeometryAgent()

        # Agent queries should be reasonably fast
        start_time = time.time()
        for i in range(100):
            result = agent.process_query(f"create a 3D sphere radius {i % 5 + 1}")
        end_time = time.time()

        elapsed_time = end_time - start_time
        assert elapsed_time < 10.0, f"Agent queries too slow: {elapsed_time:.3f}s"


# Custom performance markers and utilities
def pytest_configure(config):
    """Configure performance test markers."""
    config.addinivalue_line("markers", "benchmark: mark test as a benchmark test")
    config.addinivalue_line("markers", "stress: mark test as a stress test")
    config.addinivalue_line("markers", "scalability: mark test as a scalability test")
    config.addinivalue_line("markers", "memory: mark test as a memory test")
    config.addinivalue_line("markers", "concurrency: mark test as a concurrency test")


# Performance test utilities
class PerformanceMonitor:
    """Utility class for monitoring performance during tests."""

    def __init__(self):
        self.start_time = None
        self.start_memory = None

    def start(self):
        """Start monitoring performance."""
        self.start_time = time.time()
        self.start_memory = self.get_memory_usage()

    def stop(self):
        """Stop monitoring and return metrics."""
        end_time = time.time()
        end_memory = self.get_memory_usage()

        return {
            "elapsed_time": end_time - self.start_time,
            "memory_delta": end_memory - self.start_memory,
            "peak_memory": end_memory,
        }

    def get_memory_usage(self):
        """Get current memory usage in MB."""
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024


@pytest.fixture
def performance_monitor():
    """Performance monitoring fixture."""
    return PerformanceMonitor()
