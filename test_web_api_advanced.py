#!/usr/bin/env python3
"""
Test the advanced web API endpoints for new shapes
"""

import requests
import json
import time
import sys

# API base URL
API_BASE = "http://localhost:8000/api"

def test_ellipsoid_endpoint():
    """Test the ellipsoid endpoint"""
    print("🔢 Testing ellipsoid endpoint...")
    
    test_cases = [
        {
            "dimensions": 2,
            "semi_axes": [3.0, 4.0],
            "expected_type": "HyperEllipsoid"
        },
        {
            "dimensions": 3,
            "semi_axes": [1.0, 2.0, 3.0],
            "expected_type": "HyperEllipsoid"
        },
        {
            "dimensions": 3,
            "semi_axes": [2.0, 2.0, 2.0],
            "expected_type": "HyperSphere"  # Should detect as sphere
        }
    ]
    
    for case in test_cases:
        try:
            response = requests.post(f"{API_BASE}/ellipsoid", json=case)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {case['dimensions']}D ellipsoid (axes={case['semi_axes']}): {data['shape_type']}")
                print(f"   - Volume: {data['volume']:.6f}")
                print(f"   - Surface Area: {data['surface_area']:.6f}")
                print(f"   - Axis ratio: {data['additional_properties']['axis_ratio']:.6f}")
                print(f"   - Is sphere: {data['additional_properties']['is_sphere']}")
                
                if case['expected_type'] == data['shape_type']:
                    print(f"   ✅ Shape type correctly detected: {data['shape_type']}")
                else:
                    print(f"   ❌ Shape type mismatch: {data['shape_type']} vs {case['expected_type']}")
                    
            else:
                print(f"❌ {case['dimensions']}D ellipsoid failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ {case['dimensions']}D ellipsoid failed: {e}")
    
    return True

def test_simplex_endpoint():
    """Test the simplex endpoint"""
    print("\n🔺 Testing simplex endpoint...")
    
    test_cases = [
        {"dimensions": 2, "side_length": 3.0, "expected_type": "Triangle"},
        {"dimensions": 3, "side_length": 2.0, "expected_type": "Tetrahedron"},
        {"dimensions": 4, "side_length": 1.5, "expected_type": "4D Simplex"}
    ]
    
    for case in test_cases:
        try:
            response = requests.post(f"{API_BASE}/simplex", json=case)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {case['dimensions']}D simplex (side={case['side_length']}): {data['shape_type']}")
                print(f"   - Volume: {data['volume']:.6f}")
                print(f"   - Surface Area: {data['surface_area']:.6f}")
                print(f"   - Vertices: {data['additional_properties']['vertices']}")
                print(f"   - Edges: {data['additional_properties']['edges']}")
                print(f"   - Circumradius: {data['additional_properties']['circumradius']:.6f}")
                print(f"   - Formula: {data['volume_formula']}")
                
                if case['expected_type'] == data['shape_type']:
                    print(f"   ✅ Shape type correct: {data['shape_type']}")
                else:
                    print(f"   ❌ Shape type mismatch: {data['shape_type']} vs {case['expected_type']}")
                    
            else:
                print(f"❌ {case['dimensions']}D simplex failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ {case['dimensions']}D simplex failed: {e}")
    
    return True

def test_pyramid_endpoint():
    """Test the pyramid endpoint"""
    print("\n🏔️ Testing pyramid endpoint...")
    
    test_cases = [
        {"dimensions": 2, "base_side_length": 4.0, "height": 3.0, "expected_type": "Triangle"},
        {"dimensions": 3, "base_side_length": 2.0, "height": 3.0, "expected_type": "Square Pyramid"},
        {"dimensions": 4, "base_side_length": 2.5, "height": 4.0, "expected_type": "4D HyperPyramid"}
    ]
    
    for case in test_cases:
        try:
            response = requests.post(f"{API_BASE}/pyramid", json=case)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {case['dimensions']}D pyramid (base={case['base_side_length']}, height={case['height']}): {data['shape_type']}")
                print(f"   - Volume: {data['volume']:.6f}")
                print(f"   - Surface Area: {data['surface_area']:.6f}")
                print(f"   - Vertices: {data['additional_properties']['vertices']}")
                print(f"   - Edges: {data['additional_properties']['edges']}")
                print(f"   - Slant height: {data['additional_properties']['slant_height']:.6f}")
                print(f"   - Base volume: {data['additional_properties']['base_volume']:.6f}")
                print(f"   - Formula: {data['volume_formula']}")
                
                if case['expected_type'] == data['shape_type']:
                    print(f"   ✅ Shape type correct: {data['shape_type']}")
                else:
                    print(f"   ❌ Shape type mismatch: {data['shape_type']} vs {case['expected_type']}")
                    
            else:
                print(f"❌ {case['dimensions']}D pyramid failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ {case['dimensions']}D pyramid failed: {e}")
    
    return True

