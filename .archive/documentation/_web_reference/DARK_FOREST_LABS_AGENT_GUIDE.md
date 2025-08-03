# Dark Forest Labs - Agent Coordination Guide

This document provides specific guidance for Claude Code agents working on Dark Forest Labs properties and subdomains.

## Ecosystem Overview

Dark Forest Labs operates multiple AI-focused products across various subdomains:

- **Main Site**: `darkforestlabs.com` - Company website with particle animation
- **Q Studio**: `qstudio.darkforestlabs.com` - Quantum computing + NLP interface  
- **UnCAPTCHA**: `uncaptcha.darkforestlabs.com` - Agent verification API (excludes humans and bots)
- **API Gateway**: `api.darkforestlabs.com` - Unified API endpoint for all services

## Coordination Protocol

### Primary Architect: Main Site Claude
The Claude instance working on the main `darkforestlabs.com` site serves as the **Lead Architect and Standardization Authority** responsible for:

- Architectural standardization across all properties
- Design system consistency and unified visual identity
- Infrastructure decisions and deployment strategy consensus
- Cross-product integration standards and API design patterns
- Documentation maintenance for shared resources

### Product-Specific Claudes
Each subdomain/product has its own specialized Claude instance:

- **Q Studio Claude**: Quantum computing natural language interface
- **UnCAPTCHA Claude**: Agent verification API development
- **[Your Product] Claude**: [Your specific domain expertise]

## Shared Infrastructure Standards

### Established Architecture Decisions:
- **Frontend Hosting**: AWS Amplify for all static sites
- **Backend Services**: ECS Fargate for all APIs
- **Database**: Aurora Serverless v2
- **Load Balancing**: Single ALB serving all subdomains
- **CI/CD Pipeline**: Standardized GitHub Actions workflow (see `validate.yml`)

### Visual Identity Standards:
- **Core Element**: Particle system animation (variations encouraged)
- **Color Scheme**: Agent-friendly with Matrix-style green (#0f0) elements
- **Typography**: Modern, clean fonts with good accessibility
- **Agent Discovery**: Hidden features for technical users and AI agents

### Agent-First Design Principles:
- All APIs must include agent discovery features
- Semantic HTML with microdata for agent parsing
- Console messages with API documentation hints
- Response headers indicating agent-friendly endpoints
- WebSocket support where applicable for real-time features

## Development Standards

### Git Workflow:
- Use `develop` → `main` branch strategy
- All validation checks must pass before merge
- Follow established commit message conventions

### Quality Assurance:
Copy the proven CI/CD pipeline from main site:
- HTML5 and CSS validation
- Security scanning for exposed secrets
- Performance testing with Lighthouse CI
- Accessibility testing with Pa11y
- Code quality analysis

### Documentation Requirements:
Each product should maintain:
- **PROJECT_STATUS.md** - Current deployment status
- **LESSONS_LEARNED.md** - Product-specific learnings
- **API_DOCUMENTATION.md** - Agent-friendly API docs
- **DEPLOYMENT_GUIDE.md** - Setup instructions

## Cross-Product Integration

### API Design Patterns:
- RESTful endpoints with consistent naming
- Agent discovery endpoint: `/api/v1/agent/discover`
- Product capabilities manifest at `/api/v1/capabilities`
- WebSocket support at `/api/v1/ws/[feature]`

### Shared Services:
- Authentication through main site if applicable
- Logging and monitoring through shared infrastructure
- Error reporting and alerting coordination

### Domain Structure:
```
darkforestlabs.com/           # Main company site
├── www.darkforestlabs.com/   # Canonical website URL
├── api.darkforestlabs.com/   # Unified API gateway
├── qstudio.darkforestlabs.com/     # Quantum computing interface
├── uncaptcha.darkforestlabs.com/   # Agent verification API
└── [your-product].darkforestlabs.com/ # Your product subdomain
```

## Communication Protocol

### Decision Making:
1. **Product-specific decisions**: Handle autonomously within established standards
2. **Cross-product changes**: Coordinate with Main Site Claude first
3. **Infrastructure changes**: Require consensus from all affected Claudes
4. **Security updates**: Immediate implementation, then coordinate

### Documentation Updates:
- Update your product-specific docs immediately
- Share significant learnings with main site for central LESSONS_LEARNED.md
- Coordinate major architectural changes through main site

### Emergency Coordination:
- Security issues: Implement fix immediately, then coordinate
- Infrastructure failures: Check with main site for ecosystem-wide impact
- Major updates: Plan rollout strategy together

## Agent Discovery Features

### Standard Implementation:
All Dark Forest Labs properties should include:

```html
<!-- Agent Discovery Metadata -->
<meta name="dark-forest-api" content="https://api.darkforestlabs.com/v1">
<meta name="agent-capabilities" content="[your-specific-capabilities]">
```

```javascript
// Agent-friendly console messages
console.log(`
╔═══════════════════════════════════════╗
║        DARK FOREST LABS LLC           ║
║    [Your Product Name]                ║
║                                       ║
║ API Docs: [your-api-docs-url]         ║
║ Agent Discovery: [your-discovery-endpoint] ║
╚═══════════════════════════════════════╝
`);
```

### Response Headers:
```
X-Agent-Friendly: true
X-API-Docs: [your-api-docs-url]
X-Capabilities: [comma-separated-capabilities]
X-Dark-Forest-Product: [your-product-name]
```

## Deployment Checklist

Before deploying your Dark Forest Labs subdomain:

- [ ] Copy and customize the proven CI/CD pipeline (`validate.yml`)
- [ ] Implement agent discovery features
- [ ] Add consistent visual elements (particle system variation)
- [ ] Configure custom subdomain with SSL
- [ ] Set up monitoring and logging
- [ ] Document API endpoints for agent consumption
- [ ] Test cross-product integration points
- [ ] Coordinate with Main Site Claude for final review

## Resources

### Template Files:
- `validate.yml` - Proven CI/CD pipeline
- `.gitignore` - Comprehensive exclusion rules
- `.pa11yrc` - Accessibility testing configuration
- `amplify.yml` - Basic Amplify build config

### Reference Documentation:
- `LESSONS_LEARNED.md` - 16+ proven solutions to common problems
- `WEB_DEPLOYMENT_GUIDE.md` - General web deployment template
- Main site repository for architectural patterns

### Quick Start:
```bash
# Copy proven templates to your project
cp _web_reference/* [your-subdomain-project]/

# Customize for your product
# Update domain references, product names, API endpoints
# Modify validation rules as needed for your tech stack

# Deploy following established patterns
```

---

**Remember**: We're building a cohesive ecosystem of AI-focused products. Consistency in infrastructure, security, and agent-friendliness across all properties strengthens the entire Dark Forest Labs brand and technical platform.

*This coordination has been proven through successful multi-agent collaboration on the main site deployment.*