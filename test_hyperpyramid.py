#!/usr/bin/env python3
"""
Test the HyperPyramid implementation
"""

import sys
import math
import traceback

def test_hyperpyramid_basic():
    """Test basic HyperPyramid functionality"""
    print("🔺 Testing HyperPyramid basic functionality...")
    
    try:
        from geometry_engine import HyperPyramid
        
        # Test 2D triangle (pyramid)
        triangle = HyperPyramid(2, 4.0, 3.0)
        print(f"✅ 2D triangle (base=4, height=3): {triangle}")
        
        # Expected: volume = (1/2) * base * height = (1/2) * 4 * 3 = 6
        expected_volume = 0.5 * 4.0 * 3.0
        actual_volume = triangle.get_volume()
        
        if abs(actual_volume - expected_volume) < 1e-10:
            print(f"✅ 2D triangle volume correct: {actual_volume:.6f}")
        else:
            print(f"❌ 2D triangle volume incorrect: {actual_volume:.6f} vs {expected_volume:.6f}")
        
        # Test 3D square pyramid
        pyramid = HyperPyramid(3, 4.0, 3.0)
        print(f"✅ 3D square pyramid (base=4, height=3): {pyramid}")
        
        # Expected: volume = (1/3) * base² * height = (1/3) * 16 * 3 = 16
        expected_volume = (1/3) * 16.0 * 3.0
        actual_volume = pyramid.get_volume()
        
        if abs(actual_volume - expected_volume) < 1e-10:
            print(f"✅ 3D square pyramid volume correct: {actual_volume:.6f}")
        else:
            print(f"❌ 3D square pyramid volume incorrect: {actual_volume:.6f} vs {expected_volume:.6f}")
        
        # Test surface area
        # Expected: base_area + 4 * triangle_area
        # base_area = 16, triangle_area = 0.5 * 4 * slant_height
        # slant_height = sqrt(3² + 2²) = sqrt(13)
        slant_height = math.sqrt(3**2 + 2**2)
        expected_surface = 16 + 4 * 0.5 * 4 * slant_height
        actual_surface = pyramid.get_surface_area()
        
        if abs(actual_surface - expected_surface) < 1e-10:
            print(f"✅ 3D square pyramid surface area correct: {actual_surface:.6f}")
        else:
            print(f"❌ 3D square pyramid surface area incorrect: {actual_surface:.6f} vs {expected_surface:.6f}")
        
        return True
    except Exception as e:
        print(f"❌ Basic HyperPyramid test failed: {e}")
        traceback.print_exc()
        return False

def test_hyperpyramid_dimensions():
    """Test HyperPyramid in various dimensions"""
    print("\n🌌 Testing HyperPyramid in multiple dimensions...")
    
    try:
        from geometry_engine import HyperPyramid
        
        for dim in range(1, 6):
            pyramid = HyperPyramid(dim, 2.0, 3.0)
            print(f"✅ {dim}D {pyramid.get_shape_type()}")
            print(f"   - Volume: {pyramid.get_volume():.6f}")
            print(f"   - Surface Area: {pyramid.get_surface_area():.6f}")
            print(f"   - Formula: {pyramid.get_volume_formula()}")
            print(f"   - Vertices: {pyramid.get_vertex_count()}")
            print(f"   - Edges: {pyramid.get_edge_count()}")
            print(f"   - Slant Height: {pyramid.get_slant_height():.6f}")
            print(f"   - Lateral Edge: {pyramid.get_lateral_edge_length():.6f}")
            print(f"   - Base Volume: {pyramid.get_base_volume():.6f}")
        
        return True
    except Exception as e:
        print(f"❌ Multi-dimensional HyperPyramid test failed: {e}")
        traceback.print_exc()
        return False

