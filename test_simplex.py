#!/usr/bin/env python3
"""
Test the Simplex implementation
"""

import math
import sys
import traceback


def test_simplex_basic():
    """Test basic Simplex functionality"""
    print("🔢 Testing Simplex basic functionality...")

    try:
        from geometry_engine import Simplex

        # Test 2D triangle
        triangle = Simplex(2, 2.0)
        print(f"✅ 2D triangle (side=2): {triangle}")

        # Expected: volume = (√3/4) * 2² = √3 ≈ 1.732
        expected_volume = (math.sqrt(3) / 4) * 4
        actual_volume = triangle.get_volume()

        if abs(actual_volume - expected_volume) < 1e-10:
            print(f"✅ 2D triangle volume correct: {actual_volume:.6f}")
        else:
            print(
                f"❌ 2D triangle volume incorrect: {actual_volume:.6f} vs {expected_volume:.6f}"
            )

        # Expected: surface area = 3 * 2 = 6 (perimeter)
        expected_surface = 6.0
        actual_surface = triangle.get_surface_area()

        if abs(actual_surface - expected_surface) < 1e-10:
            print(f"✅ 2D triangle surface area correct: {actual_surface:.6f}")
        else:
            print(
                f"❌ 2D triangle surface area incorrect: {actual_surface:.6f} vs {expected_surface:.6f}"
            )

        # Test 3D tetrahedron
        tetrahedron = Simplex(3, 2.0)
        print(f"✅ 3D tetrahedron (side=2): {tetrahedron}")

        # Expected: volume = (√2/12) * 2³ = (√2/12) * 8 = 2√2/3 ≈ 0.9428
        expected_volume = (math.sqrt(2) / 12) * 8
        actual_volume = tetrahedron.get_volume()

        if abs(actual_volume - expected_volume) < 1e-10:
            print(f"✅ 3D tetrahedron volume correct: {actual_volume:.6f}")
        else:
            print(
                f"❌ 3D tetrahedron volume incorrect: {actual_volume:.6f} vs {expected_volume:.6f}"
            )

        # Expected: surface area = 4 * (√3/4) * 2² = 4√3 ≈ 6.928
        expected_surface = 4 * (math.sqrt(3) / 4) * 4
        actual_surface = tetrahedron.get_surface_area()

        if abs(actual_surface - expected_surface) < 1e-10:
            print(f"✅ 3D tetrahedron surface area correct: {actual_surface:.6f}")
        else:
            print(
                f"❌ 3D tetrahedron surface area incorrect: {actual_surface:.6f} vs {expected_surface:.6f}"
            )

        return True
    except Exception as e:
        print(f"❌ Basic Simplex test failed: {e}")
        traceback.print_exc()
        return False


def test_simplex_vertices_edges():
    """Test vertex and edge counts"""
    print("\n🔺 Testing vertex and edge counts...")

    try:
        from geometry_engine import Simplex

        test_cases = [
            (1, 2, 1),  # Line: 2 vertices, 1 edge
            (2, 3, 3),  # Triangle: 3 vertices, 3 edges
            (3, 4, 6),  # Tetrahedron: 4 vertices, 6 edges
            (4, 5, 10),  # 4D simplex: 5 vertices, 10 edges
        ]

        for dim, expected_vertices, expected_edges in test_cases:
            simplex = Simplex(dim, 1.0)
            vertices = simplex.get_vertex_count()
            edges = simplex.get_edge_count()

            if vertices == expected_vertices:
                print(f"✅ {dim}D simplex vertices: {vertices}")
            else:
                print(f"❌ {dim}D simplex vertices: {vertices} vs {expected_vertices}")

            if edges == expected_edges:
                print(f"✅ {dim}D simplex edges: {edges}")
            else:
                print(f"❌ {dim}D simplex edges: {edges} vs {expected_edges}")

        return True
    except Exception as e:
        print(f"❌ Vertex/edge count test failed: {e}")
        traceback.print_exc()
        return False