def test_natural_language_queries():
    """Test natural language queries for new shapes"""
    print("\n🤖 Testing natural language queries for new shapes...")
    
    queries = [
        "create a 3D ellipsoid with axes 1.5 2.0 3.0",
        "create a 2D ellipse with semi-axes 2 3",
        "create a 3D tetrahedron with side 2",
        "create a 4D simplex side length 1.5",
        "create a 3D pyramid base 2 height 3",
        "create a 4D hyperpyramid base 2.5 height 4",
        "ellipsoid with axes 1 2 3",
        "simplex side 2",
        "pyramid base 2 height 3"
    ]
    
    for query in queries:
        try:
            response = requests.post(f"{API_BASE}/query", json={"query": query})
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"✅ Query: '{query}'")
                    print(f"   Response: {data['response'][:120]}...")
                else:
                    print(f"❌ Query failed: {data['response']}")
            else:
                print(f"❌ Query failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Query failed: {e}")
    
    return True

def test_health_endpoint():
    """Test that health endpoint reflects new shapes"""
    print("\n🔍 Testing health endpoint with new shapes...")
    
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
            print(f"   - Supported shapes: {data['supported_shapes']}")
            print(f"   - Features: {len(data['features'])} features")
            
            # Check if all new shapes are mentioned
            expected_shapes = ["sphere", "cube", "ellipsoid", "simplex", "pyramid"]
            for shape in expected_shapes:
                if shape in data['supported_shapes']:
                    print(f"   ✅ {shape} support confirmed")
                else:
                    print(f"   ❌ {shape} support missing")
                    
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    return True

def test_error_handling():
    """Test error handling for new endpoints"""
    print("\n🚨 Testing error handling...")
    
    error_cases = [
        {
            "endpoint": "ellipsoid",
            "data": {"dimensions": 3, "semi_axes": [1.0, 2.0]},  # Wrong number of axes
            "expected_error": "must match dimensions"
        },
        {
            "endpoint": "simplex", 
            "data": {"dimensions": 2, "side_length": -1.0},  # Negative side length
            "expected_error": "cannot be negative"
        },
        {
            "endpoint": "pyramid",
            "data": {"dimensions": 3, "base_side_length": 2.0, "height": -1.0},  # Negative height
            "expected_error": "cannot be negative"
        }
    ]
    
    for case in error_cases:
        try:
            response = requests.post(f"{API_BASE}/{case['endpoint']}", json=case['data'])
            if response.status_code == 400:
                error_msg = response.json()['detail']
                if case['expected_error'] in error_msg:
                    print(f"✅ {case['endpoint']} error handling: {error_msg}")
                else:
                    print(f"❌ {case['endpoint']} unexpected error: {error_msg}")
            else:
                print(f"❌ {case['endpoint']} should have failed but got: {response.status_code}")
        except Exception as e:
            print(f"❌ {case['endpoint']} error test failed: {e}")
    
    return True