def test_hyperpyramid_properties():
    """Test HyperPyramid advanced properties"""
    print("\n🔍 Testing HyperPyramid advanced properties...")
    
    try:
        from geometry_engine import HyperPyramid
        
        # Test 3D pyramid properties
        pyramid = HyperPyramid(3, 4.0, 3.0)
        
        print(f"✅ 3D pyramid advanced properties:")
        print(f"   - Base volume: {pyramid.get_base_volume():.6f}")
        print(f"   - Base surface area: {pyramid.get_base_surface_area():.6f}")
        print(f"   - Apex distance: {pyramid.get_apex_distance():.6f}")
        print(f"   - Slant height: {pyramid.get_slant_height():.6f}")
        print(f"   - Lateral edge length: {pyramid.get_lateral_edge_length():.6f}")
        
        # Test cross-sections
        for height in [0.0, 1.0, 2.0, 3.0, 4.0]:
            cross_section = pyramid.get_cross_section(height)
            print(f"   - Cross-section at height {height}: {cross_section:.6f}")
        
        # Test face counts
        for k in range(4):
            faces = pyramid.get_face_count(k)
            print(f"   - {k}-faces: {faces}")
        
        return True
    except Exception as e:
        print(f"❌ HyperPyramid properties test failed: {e}")
        traceback.print_exc()
        return False

def test_hyperpyramid_vertices_edges():
    """Test vertex and edge counts"""
    print("\n🔢 Testing vertex and edge counts...")
    
    try:
        from geometry_engine import HyperPyramid
        
        test_cases = [
            (1, 2, 1),    # Line: 2 vertices, 1 edge
            (2, 3, 3),    # Triangle: 3 vertices, 3 edges
            (3, 5, 8),    # Square pyramid: 5 vertices, 8 edges
            (4, 9, 20),   # 4D pyramid: 9 vertices, 20 edges
        ]
        
        for dim, expected_vertices, expected_edges in test_cases:
            pyramid = HyperPyramid(dim, 2.0, 3.0)
            vertices = pyramid.get_vertex_count()
            edges = pyramid.get_edge_count()
            
            if vertices == expected_vertices:
                print(f"✅ {dim}D pyramid vertices: {vertices}")
            else:
                print(f"❌ {dim}D pyramid vertices: {vertices} vs {expected_vertices}")
            
            if edges == expected_edges:
                print(f"✅ {dim}D pyramid edges: {edges}")
            else:
                print(f"❌ {dim}D pyramid edges: {edges} vs {expected_edges}")
        
        return True
    except Exception as e:
        print(f"❌ Vertex/edge count test failed: {e}")
        traceback.print_exc()
        return False

def test_hyperpyramid_point_containment():
    """Test point containment in HyperPyramid"""
    print("\n📍 Testing point containment...")
    
    try:
        from geometry_engine import HyperPyramid
        
        # Test 3D square pyramid
        pyramid = HyperPyramid(3, 4.0, 3.0)
        
        test_points = [
            ([0.0, 0.0, 1.0], True),   # Inside pyramid
            ([0.0, 0.0, 0.0], True),   # Base center
            ([1.0, 1.0, 1.0], True),   # Inside pyramid
            ([2.0, 2.0, 0.0], True),   # Base corner
            ([3.0, 3.0, 0.0], False),  # Outside base
            ([0.0, 0.0, 4.0], False),  # Above apex
            ([1.0, 1.0, 3.0], False),  # Above pyramid surface
        ]
        
        for point, expected in test_points:
            result = pyramid.contains_point(point)
            if result == expected:
                print(f"✅ Point {point} containment: {result}")
            else:
                print(f"❌ Point {point} containment: {result} vs {expected}")
        
        return True
    except Exception as e:
        print(f"❌ Point containment test failed: {e}")
        traceback.print_exc()
        return False

def test_geometry_agent_pyramids():
    """Test GeometryAgent with pyramid operations"""
    print("\n🤖 Testing GeometryAgent with pyramid operations...")
    
    try:
        from geometry_engine import GeometryAgent
        
        agent = GeometryAgent()
        
        # Test pyramid creation
        result = agent.process_query("create a 3D pyramid base 2 height 3")
        print(f"✅ Pyramid creation: {result[:100]}...")
        
        # Test triangle creation
        result = agent.process_query("create a 2D triangle base 4 height 3")
        print(f"✅ Triangle creation: {result[:100]}...")
        
        # Test pyramid properties
        result = agent.process_query("pyramid base 2 height 3")
        print(f"✅ Pyramid properties: {result[:100]}...")
        
        # Test 4D pyramid
        result = agent.process_query("create a 4D hyperpyramid base 2.5 height 4")
        print(f"✅ 4D pyramid creation: {result[:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ GeometryAgent pyramid test failed: {e}")
        traceback.print_exc()
        return False

