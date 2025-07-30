#!/usr/bin/env python3
"""
Test script for the web API to verify everything works before starting the server
"""

import json
import sys
import traceback


def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")

    try:
        import fastapi

        print(f"✅ FastAPI: {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False

    try:
        import uvicorn

        print(f"✅ Uvicorn: {uvicorn.__version__}")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False

    try:
        import plotly

        print(f"✅ Plotly: {plotly.__version__}")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False

    try:
        import matplotlib

        print(f"✅ Matplotlib: {matplotlib.__version__}")
    except ImportError as e:
        print(f"❌ Matplotlib import failed: {e}")
        return False

    try:
        from geometry_engine import GeometryAgent, HyperSphere

        print("✅ Geometry engine imported successfully")
    except ImportError as e:
        print(f"❌ Geometry engine import failed: {e}")
        return False

    return True


def test_geometry_functionality():
    """Test basic geometry functionality"""
    print("\n🔬 Testing geometry functionality...")

    try:
        from geometry_engine import GeometryAgent, HyperSphere

        # Test HyperSphere
        sphere = HyperSphere(3, 1.0)
        volume = sphere.get_volume()
        surface = sphere.get_surface_area()
        print(f"✅ 3D unit sphere: volume={volume:.6f}, surface={surface:.6f}")

        # Test GeometryAgent
        agent = GeometryAgent()
        result = agent.process_query("create a 4D sphere with radius 2")
        print(f"✅ Geometry agent query processed: {len(result)} characters")

        # Test different dimensions
        for dim in [1, 2, 4, 5, 10]:
            sphere = HyperSphere(dim, 1.0)
            vol = sphere.get_volume()
            print(f"✅ {dim}D unit sphere volume: {vol:.6f}")

        return True
    except Exception as e:
        print(f"❌ Geometry functionality test failed: {e}")
        traceback.print_exc()
        return False


def test_visualization():
    """Test visualization functionality"""
    print("\n📊 Testing visualization...")

    try:
        import numpy as np
        import plotly.graph_objects as go

        # Test 3D sphere creation
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))

        fig = go.Figure(data=[go.Surface(x=x, y=y, z=z)])
        fig.update_layout(title="Test 3D Sphere")

        # Test JSON serialization
        fig_json = fig.to_json()
        print(f"✅ 3D visualization created: {len(fig_json)} characters")

        return True
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        traceback.print_exc()
        return False


def test_api_models():
    """Test Pydantic models"""
    print("\n📋 Testing API models...")

    try:
        from web_api import (QueryRequest, QueryResponse, SphereRequest,
                             SphereResponse)

        # Test SphereRequest
        sphere_req = SphereRequest(dimensions=3, radius=1.5)
        print(f"✅ SphereRequest: {sphere_req.dimensions}D, radius={sphere_req.radius}")

        # Test QueryRequest
        query_req = QueryRequest(query="test query")
        print(f"✅ QueryRequest: {query_req.query}")

        return True
    except Exception as e:
        print(f"❌ API models test failed: {e}")
        traceback.print_exc()
        return False


def test_file_existence():
    """Test that required files exist"""
    print("\n📁 Testing file existence...")

    import os

    files_to_check = [
        "geometry_engine.py",
        "web_api.py",
        "demo.html",
        "Sphere.java",
        "MultiSphere.java",
    ]

    all_exist = True
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False

    return all_exist


def test_java_integration():
    """Test Java integration"""
    print("\n☕ Testing Java integration...")

    try:
        from geometry_engine import JavaBridge

        bridge = JavaBridge()
        if bridge.java_available:
            print("✅ Java is available")
            result = bridge.run_original_multisphere(2.0)
            print(f"✅ Java execution successful: {len(result)} characters")
        else:
            print("⚠️  Java not available - will use Python fallback")
            result = bridge.run_original_multisphere(2.0)
            print(f"✅ Python fallback successful: {len(result)} characters")

        return True
    except Exception as e:
        print(f"❌ Java integration test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║               WEB API PRE-FLIGHT TESTS                      ║")
    print("║            Verifying everything works before launch         ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    tests = [
        ("File Existence", test_file_existence),
        ("Imports", test_imports),
        ("Geometry Functionality", test_geometry_functionality),
        ("Visualization", test_visualization),
        ("API Models", test_api_models),
        ("Java Integration", test_java_integration),
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
        print("🎉 ALL TESTS PASSED! Ready to launch web API! 🚀")
        print("\nTo start the server, run:")
        print("    python web_api.py")
        print("\nOr:")
        print("    uvicorn web_api:app --reload --host 0.0.0.0 --port 8000")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before launching.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