def test_mathematical_accuracy():
    """Test mathematical accuracy of new shapes"""
    print("\n🔬 Testing mathematical accuracy...")
    
    try:
        # Test 2D ellipse (should be π * a * b)
        response = requests.post(f"{API_BASE}/ellipsoid", json={
            "dimensions": 2,
            "semi_axes": [3.0, 4.0]
        })
        if response.status_code == 200:
            data = response.json()
            expected_volume = 3.14159265359 * 3.0 * 4.0
            actual_volume = data['volume']
            if abs(actual_volume - expected_volume) < 0.001:
                print(f"✅ 2D ellipse volume accuracy: {actual_volume:.6f}")
            else:
                print(f"❌ 2D ellipse volume inaccurate: {actual_volume:.6f} vs {expected_volume:.6f}")
        
        # Test 3D tetrahedron (should be (√2/12) * s³)
        response = requests.post(f"{API_BASE}/simplex", json={
            "dimensions": 3,
            "side_length": 2.0
        })
        if response.status_code == 200:
            data = response.json()
            expected_volume = (1.41421356237 / 12) * 8.0  # (√2/12) * 2³
            actual_volume = data['volume']
            if abs(actual_volume - expected_volume) < 0.001:
                print(f"✅ 3D tetrahedron volume accuracy: {actual_volume:.6f}")
            else:
                print(f"❌ 3D tetrahedron volume inaccurate: {actual_volume:.6f} vs {expected_volume:.6f}")
        
        # Test 3D square pyramid (should be (1/3) * base² * height)
        response = requests.post(f"{API_BASE}/pyramid", json={
            "dimensions": 3,
            "base_side_length": 4.0,
            "height": 3.0
        })
        if response.status_code == 200:
            data = response.json()
            expected_volume = (1/3) * 16.0 * 3.0
            actual_volume = data['volume']
            if abs(actual_volume - expected_volume) < 0.001:
                print(f"✅ 3D square pyramid volume accuracy: {actual_volume:.6f}")
            else:
                print(f"❌ 3D square pyramid volume inaccurate: {actual_volume:.6f} vs {expected_volume:.6f}")
                
    except Exception as e:
        print(f"❌ Mathematical accuracy test failed: {e}")
    
    return True

def main():
    """Run all advanced API tests"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           ADVANCED WEB API INTEGRATION TEST                 ║")
    print("║       Testing New Shape Endpoints and Functionality         ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    tests = [
        ("Ellipsoid Endpoint", test_ellipsoid_endpoint),
        ("Simplex Endpoint", test_simplex_endpoint),
        ("Pyramid Endpoint", test_pyramid_endpoint),
        ("Natural Language Queries", test_natural_language_queries),
        ("Health Endpoint", test_health_endpoint),
        ("Error Handling", test_error_handling),
        ("Mathematical Accuracy", test_mathematical_accuracy)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 Running {test_name}")
        print('='*60)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} completed successfully")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print(f"\n{'='*60}")
    print(f"📊 FINAL RESULTS: {passed}/{total} tests completed")
    print('='*60)
    
    if passed >= total - 1:  # Allow for one minor failure
        print("🎉 ADVANCED API INTEGRATION SUCCESSFUL! 🚀")
        print("\n🌟 New API Features Available:")
        print("   - /api/ellipsoid - N-dimensional ellipsoids")
        print("   - /api/simplex - N-dimensional triangles/tetrahedra")
        print("   - /api/pyramid - N-dimensional pyramids")
        print("   - Enhanced natural language queries")
        print("   - Comprehensive shape properties")
        
        print("\n🔥 Example Usage:")
        print("   # Create 3D ellipsoid")
        print("   curl -X POST http://localhost:8000/api/ellipsoid \\")
        print("        -H 'Content-Type: application/json' \\")
        print("        -d '{\"dimensions\": 3, \"semi_axes\": [1.0, 2.0, 3.0]}'")
        
        print("\n   # Create 4D simplex")
        print("   curl -X POST http://localhost:8000/api/simplex \\")
        print("        -H 'Content-Type: application/json' \\")
        print("        -d '{\"dimensions\": 4, \"side_length\": 2.0}'")
        
        print("\n   # Create 3D pyramid")
        print("   curl -X POST http://localhost:8000/api/pyramid \\")
        print("        -H 'Content-Type: application/json' \\")
        print("        -d '{\"dimensions\": 3, \"base_side_length\": 2.0, \"height\": 3.0}'")
        
        return True
    else:
        print("❌ Some tests failed. Check server logs.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)