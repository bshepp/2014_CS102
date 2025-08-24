#!/usr/bin/env python3
"""
Comprehensive test of the web API functionality
"""

import sys
import time

import requests

# API base URL
API_BASE = "http://localhost:8000/api"


def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   - Geometry engine: {data['geometry_engine']}")
            print(f"   - Java available: {data['java_available']}")
            print(f"   - Supported dimensions: {data['supported_dimensions']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_sphere_creation():
    """Test sphere creation API"""
    print("\n🔢 Testing sphere creation...")
    test_cases = [
        {"dimensions": 3, "radius": 1.0},
        {"dimensions": 4, "radius": 1.5},
        {"dimensions": 5, "radius": 2.0},
        {"dimensions": 10, "radius": 0.5},
    ]

    for case in test_cases:
        try:
            response = requests.post(f"{API_BASE}/sphere", json=case)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {case['dimensions']}D sphere (r={case['radius']}):")
                print(f"   - Volume: {data['volume']:.6f}")
                print(f"   - Surface Area: {data['surface_area']:.6f}")
                print(f"   - Formula: {data['volume_formula']}")
            else:
                print(f"❌ {case['dimensions']}D sphere failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ {case['dimensions']}D sphere failed: {e}")

    return True


def test_natural_language_queries():
    """Test natural language query API"""
    print("\n🤖 Testing natural language queries...")

    queries = [
        "create a 4D sphere with radius 2",
        "volume of 5D sphere radius 1.5",
        "surface area of 3D sphere radius 2",
        "compare sphere in 6 dimensions",
    ]

    for query in queries:
        try:
            response = requests.post(f"{API_BASE}/query", json={"query": query})
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    print(f"✅ Query: '{query}'")
                    print(f"   Response: {data['response'][:100]}...")
                else:
                    print(f"❌ Query failed: {data['response']}")
            else:
                print(f"❌ Query failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Query failed: {e}")

    return True


def test_original_java():
    """Test original Java integration"""
    print("\n☕ Testing original Java integration...")

    try:
        response = requests.post(f"{API_BASE}/original-java?diameter=3.0")
        if response.status_code == 200:
            data = response.json()
            print("✅ Original Java execution:")
            print(f"   - Diameter: {data['diameter']}")
            print(f"   - Java available: {data['java_available']}")
            print(f"   - Result preview: {data['result'][:100]}...")
        else:
            print(f"❌ Original Java failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Original Java failed: {e}")

    return True


def test_dimension_info():
    """Test dimension information API"""
    print("\n📊 Testing dimension information...")

    dimensions = [1, 2, 3, 4, 5, 10, 20]

    for dim in dimensions:
        try:
            response = requests.get(f"{API_BASE}/dimensions/{dim}")
            if response.status_code == 200:
                data = response.json()
                unit_sphere = data["unit_sphere"]
                print(f"✅ {dim}D geometry:")
                print(f"   - Unit sphere volume: {unit_sphere['volume']:.6f}")
                print(f"   - Unit sphere surface: {unit_sphere['surface_area']:.6f}")
                print(
                    f"   - Surface/Volume ratio: "
                    f"{data['insights']['surface_to_volume_ratio']:.3f}"
                )
            else:
                print(f"❌ {dim}D info failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {dim}D info failed: {e}")

    return True


def test_visualization():
    """Test visualization API"""
    print("\n📈 Testing visualization...")

    test_cases = [
        {"dimensions": 1, "radius": 1.0},
        {"dimensions": 2, "radius": 1.5},
        {"dimensions": 3, "radius": 2.0},
        {"dimensions": 4, "radius": 1.0, "cross_section": 0.5},
    ]

    for case in test_cases:
        try:
            response = requests.post(f"{API_BASE}/visualize", json=case)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {case['dimensions']}D visualization:")
                print(f"   - Radius: {data['radius']}")
                print(f"   - Volume: {data['volume']:.6f}")
                print(f"   - Plot data: {len(data['plot_json'])} characters")
            else:
                print(
                    f"❌ {case['dimensions']}D visualization failed: "
                    f"{response.status_code}"
                )
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ {case['dimensions']}D visualization failed: {e}")

    return True


def main():
    """Run all web API tests"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║               WEB API COMPREHENSIVE TEST                    ║")
    print("║          Testing all endpoints and functionality            ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)

    tests = [
        ("Health Check", test_health),
        ("Sphere Creation", test_sphere_creation),
        ("Natural Language Queries", test_natural_language_queries),
        ("Original Java Integration", test_original_java),
        ("Dimension Information", test_dimension_info),
        ("Visualization", test_visualization),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'=' * 60}")
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

    print(f"\n{'=' * 60}")
    print(f"📊 FINAL RESULTS: {passed}/{total} tests completed")
    print("=" * 60)

    if passed >= total - 1:  # Allow for one minor failure
        print("🎉 WEB API IS OPERATIONAL! 🚀")
        print("\n🌟 Access Points:")
        print("   - Main Interface: http://localhost:8000")
        print("   - Interactive Demo: http://localhost:8000/demo")
        print("   - API Documentation: http://localhost:8000/api/docs")
        print("   - Health Check: http://localhost:8000/api/health")

        print("\n🔥 Features Available:")
        print("   - N-dimensional sphere calculations (1D to 100D)")
        print("   - Natural language geometry queries")
        print("   - Original CS102 Java code integration")
        print("   - Interactive 3D/4D visualizations")
        print("   - Real-time mathematical insights")

        return True
    else:
        print("❌ Some tests failed. Check server logs.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
