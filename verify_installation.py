#!/usr/bin/env python3
"""
Installation Verification Script for N-Dimensional Geometry Engine

This script verifies that all required dependencies are installed and working correctly.
Run this script after installation to ensure everything is set up properly.
"""

import importlib
import os
import sys


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")


def print_success(message):
    """Print success message"""
    print(f"✅ {message}")


def print_error(message):
    """Print error message"""
    print(f"❌ {message}")


def print_warning(message):
    """Print warning message"""
    print(f"⚠️  {message}")


def check_python_version():
    """Check Python version compatibility"""
    print_header("Python Version Check")

    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor >= 9:
        print_success("Python version is compatible")
        return True
    else:
        print_error("Python 3.9+ required")
        return False


def check_virtual_environment():
    """Check if running in virtual environment"""
    print_header("Virtual Environment Check")

    # Check if in virtual environment
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print_success("Running in virtual environment")
        print(f"Virtual environment path: {sys.prefix}")
        return True
    else:
        print_warning("Not running in virtual environment")
        print("Recommendation: Create and activate virtual environment")
        print("Commands:")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate")
        return False


def check_package_import(package_name, friendly_name=None):
    """Check if a package can be imported"""
    if friendly_name is None:
        friendly_name = package_name

    try:
        module = importlib.import_module(package_name)
        version = getattr(module, "__version__", "unknown")
        print_success(f"{friendly_name} imported successfully (version: {version})")
        return True
    except ImportError as e:
        print_error(f"{friendly_name} import failed: {e}")
        return False


def check_required_packages():
    """Check all required packages"""
    print_header("Required Package Check")

    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("numpy", "NumPy"),
        ("plotly", "Plotly"),
        ("pydantic", "Pydantic"),
    ]

    all_good = True
    for package, friendly_name in packages:
        if not check_package_import(package, friendly_name):
            all_good = False

    if all_good:
        print_success("All required packages are available")
    else:
        print_error("Some packages are missing")
        print("\nTo install missing packages:")
        print("  pip install fastapi uvicorn numpy plotly pydantic python-multipart")

    return all_good


def check_project_files():
    """Check if required project files exist"""
    print_header("Project Files Check")

    required_files = [
        "web_api.py",
        "geometry_engine.py",
        "requirements.txt",
        "CLAUDE.md",
        "TROUBLESHOOTING.md",
    ]

    all_good = True
    for file in required_files:
        if os.path.exists(file):
            print_success(f"{file} exists")
        else:
            print_error(f"{file} missing")
            all_good = False

    return all_good


def check_geometry_engine():
    """Check if geometry engine can be imported"""
    print_header("Geometry Engine Check")

    try:
        from geometry_engine import HyperCube, HyperSphere

        print_success("Geometry engine imported successfully")

        # Test basic functionality
        sphere = HyperSphere(3, 1.0)
        volume = sphere.get_volume()
        print_success(f"Created 3D sphere with volume: {volume:.4f}")

        cube = HyperCube(3, 2.0)
        cube_volume = cube.get_volume()
        print_success(f"Created 3D cube with volume: {cube_volume:.4f}")

        return True
    except Exception as e:
        print_error(f"Geometry engine test failed: {e}")
        return False


def check_web_api():
    """Check if web API can be imported"""
    print_header("Web API Check")

    try:
        from web_api import app

        print_success("Web API imported successfully")

        # Check if app is FastAPI instance
        if hasattr(app, "openapi"):
            print_success("FastAPI app structure is valid")
        else:
            print_warning("App structure may be invalid")

        return True
    except Exception as e:
        print_error(f"Web API test failed: {e}")
        return False


def test_server_start():
    """Test if server can start (dry run)"""
    print_header("Server Start Test")

    try:
        # Import required modules
        import web_api  # noqa: F401

        print_success("Server components ready")
        print("To start server manually:")
        print("  python web_api.py")
        print("  or")
        print("  uvicorn web_api:app --host 0.0.0.0 --port 8000")

        return True
    except Exception as e:
        print_error(f"Server start test failed: {e}")
        return False


def provide_recommendations():
    """Provide installation recommendations"""
    print_header("Recommendations")

    print("🚀 Quick Setup Commands:")
    print("  # Create virtual environment")
    print("  python3 -m venv venv")
    print("  source venv/bin/activate")
    print("")
    print("  # Install dependencies")
    print("  pip install fastapi uvicorn numpy plotly pydantic python-multipart")
    print("")
    print("  # Start server")
    print("  python web_api.py")
    print("")
    print("  # Access web interface")
    print("  # Browser: http://localhost:8000")
    print("  # API Docs: http://localhost:8000/api/docs")
    print("")
    print("📚 For more help:")
    print("  - Read TROUBLESHOOTING.md")
    print("  - Check CLAUDE.md for full documentation")
    print(
        "  - Review ai_cognitive_framework_geometry_engine.json for AI "
        "collaboration patterns"
    )


def main():
    """Main verification function"""
    print("🔍 N-Dimensional Geometry Engine - Installation Verification")
    print("=" * 60)

    checks = [
        check_python_version(),
        check_virtual_environment(),
        check_required_packages(),
        check_project_files(),
        check_geometry_engine(),
        check_web_api(),
        test_server_start(),
    ]

    passed = sum(checks)
    total = len(checks)

    print_header("Summary")
    print(f"Passed: {passed}/{total} checks")

    if passed == total:
        print_success("🎉 All checks passed! Installation is ready.")
        print("Run 'python web_api.py' to start the server.")
    elif passed >= total - 1:
        print_warning("⚠️  Almost ready! Check warnings above.")
    else:
        print_error("❌ Installation needs attention. See errors above.")
        provide_recommendations()


if __name__ == "__main__":
    main()
