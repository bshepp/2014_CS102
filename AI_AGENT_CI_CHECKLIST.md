# AI Agent CI/CD Configuration Checklist

## Purpose
This document helps AI agents identify and fix common CI/CD configuration issues, particularly path mismatches between assumed project structures and actual implementations.

## Critical Path Verification Checklist

### 1. Test Directory Structure Analysis

**Problem**: AI agents often assume tests are in `tests/` but they may be in `src/tests/`, `test/`, or other locations.

**Check Steps:**
1. **Scan actual project structure:**
   ```bash
   find . -name "*test*" -type f | grep -v "__pycache__" | grep -v ".pyc"
   find . -name "*test*" -type d
   ls -la src/ | grep test
   ```

2. **Verify test locations in:**
   - `.github/workflows/*.yml` - All pytest, coverage, and linting commands
   - `.github/codeql/codeql-config.yml` - CodeQL analysis paths
   - `README.md` - Example commands and documentation
   - `pyproject.toml` or `setup.cfg` - Test configuration
   - `pytest.ini` or `conftest.py` - Pytest configuration

3. **Common incorrect patterns to fix:**
   ```yaml
   # WRONG - Assumes top-level tests/
   pytest tests/ -v --cov=src
   black --check --diff src/ tests/
   flake8 src/ tests/
   
   # CORRECT - Use actual test location
   pytest src/tests/ -v --cov=src
   black --check --diff src/
   flake8 src/
   ```

### 2. Directory Path Consistency

**Check these files for path consistency:**

#### GitHub Actions Workflows (`.github/workflows/*.yml`)
- [ ] `pytest` commands use correct test directory
- [ ] `black` formatter paths are correct
- [ ] `isort` import sorting paths are correct  
- [ ] `flake8` linting paths are correct
- [ ] `mypy` type checking paths are correct
- [ ] Security scanning tools (`bandit`, `semgrep`) use correct paths

### 3. Missing Dependencies Check

**Problem**: Common dependencies may be missing from `requirements.txt` causing runtime failures.

**Check Steps:**
1. **Verify Redis async client dependencies:**
   ```bash
   # Check if async_timeout is in requirements.txt
   grep -q "async-timeout" requirements.txt || echo "Missing async_timeout dependency"
   ```

2. **Common missing dependencies:**
   ```txt
   # For Redis async client
   async-timeout==4.0.3
   
   # For cryptographic operations
   cryptography>=3.4.8
   
   # For Pydantic v2 migration
   pydantic-settings>=2.0.0
   ```

3. **Test dependency resolution:**
   ```bash
   # Build test Docker container to catch missing deps
   docker build -t test-deps .
   docker run --rm test-deps python -c "import asyncio; import async_timeout; print('Dependencies OK')"
   ```

### 4. Verification Engine Logic Issues

**Problem**: Eigenvalue verification may fail due to numerical precision and complex number handling.

**Check Steps:**
1. **Verify eigenvalue comparison logic:**
   ```python
   # Check if eigenvalue verification handles complex numbers and proper tolerances
   # File: src/core/verification_engine.py
   # Method: _verify_eigenvalue_solution
   ```

2. **Common fixes needed:**
   ```python
   # Use np.sort_complex for proper complex eigenvalue sorting
   submitted_sorted = np.sort_complex(submitted_eigenvalues)
   expected_sorted = np.sort_complex(expected_eigenvalues)
   
   # Increase tolerance for numerical precision issues
   tolerance = expected.get("tolerance", 0.01)  # Was 0.001
   
   # Handle complex eigenvalues properly
   submitted_eigenvalues = np.array(solution, dtype=complex)
   ```

3. **Classification logic improvements:**
   ```python
   # Don't immediately fail incorrect solutions - check behavioral patterns
   if not solution_correct:
       if behavioral_classification == "ai" and behavioral_confidence > 0.7:
           return "ai", 0.6  # Lower confidence but still AI classification
   ```
