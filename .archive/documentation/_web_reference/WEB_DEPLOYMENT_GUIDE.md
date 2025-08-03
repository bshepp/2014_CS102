# Web Deployment Guide

## Related Documentation
- **AI_AGENT_CI_CHECKLIST.md** - Systematic CI/CD issue debugging for AI agents (17 sections, 762 lines)
- **LESSONS_LEARNED.md** - Battle-tested solutions with human context (16+ problems solved)
- **validate.yml** - Production-ready GitHub Actions workflow template
- **PROJECT_STATUS.md** - Status tracking template with customization points

This file provides guidance for deploying static websites with professional CI/CD pipelines and AWS infrastructure.

## Overview

Template for deploying static websites with:
- Comprehensive CI/CD validation pipeline
- AWS Amplify hosting with custom domains
- Professional development workflow
- Security scanning and quality assurance

## Project Structure Template

```
[YOUR_PROJECT_NAME]/
├── index.html          # Main website file
├── .github/workflows/  # CI/CD pipeline
│   └── validate.yml    # Comprehensive validation checks
├── old/                # Version archive (optional)
├── venv/               # Python virtual environment (for tooling)
├── .gitignore         # Git exclusions
├── .pa11yrc           # Accessibility testing config
├── amplify.yml        # AWS Amplify build config
└── [content files]    # Your website assets
```

## Development Commands

For static HTML/CSS/JavaScript projects:

```bash
# Serve locally (Python 3)
python -m http.server 8000

# Serve locally (Python 2)
python -m SimpleHTTPServer 8000

# Serve locally (Node.js)
npx http-server
```

## Quality Assurance Pipeline

The included GitHub Actions workflow provides:

### 1. **Core Validation**
- HTML5 and CSS validation (with common false positive handling)
- Security scanning for exposed secrets
- File size limits for performance
- Required file structure checks

### 2. **Performance Testing**
- Lighthouse CI with configurable budgets
- Page load time monitoring
- Performance regression detection

### 3. **Accessibility Testing**
- WCAG 2.0 AA compliance validation
- Pa11y automated testing with Chrome sandbox configuration
- Color contrast validation

### 4. **Code Quality**
- JavaScript static analysis
- Error handling verification
- Best practices enforcement

### 5. **Browser Compatibility**
- Modern feature detection
- Compatibility recommendations

## Deployment Architecture

### Recommended AWS Stack:
- **Frontend Hosting**: AWS Amplify
- **Domain Management**: Route 53 hosted zones
- **Security**: AWS WAF (Web Application Firewall)
- **SSL Certificates**: AWS Certificate Manager (automatic)
- **CDN**: CloudFront (included with Amplify)

### Development Workflow:
- `develop` branch → Staging environment
- `main` branch → Production environment  
- All validation checks must pass before merge
- Automatic deployment on push

## Setup Instructions

### 1. Repository Setup
```bash
# Copy template files to your project
cp _web_reference/* [YOUR_PROJECT]/
cd [YOUR_PROJECT]

# Initialize git if needed
git init
git add .
git commit -m "Initial commit with web deployment template"
```

### 2. GitHub Repository
- Create repository: `[YOUR_GITHUB_ORG]/[YOUR_PROJECT]`
- Push code to repository
- GitHub Actions will run automatically

### 3. AWS Amplify Setup
- Connect GitHub repository to Amplify
- Enable automatic deployments
- Configure custom domain (optional)

### 4. Domain Configuration (Optional)
- Create Route 53 hosted zone
- Add domain to Amplify with redirect settings
- Update nameservers at domain registrar
- Enable AWS WAF protection

## Customization Points

### Update These Values:
- `[YOUR_PROJECT_NAME]` → Your actual project name
- `[YOUR_GITHUB_ORG]` → Your GitHub organization
- `[YOUR_DOMAIN]` → Your custom domain (if using)
- Repository URLs in documentation
- Company/project specific branding

### Configuration Files:
- **validate.yml**: Adjust validation rules for your needs
- **.gitignore**: Add project-specific exclusions
- **amplify.yml**: Modify build commands if needed
- **.pa11yrc**: Configure accessibility testing standards

## Common Issues & Solutions

Refer to `LESSONS_LEARNED.md` for detailed solutions to common deployment challenges including:

- CI/CD validation failures and fixes
- DNS propagation and domain setup
- Security scanning false positives
- Accessibility testing in GitHub Actions
- Performance optimization strategies

## Reference Files

- **LESSONS_LEARNED.md** - Proven solutions to common problems
- **PROJECT_STATUS.md** - Template for tracking deployment progress
- **validate.yml** - Battle-tested CI/CD pipeline
- **.gitignore** - Comprehensive exclusion rules
- **.pa11yrc** - Working accessibility test configuration

---

*This template was battle-tested through multiple production deployments and systematic debugging of 15+ common CI/CD issues. All configurations are proven to work in real-world scenarios.*