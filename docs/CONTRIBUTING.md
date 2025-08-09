# 🤝 Contributing to the N-Dimensional Geometry Engine

**Thank you for considering contributing to this project!**

This guide will help you understand how to contribute effectively to the N-Dimensional Geometry Engine project.

## 📋 **Table of Contents**

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Testing Requirements](#testing-requirements)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)
- [Community Guidelines](#community-guidelines)

---

## 🌟 **Code of Conduct**

We are committed to fostering a welcoming, inclusive, and harassment-free environment for all contributors. By participating in this project, you agree to abide by our code of conduct:

- **Be respectful**: Treat all community members with respect and kindness
- **Be constructive**: Provide helpful feedback and suggestions
- **Be collaborative**: Work together to improve the project
- **Be patient**: Understand that reviews and responses may take time

---

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.9+
- Java 11+
- Git
- Familiarity with N-dimensional geometry (helpful but not required)

### **First Steps**
1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Follow the installation guide** in [INSTALLATION.md](INSTALLATION.md)
4. **Run the test suite** to ensure everything works
5. **Create a feature branch** for your contribution

```bash
git clone https://github.com/yourusername/2014_CS102.git
cd 2014_CS102
git checkout -b feature/your-feature-name
```

---

## 🔧 **Development Setup**

### **Environment Setup**
```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install all dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional but recommended)
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

---

## 📝 **Contribution Guidelines**

### **Types of Contributions**

#### **1. Code Contributions**
- **Bug fixes**: Address issues in existing functionality
- **New features**: Add new geometric shapes or capabilities
- **Performance improvements**: Optimize algorithms or calculations
- **API enhancements**: Improve or extend the REST API

#### **2. Documentation Contributions**
- **API documentation**: Improve endpoint descriptions
- **User guides**: Create tutorials and examples
- **Code comments**: Add or improve inline documentation
- **Architecture documentation**: Explain system design

#### **3. Testing Contributions**
- **Unit tests**: Test individual components
- **Integration tests**: Test API endpoints
- **Performance tests**: Benchmark optimizations
- **Edge case tests**: Handle unusual inputs

#### **4. Infrastructure Contributions**
- **CI/CD improvements**: Enhance GitHub Actions workflow
- **Docker enhancements**: Improve containerization
- **Security improvements**: Address vulnerabilities
- **Build system**: Optimize development tools

### **Coding Standards**

#### **Python Code Standards**
- **PEP 8**: Follow Python style guidelines
- **Type hints**: Use type annotations for all functions
- **Docstrings**: Document all public functions and classes
- **Error handling**: Use appropriate exceptions
- **Testing**: Write tests for all new functionality

```python
def calculate_hypersphere_volume(radius: float, dimensions: int) -> float:
    """
    Calculate the volume of an n-dimensional hypersphere.
    
    Args:
        radius: The radius of the hypersphere
        dimensions: The number of dimensions
        
    Returns:
        The volume of the hypersphere
        
    Raises:
        ValueError: If radius is negative or dimensions < 1
    """
    if radius < 0:
        raise ValueError("Radius must be non-negative")
    if dimensions < 1:
        raise ValueError("Dimensions must be at least 1")
    
    # Implementation here
    return volume
```

#### **Java Code Standards**
- **Original CS102 code**: Minimize changes to preserve historical context
- **Documentation**: Add JavaDoc comments for new methods
- **Compatibility**: Ensure compatibility with existing functionality
- **Testing**: Test Java bridge functionality

#### **API Standards**
- **RESTful design**: Follow REST principles
- **Consistent responses**: Use standard response format
- **Error handling**: Provide meaningful error messages
- **Documentation**: Update API documentation for changes

---

## 🧪 **Testing Requirements**

### **Before Submitting**
All contributions must pass the following tests:

```bash
# Run all tests
python run_tests.py

# Check code formatting
black --check .
flake8 .

# Type checking
mypy .

# Security scanning
bandit -r .

# Test coverage
pytest --cov=. --cov-report=html
```

### **Test Categories**
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and workflows
- **Performance Tests**: Ensure no performance regressions
- **Mathematical Tests**: Verify mathematical accuracy

### **Writing Tests**
```python
import pytest
from geometry_engine import HyperSphere

class TestHyperSphere:
    def test_volume_calculation(self):
        """Test hypersphere volume calculation."""
        sphere = HyperSphere(radius=2.0, dimensions=3)
        expected_volume = (4/3) * math.pi * (2.0 ** 3)
        assert abs(sphere.volume - expected_volume) < 1e-10
    
    def test_invalid_radius(self):
        """Test error handling for invalid radius."""
        with pytest.raises(ValueError, match="Radius must be non-negative"):
            HyperSphere(radius=-1.0, dimensions=3)
```

---

## 📚 **Documentation Standards**

### **Code Documentation**
- **Docstrings**: Use Google-style docstrings
- **Type hints**: Include type annotations
- **Examples**: Provide usage examples
- **Mathematics**: Document formulas and algorithms

### **API Documentation**
- **Endpoint descriptions**: Clear, concise descriptions
- **Parameters**: Document all parameters and types
- **Examples**: Include request/response examples
- **Error codes**: Document possible error conditions

### **User Documentation**
- **Clear instructions**: Step-by-step guides
- **Examples**: Working code examples
- **Troubleshooting**: Common issues and solutions
- **Architecture**: System design explanations

---

## 🔄 **Pull Request Process**

### **Before Creating a Pull Request**
1. **Create a feature branch** from main
2. **Make your changes** following the guidelines
3. **Run the test suite** and ensure all tests pass
4. **Update documentation** if needed
5. **Test your changes** thoroughly

### **Pull Request Checklist**
- [ ] **Branch**: Created from latest main branch
- [ ] **Tests**: All tests pass locally
- [ ] **Documentation**: Updated if needed
- [ ] **Code quality**: Follows coding standards
- [ ] **Commit messages**: Clear and descriptive
- [ ] **PR description**: Explains changes and motivation

### **Pull Request Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review of code completed
- [ ] Documentation updated
- [ ] No new warnings or errors
```

### **Review Process**
1. **Automated checks**: GitHub Actions run tests
2. **Code review**: Maintainers review changes
3. **Feedback**: Address review comments
4. **Approval**: Maintainer approval required
5. **Merge**: Squash and merge to main

---

## 👥 **Community Guidelines**

### **Communication**
- **GitHub Issues**: Report bugs and request features
- **Pull Requests**: Contribute code changes
- **Discussions**: Ask questions and share ideas
- **Code Reviews**: Provide constructive feedback

### **Issue Guidelines**
- **Search existing issues** before creating new ones
- **Use issue templates** when available
- **Provide clear descriptions** and reproduction steps
- **Add relevant labels** and milestones

### **Bug Reports**
```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- Version: [e.g., 1.0.0]
```

### **Feature Requests**
```markdown
## Feature Description
Clear description of the proposed feature

## Motivation
Why is this feature needed?

## Proposed Implementation
How should this feature work?

## Alternatives Considered
Other approaches that were considered
```

---

## 🎯 **Development Areas**

### **High Priority**
- **Mathematical accuracy**: Improve precision of calculations
- **Performance optimization**: Faster algorithms for high dimensions
- **API enhancements**: New endpoints and features
- **Test coverage**: Increase test coverage to 95%+

### **Medium Priority**
- **Visualization improvements**: Better 3D/4D graphics
- **Documentation**: More examples and tutorials
- **Error handling**: Better error messages and validation
- **Security**: Enhanced input validation

### **Low Priority**
- **Code cleanup**: Refactoring and optimization
- **Build system**: Development tool improvements
- **Compatibility**: Support for older Python versions
- **Internationalization**: Multi-language support

---

## 🏆 **Recognition**

### **Contributors**
All contributors are recognized in:
- **README.md**: Listed in acknowledgments
- **CHANGELOG.md**: Mentioned in release notes
- **Git history**: Permanent record of contributions
- **Community**: Highlighted in discussions

### **Maintainers**
Active contributors may be invited to become maintainers with:
- **Review permissions**: Ability to review pull requests
- **Merge permissions**: Ability to merge approved changes
- **Issue management**: Ability to manage issues and labels
- **Release management**: Participation in release planning

---

## 📞 **Getting Help**

### **Resources**
- **Documentation**: [CLAUDE.md](CLAUDE.md), [TESTING.md](TESTING.md), [API_REFERENCE.md](API_REFERENCE.md)
- **Installation**: [INSTALLATION.md](INSTALLATION.md)
- **Examples**: Check `/tests/` directory for examples
- **API Docs**: http://localhost:8000/api/docs

### **Contact**
- **GitHub Issues**: Technical questions and bug reports
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code contributions and reviews

---

## 📈 **Project Roadmap**

### **Current Focus**
- **Stability**: Bug fixes and testing improvements
- **Performance**: Optimization for high-dimensional operations
- **Documentation**: Comprehensive guides and examples
- **API**: Feature completeness and consistency

### **Future Plans**
- **Deployment**: Production deployment capabilities
- **SDK**: Python and JavaScript client libraries
- **Visualization**: Advanced 3D/4D rendering
- **Machine Learning**: Integration with ML frameworks

---

**Thank you for contributing to the N-Dimensional Geometry Engine! Your contributions help make this project better for everyone. 🚀**

---

*For questions about contributing, please open an issue or start a discussion on GitHub.*