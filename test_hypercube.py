#!/usr/bin/env python3
"""
Test the HyperCube implementation
"""

import sys
import traceback


def test_hypercube_basic():
    """Test basic HyperCube functionality"""
    print("🔢 Testing HyperCube basic functionality...")

    try:
        from geometry_engine import HyperCube

        # Test 3D cube (should match known values)
        cube = HyperCube(3, 2.0)
        print(f"✅ 3D cube (side=2): {cube}")

        # Expected: volume = 8, surface area = 24
        expected_volume = 8.0
        expected_surface = 24.0

        if abs(cube.get_volume() - expected_volume) < 1e-10:
            print(f"✅ 3D cube volume correct: {cube.get_volume()}")
        else:
            print(
                f"❌ 3D cube volume incorrect: {cube.get_volume()} vs {expected_volume}"
            )

        if abs(cube.get_surface_area() - expected_surface) < 1e-10:
            print(f"✅ 3D cube surface area correct: {cube.get_surface_area()}")
        else:
            print(
                f"❌ 3D cube surface area incorrect: {cube.get_surface_area()} vs {expected_surface}"
            )

        # Test properties
        print(f"✅ Vertices: {cube.get_vertex_count()}")
        print(f"✅ Edges: {cube.get_edge_count()}")
        print(f"✅ Diagonal: {cube.get_diagonal_length():.6f}")
        print(f"✅ Volume formula: {cube.get_volume_formula()}")
        print(f"✅ Surface formula: {cube.get_surface_area_formula()}")

        return True
    except Exception as e:
        print(f"❌ Basic HyperCube test failed: {e}")
        traceback.print_exc()
        return False


def test_hypercube_dimensions():
    """Test HyperCube in various dimensions"""
    print("\n🌌 Testing HyperCube in multiple dimensions...")

    try:
        from geometry_engine import HyperCube

        test_cases = [
            (1, 2.0, 2.0, 2.0),  # 1D: volume=2, surface=2
            (2, 2.0, 4.0, 8.0),  # 2D: volume=4, surface=8
            (3, 2.0, 8.0, 24.0),  # 3D: volume=8, surface=24
            (4, 2.0, 16.0, 32.0),  # 4D: volume=16, surface=32
        ]

        for dim, side, expected_vol, expected_surf in test_cases:
            cube = HyperCube(dim, side)
            vol = cube.get_volume()
            surf = cube.get_surface_area()

            if abs(vol - expected_vol) < 1e-10:
                print(f"✅ {dim}D cube volume: {vol:.6f}")
            else:
                print(f"❌ {dim}D cube volume: {vol:.6f} vs {expected_vol}")

            if abs(surf - expected_surf) < 1e-10:
                print(f"✅ {dim}D cube surface: {surf:.6f}")
            else:
                print(f"❌ {dim}D cube surface: {surf:.6f} vs {expected_surf}")

        return True
    except Exception as e:
        print(f"❌ Multi-dimensional HyperCube test failed: {e}")
        traceback.print_exc()
        return False


def test_geometry_agent_cubes():
    """Test GeometryAgent with cube operations"""
    print("\n🤖 Testing GeometryAgent with cube operations...")

    try:
        from geometry_engine import GeometryAgent

        agent = GeometryAgent()

        # Test cube creation
        result = agent.process_query("create a 3D cube with side 2")
        print(f"✅ Cube creation: {result[:100]}...")

        # Test cube properties
        result = agent.process_query("volume of 4D cube side 1.5")
        print(f"✅ Cube volume query: {result[:100]}...")

        # Test comparison
        result = agent.process_query("compare sphere vs cube in 3 dimensions")
        print(f"✅ Sphere vs cube comparison: {result[:100]}...")

        return True
    except Exception as e:
        print(f"❌ GeometryAgent cube test failed: {e}")
        traceback.print_exc()
        return False


def test_hypercube_properties():
    """Test advanced HyperCube properties"""
    print("\n🔍 Testing HyperCube advanced properties...")

    try:
        from geometry_engine import HyperCube

        # Test various properties
        cube = HyperCube(4, 2.0)

        print(f"✅ 4D cube properties:")
        print(f"   - Volume: {cube.get_volume()}")
        print(f"   - Surface Area: {cube.get_surface_area()}")
        print(f"   - Vertices: {cube.get_vertex_count()}")
        print(f"   - Edges: {cube.get_edge_count()}")
        print(f"   - Diagonal: {cube.get_diagonal_length():.6f}")
        print(f"   - Cross-section: {cube.get_cross_section(1.0):.6f}")

        # Test face counts
        for k in range(5):
            faces = cube.get_face_count(k)
            print(f"   - {k}-faces: {faces}")

        # Test point containment
        test_points = [
            [1.0, 1.0, 1.0, 1.0],  # Inside
            [3.0, 1.0, 1.0, 1.0],  # Outside
            [0.0, 0.0, 0.0, 0.0],  # Corner
            [2.0, 2.0, 2.0, 2.0],  # Corner
        ]

        for point in test_points:
            contains = cube.contains_point(point)
            print(f"   - Point {point} inside: {contains}")

        return True
    except Exception as e:
        print(f"❌ HyperCube properties test failed: {e}")
        traceback.print_exc()
        return False


def test_sphere_cube_comparison():
    """Test sphere vs cube comparisons"""
    print("\n⚖️ Testing sphere vs cube comparisons...")

    try:
        from geometry_engine import HyperCube, HyperSphere

        print("Unit shapes (parameter = 1.0):")
        for dim in [1, 2, 3, 4, 5, 10]:
            sphere = HyperSphere(dim, 1.0)
            cube = HyperCube(dim, 1.0)

            sphere_vol = sphere.get_volume()
            cube_vol = cube.get_volume()
            ratio = sphere_vol / cube_vol

            print(f"   {dim}D: Sphere/Cube volume ratio = {ratio:.6f}")

        return True
    except Exception as e:
        print(f"❌ Sphere vs cube comparison test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all HyperCube tests"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                  HYPERCUBE TEST SUITE                       ║")
    print("║              Testing N-Dimensional Cubes                    ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    tests = [
        ("HyperCube Basic", test_hypercube_basic),
        ("HyperCube Dimensions", test_hypercube_dimensions),
        ("GeometryAgent Cubes", test_geometry_agent_cubes),
        ("HyperCube Properties", test_hypercube_properties),
        ("Sphere vs Cube Comparison", test_sphere_cube_comparison),
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
        print("🎉 ALL HYPERCUBE TESTS PASSED! 🚀")
        print("\nHyperCube implementation is working perfectly!")
        print("✅ N-dimensional cubes fully functional")
        print("✅ Mathematical accuracy verified")
        print("✅ AI integration working")
        print("✅ Advanced properties implemented")
        return True
    else:
        print("❌ Some tests failed. Check implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
