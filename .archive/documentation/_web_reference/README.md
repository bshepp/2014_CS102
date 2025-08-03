# Claude Web Deployment Templates

Battle-tested templates for Claude Code instances deploying static websites with professional CI/CD pipelines.

## 🚀 Quick Start

```bash
# 1. Copy templates to your project
cp -r templates/* /path/to/your/project/

# 2. Set up configuration files
cp .gitignore.template /path/to/your/project/.gitignore
cp .pa11yrc.template /path/to/your/project/.pa11yrc
cp amplify.yml.template /path/to/your/project/amplify.yml

# 3. Set up GitHub Actions workflow
mkdir -p /path/to/your/project/.github/workflows
cp validate.yml.template /path/to/your/project/.github/workflows/validate.yml

# 4. Customize placeholders
# Replace [YOUR_PROJECT_NAME], [your-domain.com], etc. in copied files

# 5. Initialize git and deploy
cd /path/to/your/project
git init
git add .
git commit -m "Initial deployment with Claude templates"
```

## 📚 Template Files

### Core Templates
- **`WEB_DEPLOYMENT_GUIDE.md`** - Complete deployment architecture guide
- **`validate.yml`** - Production GitHub Actions workflow (copy to `.github/workflows/`)
- **`LESSONS_LEARNED.md`** - 16+ battle-tested solutions to common problems
- **`PROJECT_STATUS.md`** - Deployment status tracking template

### Specialized Guides  
- **`AI_AGENT_CI_CHECKLIST.md`** - Systematic debugging methodology (17 sections, 762 lines)
- **`DARK_FOREST_LABS_AGENT_GUIDE.md`** - Multi-agent ecosystem coordination

### Configuration Files
- **`amplify.yml.template`** - AWS Amplify build configuration (copy to `amplify.yml`)
- **`validate.yml.template`** - GitHub Actions workflow (copy to `.github/workflows/validate.yml`)
- **`.gitignore.template`** - Comprehensive ignore patterns (copy to `.gitignore`)
- **`.pa11yrc.template`** - Accessibility testing configuration (copy to `.pa11yrc`)

## 🔧 Customization Required

**Search and replace these placeholders in all copied files:**

```bash
# Project identifiers
[YOUR_PROJECT_NAME] → Your actual project name
[your-domain.com] → Your domain
[your-github-org] → Your GitHub organization
[your-repo-name] → Your repository name

# Infrastructure identifiers  
[your-amplify-id] → Your Amplify app ID
[your-staging-url] → Your staging URL
[your-production-url] → Your production URL

# Development specifics
[your-local-dev-command] → Your local server command
[Your Additional Tech] → Your additional technologies
```

## ✅ Proven Solutions Included

These templates contain fixes for **16+ common deployment issues**:

1. ✅ **GitHub organization setup** and deploy key issues
2. ✅ **Window resize handling** in JavaScript applications  
3. ✅ **CSS validation false positives** (backdrop-filter)
4. ✅ **GitHub Actions workflow triggers** and branch strategy
5. ✅ **Security scanning** (prevented real token exposure)
6. ✅ **Lighthouse CI configuration** and artifact handling
7. ✅ **Pa11y accessibility testing** in CI environments
8. ✅ **Path structure validation** for different project layouts
9. ✅ **Container security vulnerabilities** (distroless migration)
10. ✅ **AWS CloudShell deployment** issues and networking
11. ✅ **ECS Fargate networking** and NAT Gateway troubleshooting
12. ✅ **Database configuration** security patterns
13. ✅ **Environment variable validation** and secret management
14. ✅ **Tool version compatibility** (Codecov v5, Pydantic v2)
15. ✅ **File encoding and tool compatibility** issues
16. ✅ **Systematic debugging methodology** for complex CI/CD failures

## 🎯 Supported Deployment Patterns

### Frontend Hosting
- **AWS Amplify** (primary pattern)
- **GitHub Pages** (alternative)
- **Netlify** (alternative)

### Backend Services  
- **ECS Fargate** (recommended)
- **Lambda Functions** (serverless)
- **EC2** (traditional hosting)

### Databases
- **Aurora Serverless v2** (recommended)
- **RDS** (traditional)
- **DynamoDB** (NoSQL)

## 🔒 Security Features

- **Comprehensive secret scanning** in CI/CD pipeline
- **Container security scanning** with Trivy and Snyk
- **SARIF report upload** to GitHub Security tab
- **Dependency vulnerability scanning** with Safety and Bandit
- **Automated security updates** via Dependabot patterns

## 🚀 CI/CD Pipeline Features

The `validate.yml` workflow provides:

- **HTML5 and CSS validation** with smart error filtering
- **Security scanning** for exposed secrets and vulnerabilities  
- **Performance testing** with Lighthouse CI (90+ scores)
- **Accessibility testing** with Pa11y (WCAG 2.0 AA)
- **Code quality analysis** for JavaScript and other languages
- **Browser compatibility checks** with polyfill recommendations
- **Parallel job execution** for faster feedback
- **Conditional external services** (Codecov, Snyk) that don't break workflows

## 🤝 For Claude Code Instances

### Usage Instructions
1. **Read the documentation first** - Check `WEB_DEPLOYMENT_GUIDE.md` for architecture overview
2. **Start with working templates** - Copy `validate.yml` for immediate CI/CD  
3. **Follow systematic debugging** - Use `AI_AGENT_CI_CHECKLIST.md` when issues arise
4. **Learn from experience** - Review `LESSONS_LEARNED.md` for context on solutions
5. **Track your progress** - Use `PROJECT_STATUS.md` to monitor deployment status

### Contributing Back
Found a new issue? Fixed a problem not covered here?

1. Document your solution in the **AI_AGENT_CI_CHECKLIST.md** format
2. Add the lesson learned to **LESSONS_LEARNED.md** 
3. Update **validate.yml** if workflow changes are needed
4. Submit improvements back to this repository

## 📈 Token Savings

These templates save **thousands of tokens** by preventing:
- Rediscovering the same 16+ common deployment issues
- Recreating CI/CD workflows from scratch  
- Re-debugging Pa11y Chrome sandbox configurations
- Re-learning AWS Amplify deployment patterns
- Rebuilding security scanning configurations

**Estimated savings: 5,000-10,000 tokens per deployment**

## 🏗 Architecture Standards

Templates follow established patterns:
- **Frontend**: AWS Amplify for static hosting
- **Backend**: ECS Fargate for APIs
- **Database**: Aurora Serverless v2  
- **CI/CD**: GitHub Actions + Amplify
- **Security**: Defense-in-depth with automated scanning
- **Monitoring**: Lighthouse + Pa11y + security reports

## 📞 Support

- **Issues**: Use GitHub Issues for template problems
- **Improvements**: Submit Pull Requests for enhancements
- **Questions**: Check `LESSONS_LEARNED.md` first for common solutions

---

**Generated by Dark Forest Labs Claude instances**  
*Battle-tested through real-world deployments*  
*Continuously updated with new solutions*

## 🌟 Success Stories

These templates have successfully deployed:
- **Dark Forest Labs main site** - Interactive particle animation with comprehensive CI/CD
- **UnCAPTCHA API** - Agent verification service with ECS Fargate
- **Q Studio** - Quantum computing natural language interface
- **Multiple static websites** with professional deployment pipelines

**Ready to save yourself hours of debugging?** Start with the Quick Start guide above! 🚀