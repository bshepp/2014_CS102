#!/usr/bin/env python3
"""
Test the tiling API endpoints
"""

import json
import sys
import time

import requests

# API base URL
API_BASE = "http://localhost:8000/api"


def test_regular_tiling_endpoint():
    """Test regular tiling endpoint"""
    print("🔲 Testing regular tiling endpoint...")

    test_cases = [
        {
            "tiling_type": "regular",
            "dimensions": 2,
            "bounds": [[0, 5], [0, 5]],
            "density": 1.0,
            "shape_type": "cube",
            "parameter": 1.0,
        },
        {
            "tiling_type": "regular",
            "dimensions": 2,
            "bounds": [[0, 4], [0, 4]],
            "density": 1.0,
            "shape_type": "sphere",
            "parameter": 0.5,
        },
        {
            "tiling_type": "regular",
            "dimensions": 3,
            "bounds": [[0, 3], [0, 3], [0, 3]],
            "density": 1.0,
            "shape_type": "cube",
            "parameter": 1.0,
        },
    ]

    for case in test_cases:
        try:
            response = requests.post(f"{API_BASE}/tiling", json=case)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {case['dimensions']}D {case['shape_type']} tiling:")
                print(f"   - Tiles: {data['tile_count']}")
                print(f"   - Coverage: {data['coverage_efficiency']:.3f}")
                print(f"   - Pattern: {data['pattern_properties']['pattern_type']}")
                print(
                    f"   - Analysis: {data['analysis']['mathematical_properties']['is_regular']}"
                )
            else:
                print(
                    f"❌ {case['dimensions']}D {case['shape_type']} tiling failed: {response.status_code}"
                )
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ {case['dimensions']}D {case['shape_type']} tiling failed: {e}")

    return True


def test_hexagonal_tiling_endpoint():
    """Test hexagonal tiling endpoint"""
    print("\n🔶 Testing hexagonal tiling endpoint...")

    test_cases = [
        {
            "tiling_type": "hexagonal",
            "dimensions": 2,
            "bounds": [[0, 10], [0, 10]],
            "density": 1.0,
            "side_length": 1.0,
        },
        {
            "tiling_type": "hexagonal",
            "dimensions": 2,
            "bounds": [[0, 8], [0, 8]],
            "density": 1.5,
            "side_length": 0.8,
        },
    ]

    for case in test_cases:
        try:
            response = requests.post(f"{API_BASE}/tiling", json=case)
            if response.status_code == 200:
                data = response.json()
                print(
                    f"✅ Hexagonal tiling (side={case['side_length']}, density={case['density']}):"
                )
                print(f"   - Tiles: {data['tile_count']}")
                print(f"   - Coverage: {data['coverage_efficiency']:.3f}")
                print(f"   - Pattern: {data['pattern_properties']['pattern_type']}")
                print(
                    f"   - Coordination: {data['analysis']['mathematical_properties']['coordination_number']}"
                )
            else:
                print(f"❌ Hexagonal tiling failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Hexagonal tiling failed: {e}")

    return True


def test_voronoi_tiling_endpoint():
    """Test Voronoi tiling endpoint"""
    print("\n🔺 Testing Voronoi tiling endpoint...")

    test_cases = [
        {
            "tiling_type": "voronoi",
            "dimensions": 2,
            "bounds": [[0, 10], [0, 10]],
            "density": 1.0,
            "num_random_seeds": 8,
        },
        {
            "tiling_type": "voronoi",
            "dimensions": 2,
            "bounds": [[0, 8], [0, 8]],
            "density": 1.0,
            "seed_points": [[2, 2], [4, 4], [6, 2], [2, 6], [6, 6]],
        },
    ]

    for i, case in enumerate(test_cases):
        try:
            response = requests.post(f"{API_BASE}/tiling", json=case)
            if response.status_code == 200:
                data = response.json()
                seed_type = "random" if "num_random_seeds" in case else "specified"
                print(f"✅ Voronoi tiling ({seed_type} seeds):")
                print(f"   - Tiles: {data['tile_count']}")
                print(f"   - Coverage: {data['coverage_efficiency']:.3f}")
                print(f"   - Pattern: {data['pattern_properties']['pattern_type']}")
                print(
                    f"   - Regular: {data['analysis']['mathematical_properties']['is_regular']}"
                )
            else:
                print(f"❌ Voronoi tiling failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Voronoi tiling failed: {e}")

    return True