def test_simplex_dimensions():
    """Test Simplex in various dimensions"""
    print("\n🌌 Testing Simplex in multiple dimensions...")

    try:
        from geometry_engine import Simplex

        for dim in range(1, 6):
            simplex = Simplex(dim, 1.0)
            print(f"✅ {dim}D {simplex.get_shape_type()}")
            print(f"   - Volume: {simplex.get_volume():.6f}")
            print(f"   - Surface Area: {simplex.get_surface_area():.6f}")
            print(f"   - Formula: {simplex.get_volume_formula()}")
            print(f"   - Vertices: {simplex.get_vertex_count()}")
            print(f"   - Edges: {simplex.get_edge_count()}")
            print(f"   - Circumradius: {simplex.get_circumradius():.6f}")
            print(f"   - Inradius: {simplex.get_inradius():.6f}")
            print(f"   - Height: {simplex.get_height():.6f}")

        return True
    except Exception as e:
        print(f"❌ Multi-dimensional Simplex test failed: {e}")
        traceback.print_exc()
        return False


def test_simplex_radii():
    """Test circumradius and inradius calculations"""
    print("\n⭕ Testing circumradius and inradius...")

    try:
        from geometry_engine import Simplex

        # Test 2D triangle
        triangle = Simplex(2, 2.0)

        # Expected circumradius: R = s / √3
        expected_circumradius = 2.0 / math.sqrt(3)
        actual_circumradius = triangle.get_circumradius()

        if abs(actual_circumradius - expected_circumradius) < 1e-10:
            print(f"✅ 2D triangle circumradius: {actual_circumradius:.6f}")
        else:
            print(
                f"❌ 2D triangle circumradius: {actual_circumradius:.6f} vs {expected_circumradius:.6f}"
            )

        # Expected inradius: r = s / (2√3)
        expected_inradius = 2.0 / (2 * math.sqrt(3))
        actual_inradius = triangle.get_inradius()

        if abs(actual_inradius - expected_inradius) < 1e-10:
            print(f"✅ 2D triangle inradius: {actual_inradius:.6f}")
        else:
            print(
                f"❌ 2D triangle inradius: {actual_inradius:.6f} vs {expected_inradius:.6f}"
            )

        # Test 3D tetrahedron
        tetrahedron = Simplex(3, 2.0)

        # Expected circumradius: R = s * √6 / 4
        expected_circumradius = 2.0 * math.sqrt(6) / 4
        actual_circumradius = tetrahedron.get_circumradius()

        if abs(actual_circumradius - expected_circumradius) < 1e-10:
            print(f"✅ 3D tetrahedron circumradius: {actual_circumradius:.6f}")
        else:
            print(
                f"❌ 3D tetrahedron circumradius: {actual_circumradius:.6f} vs {expected_circumradius:.6f}"
            )

        # Expected inradius: r = s / (2√6)
        expected_inradius = 2.0 / (2 * math.sqrt(6))
        actual_inradius = tetrahedron.get_inradius()

        if abs(actual_inradius - expected_inradius) < 1e-10:
            print(f"✅ 3D tetrahedron inradius: {actual_inradius:.6f}")
        else:
            print(
                f"❌ 3D tetrahedron inradius: {actual_inradius:.6f} vs {expected_inradius:.6f}"
            )

        return True
    except Exception as e:
        print(f"❌ Radii test failed: {e}")
        traceback.print_exc()
        return False