- [ ] Coverage report generation uses correct test paths

#### CodeQL Configuration (`.github/codeql/codeql-config.yml`)
- [ ] `paths:` section includes actual test directory
- [ ] `paths-ignore:` patterns match actual structure

#### Documentation Files
- [ ] `README.md` example commands use correct paths
- [ ] Test running instructions are accurate
- [ ] Development setup guides reference correct directories

### 3. Common CI/CD Command Syntax Issues

**Check for these common command syntax problems:**

#### cyclonedx-py (SBOM Generation)
```bash
# WRONG - Tool doesn't support --format flag
cyclonedx-py requirements -i requirements.txt -o sbom.json --format json

# CORRECT - Format determined by file extension  
cyclonedx-py requirements -i requirements.txt -o sbom.json
```

#### GitHub Actions Conditionals
```yaml
# WRONG - Invalid conditional syntax
if: always() && secrets.TOKEN_NAME

# CORRECT - Simplified conditional
if: always()
# Or use proper exists check if needed
```

#### Codecov Action Versions
```yaml
# OUTDATED - Use latest version
uses: codecov/codecov-action@v4

# CURRENT - Latest version with explicit repo
uses: codecov/codecov-action@v5
with:
  slug: owner/repo-name
```

### 4. Security Scanning Tool Configurations

**Verify these security tools are properly configured:**

#### Container Security Scanning
- [ ] Trivy commands use correct image references
- [ ] Snyk integration properly configured with tokens
- [ ] SARIF uploads reference correct file paths
- [ ] Container build contexts are correct

#### Python Security Tools
- [ ] Bandit scans correct source directories
- [ ] Safety checks run properly  
- [ ] Semgrep configurations target right paths
- [ ] Security report file paths match .gitignore patterns

### 5. Package Manager and Dependencies

**Check for version compatibility issues:**

#### Pydantic Migrations
- [ ] Pydantic v2 compatibility (`pydantic-settings` imports)
- [ ] Field validators use `@field_validator` with `@classmethod`
- [ ] Model configuration uses `model_config` dict syntax

#### Tool Version Updates
- [ ] GitHub Actions use current versions (checkout@v4, setup-python@v5, etc.)
- [ ] Security scanning tools use latest stable versions
- [ ] Python package versions are compatible

### 6. .gitignore Completeness

**Ensure .gitignore covers all generated files:**

```gitignore
# Security Reports  
*.sarif
bandit-report.json
safety-report.json
semgrep-report.json
trivy-results.sarif
snyk.sarif

# SBOM Files
sbom-*.json
sbom-*.xml
sbom.spdx.json
sbom-container.spdx.json

# Coverage Reports
coverage.xml
.coverage
.coverage.*
htmlcov/

# Build Artifacts
dist/
build/
*.egg-info/
```

## Verification Commands

**Run these commands to verify configurations:**

```bash
# Check test discovery
python -m pytest --collect-only

# Verify linting tools find files
black --check --diff src/
flake8 src/
mypy src/

# Test coverage generation
pytest src/tests/ --cov=src --cov-report=term-missing

# Validate workflow syntax
yamllint .github/workflows/*.yml
```

## Instructions for AI Agents

**When reviewing or setting up CI/CD configurations:**

1. **Always scan actual project structure first** - Don't assume standard layouts
2. **Verify every path reference** in workflows, configs, and documentation
3. **Test command syntax** against current tool versions and APIs
4. **Check for breaking changes** in security tools and GitHub Actions
5. **Validate .gitignore completeness** for all generated artifacts

### Self-Improvement Instructions

**AI Agent: Please append additional issues you discover to this checklist.**

**Template for additions:**
```markdown
### X. [Issue Category Name]

**Problem**: [Brief description of the issue]

**Check Steps:**
1. [Specific verification steps]
2. [Commands to run]
3. [Files to check]

**Common patterns to fix:**
```[language]
# WRONG
[incorrect example]

