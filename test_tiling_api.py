#!/usr/bin/env python3
"""
API Integration Test for Tiling Endpoints
Tests the tiling API endpoints with real HTTP requests
"""

import requests
import sys
import time


def test_api_health():
    """Test API health endpoint"""
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        response.raise_for_status()
        print("✅ API health check passed")
        return True
    except Exception as e:
        print(f"❌ API health check failed: {e}")
        return False


def test_tiling_endpoints():
    """Test tiling API endpoints"""
    base_url = "http://localhost:8000/api/tiling"
    
    # Test regular tiling
    try:
        payload = {
            "pattern_type": "regular",
            "shape_type": "square",
            "area": [10, 10],
            "tile_size": 1.0
        }
        response = requests.post(base_url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "tiles" in data and "count" in data:
            print("✅ Regular tiling API test passed")
            return True
        else:
            print("❌ Regular tiling API response missing required fields")
            return False
            
    except Exception as e:
        print(f"❌ Regular tiling API test failed: {e}")
        return False


def test_hexagonal_tiling():
    """Test hexagonal tiling endpoint"""
    base_url = "http://localhost:8000/api/tiling"
    
    try:
        payload = {
            "pattern_type": "hexagonal",
            "area": [10, 10],
            "hex_size": 1.0
        }
        response = requests.post(base_url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "tiles" in data and "count" in data:
            print("✅ Hexagonal tiling API test passed")
            return True
        else:
            print("❌ Hexagonal tiling API response missing required fields")
            return False
            
    except Exception as e:
        print(f"❌ Hexagonal tiling API test failed: {e}")
        return False


def main():
    """Run all tiling API tests"""
    print("🔲 Starting Tiling API Tests...")
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    tests = [
        test_api_health,
        test_tiling_endpoints,
        test_hexagonal_tiling
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed with exception: {e}")
    
    print(f"\n📊 Tiling API Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tiling API tests passed!")
        sys.exit(0)
    else:
        print("💥 Some tiling API tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()