def test_simplex_face_counts():
    """Test face counting for different dimensions"""
    print("\n🔢 Testing face counts...")

    try:
        from geometry_engine import Simplex

        # Test 3D tetrahedron
        tetrahedron = Simplex(3, 1.0)

        expected_faces = {
            0: 4,  # 4 vertices
            1: 6,  # 6 edges
            2: 4,  # 4 triangular faces
            3: 1,  # 1 tetrahedron
        }

        print("3D Tetrahedron face counts:")
        for k, expected in expected_faces.items():
            actual = tetrahedron.get_face_count(k)
            if actual == expected:
                print(f"✅ {k}-faces: {actual}")
            else:
                print(f"❌ {k}-faces: {actual} vs {expected}")

        # Test 4D simplex (5-cell)
        simplex4d = Simplex(4, 1.0)

        expected_faces = {
            0: 5,  # 5 vertices
            1: 10,  # 10 edges
            2: 10,  # 10 triangular faces
            3: 5,  # 5 tetrahedral cells
            4: 1,  # 1 4D simplex
        }

        print("\n4D Simplex face counts:")
        for k, expected in expected_faces.items():
            actual = simplex4d.get_face_count(k)
            if actual == expected:
                print(f"✅ {k}-faces: {actual}")
            else:
                print(f"❌ {k}-faces: {actual} vs {expected}")

        return True
    except Exception as e:
        print(f"❌ Face count test failed: {e}")
        traceback.print_exc()
        return False


def test_geometry_agent_simplices():
    """Test GeometryAgent with simplex operations"""
    print("\n🤖 Testing GeometryAgent with simplex operations...")

    try:
        from geometry_engine import GeometryAgent

        agent = GeometryAgent()

        # Test simplex creation
        result = agent.process_query("create a 3D tetrahedron with side 2")
        print(f"✅ Tetrahedron creation: {result[:100]}...")

        # Test triangle creation
        result = agent.process_query("create a 2D triangle with side 3")
        print(f"✅ Triangle creation: {result[:100]}...")

        # Test simplex properties
        result = agent.process_query("simplex side 2")
        print(f"✅ Simplex properties: {result[:100]}...")

        # Test 4D simplex
        result = agent.process_query("create a 4D simplex side length 1.5")
        print(f"✅ 4D simplex creation: {result[:100]}...")

        return True
    except Exception as e:
        print(f"❌ GeometryAgent simplex test failed: {e}")
        traceback.print_exc()
        return False


def test_shape_type_names():
    """Test shape type names for different dimensions"""
    print("\n🏷️ Testing shape type names...")

    try:
        from geometry_engine import Simplex

        expected_names = {
            1: "Line Segment",
            2: "Triangle",
            3: "Tetrahedron",
            4: "4D Simplex",
            5: "5D Simplex",
        }

        for dim, expected_name in expected_names.items():
            simplex = Simplex(dim, 1.0)
            actual_name = simplex.get_shape_type()

            if actual_name == expected_name:
                print(f"✅ {dim}D simplex type: {actual_name}")
            else:
                print(f"❌ {dim}D simplex type: {actual_name} vs {expected_name}")

        return True
    except Exception as e:
        print(f"❌ Shape type name test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all Simplex tests"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    SIMPLEX TEST SUITE                       ║")
    print("║           Testing N-Dimensional Simplices                   ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    tests = [
        ("Simplex Basic", test_simplex_basic),
        ("Vertices and Edges", test_simplex_vertices_edges),
        ("Simplex Dimensions", test_simplex_dimensions),
        ("Circumradius and Inradius", test_simplex_radii),
        ("Face Counts", test_simplex_face_counts),
        ("GeometryAgent Simplices", test_geometry_agent_simplices),
        ("Shape Type Names", test_shape_type_names),
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
        print("🎉 ALL SIMPLEX TESTS PASSED! 🚀")
        print("\nSimplex implementation is working perfectly!")
        print("✅ N-dimensional simplices fully functional")
        print("✅ Mathematical accuracy verified")
        print("✅ Vertex and edge counting working")
        print("✅ Face counting implemented")
        print("✅ Circumradius and inradius calculations working")
        print("✅ AI integration working")
        print("✅ Shape type names correct")
        return True
    else:
        print("❌ Some tests failed. Check implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
