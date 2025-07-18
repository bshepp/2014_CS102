# 🧪 Comprehensive Testing Guide
## N-Dimensional Geometry Engine Test Suite

This document provides a complete guide to testing the N-Dimensional Geometry Engine, covering all test types, configurations, and best practices.

## 📋 Table of Contents

- [Overview](#overview)
- [Test Architecture](#test-architecture)
- [Quick Start](#quick-start)
- [Test Categories](#test-categories)
- [Running Tests](#running-tests)
- [GitHub Actions CI/CD](#github-actions-cicd)
- [Docker Testing](#docker-testing)
- [Performance Testing](#performance-testing)
- [Mathematical Accuracy Testing](#mathematical-accuracy-testing)
- [API Testing](#api-testing)
- [Code Quality](#code-quality)
- [Coverage Reports](#coverage-reports)
- [Troubleshooting](#troubleshooting)

## Overview

The test suite is designed to ensure the reliability, accuracy, and performance of the N-Dimensional Geometry Engine across all supported platforms and use cases.

### Test Statistics
- **Total Tests**: 400+ comprehensive tests
- **Coverage Target**: 90%+ code coverage
- **Supported Platforms**: Linux, macOS, Windows
- **Python Versions**: 3.9, 3.10, 3.11, 3.12
- **Test Types**: Unit, Integration, Performance, Mathematical, API, Tiling

## Test Architecture

```
tests/
├── conftest.py                 # Test configuration and fixtures
├── test_core.py               # Core geometry engine tests
├── test_api_integration.py    # API endpoint tests
├── test_performance.py        # Performance benchmarks
├── test_mathematics.py        # Mathematical accuracy tests
├── test_tiling.py            # Tiling functionality tests
└── test_edge_cases.py        # Edge cases and error handling
```

## Quick Start

### Prerequisites

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install Java (for Java bridge testing)
# Ubuntu/Debian:
sudo apt-get install openjdk-11-jdk

# macOS:
brew install openjdk@11

# Windows:
# Download from https://adoptopenjdk.net/
```

### Run All Tests

```bash
# Run complete test suite
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test categories
pytest -m unit                 # Unit tests only
pytest -m integration          # Integration tests only
pytest -m performance          # Performance tests only
pytest -m mathematical         # Mathematical tests only
pytest -m api                  # API tests only
pytest -m tiling               # Tiling tests only
```

## Test Categories

### 🔧 Unit Tests (`test_core.py`)

Tests individual components in isolation:

```bash
# Run all unit tests
pytest tests/test_core.py -v

# Test specific shapes
pytest tests/test_core.py::TestHyperSphere -v
pytest tests/test_core.py::TestHyperCube -v
pytest tests/test_core.py::TestHyperEllipsoid -v
pytest tests/test_core.py::TestSimplex -v
pytest tests/test_core.py::TestHyperPyramid -v
```

**Coverage**:
- HyperSphere: Volume, surface area, scaling, containment
- HyperCube: Volume, surface area, vertices, edges, diagonal
- HyperEllipsoid: Volume, eccentricity, sphere detection
- Simplex: Volume, circumradius, inradius, height
- HyperPyramid: Volume, slant height, lateral edges
- GeometryAgent: Natural language processing
- JavaBridge: Original Java code integration

### 🌐 Integration Tests (`test_api_integration.py`)

Tests API endpoints and component interactions:

```bash
# Run all API tests
pytest tests/test_api_integration.py -v

# Test specific endpoints
pytest tests/test_api_integration.py::TestSphereEndpoint -v
pytest tests/test_api_integration.py::TestTilingEndpoint -v
pytest tests/test_api_integration.py::TestQueryEndpoint -v
```

**Coverage**:
- REST API endpoints (/api/sphere, /api/cube, /api/ellipsoid, etc.)
- Tiling API (/api/tiling)
- Natural language API (/api/query)
- Health check (/api/health)
- Error handling and validation
- Response format validation

### ⚡ Performance Tests (`test_performance.py`)

Benchmarks and scalability tests:

```bash
# Run performance tests
pytest tests/test_performance.py -v --benchmark-only

# Run scalability tests
pytest tests/test_performance.py::TestScalabilityLimits -v

# Run memory tests
pytest tests/test_performance.py::TestMemoryUsage -v

# Run concurrency tests
pytest tests/test_performance.py::TestConcurrency -v
```

**Coverage**:
- Shape creation performance
- Volume/surface area calculation benchmarks
- Tiling generation performance
- Memory usage analysis
- Concurrency testing
- High-dimensional shape handling
- Stress testing with large datasets

### 📐 Mathematical Accuracy Tests (`test_mathematics.py`)

Verifies mathematical correctness:

```bash
# Run mathematical accuracy tests
pytest tests/test_mathematics.py -v

# Test specific mathematical areas
pytest tests/test_mathematics.py::TestHyperSphereFormulas -v
pytest tests/test_mathematics.py::TestTilingMathematics -v
pytest tests/test_mathematics.py::TestGeometricRelationships -v
```

**Coverage**:
- Known mathematical formulas (circle area, sphere volume, etc.)
- Dimensional scaling laws
- Geometric relationships and theorems
- Numerical stability testing
- Edge case mathematical behavior
- High-precision calculations

### 🔲 Tiling Tests (`test_tiling.py`)

Tests tiling and tessellation functionality:

```bash
# Run tiling tests
pytest tests/test_tiling.py -v

# Test specific tiling types
pytest tests/test_tiling.py::TestRegularTiling -v
pytest tests/test_tiling.py::TestHexagonalTiling -v
pytest tests/test_tiling.py::TestVoronoiTiling -v
```

**Coverage**:
- Regular tiling patterns (square, triangular, hexagonal)
- Sphere packing algorithms
- Voronoi diagrams
- Tiling analysis and efficiency calculations
- Pattern symmetry detection
- N-dimensional space filling

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_core.py

# Run specific test class
pytest tests/test_core.py::TestHyperSphere

# Run specific test method
pytest tests/test_core.py::TestHyperSphere::test_hypersphere_volume
```

### Advanced Options

```bash
# Run tests in parallel
pytest -n auto

# Run tests with coverage
pytest --cov=. --cov-report=html --cov-report=term-missing

# Run tests with benchmark output
pytest --benchmark-only --benchmark-sort=mean

# Run tests with HTML report
pytest --html=report.html --self-contained-html

# Run tests with timeout
pytest --timeout=300

# Run tests excluding slow tests
pytest -m "not slow"

# Run tests requiring Java
pytest -m requires_java
```

### Test Selection

```bash
# Run by marker
pytest -m unit                 # Unit tests only
pytest -m integration          # Integration tests only
pytest -m performance          # Performance tests only
pytest -m mathematical         # Mathematical tests only
pytest -m "unit and not slow"  # Fast unit tests only
pytest -m "performance and benchmark"  # Performance benchmarks only

# Run by keyword
pytest -k "sphere"             # Tests containing "sphere"
pytest -k "tiling"             # Tests containing "tiling"
pytest -k "not java"           # Exclude Java-related tests
```

## GitHub Actions CI/CD

The repository includes a comprehensive GitHub Actions workflow (`.github/workflows/ci.yml`) that:

### Code Quality Pipeline
- **Black**: Code formatting validation
- **isort**: Import sorting validation
- **Flake8**: Linting and style checking
- **MyPy**: Type checking
- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency vulnerability checking
- **Pylint**: Advanced code analysis

### Multi-Platform Testing
- **Python Versions**: 3.9, 3.10, 3.11, 3.12
- **Operating Systems**: Ubuntu, Windows, macOS
- **Java Integration**: OpenJDK 11 testing
- **Coverage**: Codecov integration

### Specialized Test Jobs
- **API Integration**: Full REST API testing
- **Performance**: Benchmark validation
- **Mathematical**: Formula accuracy verification
- **Docker**: Container testing
- **Documentation**: Docstring testing

### Running CI Locally

```bash
# Install pre-commit hooks
pre-commit install

# Run all quality checks
pre-commit run --all-files

# Run specific checks
black --check .
flake8 .
mypy .
bandit -r .
safety check
```

## Docker Testing

### Build Test Container

```bash
# Build the test container
docker build -f Dockerfile.test -t geometry-engine-test .

# Run all tests in container
docker run --rm geometry-engine-test

# Run specific test category
docker run --rm geometry-engine-test pytest tests/test_core.py -v

# Get coverage report
docker run --rm -v $(pwd)/htmlcov:/app/htmlcov geometry-engine-test
```

### Docker Compose Testing

```yaml
# docker-compose.test.yml
version: '3.8'
services:
  test:
    build:
      context: .
      dockerfile: Dockerfile.test
    volumes:
      - ./htmlcov:/app/htmlcov
      - ./test-results.xml:/app/test-results.xml
    command: pytest tests/ -v --cov=. --cov-report=html --junit-xml=test-results.xml
```

```bash
# Run with docker-compose
docker-compose -f docker-compose.test.yml up --build
```

## Performance Testing

### Benchmark Configuration

```bash
# Basic benchmarking
pytest tests/test_performance.py --benchmark-only

# Detailed benchmark report
pytest tests/test_performance.py --benchmark-only --benchmark-sort=mean --benchmark-verbose

# Save benchmark results
pytest tests/test_performance.py --benchmark-only --benchmark-json=benchmark.json

# Compare with previous results
pytest tests/test_performance.py --benchmark-only --benchmark-compare
```

### Performance Limits

The test suite includes performance limits:
- **Max Response Time**: 1 second per operation
- **Max Memory Usage**: 100 MB per test
- **Max Dimension**: 20 dimensions
- **Max Tile Count**: 10,000 tiles

### Profiling

```bash
# Memory profiling
pytest tests/test_performance.py::TestMemoryUsage -v -s

# CPU profiling
pytest tests/test_performance.py --profile

# Line-by-line profiling
kernprof -l -v tests/test_performance.py
```

## Mathematical Accuracy Testing

### Verification Methods

1. **Known Values**: Test against textbook formulas
2. **Scaling Laws**: Verify dimensional scaling relationships
3. **Numerical Stability**: Test with extreme values
4. **Geometric Theorems**: Verify mathematical relationships

### Tolerance Settings

```python
# Default tolerance for floating-point comparisons
TOLERANCE = 1e-10

# High-precision tolerance
HIGH_PRECISION_TOLERANCE = 1e-15

# Geometric tolerance (for practical calculations)
GEOMETRIC_TOLERANCE = 1e-6
```

### Mathematical Test Coverage

- **2D Shapes**: Circle area, square area, ellipse properties
- **3D Shapes**: Sphere volume, cube volume, pyramid volume
- **N-D Shapes**: Hypersphere formulas, hypercube properties
- **Tiling**: Coverage efficiency, coordination numbers
- **Relationships**: Isoperimetric inequality, Euler characteristic

## API Testing

### Test Client Setup

```python
from fastapi.testclient import TestClient
from web_api import app

client = TestClient(app)
```

### Endpoint Testing

```bash
# Test all API endpoints
pytest tests/test_api_integration.py -v

# Test specific endpoint groups
pytest tests/test_api_integration.py::TestSphereEndpoint -v
pytest tests/test_api_integration.py::TestTilingEndpoint -v
pytest tests/test_api_integration.py::TestQueryEndpoint -v
```

### API Test Coverage

- **Shape Endpoints**: /api/sphere, /api/cube, /api/ellipsoid, /api/simplex, /api/pyramid
- **Tiling Endpoints**: /api/tiling (regular, hexagonal, voronoi)
- **Query Endpoints**: /api/query (natural language)
- **Utility Endpoints**: /api/health, /api/compare, /api/dimensions
- **Error Handling**: Invalid inputs, malformed requests
- **Response Validation**: Schema compliance, data accuracy

## Code Quality

### Quality Metrics

```bash
# Code formatting
black --check .
black --diff .

# Import sorting
isort --check-only --diff .

# Linting
flake8 --statistics .

# Type checking
mypy --strict .

# Security scanning
bandit -r . -f json

# Dependency scanning
safety check --json
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.0
    hooks:
      - id: mypy
```

## Coverage Reports

### Generating Coverage

```bash
# HTML coverage report
pytest --cov=. --cov-report=html

# Terminal coverage report
pytest --cov=. --cov-report=term-missing

# XML coverage report (for CI)
pytest --cov=. --cov-report=xml

# JSON coverage report
pytest --cov=. --cov-report=json
```

### Coverage Targets

- **Overall Coverage**: 90%+
- **Core Engine**: 95%+
- **API Endpoints**: 90%+
- **Mathematical Functions**: 98%+
- **Tiling Operations**: 85%+

### Viewing Coverage

```bash
# Open HTML report
open htmlcov/index.html          # macOS
xdg-open htmlcov/index.html      # Linux
start htmlcov/index.html         # Windows
```

## Troubleshooting

### Common Issues

#### Java Not Found
```bash
# Error: javac: command not found
# Solution: Install Java JDK
sudo apt-get install openjdk-11-jdk  # Ubuntu
brew install openjdk@11              # macOS
# Windows: Download from https://adoptopenjdk.net/

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

#### Import Errors
```bash
# Error: ModuleNotFoundError
# Solution: Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Or use development install
pip install -e .
```

#### Performance Test Failures
```bash
# Error: Test exceeded time limit
# Solution: Increase timeout or check system resources
pytest --timeout=600  # 10 minute timeout
```

#### Memory Issues
```bash
# Error: Memory limit exceeded
# Solution: Reduce test scope or increase limits
pytest -k "not memory"  # Skip memory tests
```

### Debug Mode

```bash
# Run tests with debug output
pytest -v -s --tb=long

# Run single test with debugging
pytest tests/test_core.py::test_specific_function -v -s --pdb

# Capture output
pytest --capture=no
```

### Test Selection for Debugging

```bash
# Run only fast tests
pytest -m "not slow"

# Run only unit tests
pytest -m unit

# Run without Java tests
pytest -m "not requires_java"

# Run specific functionality
pytest -k "sphere" -v
pytest -k "tiling" -v
pytest -k "api" -v
```

## Best Practices

### Writing Tests

1. **Use Descriptive Names**: Test names should describe what they test
2. **Follow AAA Pattern**: Arrange, Act, Assert
3. **Use Fixtures**: Leverage pytest fixtures for setup/teardown
4. **Test Edge Cases**: Include boundary conditions and error cases
5. **Mock External Dependencies**: Use mocks for network calls, file I/O
6. **Parameterize Tests**: Use pytest.mark.parametrize for multiple inputs

### Test Organization

1. **Group Related Tests**: Use test classes for related functionality
2. **Use Markers**: Mark tests by category (unit, integration, slow, etc.)
3. **Separate Concerns**: Keep unit tests separate from integration tests
4. **Test Independence**: Each test should be independent and idempotent

### Performance Considerations

1. **Use Benchmarks**: For performance-critical code
2. **Set Timeouts**: Prevent hanging tests
3. **Monitor Resources**: Check memory and CPU usage
4. **Profile Slow Tests**: Identify bottlenecks

## Contributing

### Running Tests Before Commit

```bash
# Run quality checks
pre-commit run --all-files

# Run fast tests
pytest -m "not slow" --maxfail=5

# Run full test suite
pytest --tb=short
```

### Adding New Tests

1. **Follow Naming Convention**: `test_*.py` files, `test_*` functions
2. **Add Appropriate Markers**: Use `@pytest.mark.unit`, etc.
3. **Include Documentation**: Add docstrings to test functions
4. **Update This Guide**: Add new test categories to documentation

## Conclusion

This comprehensive test suite ensures the reliability, accuracy, and performance of the N-Dimensional Geometry Engine. The combination of unit tests, integration tests, performance benchmarks, and mathematical accuracy verification provides confidence in the system's correctness across all supported platforms and use cases.

For questions or issues with testing, please refer to the troubleshooting section or open an issue on the repository.

---

**Happy Testing!** 🧪✨