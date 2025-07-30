# 🔧 Troubleshooting Guide

## N-Dimensional Geometry Engine - Common Issues and Solutions

---

## 🧪 **Test Suite Issues** ✅ **RECENTLY RESOLVED**

### Test Runner Failures - Command Line Errors
**Problem**: `python run_tests.py` fails with command line argument errors:
- `Error: No such option: --dif (Possible options: --diff, --pyi)`
- `bandit -r . - json -o test-reports/bandit.json` fails
- `safety check --json --output test-reports/safety.json` fails

**Root Cause**: Incorrect command line arguments in `run_tests.py`

**Solution** ✅ **FIXED**:
1. **Fixed Black command**: Changed `--dif` to `--diff`
2. **Fixed isort command**: Changed `--dif` to `--diff`
3. **Fixed Bandit command**: Changed `-` to `-f` for JSON format
4. **Fixed Safety command**: Removed invalid `--output` parameter

### Missing Test Dependencies
**Problem**: `ImportError: No module named 'pytest'` or similar errors

**Root Cause**: Development dependencies not installed

**Solution** ✅ **FIXED**:
```bash
pip install pytest pytest-cov pytest-benchmark pytest-html
pip install pytest-asyncio mypy bandit safety scipy numpy
```

### Missing Test Files
**Problem**: `ERROR: file or directory not found: tests/test_tiling.py`

**Root Cause**: `test_tiling.py` file was missing from the test suite

**Solution** ✅ **FIXED**:
- Created comprehensive `tests/test_tiling.py` with 12 test functions
- All tiling tests now passing (12/12 ✅)
- Covers RegularTiling, HexagonalTiling, VoronoiTiling, TilingAnalyzer

### Pytest AsyncIO Plugin Missing
**Problem**: `ImportError: Error importing plugin "pytest_asyncio": No module named 'pytest_asyncio'`

**Root Cause**: `conftest.py` requires pytest_asyncio but it wasn't installed

**Solution** ✅ **FIXED**:
```bash
pip install pytest-asyncio
```

### SciPy Import Errors
**Problem**: `ImportError: libscipy_openblas-68440149.so: cannot open shared object file`

**Root Cause**: SciPy not properly installed or corrupted

**Solution** ✅ **FIXED**:
```bash
pip install scipy numpy
```

---

### 🚨 Web API Issues

#### Internal Server Error - Interactive Demo Not Working
**Problem**: When accessing the interactive demo, you get "Internal Server Error"

**Root Cause**: Web API server is not running or dependencies are missing

**Solution**:
1. **Check server status**:
   ```bash
   ps aux | grep "web_api" | grep -v grep
   ```

2. **If no server running, start it**:
   ```bash
   source venv/bin/activate
   python web_api.py
   ```

3. **If import errors occur, fix dependencies**:
   ```bash
   source venv/bin/activate
   pip install fastapi uvicorn numpy plotly pydantic python-multipart
   ```

#### ModuleNotFoundError: No module named 'fastapi'
**Problem**: Python can't find FastAPI or other required packages

**Root Cause**: Virtual environment is corrupted or dependencies not installed

**Solution**:
1. **Recreate virtual environment**:
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install essential packages**:
   ```bash
   pip install fastapi uvicorn numpy plotly pydantic python-multipart
   ```

3. **Verify installation**:
   ```bash
   python -c "import fastapi; print('FastAPI installed successfully')"
   ```

### 🐍 Virtual Environment Issues

#### Virtual Environment Corruption
**Problem**: `venv/bin/pip` shows syntax errors or import failures

**Root Cause**: Virtual environment files are corrupted

**Solution**:
1. **Remove corrupted venv**:
   ```bash
   rm -rf venv
   ```