# CORRECT  
[corrected example]
```

**Verification:**
- [ ] [Checklist item 1]
- [ ] [Checklist item 2]
```

## Common Project Structure Variations

**Be aware these structures exist:**

```
# FastAPI with src/ layout (this project)
src/
├── api/
├── tests/
└── models/

# Django standard
myproject/
├── myapp/
└── tests/

# Standard Python package
package_name/
tests/

# Poetry/modern Python
src/
  package_name/
tests/

# Monorepo structure  
packages/
  service1/
    tests/
  service2/
    tests/
```

### 7. Database Configuration Issues

**Problem**: AI agents may include problematic database parameters that require superuser privileges or restart permissions.

**Check Steps:**
1. **Review database connection configurations:**
   ```bash
   grep -r "shared_preload_libraries\|server_" src/ --include="*.py"
   grep -r "postgresql://" src/ --include="*.py"
   ```

2. **Common problematic patterns:**
   ```python
   # WRONG - Requires superuser privileges
   'shared_preload_libraries': '',
   'log_statement': 'all',
   'log_min_duration_statement': 0,
   
   # CORRECT - Use connection-level parameters only
   'pool_size': 20,
   'max_overflow': 30,
   'pool_timeout': 30
   ```

**Verification:**
- [ ] Database connections don't set server parameters
- [ ] Connection pooling uses client-side parameters only
- [ ] No server restart required parameters in configuration

### 8. Logging Configuration Complexity

**Problem**: Overly complex logging configurations with custom formatters can fail in CI environments.

**Check Steps:**
1. **Simplify logging setups:**
   ```python
   # COMPLEX - May fail with import/path issues
   log_config = {
       "formatters": {
           "json": {"()": "module.CustomFormatter"}
       }
   }
   
   # SIMPLE - Reliable in all environments
   logging.basicConfig(
       level=logging.INFO,
       format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
   )
   ```

**Verification:**
- [ ] Logging configuration works without custom formatter imports
- [ ] No hardcoded file paths in logging handlers
- [ ] Environment-aware formatting (dev vs production)

### 9. Environment Variable Validation Issues

**Problem**: Hardcoded secrets and improper environment variable handling in configuration files.

**Check Steps:**
1. **Scan for hardcoded secrets:**
   ```bash
   grep -r "secret\|key\|password" src/ --include="*.py" | grep -v "environment\|getenv"
   grep -r "sk-\|api_key.*=" src/ --include="*.py"
   ```

2. **Fix hardcoded patterns:**
   ```python
   # WRONG - Hardcoded secrets
   API_KEY = "sk-1234567890abcdef"
   JWT_SECRET = "hardcoded-secret-key"
   
   # CORRECT - Environment-based
   API_KEY = os.getenv("API_KEY")
   JWT_SECRET = os.getenv("JWT_SECRET_KEY")
   ```

**Verification:**
- [ ] No hardcoded API keys, tokens, or secrets
- [ ] Environment variables have proper defaults for development
- [ ] Production settings require all secrets via environment

### 10. File Path Encoding and Tool Compatibility

**Problem**: Files with unusual encoding or tool compatibility issues that break standard operations.

**Check Steps:**
1. **Check file encoding and tool access:**
   ```bash
   file README.md  # Check encoding
   head -1 requirements.txt  # Verify format
   python -c "import requirements; print('OK')"  # Test imports
   ```

2. **Use alternative approaches for problem files:**
   ```bash
   # If Edit tool fails, use sed/bash alternatives
   sed -i 's/old/new/' file.txt
   # Or recreate file if encoding issues persist
   ```

**Verification:**
- [ ] All files are in UTF-8 encoding
- [ ] Standard tools can read/write project files
- [ ] Alternative commands available for file operations

### 11. Secret Management in CI/CD

**Problem**: Services requiring authentication tokens (Codecov, Snyk) fail when tokens aren't configured.