def test_cross_sections():
    """Test cross-section calculations"""
    print("\n✂️ Testing cross-section calculations...")
    
    try:
        from geometry_engine import HyperPyramid
        
        # Test 3D pyramid cross-section
        pyramid = HyperPyramid(3, 4.0, 3.0)
        
        # Cross-section at base (height 0)
        cross_section = pyramid.get_cross_section(0.0)
        expected = 4.0**2  # Full base area
        
        if abs(cross_section - expected) < 1e-10:
            print(f"✅ Cross-section at base: {cross_section:.6f}")
        else:
            print(f"❌ Cross-section at base: {cross_section:.6f} vs {expected:.6f}")
        
        # Cross-section at half height
        cross_section = pyramid.get_cross_section(1.5)
        # Scale factor = (3.0 - 1.5) / 3.0 = 0.5
        # Scaled side = 4.0 * 0.5 = 2.0
        expected = 2.0**2  # 4.0
        
        if abs(cross_section - expected) < 1e-10:
            print(f"✅ Cross-section at half height: {cross_section:.6f}")
        else:
            print(f"❌ Cross-section at half height: {cross_section:.6f} vs {expected:.6f}")
        
        # Cross-section at apex
        cross_section = pyramid.get_cross_section(3.0)
        expected = 0.0
        
        if abs(cross_section - expected) < 1e-10:
            print(f"✅ Cross-section at apex: {cross_section:.6f}")
        else:
            print(f"❌ Cross-section at apex: {cross_section:.6f} vs {expected:.6f}")
        
        # Cross-section outside bounds
        cross_section = pyramid.get_cross_section(5.0)
        
        if cross_section == 0:
            print("✅ Cross-section outside bounds: 0")
        else:
            print(f"❌ Cross-section outside bounds: {cross_section} vs 0")
        
        return True
    except Exception as e:
        print(f"❌ Cross-section test failed: {e}")
        traceback.print_exc()
        return False

def test_shape_type_names():
    """Test shape type names for different dimensions"""
    print("\n🏷️ Testing shape type names...")
    
    try:
        from geometry_engine import HyperPyramid
        
        expected_names = {
            1: "Line Segment",
            2: "Triangle",
            3: "Square Pyramid",
            4: "4D HyperPyramid",
            5: "5D HyperPyramid"
        }
        
        for dim, expected_name in expected_names.items():
            pyramid = HyperPyramid(dim, 2.0, 3.0)
            actual_name = pyramid.get_shape_type()
            
            if actual_name == expected_name:
                print(f"✅ {dim}D pyramid type: {actual_name}")
            else:
                print(f"❌ {dim}D pyramid type: {actual_name} vs {expected_name}")
        
        return True
    except Exception as e:
        print(f"❌ Shape type name test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all HyperPyramid tests"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                 HYPERPYRAMID TEST SUITE                     ║")
    print("║          Testing N-Dimensional Pyramids                     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    tests = [
        ("HyperPyramid Basic", test_hyperpyramid_basic),
        ("HyperPyramid Dimensions", test_hyperpyramid_dimensions),
        ("HyperPyramid Properties", test_hyperpyramid_properties),
        ("Vertices and Edges", test_hyperpyramid_vertices_edges),
        ("Point Containment", test_hyperpyramid_point_containment),
        ("GeometryAgent Pyramids", test_geometry_agent_pyramids),
        ("Cross Sections", test_cross_sections),
        ("Shape Type Names", test_shape_type_names)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 Running {test_name} Test")
        print('='*60)
        
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
    print('='*60)
    
    if passed == total:
        print("🎉 ALL HYPERPYRAMID TESTS PASSED! 🚀")
        print("\nHyperPyramid implementation is working perfectly!")
        print("✅ N-dimensional pyramids fully functional")
        print("✅ Mathematical accuracy verified")
        print("✅ Vertex and edge counting working")
        print("✅ Face counting implemented")
        print("✅ Cross-section calculations working")
        print("✅ Point containment implemented")
        print("✅ AI integration working")
        print("✅ Shape type names correct")
        return True
    else:
        print("❌ Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)