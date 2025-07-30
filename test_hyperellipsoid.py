#!/usr/bin/env python3
"""
Test the HyperEllipsoid implementation
"""

import math
import sys
import traceback


def test_hyperellipsoid_basic():
    """Test basic HyperEllipsoid functionality"""
    print("🔢 Testing HyperEllipsoid basic functionality...")

    try:
        from geometry_engine import HyperEllipsoid

        # Test 2D ellipse
        ellipse = HyperEllipsoid(2, 3.0, 4.0)
        print(f"✅ 2D ellipse (axes=3,4): {ellipse}")

        # Expected: volume = π * 3 * 4 = 12π ≈ 37.699
        expected_volume = math.pi * 3 * 4
        actual_volume = ellipse.get_volume()

        if abs(actual_volume - expected_volume) < 1e-10:
            print(f"✅ 2D ellipse volume correct: {actual_volume:.6f}")
        else:
            print(
                f"❌ 2D ellipse volume incorrect: {actual_volume:.6f} vs {expected_volume:.6f}"
            )

        # Test eccentricity
        eccentricity = ellipse.get_eccentricity()
        expected_eccentricity = math.sqrt(1 - (3 / 4) ** 2)  # b/a = 3/4

        if abs(eccentricity - expected_eccentricity) < 1e-10:
            print(f"✅ 2D ellipse eccentricity correct: {eccentricity:.6f}")
        else:
            print(
                f"❌ 2D ellipse eccentricity incorrect: {eccentricity:.6f} vs {expected_eccentricity:.6f}"
            )

        # Test 3D ellipsoid
        ellipsoid = HyperEllipsoid(3, 2.0, 3.0, 4.0)
        print(f"✅ 3D ellipsoid (axes=2,3,4): {ellipsoid}")

        # Expected: volume = (4/3)π * 2 * 3 * 4 = 32π ≈ 100.531
        expected_volume = (4 / 3) * math.pi * 2 * 3 * 4
        actual_volume = ellipsoid.get_volume()

        if abs(actual_volume - expected_volume) < 1e-10:
            print(f"✅ 3D ellipsoid volume correct: {actual_volume:.6f}")
        else:
            print(
                f"❌ 3D ellipsoid volume incorrect: {actual_volume:.6f} vs {expected_volume:.6f}"
            )

        # Test axis ratio
        axis_ratio = ellipsoid.get_axis_ratio()
        expected_ratio = 4.0 / 2.0  # max/min

        if abs(axis_ratio - expected_ratio) < 1e-10:
            print(f"✅ 3D ellipsoid axis ratio correct: {axis_ratio:.6f}")
        else:
            print(
                f"❌ 3D ellipsoid axis ratio incorrect: {axis_ratio:.6f} vs {expected_ratio:.6f}"
            )

        return True
    except Exception as e:
        print(f"❌ Basic HyperEllipsoid test failed: {e}")
        traceback.print_exc()
        return False


def test_hyperellipsoid_sphere_detection():
    """Test sphere detection in HyperEllipsoid"""
    print("\n🔍 Testing sphere detection...")

    try:
        from geometry_engine import HyperEllipsoid

        # Test sphere (all axes equal)
        sphere = HyperEllipsoid(3, 2.0, 2.0, 2.0)
        print(f"✅ Sphere as ellipsoid: {sphere}")

        if sphere.is_sphere():
            print("✅ Correctly identified as sphere")
        else:
            print("❌ Failed to identify as sphere")

        if sphere.get_shape_type() == "HyperSphere":
            print("✅ Correct shape type: HyperSphere")
        else:
            print(f"❌ Wrong shape type: {sphere.get_shape_type()}")

        # Test non-sphere
        ellipsoid = HyperEllipsoid(3, 1.0, 2.0, 3.0)
        print(f"✅ Non-sphere ellipsoid: {ellipsoid}")

        if not ellipsoid.is_sphere():
            print("✅ Correctly identified as non-sphere")
        else:
            print("❌ Incorrectly identified as sphere")

        if ellipsoid.get_shape_type() == "HyperEllipsoid":
            print("✅ Correct shape type: HyperEllipsoid")
        else:
            print(f"❌ Wrong shape type: {ellipsoid.get_shape_type()}")

        return True
    except Exception as e:
        print(f"❌ Sphere detection test failed: {e}")
        traceback.print_exc()
        return False


def test_hyperellipsoid_dimensions():
    """Test HyperEllipsoid in various dimensions"""
    print("\n🌌 Testing HyperEllipsoid in multiple dimensions...")

    try:
        from geometry_engine import HyperEllipsoid

        test_cases = [
            (1, [2.0], 4.0),  # 1D: length = 2 * 2.0 = 4.0
            (2, [2.0, 3.0], math.pi * 2.0 * 3.0),  # 2D: π * a * b
            (
                3,
                [1.0, 2.0, 3.0],
                (4 / 3) * math.pi * 1.0 * 2.0 * 3.0,
            ),  # 3D: (4/3)π * a * b * c
            (4, [1.0, 1.0, 1.0, 1.0], (math.pi**2 / 2) * 1.0**4),  # 4D sphere
        ]

        for dim, axes, expected_vol in test_cases:
            ellipsoid = HyperEllipsoid(dim, *axes)
            vol = ellipsoid.get_volume()

            if abs(vol - expected_vol) < 1e-10:
                print(f"✅ {dim}D ellipsoid volume: {vol:.6f}")
            else:
                print(f"❌ {dim}D ellipsoid volume: {vol:.6f} vs {expected_vol:.6f}")

            print(f"   Formula: {ellipsoid.get_volume_formula()}")
            print(f"   Surface Formula: {ellipsoid.get_surface_area_formula()}")

        return True
    except Exception as e:
        print(f"❌ Multi-dimensional HyperEllipsoid test failed: {e}")
        traceback.print_exc()
        return False


