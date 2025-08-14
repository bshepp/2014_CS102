# N-Dimensional Geometry Engine - Deployment Guide

This guide covers deployment of the N-Dimensional Geometry Engine to production environments, following web standards and best practices.

## 🚀 Quick Start

### Prerequisites
- AWS Account with appropriate permissions
- Domain name (optional, for custom domain)
- GitHub repository with the code
- Python 3.11+ and Node.js 18+ installed locally

### Local Development
```bash
# Clone the repository
git clone https://github.com/bshepp/2014_CS102.git
cd geometry-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
python web_api.py

# Access the application
# API: http://localhost:8000/api/docs
# Web: http://localhost:8000/demo.html
```

## 🌳 Branch-Based Deployment Strategy

### Branch Structure
```
main (production)
├── develop (development)
│   ├── feature/new-features
│   └── bugfix/fixes
└── hotfix/critical-fixes
```

### Deployment Flow
1. **Feature Development**: `feature/branch` → `develop`
2. **Development Testing**: Push to `develop` → Auto-deploy to dev environment
3. **Production Promotion**: Auto-PR from `develop` → `main` → Deploy to production

### Environment URLs (Current Status: Aug 14, 2025)
- Development: local only (http://localhost:8000)
- Production: `gengine.darkforestlabs.com` associated in Amplify; DNS/SSL validation in progress. MCP/API custom domains pending.

## 🌐 AWS Deployment Options

### Option 1: Static Web + Lambda API (Frontend domain associated)

#### Architecture
- **Frontend**: Amplify static hosting (CloudFront) — custom domain associated; awaiting validation.
- **API**: AWS Lambda + API Gateway
- **Benefits**: Pay-per-request, automatic scaling, minimal maintenance
- **Cost**: ~$0.20 per million requests + data transfer

#### Steps

1. **Deploy Frontend to AWS Amplify**
```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Initialize Amplify
amplify init

# Add hosting
amplify add hosting

# Deploy
amplify publish
```

2. **Deploy API to Lambda**
```bash
# Install dependencies for Lambda
pip install -r requirements.txt -t lambda_package/
cp web_api.py lambda_package/
cp geometry_engine.py lambda_package/

# Add Lambda handler to web_api.py
echo "
from mangum import Mangum
handler = Mangum(app)
" >> lambda_package/web_api.py

# Create deployment package
cd lambda_package
zip -r ../api_deployment.zip .
cd ..

# Deploy using AWS CLI
aws lambda create-function \
  --function-name geometry-engine-api \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
  --handler web_api.handler \
  --zip-file fileb://api_deployment.zip \
  --timeout 30 \
  --memory-size 512

# Create API Gateway
aws apigatewayv2 create-api \
  --name geometry-engine-api \
  --protocol-type HTTP \
  --target arn:aws:lambda:REGION:ACCOUNT:function:geometry-engine-api
```

### Option 2: Full AWS ECS Deployment (Optional Path)

#### Architecture
- **Frontend**: CloudFront + S3
- **API**: ECS Fargate + Application Load Balancer
- **Database**: (Optional) Aurora Serverless v2
- **Benefits**: Always-on, consistent performance, full control
- **Cost**: ~$50-100/month minimum

#### Current Production Setup
Production custom domains are pending DNS/SSL cutover. ECS/ECR workflows exist, but backend deployment target is selected via `BACKEND_TYPE` variable (lambda or ecs). No public endpoints are live at `*.gengine.darkforestlabs.com` yet.

## 📋 Web Standards Compliance

### Security Headers
The API automatically adds these security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: geolocation=(), microphone=(), camera=()`

### CORS Configuration
Production CORS settings in `web_api.py`:
```python
ALLOWED_ORIGINS = [
    "https://localhost:8000",
    "https://www.localhost:8000",
    "http://localhost:8000",  # Development
]
```

### Accessibility
- WCAG 2.0 AA compliant
- All interactive elements have ARIA labels
- Keyboard navigation supported
- Screen reader compatible

## 🔧 Configuration Files

### amplify.yml
Controls AWS Amplify build and deployment:
- Frontend build steps
- Custom security headers
- Cache control settings

### .github/workflows/web-validate.yml
Automated validation pipeline:
- HTML5/CSS validation
- Accessibility testing (Pa11y)
- Security scanning
- Performance testing (Lighthouse)

### .pa11yrc
Accessibility testing configuration:
- WCAG 2.0 AA standard
- Chrome headless configuration
- Timeout and retry settings

## 📊 Monitoring & Maintenance

### Health Checks
- API Health (local): `GET /api/health` → 200
- Production health checks against custom domains are deferred until DNS is live.

### Performance Monitoring
```bash
# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s https://localhost:8000/api/health

# Run Lighthouse audit
lighthouse https://localhost:8000 --output html --view
```

### Log Analysis
```bash
# View CloudWatch logs (if using AWS)
aws logs tail /aws/ecs/geometry-engine --follow

# Local logs
tail -f server.log
```

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check `ALLOWED_ORIGINS` in `web_api.py`
   - Ensure frontend URL is included
   - Verify API Gateway CORS settings

2. **Performance Issues**
   - Check Lambda memory allocation (512MB minimum)
   - Monitor CloudWatch metrics
   - Enable API Gateway caching

3. **Deployment Failures**
   - Verify AWS credentials
   - Check IAM role permissions
   - Review CloudFormation/Amplify logs

### Rollback Procedure
```bash
# Amplify rollback
amplify env checkout prod
amplify publish

# Lambda rollback
aws lambda update-function-code \
  --function-name geometry-engine-api \
  --zip-file fileb://previous_version.zip
```

## 🔒 Security Best Practices

1. **Environment Variables**
   - Never commit secrets to git
   - Use AWS Secrets Manager or Parameter Store
   - Rotate credentials regularly

2. **API Rate Limiting**
   - Configure API Gateway throttling
   - Implement request quotas
   - Monitor for abuse patterns

3. **SSL/TLS**
   - Always use HTTPS in production
   - Enable HSTS headers
   - Use AWS Certificate Manager

## 📈 Scaling Considerations

### Auto-Scaling Configuration
```yaml
# ECS Service Auto-scaling
TargetTrackingScalingPolicy:
  TargetValue: 70.0
  PredefinedMetricType: ECSServiceAverageCPUUtilization
  ScaleInCooldown: 300
  ScaleOutCooldown: 60
```

### Performance Optimization
- Enable CloudFront caching for static assets
- Use API Gateway caching for repeated queries
- Implement database connection pooling
- Optimize Lambda cold starts

## 🎯 Production Checklist

- [ ] Security headers configured
- [ ] CORS settings updated for production
- [ ] SSL certificate installed
- [ ] Health checks passing
- [ ] Monitoring alerts configured
- [ ] Backup strategy implemented
- [ ] Rate limiting enabled
- [ ] Error tracking setup
- [ ] Documentation updated
- [ ] Team access configured

## 📚 Additional Resources

- [AWS Amplify Documentation](https://docs.amplify.aws/)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Web Security Guidelines](https://owasp.org/www-project-web-security-testing-guide/)
- [WCAG 2.0 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

For questions or issues, please refer to the project documentation or create an issue in the GitHub repository.