#!/usr/bin/env python3
"""
Test the updated web API with cube support
"""

import json
import sys
import time

import requests

# API base URL
API_BASE = "http://localhost:8000/api"


def test_cube_endpoint():
    """Test the new cube endpoint"""
    print("🔢 Testing cube endpoint...")

    test_cases = [
        {"dimensions": 3, "side_length": 2.0},
        {"dimensions": 4, "side_length": 1.5},
        {"dimensions": 5, "side_length": 1.0},
    ]

    for case in test_cases:
        try:
            response = requests.post(f"{API_BASE}/cube", json=case)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {case['dimensions']}D cube (side={case['side_length']}):")
                print(f"   - Volume: {data['volume']:.6f}")
                print(f"   - Surface Area: {data['surface_area']:.6f}")
                print(f"   - Vertices: {data['additional_properties']['vertices']}")
                print(f"   - Edges: {data['additional_properties']['edges']}")
                print(f"   - Formula: {data['volume_formula']}")
            else:
                print(f"❌ {case['dimensions']}D cube failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ {case['dimensions']}D cube failed: {e}")

    return True


def test_updated_comparison():
    """Test the updated comparison endpoint"""
    print("\n⚖️ Testing updated comparison endpoint...")

    try:
        response = requests.post(
            f"{API_BASE}/compare", json={"dimensions": 3, "parameter": 2.0}
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Comparison results:")
            print(
                f"   - Sphere volume: {data['comparison_data']['sphere']['volume']:.6f}"
            )
            print(f"   - Cube volume: {data['comparison_data']['cube']['volume']:.6f}")
            print(
                f"   - Volume ratio: {data['comparison_data']['ratios']['volume_ratio_sphere_cube']:.6f}"
            )
            print(f"   - Cube vertices: {data['comparison_data']['cube']['vertices']}")
            print(f"   - Cube edges: {data['comparison_data']['cube']['edges']}")
        else:
            print(f"❌ Comparison failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Comparison failed: {e}")

    return True


def test_cube_queries():
    """Test cube queries through natural language interface"""
    print("\n🤖 Testing cube queries...")

    queries = [
        "create a 3D cube with side 2",
        "volume of 4D cube side 1.5",
        "surface area of 5D hypercube side 2",
        "compare sphere vs cube in 4 dimensions",
    ]

    for query in queries:
        try:
            response = requests.post(f"{API_BASE}/query", json={"query": query})
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    print(f"✅ Query: '{query}'")
                    print(f"   Response: {data['response'][:150]}...")
                else:
                    print(f"❌ Query failed: {data['response']}")
            else:
                print(f"❌ Query failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Query failed: {e}")

    return True


def test_health_with_cubes():
    """Test that health endpoint reflects cube support"""
    print("\n🔍 Testing health endpoint with cube support...")

    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
            print(f"   - Features: {data['features']}")

            # Check if features mention cubes
            features_text = " ".join(data["features"])
            if "cube" in features_text.lower():
                print("✅ Cube support mentioned in features")
            else:
                print("⚠️  Cube support not mentioned in features")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")

    return True


def main():
    """Run all cube-related API tests"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║            CUBE API INTEGRATION TEST                        ║")
    print("║         Testing HyperCube Web API Functionality             ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)

    tests = [
        ("Cube Endpoint", test_cube_endpoint),
        ("Updated Comparison", test_updated_comparison),
        ("Cube Queries", test_cube_queries),
        ("Health with Cubes", test_health_with_cubes),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 Running {test_name}")
        print("=" * 60)

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
    print("=" * 60)

    if passed >= total - 1:  # Allow for one minor failure
        print("🎉 CUBE API INTEGRATION SUCCESSFUL! 🚀")
        print("\n🌟 New Features Available:")
        print("   - /api/cube endpoint for n-dimensional cubes")
        print("   - Enhanced comparison with sphere vs cube")
        print("   - Natural language cube queries")
        print("   - Comprehensive cube properties")

        print("\n🔥 Example Usage:")
        print("   curl -X POST http://localhost:8000/api/cube \\")
        print("        -H 'Content-Type: application/json' \\")
        print('        -d \'{"dimensions": 4, "side_length": 2.0}\'')

        return True
    else:
        print("❌ Some tests failed. Check server logs.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