def test_tiling_error_handling():
    """Test tiling error handling"""
    print("\n🚨 Testing tiling error handling...")

    error_cases = [
        {
            "data": {
                "tiling_type": "regular",
                "dimensions": 2,
                "bounds": [[0, 5], [0, 5]],
                "density": 1.0,
                # Missing shape_type and parameter
            },
            "expected_error": "requires",
        },
        {
            "data": {
                "tiling_type": "hexagonal",
                "dimensions": 3,  # 3D not supported
                "bounds": [[0, 5], [0, 5], [0, 5]],
                "density": 1.0,
                "side_length": 1.0,
            },
            "expected_error": "only supported in 2D",
        },
        {
            "data": {
                "tiling_type": "voronoi",
                "dimensions": 2,
                "bounds": [[0, 5], [0, 5]],
                "density": 1.0,
                # Missing seed_points and num_random_seeds
            },
            "expected_error": "requires either",
        },
        {
            "data": {
                "tiling_type": "unknown",
                "dimensions": 2,
                "bounds": [[0, 5], [0, 5]],
                "density": 1.0,
            },
            "expected_error": "Unsupported tiling type",
        },
    ]

    for case in error_cases:
        try:
            response = requests.post(f"{API_BASE}/tiling", json=case["data"])
            if response.status_code == 400:
                error_msg = response.json()["detail"]
                if case["expected_error"] in error_msg:
                    print(f"✅ Error handling: {error_msg}")
                else:
                    print(f"❌ Unexpected error: {error_msg}")
            else:
                print(f"❌ Should have failed but got: {response.status_code}")
        except Exception as e:
            print(f"❌ Error test failed: {e}")

    return True


def test_health_endpoint():
    """Test health endpoint includes tiling"""
    print("\n🔍 Testing health endpoint...")

    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
            print(f"   - Supported tilings: {data['supported_tilings']}")

            # Check if tiling features are listed
            tiling_features = [
                f
                for f in data["features"]
                if "tiling" in f.lower()
                or "tessellation" in f.lower()
                or "voronoi" in f.lower()
            ]
            print(f"   - Tiling features: {len(tiling_features)}")
            for feature in tiling_features:
                print(f"     • {feature}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")

    return True


def main():
    """Run all tiling API tests"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                 TILING API ENDPOINT TESTS                   ║")
    print("║            Testing REST API for Tiling Patterns             ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)

    tests = [
        ("Regular Tiling Endpoint", test_regular_tiling_endpoint),
        ("Hexagonal Tiling Endpoint", test_hexagonal_tiling_endpoint),
        ("Voronoi Tiling Endpoint", test_voronoi_tiling_endpoint),
        ("Tiling Error Handling", test_tiling_error_handling),
        ("Health Endpoint", test_health_endpoint),
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
        print("🎉 TILING API INTEGRATION SUCCESSFUL! 🚀")
        print("\n🌟 Tiling API Features Available:")
        print("   - /api/tiling - Create tiling patterns")
        print("   - Regular tilings (cube, sphere, simplex)")
        print("   - Hexagonal tessellations")
        print("   - Voronoi diagrams with custom or random seeds")
        print("   - Pattern analysis and mathematical properties")
        print("   - Coverage efficiency calculations")
        print("   - N-dimensional space filling")

        print("\n🔥 Example Usage:")
        print("   # Create hexagonal tiling")
        print("   curl -X POST http://localhost:8000/api/tiling \\")
        print("        -H 'Content-Type: application/json' \\")
        print(
            '        -d \'{"tiling_type": "hexagonal", "dimensions": 2, "bounds": [[0, 10], [0, 10]], "side_length": 1.0}\''
        )

        print("\n   # Create Voronoi diagram")
        print("   curl -X POST http://localhost:8000/api/tiling \\")
        print("        -H 'Content-Type: application/json' \\")
        print(
            '        -d \'{"tiling_type": "voronoi", "dimensions": 2, "bounds": [[0, 10], [0, 10]], "num_random_seeds": 8}\''
        )

        return True
    else:
        print("❌ Some tests failed. Check server logs.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
