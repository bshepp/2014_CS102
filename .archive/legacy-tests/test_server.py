#!/usr/bin/env python3
import sys

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    import fastapi

    print("✓ FastAPI imported successfully")
except ImportError as e:
    print(f"✗ FastAPI import failed: {e}")

try:
    import uvicorn

    print("✓ Uvicorn imported successfully")
except ImportError as e:
    print(f"✗ Uvicorn import failed: {e}")

try:
    from web_api import app

    print("✓ Web API app imported successfully")
    print("Starting server on http://localhost:8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback

    traceback.print_exc()