**Check Steps:**
1. **Make external services conditional:**
   ```yaml
   # WRONG - Fails if token missing
   - uses: codecov/codecov-action@v5
     with:
       token: ${{ secrets.CODECOV_TOKEN }}
   
   # BETTER - Conditional execution
   - uses: codecov/codecov-action@v5
     if: always() && secrets.CODECOV_TOKEN
     with:
       token: ${{ secrets.CODECOV_TOKEN }}
       fail_ci_if_error: false
   ```

2. **Document required secrets:**
   ```markdown
   ## Required Repository Secrets
   - `CODECOV_TOKEN`: For coverage reporting
   - `SNYK_TOKEN`: For container vulnerability scanning
   ```

**Verification:**
- [ ] CI workflows don't fail when optional tokens are missing
- [ ] Required secrets are documented
- [ ] External service integrations use `continue-on-error` or conditionals

### 12. Codecov Action Parameter Changes

**Problem**: Codecov action v5+ has different parameter names than v4, causing workflow failures.

**Error Message:**
```
Unexpected input(s) 'file', valid inputs are ['files', 'token', 'flags', ...]
```

**Fix Steps:**
1. **Update parameter name:**
   ```yaml
   # WRONG (v4 syntax)
   - uses: codecov/codecov-action@v5
     with:
       file: ./coverage.xml
   
   # CORRECT (v5 syntax)  
   - uses: codecov/codecov-action@v5
     with:
       files: ./coverage.xml  # Note: 'files' is plural
   ```

2. **Check for other parameter changes:**
   ```bash
   grep -r "codecov/codecov-action" .github/workflows/
   ```

**Verification:**
- [ ] Codecov action uses `files` parameter (not `file`)
- [ ] Action version matches parameter syntax
- [ ] Coverage upload succeeds in CI

**Prevention**: Always check action documentation when upgrading major versions.

### 13. Container Security Vulnerabilities

**Problem**: Base container images often contain numerous security vulnerabilities that can be dramatically reduced.

**Check Steps:**
1. **Scan current container for vulnerabilities:**
   ```bash
   # Build current image
   docker build -t app:current .
   
   # Scan with multiple tools
   trivy image --severity HIGH,CRITICAL app:current
   grype app:current
   snyk container test app:current
   ```

