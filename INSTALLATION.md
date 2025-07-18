# 🛠️ Installation Guide

**Complete setup instructions for the N-Dimensional Geometry Engine**

## 📋 **Table of Contents**

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Installation](#detailed-installation)
- [Development Setup](#development-setup)
- [Docker Installation](#docker-installation)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## 🎯 **Prerequisites**

### **System Requirements**
- **Operating System**: Linux, macOS, or Windows 10+
- **Python**: 3.9 or higher
- **Java**: 11 or higher (for Java bridge functionality)
- **Memory**: 4GB RAM minimum (8GB recommended for high-dimensional operations)
- **Storage**: 500MB free space

### **Required Software**
- **Git**: For cloning the repository
- **Python**: With pip package manager
- **Java**: OpenJDK 11 or higher

---

## ⚡ **Quick Start**

### **1. Clone and Install**
```bash
# Clone the repository
git clone https://github.com/bshepp/2014_CS102.git
cd 2014_CS102

# Set up Python environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### **2. Run the Application**
```bash
# Start the web interface
python web_api.py

# Access at http://localhost:8000
# API docs at http://localhost:8000/api/docs
```

### **3. Test Installation**
```bash
# Run basic tests
python -m pytest tests/test_core.py -v

# Run all tests
python run_tests.py
```

---

## 🔧 **Detailed Installation**

### **Step 1: Install Python**

#### **Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### **macOS**
```bash
# Using Homebrew
brew install python

# Using MacPorts
sudo port install python39 +universal
```

#### **Windows**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and check "Add Python to PATH"
3. Verify installation: `python --version`

### **Step 2: Install Java**

#### **Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install openjdk-11-jdk

# Verify installation
java --version
javac --version
```

#### **macOS**
```bash
# Using Homebrew
brew install openjdk@11

# Add to PATH
echo 'export PATH="/usr/local/opt/openjdk@11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### **Windows**
1. Download OpenJDK from [Adoptium](https://adoptium.net/)
2. Install and add to PATH
3. Set JAVA_HOME environment variable

### **Step 3: Clone Repository**
```bash
git clone https://github.com/bshepp/2014_CS102.git
cd 2014_CS102
```

### **Step 4: Set Up Python Environment**

#### **Create Virtual Environment**
```bash
python -m venv venv
```

#### **Activate Virtual Environment**
```bash
# Linux/macOS
source venv/bin/activate

# Windows Command Prompt
venv\Scripts\activate

# Windows PowerShell
venv\Scripts\Activate.ps1
```

#### **Upgrade pip**
```bash
pip install --upgrade pip
```

### **Step 5: Install Dependencies**

#### **Production Dependencies**
```bash
pip install -r requirements.txt
```

#### **Development Dependencies (Optional)**
```bash
pip install -r requirements-dev.txt
```

#### **Dependencies Overview**
- **FastAPI**: Web framework for API
- **Uvicorn**: ASGI server
- **NumPy**: Numerical computing
- **Plotly**: Interactive visualizations
- **Pydantic**: Data validation
- **Anthropic**: AI integration (optional)

---

## 🔬 **Development Setup**

### **Additional Development Tools**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional)
pre-commit install
```

### **Development Dependencies**
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **pytest-benchmark**: Performance testing
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking
- **bandit**: Security scanning

### **IDE Setup**

#### **VS Code**
1. Install Python extension
2. Install Java Extension Pack
3. Configure Python interpreter to use venv
4. Install recommended extensions:
   - Python
   - Pylance
   - Python Test Explorer
   - autoDocstring

#### **PyCharm**
1. Open project directory
2. Configure Python interpreter (venv)
3. Install plugins:
   - Python
   - Markdown
   - Docker (optional)

---

## 🐳 **Docker Installation**

### **Using Docker (Recommended for Testing)**

#### **Build Test Environment**
```bash
# Build Docker image
docker build -f Dockerfile.test -t geometry-engine-test .

# Run all tests
docker run --rm geometry-engine-test

# Run specific test category
docker run --rm geometry-engine-test pytest tests/test_core.py -v
```

#### **Get Test Reports**
```bash
# Mount volume for reports
docker run --rm -v $(pwd)/test-reports:/app/test-reports geometry-engine-test
```

### **Docker Compose (Optional)**
```yaml
# docker-compose.yml
version: '3.8'
services:
  geometry-engine:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - PYTHONPATH=/app
```

```bash
# Run with Docker Compose
docker-compose up
```

---

## ✅ **Verification**

### **1. Basic Functionality Test**
```bash
# Test Python import
python -c "import geometry_engine; print('✅ Python engine OK')"

# Test Java compilation
javac Sphere.java MultiSphere.java
java MultiSphere
```

### **2. Web Interface Test**
```bash
# Start web server
python web_api.py &

# Test API endpoint
curl http://localhost:8000/api/health

# Expected response:
# {"success": true, "data": {"status": "healthy", ...}}
```

### **3. Comprehensive Test Suite**
```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py unit
python run_tests.py integration
python run_tests.py performance
```

### **4. Interactive Testing**
```bash
# Open Python REPL
python

# Test geometry engine
>>> from geometry_engine import HyperSphere
>>> sphere = HyperSphere(radius=2.0, dimensions=4)
>>> print(f"Volume: {sphere.volume}")
Volume: 39.4784...
```

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **1. Python Import Errors**
```bash
# Error: ModuleNotFoundError
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install missing dependencies
pip install -r requirements.txt
```

#### **2. Java Compilation Errors**
```bash
# Error: javac: command not found
# Solution: Install Java and add to PATH

# Linux/Mac
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Windows
set JAVA_HOME=C:\Program Files\Java\jdk-11
set PATH=%JAVA_HOME%\bin;%PATH%
```

#### **3. Permission Errors**
```bash
# Linux/Mac: Fix permissions
chmod +x venv/bin/activate
chmod +x *.py

# Windows: Run as administrator if needed
```

#### **4. Port Already in Use**
```bash
# Error: Address already in use
# Solution: Use different port
python web_api.py --port 8001

# Or kill existing process
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### **5. Memory Issues**
```bash
# For high-dimensional operations
export PYTHONHASHSEED=0
python -Xms512m -Xmx2g web_api.py
```

### **Performance Optimization**

#### **1. System Configuration**
```bash
# Increase memory limits
ulimit -v 8388608  # 8GB virtual memory

# Optimize Python
export PYTHONOPTIMIZE=1
export PYTHONDONTWRITEBYTECODE=1
```

#### **2. Dependency Optimization**
```bash
# Install optimized NumPy
pip install numpy[mkl]

# Use faster JSON parser
pip install ujson
```

---

## 📞 **Getting Help**

### **Documentation**
- **API Reference**: [API_REFERENCE.md](API_REFERENCE.md)
- **Testing Guide**: [TESTING.md](TESTING.md)
- **Architecture**: [CLAUDE.md](CLAUDE.md)

### **Interactive Documentation**
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### **Support Channels**
- **GitHub Issues**: [Report problems](https://github.com/bshepp/2014_CS102/issues)
- **Discussions**: [Community support](https://github.com/bshepp/2014_CS102/discussions)

---

## 🔄 **Update Instructions**

### **Update to Latest Version**
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run tests to verify
python run_tests.py
```

### **Version Management**
```bash
# Check current version
python -c "import geometry_engine; print(geometry_engine.__version__)"

# List available versions
git tag -l
```

---

## 🎉 **Next Steps**

After successful installation:

1. **Explore the API**: Visit http://localhost:8000/api/docs
2. **Run Examples**: Try the code examples in [API_REFERENCE.md](API_REFERENCE.md)
3. **Read Documentation**: Check [CLAUDE.md](CLAUDE.md) for architecture details
4. **Run Tests**: Execute `python run_tests.py` to verify everything works
5. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines

---

**Installation complete! Your N-Dimensional Geometry Engine is ready to use. 🚀**