2. **Create fresh virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install fastapi uvicorn numpy plotly pydantic python-multipart
   ```

#### System Python vs Virtual Environment
**Problem**: Dependencies installed in system Python but not in venv

**Root Cause**: Using system Python instead of virtual environment

**Solution**:
1. **Always activate venv first**:
   ```bash
   source venv/bin/activate
   ```

2. **Verify you're using venv Python**:
   ```bash
   which python
   # Should show: /path/to/2014_CS102/venv/bin/python
   ```

3. **Install packages in venv**:
   ```bash
   pip install fastapi uvicorn numpy plotly pydantic python-multipart
   ```

### 📦 Dependency Installation Issues

#### Installation Timeouts
**Problem**: `pip install` commands timeout or fail

**Root Cause**: Large packages or slow network

**Solution**:
1. **Install core packages first**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Install additional packages separately**:
   ```bash
   pip install numpy
   pip install plotly
   pip install pydantic python-multipart
   ```

3. **If still failing, use cached wheels**:
   ```bash
   pip install --no-deps fastapi uvicorn numpy plotly pydantic python-multipart
   ```

#### Externally Managed Environment Error
**Problem**: Can't install packages with system Python

**Root Cause**: Modern Python distributions prevent system-wide package installation

**Solution**:
1. **Always use virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Never use system Python for package installation**
3. **If absolutely necessary, use `--break-system-packages` (not recommended)**

### 🌐 Web Server Issues

#### Port Already in Use
**Problem**: Port 8000 is already occupied

**Solution**:
1. **Find what's using port 8000**:
   ```bash
   lsof -i :8000
   ```

2. **Kill the process if safe**:
   ```bash
   kill -9 <PID>
   ```

3. **Or use different port**:
   ```bash
   python web_api.py --port 8001
   ```

#### Server Starts but No Response
**Problem**: Server starts but web interface doesn't load

**Solution**:
1. **Check server logs**:
   ```bash
   python web_api.py
   # Look for startup errors
   ```

2. **Test API health endpoint**:
   ```bash
   curl http://localhost:8000/api/health
   ```

3. **Check if server is listening**:
   ```bash
   netstat -tuln | grep 8000
   ```

### 🔍 Verification Steps

#### Complete Server Verification
After resolving issues, verify everything works:

1. **Check Python environment**:
   ```bash
   source venv/bin/activate
   python --version
   which python
   ```

2. **Verify package installation**:
   ```bash
   python -c "import fastapi, uvicorn, numpy, plotly; print('All packages imported successfully')"
   ```

3. **Start server**:
   ```bash
   python web_api.py
   ```

4. **Test endpoints**:
   ```bash
   curl http://localhost:8000/api/health
   curl http://localhost:8000/api/docs
   ```

5. **Access web interface**:
   - Browser: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs

### 📊 Performance Issues

#### Slow Calculations
**Problem**: Geometry calculations taking too long

**Solution**:
1. **Ensure NumPy is installed**:
   ```bash
   pip install numpy
   ```

2. **For high dimensions (>50D), calculations are naturally slower**

3. **Run performance tests**:
   ```bash
   python run_tests.py performance
   ```

### 🔧 Quick Fix Commands

#### Reset Everything
```bash
# Nuclear option - reset entire environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn numpy plotly pydantic python-multipart
python web_api.py
```

#### Minimal Working Setup
```bash
# Minimal packages for basic functionality
source venv/bin/activate
pip install fastapi uvicorn numpy
python web_api.py
```

#### Debug Server Issues
```bash
# Run server with debug output
source venv/bin/activate
python -c "
import uvicorn
from web_api import app
uvicorn.run(app, host='0.0.0.0', port=8000, log_level='debug')
"
```

### 📋 Common Error Messages

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `ModuleNotFoundError: No module named 'fastapi'` | Missing dependencies | Install packages in venv |
| `Internal Server Error` | Server not running | Start `python web_api.py` |
| `Port 8000 already in use` | Port conflict | Use different port or kill process |
| `externally-managed-environment` | System Python usage | Use virtual environment |
| `Command 'pip' not found` | venv not activated | `source venv/bin/activate` |

---

## 🆘 Still Having Issues?

If these solutions don't work:

1. **Check system requirements**:
   - Python 3.9+ required
   - At least 1GB RAM for full functionality
   - 500MB disk space for dependencies

2. **Try the nuclear option**:
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn numpy plotly pydantic python-multipart
   ```

3. **Check for conflicting installations**:
   ```bash
   which python
   which pip
   pip list | grep fastapi
   ```

4. **Review the full error message** - often contains specific details about the issue

5. **For AI collaboration troubleshooting** - Reference the `ai_cognitive_framework_geometry_engine.json` file which contains detailed patterns of successful collaboration, common troubleshooting approaches, and escalation strategies used by the GeometryOracle AI instance.

Remember: Most issues are environment-related and can be resolved by recreating the virtual environment and reinstalling dependencies.