2. **Consider distroless migration for maximum security:**
   ```dockerfile
   # BEFORE - Standard base image (206 vulnerabilities)
   FROM python:3.11.11-slim-bookworm
   
   # AFTER - Distroless multi-stage (4 vulnerabilities, 98% reduction)
   FROM python:3.11.11-slim-bookworm as builder
   RUN pip install --target=/app/dependencies -r requirements.txt
   
   FROM gcr.io/distroless/python3-debian12:latest
   USER 65532:65532
   COPY --from=builder /app/dependencies /app/dependencies
   ENTRYPOINT ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

**Common security improvements:**
- Use distroless base images (Google's gcr.io/distroless/*)
- Implement multi-stage builds to reduce attack surface
- Run as non-root user (distroless uses UID 65532)
- Remove shell access and unnecessary system components
- Use specific image tags instead of 'latest'

**Verification:**
- [ ] Container vulnerability count under 10 (ideally under 5)
- [ ] No root user execution in production stage
- [ ] Multi-stage build separates dependencies from runtime
- [ ] Security scans integrated in CI/CD pipeline
- [ ] SARIF reports uploaded to GitHub Security tab

### 14. Application Security Code Issues

**Problem**: Application code may contain security vulnerabilities like insecure random generation, dangerous assertions, and improper host binding.

**Check Steps:**
1. **Scan for insecure patterns:**
   ```bash
   # Insecure random usage
   grep -r "import random" src/ --include="*.py"
   grep -r "random\." src/ --include="*.py"
   
   # Dangerous assertions
   grep -r "assert " src/ --include="*.py"
   
   # Insecure host binding
   grep -r "0\.0\.0\.0" src/ --include="*.py"
   grep -r "host.*=" src/ --include="*.py"
   ```

2. **Fix common security issues:**
   ```python
   # WRONG - Insecure random for security purposes
   import random
   delay *= 0.5 + random.random() * 0.5
   
   # CORRECT - Cryptographically secure random
   import secrets
   delay *= 0.5 + secrets.SystemRandom().random() * 0.5
   
   # WRONG - Host binding to all interfaces in development
   host: str = "0.0.0.0"
   
   # CORRECT - Secure local binding for development
   host: str = "127.0.0.1"
   
   # WRONG - Assert statements can be disabled
   assert user.is_authenticated, "User must be authenticated"
   
   # CORRECT - Proper error handling
   if not user.is_authenticated:
       raise HTTPException(status_code=401, detail="Authentication required")
   ```

**Verification:**
- [ ] No usage of `random` module for security purposes
- [ ] Development environments bind to localhost only
- [ ] No assert statements for security validation
- [ ] Proper exception handling for authentication/authorization
- [ ] Secrets properly encrypted with valid Fernet keys

### 15. AWS CloudShell Deployment Issues

**Problem**: CloudShell deployment failures due to AWS CLI paging, networking configuration, and database URL encoding issues.

**Check Steps:**
1. **AWS CLI Paging Issues:**
   ```bash
   # WRONG - Pauses deployment waiting for user input
   aws ecs describe-services --cluster uncaptcha-cluster --services uncaptcha-service
   
   # CORRECT - Disable paging for unattended scripts
   aws ecs describe-services --cluster uncaptcha-cluster --services uncaptcha-service --no-cli-pager
   ```

2. **VPC Networking Configuration:**
   ```bash
   # Check internet gateway attachment
   aws ec2 describe-internet-gateways --filters "Name=attachment.vpc-id,Values=vpc-XXXXXX"
   
   # Check route table routes
   aws ec2 describe-route-tables --filters "Name=vpc-id,Values=vpc-XXXXXX"
   
   # Fix blackholed routes
   aws ec2 replace-route --route-table-id rtb-XXXXXX --destination-cidr-block 0.0.0.0/0 --gateway-id igw-XXXXXX
   ```

3. **Database URL Encoding:**
   ```bash
   # WRONG - Special characters in password break URL parsing
   DATABASE_URL="postgresql://user:p@ss<>w0rd@host:5432/db"
   
   # CORRECT - URL encode password with special characters
   DB_PASSWORD=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$DB_PASSWORD'))")
   DATABASE_URL="postgresql://user:${DB_PASSWORD}@host:5432/db"
   ```

**Common deployment failures:**
- **ECS Tasks failing with "Invalid IPv6 URL"**: Password contains `<>` characters that break URL parsing
- **ECR connection timeouts**: Route tables missing internet gateway routes (blackholed state)
- **ECS service stuck in DRAINING**: Old inactive services need manual deletion before recreation
- **Deployment scripts hanging**: AWS CLI pager waiting for user input (`press q to continue`)

**Verification:**
- [ ] All AWS CLI commands in scripts use `--no-cli-pager` flag
- [ ] VPC route tables have working internet gateway routes
- [ ] Database passwords are URL-encoded before inclusion in connection strings
- [ ] ECS services are properly deleted before recreation
- [ ] IAM roles have Secrets Manager read permissions
- [ ] Security groups allow ECS tasks to reach ECR and other AWS services

### 16. AWS Resource State Management

**Problem**: AWS resources can get into inconsistent states requiring manual intervention during deployment.

**Check Steps:**
1. **ECS Cluster State Issues:**
   ```bash
   # Check cluster status
   aws ecs describe-clusters --clusters cluster-name
   
   # Recreate inactive cluster
   aws ecs create-cluster --cluster-name cluster-name
   ```

2. **Service Scaling and State:**
   ```bash
   # Check service desired count
   aws ecs describe-services --cluster cluster-name --services service-name --query 'services[0].desiredCount'
   
   # Scale service (can't update INACTIVE services)
   aws ecs update-service --cluster cluster-name --service service-name --desired-count 2
   ```

3. **Route Table Blackhole Detection:**
   ```bash
   # Check for blackholed routes
   aws ec2 describe-route-tables --query 'RouteTables[].Routes[?State==`blackhole`]'
   
   # Fix with correct internet gateway
   aws ec2 replace-route --route-table-id rtb-XXXXXX --destination-cidr-block 0.0.0.0/0 --gateway-id igw-XXXXXX
   ```

**Verification:**
- [ ] ECS clusters are in ACTIVE state before creating services
- [ ] Services have desired count > 0 to actually run tasks
- [ ] Route tables have no blackholed routes
- [ ] Internet gateways are attached to VPCs
- [ ] Tasks can successfully pull from ECR (no network timeouts)

### 17. ECS Fargate Networking and NAT Gateway Issues

**Problem**: ECS Fargate tasks in private subnets fail to start due to ECR connectivity issues when NAT Gateways are missing.

**Error Messages:**
```
ResourceInitializationError: unable to pull secrets or registry auth: The task cannot pull registry auth from Amazon ECR: There is a connection issue between the task and Amazon ECR. Check your task network configuration. RequestError: send request failed caused by: Post "https://api.ecr.us-east-2.amazonaws.com/": dial tcp 3.17.137.97:443: i/o timeout
```

**Root Cause Analysis:**
1. **Check NAT Gateway Existence:**
   ```bash
   # Verify NAT Gateways exist for private subnets
   aws ec2 describe-nat-gateways --filter "Name=vpc-id,Values=vpc-XXXXXX" --query 'NatGateways[].{NatGatewayId:NatGatewayId,State:State,SubnetId:SubnetId}'
   ```

2. **Check Task IAM Role:**
   ```bash
   # Task definition must have taskRoleArn for service creation
   aws ecs describe-task-definition --task-definition task-name --query 'taskDefinition.taskRoleArn'
   
   # If missing, create task role
   aws iam create-role --role-name task-role --assume-role-policy-document file://trust-policy.json
   ```

3. **Check Route Table Configuration:**
   ```bash
   # Verify private subnets have routes to NAT Gateways
   aws ec2 describe-route-tables --filters "Name=vpc-id,Values=vpc-XXXXXX" --query 'RouteTables[].{RouteTableId:RouteTableId,Routes:Routes[?DestinationCidrBlock==`0.0.0.0/0`]}'
   ```

**Fix Steps:**
1. **Create NAT Gateways:**
   ```bash
   # Allocate Elastic IPs
   aws ec2 allocate-address --domain vpc --region us-east-2
   
   # Create NAT Gateways in public subnets
   aws ec2 create-nat-gateway --subnet-id subnet-public-1 --allocation-id eipalloc-XXXXXX
   aws ec2 create-nat-gateway --subnet-id subnet-public-2 --allocation-id eipalloc-XXXXXX
   ```

2. **Create Route Tables for Private Subnets:**
   ```bash
   # Create dedicated route tables
   aws ec2 create-route-table --vpc-id vpc-XXXXXX
   aws ec2 create-route-table --vpc-id vpc-XXXXXX
   
   # Add routes to NAT Gateways
   aws ec2 create-route --route-table-id rtb-XXXXXX --destination-cidr-block 0.0.0.0/0 --nat-gateway-id nat-XXXXXX
   
   # Associate with private subnets
   aws ec2 associate-route-table --route-table-id rtb-XXXXXX --subnet-id subnet-private-1
   ```

3. **Create ECS Task Role:**
   ```bash
   # Create task role with trust policy
   cat > trust-policy.json << EOF
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Service": "ecs-tasks.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   EOF
   
   aws iam create-role --role-name uncaptcha-task-role --assume-role-policy-document file://trust-policy.json
   aws iam attach-role-policy --role-name uncaptcha-task-role --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
   ```

**Verification:**
- [ ] NAT Gateways exist in public subnets and are in "available" state
- [ ] Private subnets have dedicated route tables with 0.0.0.0/0 routes to NAT Gateways
- [ ] ECS task definitions include both executionRoleArn and taskRoleArn
- [ ] ECS tasks can successfully pull images from ECR (no timeout errors)
- [ ] Tasks reach RUNNING state and pass health checks
- [ ] Application logs show successful database and Redis connections

### 18. ECS Container Health Check and Startup Command Issues

**Problem**: ECS tasks start but immediately fail health checks and are deregistered from load balancer targets, causing 503 errors.

**Common Issues:**
1. **Health check command dependencies**: Using Python `requests` library in health check when it may not be available
2. **Startup command confusion**: Using `uvicorn` CLI vs. Python script execution leads to different behavior
3. **Missing curl in container**: Health checks fail when curl is not installed

**Check Steps:**
1. **Verify health check command works in container:**
   ```bash
   # Test container locally first
   docker run -d -p 8000:8000 --name test-container image:tag
   docker exec test-container curl -f http://localhost:8000/api/health
   ```

2. **Check ECS task logs for health check failures:**
   ```bash
   # Get recent log streams
   aws logs describe-log-streams --log-group-name "/ecs/task-name" --order-by LastEventTime --descending --max-items 3
   
   # Check logs for health check errors
   aws logs get-log-events --log-group-name "/ecs/task-name" --log-stream-name "stream-name"
   ```

3. **Monitor target group health:**
   ```bash
   # Check target health status
   aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:region:account:targetgroup/name/id
   ```

**Fix Steps:**
1. **Use curl instead of Python for health checks:**
   ```dockerfile
   # Install curl in container
   RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
   
   # Use curl for health checks
   HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
       CMD curl -f http://localhost:$PORT/api/health || exit 1
   ```

2. **Fix task definition health check:**
   ```json
   {
       "healthCheck": {
           "command": ["CMD-SHELL", "curl -f http://localhost:8000/api/health || exit 1"],
           "interval": 30,
           "timeout": 5,
           "retries": 3,
           "startPeriod": 60
       }
   }
   ```

3. **Ensure startup command matches application expectations:**
   ```dockerfile
   # If app expects to run with reload=True, use Python directly
   CMD ["python", "web_api.py"]
   
   # If using uvicorn CLI, ensure app variable is properly exposed
   CMD ["python", "-m", "uvicorn", "web_api:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

4. **Add taskRoleArn to task definition:**
   ```json
   {
       "taskRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
       "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole"
   }
   ```

**Troubleshooting Techniques:**
1. **Test Docker image locally before ECS deployment**
2. **Check CloudWatch logs immediately after task starts**
3. **Verify health endpoint works in running container**
4. **Use specific image tags (not :latest) to avoid caching issues**
5. **Monitor target group health state changes**

**Prevention:**
- [ ] Health check command tested in local container
- [ ] Curl installed in production container
- [ ] Task definition includes both executionRoleArn and taskRoleArn
- [ ] Health endpoint returns 200 status code
- [ ] Container startup logs show successful application start

## Changelog

- **2025-07-14**: Initial version based on unCAPTCHA API CI/CD fixes
- **2025-07-14**: Added database configuration, logging, environment variables, file encoding, and secret management issues discovered during implementation
- **2025-07-14**: Added container security vulnerabilities and application security code issues after implementing distroless architecture
- **2025-07-15**: Added AWS CloudShell deployment issues and resource state management after extensive debugging session
- **2025-07-16**: Added ECS Fargate networking and NAT Gateway issues (#17) after successful resolution of production deployment failure
- **2025-07-18**: Added ECS Container Health Check and Startup Command Issues (#18) during geometry engine deployment troubleshooting
- **[AI Agent]**: Please add your discoveries and improvements here

---

**Note**: This document should be reviewed and updated whenever new CI/CD issues are discovered during project setup or maintenance.