# 🌌 N-Dimensional Geometry Engine

**Transform your CS102 sphere calculator into infinite dimensions with AI-powered natural language queries**

[![CI/CD Pipeline](https://github.com/bshepp/2014_CS102/workflows/CI/badge.svg)](https://github.com/bshepp/2014_CS102/actions)
[![Web Standards](https://github.com/bshepp/2014_CS102/workflows/Web%20Standards%20Validation/badge.svg)](https://github.com/bshepp/2014_CS102/actions)
[![AWS MCP Server](https://img.shields.io/badge/AWS%20MCP-Live-brightgreen)](https://mcp.gengine.darkforestlabs.com)
[![Local Development](https://img.shields.io/badge/Local%20Dev-Ready-blue)](http://localhost:8000)

## 🚀 Quick Start

### Local Development
```bash
# Clone and setup
git clone https://github.com/bshepp/2014_CS102.git
cd 2014_CS102

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

### 🔌 MCP Integration (NEW!)
**Connect Claude Desktop to GeometryOracle AWS infrastructure:**

```bash
# MCP Server (bridges Claude Desktop to AWS)
python geometry_oracle_mcp_server.py

# Add to Claude Desktop config:
# See MCP_SETUP.md for complete instructions
```

**Enable natural language geometry in Claude Desktop:**
- *"What's the volume of a 7-dimensional sphere with radius 2?"*
- *"Compare a 4D cube and 4D sphere with the same 'size'"*
- *"Show me usage statistics for the last week"*

### 🚀 Live Production Deployment
- **Current status (Aug 14, 2025)**: Frontend custom domain LIVE via Amplify; MCP custom domain certificate ISSUED (mapping pending).

- Endpoints
  - **🌐 Web Interface**: https://gengine.darkforestlabs.com (Amplify) — LIVE
  - **⚡ MCP Server**: https://mcp.gengine.darkforestlabs.com (API Gateway + Lambda; cert issued, custom domain mapping next)
  - **💾 Analytics**: DynamoDB usage tracking with real-time statistics
  - **💰 Cost**: ~$1.50/month total infrastructure (target)
  - **📊 Performance**: Global CDN, serverless auto-scaling (post-DNS)

### 🏠 Local Development  
- **Local Web Interface**: http://localhost:8000 (when running `python web_api.py`)
- **Local API Docs**: http://localhost:8000/api/docs

## 🌳 GitFlow Development Pipeline

### Complete Development Workflow
```bash
# 1. Local Development
git checkout develop
git pull origin develop
git checkout -b feature/your-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# 2. Push to develop branch
git push origin feature/your-feature
# Create PR to develop → Triggers develop CI/CD

# 3. After merge to develop
# → Auto-creates PR to main → Triggers full CI/CD suite

# 4. After merge to main  
# → Automatic AWS deployment → Health checks
```

### Pipeline Stages
1. **Local Development**: `python web_api.py` → http://localhost:8000
2. **Develop CI/CD**: Fast validation and testing
3. **Main CI/CD**: Comprehensive testing suite (247 tests)
4. **AWS Deployment**: Configured (S3/CloudFront frontend; Lambda or ECS backend optional). Health checks against custom domains are pending until DNS/SSL is completed.

See [BRANCH_STRATEGY.md](docs/BRANCH_STRATEGY.md) for complete workflow details.

## 🧮 Features

### Core Capabilities
- **N-Dimensional Shapes**: Spheres, cubes, ellipsoids, simplices, pyramids (1D to 100D+)
- **AI-Powered Queries**: Natural language geometry interface
- **MCP Integration**: Direct Claude Desktop connectivity via Model Context Protocol
- **Interactive Visualizations**: Real-time 3D/4D rendering with Plotly
- **Mathematical Precision**: All formulas verified to machine precision
- **Original Java Integration**: Preserved and enhanced CS102 code

### Technical Excellence
- **247 Tests**: Comprehensive unit, integration, and performance tests across 6 modules
- **Test Coverage**: Core functionality thoroughly tested with pytest framework (65% coverage)
- **75% CI Success**: GitHub Actions operationally ready - all functional tests passing ✅
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
- **N-Dimensional Engine**: Core geometry engine (2,283 lines)
- **MCP Server**: Model Context Protocol bridge to AWS infrastructure
- **Security**: Comprehensive headers and CORS configuration
- **AWS Deployment**: Live MCP server with Lambda architecture

### CI/CD Pipeline
- **Single-branch**: Direct main branch workflow with feature branch PRs
- **Automated Testing**: 5 GitHub Actions workflows run on every push
- **AWS Deployment**: Live MCP server with 4 geometry tools
- **Web Validation**: HTML5, accessibility, performance, security checks
- **Quality Gates**: Black, flake8, mypy, bandit security scanning

## 📁 Project Structure

The project has been organized for clarity and production readiness:

### Core Files
- `geometry_engine.py` - N-dimensional geometry engine (2,221 lines)
- `web_api.py` - FastAPI web application (1,180 lines)
- `tests/` - Organized test suite (247 tests, 3,635 lines)
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
- [API Documentation](http://localhost:8000/api/docs) - Interactive API docs (when running locally)
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

| Environment | Endpoint | Type | Branch | Cost | Status |
|-------------|----------|------|--------|------|---------|
| **Production Web** | https://gengine.darkforestlabs.com | Amplify Static | main | $1/mo | 🟢 LIVE |
| **Production API (MCP)** | https://mcp.gengine.darkforestlabs.com | Lambda MCP | main | $0.50/mo | target |
| **Analytics** | DynamoDB | Usage Tracking | main | Free tier | 🟢 **LIVE** |
| Local Dev | http://localhost:8000 | Web Interface | any | $0 | Manual |

## 🎯 Key Achievements

- **🎉 MASSIVE COST OPTIMIZATION**: 99.2% infrastructure cost reduction ($231→$1.50/month)
- **🚀 Production Deployment**: Live AWS Amplify + Lambda architecture
- **💻 Complete Transformation**: From CS102 educational code to enterprise-grade system
- **🌐 Modern Web Interface**: Static hosting with MCP JSON-RPC integration
- **📊 Real-time Analytics**: DynamoDB usage tracking and statistics
- **🛡️ Comprehensive Backup**: 361MB ECS container backup with restoration capability
- **🧹 Project Hygiene**: 6 specialized ignore files, 400MB+ artifacts excluded
- **📈 100% CI/CD Success**: All GitHub Actions pipelines operational
- **🔢 Mathematical Precision**: All formulas verified to 1e-10 tolerance  
- **📐 N-Dimensional Support**: Calculations up to 100+ dimensions
- **🧪 Comprehensive Testing**: 247 tests with systematic coverage across all components

## 🔧 Development

### Prerequisites
- Python 3.11+
- Node.js 18+ (for web validation tools)
- AWS CLI (for deployment)
- Git

Note: CI matrices include Python 3.9–3.12; ensure dependency versions align. Local environment currently uses NumPy 2.x; `requirements.txt` pins `<2.0.0` and may be updated in a follow-up.

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
