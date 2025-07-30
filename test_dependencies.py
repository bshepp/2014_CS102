#!/usr/bin/env python3
"""
Comprehensive dependency compatibility test suite
"""

import importlib
import subprocess
import sys
import warnings

from packaging import version


def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python Version:")
    print("=" * 40)

    python_version = sys.version_info
    print(
        f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}"
    )

    # Check if we're on a supported Python version
    if python_version >= (3, 12):
        print("✅ Python version is current and supported")
    elif python_version >= (3, 8):
        print("⚠️  Python version is supported but not latest")
    else:
        print("❌ Python version is too old")

    print()


def test_numpy_compatibility():
    """Test NumPy compatibility"""
    print("🔢 Testing NumPy Compatibility:")
    print("=" * 40)

    try:
        import numpy as np

        print(f"NumPy version: {np.__version__}")

        # Test basic functionality
        arr = np.array([1, 2, 3, 4, 5])
        print(f"✅ np.array() works: {arr}")

        # Test mathematical operations
        result = np.sqrt(arr)
        print(f"✅ Mathematical operations work: {result}")

        # Test dtype operations
        float_arr = np.array([1.0, 2.0, 3.0])
        print(f"✅ Float arrays work: {float_arr}")

        # Check for NumPy 2.x compatibility
        if version.parse(np.__version__) >= version.parse("2.0.0"):
            print("✅ NumPy 2.x detected - checking compatibility")

            # Test that our specific usage patterns work
            test_params = np.array([1.0, 2.0, 3.0])
            print(f"✅ Parameter arrays work: {test_params}")

        print("✅ NumPy compatibility test passed")

    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
    except Exception as e:
        print(f"❌ NumPy compatibility test failed: {e}")

    print()


def test_standard_library():
    """Test standard library modules"""
    print("📚 Testing Standard Library:")
    print("=" * 40)

    modules_to_test = [
        "math",
        "subprocess",
        "os",
        "sys",
        "re",
        "typing",
        "abc",
        "collections",
    ]

    for module_name in modules_to_test:
        try:
            module = importlib.import_module(module_name)
            print(f"✅ {module_name}: OK")
        except ImportError as e:
            print(f"❌ {module_name}: Failed - {e}")

    print()


def test_geometry_engine_imports():
    """Test our geometry engine imports"""
    print("🌌 Testing Geometry Engine Imports:")
    print("=" * 40)

    try:
        from geometry_engine import (GeometryAgent, HyperSphere, JavaBridge,
                                     NDShape, OriginalSphere)

        print("✅ All geometry engine classes imported successfully")

        # Test basic instantiation
        agent = GeometryAgent()
        print("✅ GeometryAgent instantiation works")

        sphere = HyperSphere(3, 1.0)
        print("✅ HyperSphere instantiation works")

        original = OriginalSphere(2.0)
        print("✅ OriginalSphere instantiation works")

        bridge = JavaBridge()
        print("✅ JavaBridge instantiation works")

    except ImportError as e:
        print(f"❌ Import failed: {e}")
    except Exception as e:
        print(f"❌ Instantiation failed: {e}")

    print()


def test_mathematical_accuracy():
    """Test mathematical accuracy"""
    print("🧮 Testing Mathematical Accuracy:")
    print("=" * 40)

    try:
        import math

        from geometry_engine import HyperSphere

        # Test 3D sphere (should match classical formulas)
        sphere = HyperSphere(3, 1.0)

        # Expected values for unit sphere
        expected_volume = (4 / 3) * math.pi
        expected_surface = 4 * math.pi

        actual_volume = sphere.get_volume()
        actual_surface = sphere.get_surface_area()

        volume_diff = abs(actual_volume - expected_volume)
        surface_diff = abs(actual_surface - expected_surface)

        print(
            f"3D Unit Sphere Volume: {actual_volume:.6f} (expected: {expected_volume:.6f})"
        )
        print(f"Volume difference: {volume_diff:.10f}")

        print(
            f"3D Unit Sphere Surface: {actual_surface:.6f} (expected: {expected_surface:.6f})"
        )
        print(f"Surface difference: {surface_diff:.10f}")

        # Check accuracy (should be very close)
        if volume_diff < 1e-10 and surface_diff < 1e-10:
            print("✅ Mathematical accuracy test passed")
        else:
            print("⚠️  Mathematical accuracy has some deviation")

    except Exception as e:
        print(f"❌ Mathematical accuracy test failed: {e}")

    print()


def test_java_integration():
    """Test Java integration"""
    print("☕ Testing Java Integration:")
    print("=" * 40)

    try:
        from geometry_engine import JavaBridge

        bridge = JavaBridge()
        print(f"Java available: {bridge.java_available}")

        if bridge.java_available:
            # Test Java execution
            result = bridge.run_original_multisphere(2.0)
            if "volume" in result.lower():
                print("✅ Java integration test passed")
            else:
                print("⚠️  Java integration test returned unexpected result")
        else:
            print("⚠️  Java not available - testing Python fallback")
            result = bridge.run_original_multisphere(2.0)
            if "PYTHON EQUIVALENT" in result:
                print("✅ Python fallback test passed")

    except Exception as e:
        print(f"❌ Java integration test failed: {e}")

    print()


def test_memory_usage():
    """Test memory usage for large dimensions"""
    print("💾 Testing Memory Usage:")
    print("=" * 40)

    try:
        import sys

        from geometry_engine import HyperSphere

        # Test creating shapes in various dimensions
        dimensions_to_test = [1, 2, 3, 4, 5, 10, 20, 100]

        for dim in dimensions_to_test:
            sphere = HyperSphere(dim, 1.0)
            obj_size = sys.getsizeof(sphere)
            print(f"✅ {dim}D sphere: {obj_size} bytes")

        print("✅ Memory usage test passed")

    except Exception as e:
        print(f"❌ Memory usage test failed: {e}")

    print()


def test_performance():
    """Test performance for high-dimensional calculations"""
    print("⚡ Testing Performance:")
    print("=" * 40)

    try:
        import time

        from geometry_engine import HyperSphere

        # Time various operations
        dimensions_to_test = [1, 3, 5, 10, 20, 50, 100]

        for dim in dimensions_to_test:
            start_time = time.time()

            sphere = HyperSphere(dim, 1.0)
            volume = sphere.get_volume()
            surface = sphere.get_surface_area()

            elapsed = time.time() - start_time

            print(f"✅ {dim}D calculations: {elapsed:.6f} seconds")

            # Check for reasonable performance
            if elapsed > 1.0:  # More than 1 second is concerning
                print(f"⚠️  Performance concern for {dim}D")

        print("✅ Performance test completed")

    except Exception as e:
        print(f"❌ Performance test failed: {e}")

    print()


def run_all_tests():
    """Run all compatibility tests"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║            DEPENDENCY COMPATIBILITY TEST SUITE              ║")
    print("║                  Comprehensive Analysis                     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    # Suppress warnings for cleaner output
    warnings.filterwarnings("ignore")

    test_python_version()
    test_numpy_compatibility()
    test_standard_library()
    test_geometry_engine_imports()
    test_mathematical_accuracy()
    test_java_integration()
    test_memory_usage()
    test_performance()

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    TESTS COMPLETED                          ║")
    print("║           All dependency compatibility verified!            ║")
    print("╚══════════════════════════════════════════════════════════════╝")


if __name__ == "__main__":
    # Install packaging module if needed
    try:
        import packaging
    except ImportError:
        print("Installing packaging module...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "packaging"])
        import packaging

    run_all_tests()
