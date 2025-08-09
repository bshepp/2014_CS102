# 🌌 N-Dimensional Geometry Engine

**Transform your CS102 sphere calculator into infinite dimensions with AI-powered natural language queries**

[![CI/CD Pipeline](https://github.com/your-org/geometry-engine/workflows/CI/badge.svg)](https://github.com/your-org/geometry-engine/actions)
[![Web Standards](https://github.com/your-org/geometry-engine/workflows/Web%20Standards%20Validation/badge.svg)](https://github.com/your-org/geometry-engine/actions)
[![Production](https://img.shields.io/badge/Production-Live-brightgreen)](https://geometry-engine-api.com)
[![Development](https://img.shields.io/badge/Development-Live-blue)](https://dev.geometry-engine-api.com)

## 🚀 Quick Start

### Local Development
```bash
# Clone and setup
git clone https://github.com/your-org/geometry-engine.git
cd geometry-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
python web_api.py

# Access the application
# Web Interface: http://localhost:8000
# API Documentation: http://localhost:8000/api/docs
```

### Production URLs
- **Frontend**: https://geometry-engine-api.com
- **API**: https://api.geometry-engine-api.com
- **Development**: https://dev.geometry-engine-api.com

## 🌳 Branch Strategy & Deployment

### Development Workflow
```bash
# Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/your-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to GitHub (triggers CI/CD)
git push origin feature/your-feature

# Create PR to develop branch
# → Automatic testing and deployment to dev environment
```

### Production Deployment
1. **Push to `develop`** → Auto-deploy to https://dev.geometry-engine-api.com
2. **Auto-PR created** to `main` branch after successful dev deployment
3. **Review and merge PR** → Deploy to https://geometry-engine-api.com

See [BRANCH_STRATEGY.md](BRANCH_STRATEGY.md) for complete workflow details.

## 🧮 Features

### Core Capabilities
- **N-Dimensional Shapes**: Spheres, cubes, ellipsoids, simplices, pyramids (1D to 100D+)
- **AI-Powered Queries**: Natural language geometry interface
- **Interactive Visualizations**: Real-time 3D/4D rendering with Plotly
- **Mathematical Precision**: All formulas verified to machine precision
- **Original Java Integration**: Preserved and enhanced CS102 code

### Technical Excellence
- **253 Tests**: Comprehensive unit, integration, and performance tests across 6 modules
- **Test Coverage**: Core functionality thoroughly tested with pytest framework (65% coverage)
- **100% CI Success**: All GitHub Actions pipelines passing with comprehensive validation
- **Web Standards**: WCAG 2.0 AA compliant, HTML5 validated, security headers
- **CI/CD Pipeline**: Automated testing, deployment, and rollback capabilities
- **Production Ready**: AWS deployment with monitoring and scaling

## 📊 Architecture

### Frontend
- **HTML5/CSS3/JavaScript**: Interactive web interface
- **Plotly.js**: 3D/4D visualizations
- **Accessibility**: Full WCAG 2.0 AA compliance
- **Performance**: Lighthouse score >90

### Backend
- **FastAPI**: Production-ready Python API
- **N-Dimensional Engine**: 79,216 lines of geometry calculations
- **Security**: Comprehensive headers and CORS configuration
- **Deployment**: Supports both Lambda and ECS architectures

### CI/CD Pipeline
- **Branch-based**: `develop` → `main` promotion workflow
- **Automated Testing**: All validation suites run on every push
- **Environment Separation**: Isolated dev and production deployments
- **Web Validation**: HTML5, accessibility, performance, security checks
- **Rollback Capability**: Automatic rollback on deployment failure

## 📁 Project Structure

The project has been organized for clarity and production readiness:

### Core Files
- `geometry_engine.py` - N-dimensional geometry engine (2,221 lines)
- `web_api.py` - FastAPI web application (1,180 lines)
- `tests/` - Organized test suite (253 tests, 2,658 lines)
- `requirements.txt` - Production dependencies
- `Dockerfile` - Production containerization

### Documentation
- `README.md` - This file
- `CLAUDE.md` - Comprehensive AI assistant guide
- `INSTALLATION.md` - Setup instructions
- `TESTING.md` - Testing procedures

### Archive
Non-essential files have been moved to `.archive/` for cleaner organization:
- `.archive/legacy-tests/` - Standalone test files (replaced by organized `tests/`)
- `.archive/documentation/` - Framework docs, reference materials
- `.archive/development-artifacts/` - Config files, deployment scripts
- `.archive/cache/` - Java class files, Python cache
- `.archive/logs/` - Runtime logs

See [.archive/README.md](.archive/README.md) for restoration instructions.

## 📚 Documentation

### User Guides
- [DEPLOYMENT.md](DEPLOYMENT.md) - AWS deployment guide
- [BRANCH_STRATEGY.md](BRANCH_STRATEGY.md) - CI/CD workflow and branch management
- [TESTING.md](TESTING.md) - Testing framework and procedures
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions

### Technical Documentation
- [CLAUDE.md](CLAUDE.md) - Comprehensive project guide for AI assistant
- [API Documentation](https://api.geometry-engine-api.com/api/docs) - Interactive API docs
- [Cognitive Framework](config/ai_cognitive_framework_geometry_engine.json) - AI collaboration framework

## 🧪 Testing

```bash
# Run all tests
python run_tests.py

# Specific test categories  
python run_tests.py unit           # Unit tests
python run_tests.py integration    # API integration tests
python run_tests.py performance    # Performance benchmarks
python run_tests.py mathematical   # Mathematical accuracy

# Web standards validation
npm install -g @lhci/cli pa11y html5validator
lighthouse http://localhost:8000/demo.html
pa11y http://localhost:8000/demo.html
```

## 🌐 Web Standards Compliance

- ✅ **HTML5 Validation**: W3C compliant markup
- ✅ **Accessibility**: WCAG 2.0 AA with Pa11y testing
- ✅ **Performance**: Lighthouse performance budget >80
- ✅ **Security**: Comprehensive security headers
- ✅ **SEO**: Proper meta tags and Open Graph support

## 🚀 Deployment Environments

| Environment | Frontend | API | Branch | Auto-Deploy |
|-------------|----------|-----|---------|-------------|
| Local | http://localhost:8000 | http://localhost:8000/api | any | Manual |
| Development | https://dev.geometry-engine-api.com | https://api-dev.geometry-engine-api.com | develop | ✅ Yes |
| Production | https://geometry-engine-api.com | https://api.geometry-engine-api.com | main | ✅ After review |

## 🎯 Key Achievements

- **Complete Transformation**: From CS102 educational code to production system
- **100% CI/CD Success**: All GitHub Actions pipelines passing with comprehensive infrastructure fixes
- **Mathematical Precision**: All formulas verified to 1e-10 tolerance  
- **N-Dimensional Support**: Calculations up to 100+ dimensions
- **AI Integration**: Natural language geometry queries
- **Production Deployment**: Live AWS infrastructure with monitoring
- **Web Standards**: Full compliance with modern web standards
- **Comprehensive Testing**: 253 tests with systematic coverage across all components

## 🔧 Development

### Prerequisites
- Python 3.11+
- Node.js 18+ (for web validation tools)
- AWS CLI (for deployment)
- Git

### Environment Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install web validation tools
npm install -g @lhci/cli pa11y html5validator

# Setup pre-commit hooks (optional)
pre-commit install
```

### Configuration
- **Environment Settings**: `config/environments.json`
- **AWS Amplify**: `amplify.yml` and `amplify-branch-config.json`
- **Accessibility**: `.pa11yrc`
- **Performance**: `.lighthouserc.json`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch from `develop`
3. Make changes with tests
4. Ensure all CI checks pass
5. Create pull request to `develop`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🌌 Explore infinite dimensions with mathematical precision!**
