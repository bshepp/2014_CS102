# GeometryOracle MCP Server

**Advanced N-Dimensional Geometry MCP Server for AI Agents**  
*Transform Claude Desktop into an N-dimensional geometry powerhouse*

[![CI/CD Pipeline](https://github.com/bshepp/2014_CS102/workflows/CI/badge.svg)](https://github.com/bshepp/2014_CS102/actions)
[![AWS MCP Server](https://img.shields.io/badge/AWS%20MCP-Live-brightgreen)](https://s6ngc23inj.execute-api.us-east-1.amazonaws.com/prod/mcp)
[![Claude Desktop](https://img.shields.io/badge/Claude%20Desktop-Ready-blue)](https://claude.ai/desktop)

## Quick Start

### MCP Server Setup
```bash
# Clone and setup
git clone https://github.com/bshepp/2014_CS102.git
cd 2014_CS102

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test MCP server locally
python geometry_oracle_mcp_server.py

# Configure Claude Desktop (see MCP_SETUP.md for details)
```

### Available MCP Tools

Once configured with Claude Desktop, you get access to:

**calculate_hypersphere** - N-dimensional sphere calculations (1D to 100D+)  
**calculate_hypercube** - N-dimensional cube calculations  
**compare_shapes** - Multi-shape analysis and comparisons  
**get_usage_statistics** - Real-time server analytics  

**Natural language examples:**
- *"What's the volume of a 7-dimensional sphere with radius 2?"*
- *"Compare a 4D cube and 4D sphere with the same 'size'"*
- *"Show me usage statistics for the last week"*

### Live Production Infrastructure

- **MCP Server**: https://s6ngc23inj.execute-api.us-east-1.amazonaws.com/prod/mcp (AWS Lambda)
- **Analytics**: DynamoDB usage tracking with 34+ real usage entries
- **Cost**: ~$1.50/month total infrastructure 
- **Performance**: Serverless auto-scaling, sub-second response times

### Local Development  
- **Local MCP Server**: `python geometry_oracle_mcp_server.py`
- **Test Connectivity**: Validates AWS connection on startup

## GitFlow Development Pipeline

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
1. **Local Development**: `python geometry_oracle_mcp_server.py` → Claude Desktop integration
2. **Develop CI/CD**: Fast validation and testing
3. **Main CI/CD**: Comprehensive testing suite (247 tests)
4. **AWS Deployment**: Lambda MCP server with DynamoDB analytics

See [BRANCH_STRATEGY.md](docs/BRANCH_STRATEGY.md) for complete workflow details.

## Features

### Core Capabilities
- **N-Dimensional Shapes**: Spheres, cubes, ellipsoids, simplices, pyramids (1D to 100D+)
- **AI-Powered Queries**: Natural language geometry interface via MCP
- **Claude Desktop Integration**: Direct connectivity via Model Context Protocol
- **Mathematical Precision**: All formulas verified to machine precision
- **AWS Production Backend**: Serverless Lambda architecture with analytics
- **Original Java Integration**: Preserved and enhanced CS102 code

### Technical Excellence
- **247 Tests**: Comprehensive unit, integration, and performance tests across 6 modules
- **Test Coverage**: Core functionality thoroughly tested with pytest framework
- **CI/CD Pipeline**: Automated testing, deployment, and rollback capabilities
- **Production Ready**: AWS Lambda deployment with DynamoDB analytics
- **Security**: Comprehensive scanning with bandit and safety
- **Performance**: Sub-second response times for complex N-dimensional calculations

## Architecture

### MCP Server
- **Local Bridge**: `geometry_oracle_mcp_server.py` - Claude Desktop to AWS proxy
- **N-Dimensional Engine**: Core geometry engine (88KB, 2,283+ lines)
- **AWS Lambda**: Production MCP server with 4 active tools
- **Real-time Analytics**: DynamoDB usage tracking and statistics
- **Claude Desktop Integration**: Model Context Protocol compliance

### Infrastructure
- **AWS Lambda**: `geometry-oracle-mcp` function (Python 3.12)
- **API Gateway**: JSON-RPC 2.0 endpoint for MCP protocol
- **DynamoDB**: `geometry-oracle-mcp-prod-queries` analytics table
- **Cost Efficiency**: ~$1.50/month for serverless auto-scaling

### CI/CD Pipeline
- **Branch Strategy**: Feature branches → main with automated testing
- **Automated Testing**: GitHub Actions workflows for every push
- **AWS Deployment**: Live Lambda MCP server deployment
- **Quality Gates**: Black, flake8, mypy, bandit security scanning
- **Performance Testing**: Mathematical accuracy and calculation benchmarks

## Project Structure

The project has been organized for clarity and production readiness:

### Core Files
- `geometry_engine.py` - N-dimensional geometry engine (88KB, 2,283+ lines)
- `geometry_oracle_mcp_server.py` - MCP bridge to AWS infrastructure (284 lines)
- `tests/` - Comprehensive test suite (247 tests, 3,635+ lines)
- `requirements.txt` - MCP-focused dependencies
- `mcp-server/` - AWS Lambda deployment infrastructure

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

## Documentation

### User Guides
- [DEPLOYMENT.md](DEPLOYMENT.md) - AWS deployment guide
- [BRANCH_STRATEGY.md](BRANCH_STRATEGY.md) - CI/CD workflow and branch management
- [TESTING.md](TESTING.md) - Testing framework and procedures
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions

### Technical Documentation
- [CLAUDE.md](CLAUDE.md) - Comprehensive project guide for AI assistant
- [API Documentation](http://localhost:8000/api/docs) - Interactive API docs (when running locally)
- [Cognitive Framework](config/ai_cognitive_framework_geometry_engine.json) - AI collaboration framework

## Testing

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

## Web Standards Compliance

- **HTML5 Validation**: W3C compliant markup
- **Accessibility**: WCAG 2.0 AA with Pa11y testing
- **Performance**: Lighthouse performance budget >80
- **Security**: Comprehensive security headers
- **SEO**: Proper meta tags and Open Graph support

## Deployment Environments

| Environment | Endpoint | Type | Branch | Cost | Status |
|-------------|----------|------|--------|------|---------|
| **Production Web** | https://gengine.darkforestlabs.com | Amplify Static | main | $1/mo | LIVE |
| **Production API (MCP)** | https://mcp.gengine.darkforestlabs.com | Lambda MCP | main | $0.50/mo | target |
| **Analytics** | DynamoDB | Usage Tracking | main | Free tier | LIVE |
| Local Dev | http://localhost:8000 | Web Interface | any | $0 | Manual |

## Key Achievements

- **MASSIVE COST OPTIMIZATION**: 99.2% infrastructure cost reduction ($231→$1.50/month)
- **Production Deployment**: Live AWS Amplify + Lambda architecture
- **Complete Transformation**: From CS102 educational code to enterprise-grade system
- **Modern Web Interface**: Static hosting with MCP JSON-RPC integration
- **Real-time Analytics**: DynamoDB usage tracking and statistics
- **Comprehensive Backup**: 361MB ECS container backup with restoration capability
- **Project Hygiene**: 6 specialized ignore files, 400MB+ artifacts excluded
- **100% CI/CD Success**: All GitHub Actions pipelines operational
- **Mathematical Precision**: All formulas verified to 1e-10 tolerance  
- **N-Dimensional Support**: Calculations up to 100+ dimensions
- **Comprehensive Testing**: 247 tests with systematic coverage across all components

## Development

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

## Contributing

1. Fork the repository
2. Create feature branch from `develop`
3. Make changes with tests
4. Ensure all CI checks pass
5. Create pull request to `develop`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Explore infinite dimensions with mathematical precision!**