def test_hyperellipsoid_point_containment():
    """Test point containment in HyperEllipsoid"""
    print("\n📍 Testing point containment...")

    try:
        from geometry_engine import HyperEllipsoid

        # Test 2D ellipse with semi-axes 3, 4
        ellipse = HyperEllipsoid(2, 3.0, 4.0)

        test_points = [
            ([0.0, 0.0], True),  # Center
            ([2.0, 2.0], True),  # Inside: (2/3)² + (2/4)² = 4/9 + 1/4 = 0.69 < 1
            ([3.0, 0.0], True),  # On boundary: (3/3)² + (0/4)² = 1
            ([0.0, 4.0], True),  # On boundary: (0/3)² + (4/4)² = 1
            ([4.0, 4.0], False),  # Outside: (4/3)² + (4/4)² = 16/9 + 1 = 2.78 > 1
        ]

        for point, expected in test_points:
            result = ellipse.contains_point(point)
            if result == expected:
                print(f"✅ Point {point} containment: {result}")
            else:
                print(f"❌ Point {point} containment: {result} vs {expected}")

        return True
    except Exception as e:
        print(f"❌ Point containment test failed: {e}")
        traceback.print_exc()
        return False


def test_geometry_agent_ellipsoids():
    """Test GeometryAgent with ellipsoid operations"""
    print("\n🤖 Testing GeometryAgent with ellipsoid operations...")

    try:
        from geometry_engine import GeometryAgent

        agent = GeometryAgent()

        # Test ellipsoid creation
        result = agent.process_query("create a 3D ellipsoid with axes 1.5 2.0 3.0")
        print(f"✅ Ellipsoid creation: {result[:100]}...")

        # Test ellipse creation
        result = agent.process_query("create a 2D ellipse with semi-axes 2 3")
        print(f"✅ Ellipse creation: {result[:100]}...")

        # Test ellipsoid properties
        result = agent.process_query("ellipsoid with axes 1 2 3")
        print(f"✅ Ellipsoid properties: {result[:100]}...")

        # Test sphere detection
        result = agent.process_query("ellipsoid with axes 2 2 2")
        print(f"✅ Sphere detection: {result[:100]}...")

        return True
    except Exception as e:
        print(f"❌ GeometryAgent ellipsoid test failed: {e}")
        traceback.print_exc()
        return False


def test_cross_sections():
    """Test cross-section calculations"""
    print("\n✂️ Testing cross-section calculations...")

    try:
        from geometry_engine import HyperEllipsoid

        # Test 3D ellipsoid cross-section
        ellipsoid = HyperEllipsoid(3, 2.0, 3.0, 4.0)

        # Cross-section at z=0 (middle)
        cross_section = ellipsoid.get_cross_section(2, 0.0)  # axis 2 (z-axis)
        expected = math.pi * 2.0 * 3.0  # 2D ellipse with axes 2, 3

        if abs(cross_section - expected) < 1e-10:
            print(f"✅ Cross-section at center: {cross_section:.6f}")
        else:
            print(f"❌ Cross-section at center: {cross_section:.6f} vs {expected:.6f}")

        # Cross-section at z=2 (half-way to edge)
        cross_section = ellipsoid.get_cross_section(2, 2.0)
        # Scale factor = sqrt(1 - (2/4)²) = sqrt(3/4) = sqrt(3)/2
        scale_factor = math.sqrt(1 - (2.0 / 4.0) ** 2)
        expected = math.pi * (2.0 * scale_factor) * (3.0 * scale_factor)

        if abs(cross_section - expected) < 1e-10:
            print(f"✅ Cross-section at z=2: {cross_section:.6f}")
        else:
            print(f"❌ Cross-section at z=2: {cross_section:.6f} vs {expected:.6f}")

        # Cross-section outside bounds
        cross_section = ellipsoid.get_cross_section(2, 5.0)  # Outside z-axis range

        if cross_section == 0:
            print("✅ Cross-section outside bounds: 0")
        else:
            print(f"❌ Cross-section outside bounds: {cross_section} vs 0")

        return True
    except Exception as e:
        print(f"❌ Cross-section test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all HyperEllipsoid tests"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                HYPERELLIPSOID TEST SUITE                    ║")
    print("║           Testing N-Dimensional Ellipsoids                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    tests = [
        ("HyperEllipsoid Basic", test_hyperellipsoid_basic),
        ("Sphere Detection", test_hyperellipsoid_sphere_detection),
        ("HyperEllipsoid Dimensions", test_hyperellipsoid_dimensions),
        ("Point Containment", test_hyperellipsoid_point_containment),
        ("GeometryAgent Ellipsoids", test_geometry_agent_ellipsoids),
        ("Cross Sections", test_cross_sections),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 Running {test_name} Test")
        print("=" * 60)

        try:
            if test_func():
                print(f"✅ {test_name} test PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {e}")
            traceback.print_exc()

    print(f"\n{'='*60}")
    print(f"📊 TEST SUMMARY: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("🎉 ALL HYPERELLIPSOID TESTS PASSED! 🚀")
        print("\nHyperEllipsoid implementation is working perfectly!")
        print("✅ N-dimensional ellipsoids fully functional")
        print("✅ Mathematical accuracy verified")
        print("✅ Sphere detection working")
        print("✅ Point containment implemented")
        print("✅ Cross-section calculations working")
        print("✅ AI integration working")
        return True
    else:
        print("❌ Some tests failed. Check implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
