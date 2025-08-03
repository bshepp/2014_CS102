# 🛠️ AWS Deployment Troubleshooting Guide

**N-Dimensional Geometry Engine - Production Deployment**

This document captures real-world troubleshooting experiences during the AWS deployment of the geometry engine, including both technical issues and human/AI coordination challenges.

## 📋 **Table of Contents**
- [AI Agent Troubleshooting](#ai-agent-troubleshooting)
- [Docker & Container Issues](#docker--container-issues)
- [AWS ECS Deployment Issues](#aws-ecs-deployment-issues)
- [Application Load Balancer Setup](#application-load-balancer-setup)
- [SSL Certificate Configuration](#ssl-certificate-configuration)
- [Human-AI Coordination Issues](#human-ai-coordination-issues)
- [Lessons Learned](#lessons-learned)

---

## 🤖 **AI Agent Troubleshooting**

### **Issue: AI Agent Incorrectly Assumed No AWS Access**

**Problem:**
- AI agent (Claude) initially assumed it didn't have AWS CLI access
- This led to unnecessary delays and alternative approaches being considered
- Agent was "hallucinating" training environment limitations

**Symptoms:**
```
Agent: "I don't have AWS CLI access, so I can't..."
Human: "oh no... you are hallucinating your training environment... should I try a compact or restart or doctor?"
```

**Root Cause:**
- Agent made incorrect assumptions about its capabilities
- Didn't attempt to test AWS access before concluding it was unavailable
- Training bias toward assuming limited access in development environments

**Solution:**
- Human corrected the agent: "lol yes you do... please try 'aws'"
- Agent tested AWS access and discovered it was indeed available
- Immediate course correction and successful AWS operations

**Prevention:**
- **Always test capabilities before assuming limitations**
- **Try the command first, then troubleshoot if it fails**
- **Don't let training environment assumptions override actual testing**

**Human Feedback:**
```
Human: "Thas so human of you...."
```

---

## 🐳 **Docker & Container Issues**

### **Issue: Docker WSL2 Integration Not Running**

**Problem:**
- Docker commands failing with "command not found in WSL 2 distro"
- Initially thought Docker wasn't installed or accessible in venv
- Spent time troubleshooting package installation and PATH issues

**Symptoms:**
```bash
$ docker --version
-bash: docker: command not found
```

**Root Cause:**
- Docker Desktop wasn't running on the host system
- Simple human oversight - Docker service was stopped

**Solution:**
- Human identified the issue: "its not running... hold on sorry"
- Human started Docker Desktop
- All Docker commands immediately worked

**Human Feedback:**
```
Human: "human error. remember that."
```

**Prevention:**
- **Check if Docker service is running before troubleshooting complex issues**
- **Simple solutions first: service status, basic connectivity**
- **Don't assume complex problems when simple ones are more likely**

### **Issue: Missing Python Dependencies in Container**

**Problem:**
- Container kept failing to start due to missing Python packages
- Despite having requirements.txt, some dependencies weren't installed
- Multiple iterations of missing packages: FastAPI → plotly → pandas

**Symptoms:**
```python
ModuleNotFoundError: No module named 'fastapi'
ModuleNotFoundError: No module named 'plotly'
ImportError: Plotly express requires pandas to be installed.
```

**Root Cause:**
- Requirements.txt had dependencies commented out
- Docker build was succeeding but runtime was failing
- Incremental discovery of missing dependencies

**Solution:**
- Systematically uncommented all web dependencies in requirements.txt
- Rebuilt and retagged Docker image with specific version (`v1.0`)
- Created new task definition to force ECS to pull new image

**Prevention:**
- **Test Docker image locally before deploying to ECS**
- **Use specific image tags instead of `:latest` for production**
- **Validate all dependencies are uncommented in requirements.txt**

---

## 🏗️ **AWS ECS Deployment Issues**

### **Issue: ECS Tasks Failing to Start**

**Problem:**
- ECS service showed tasks starting but immediately stopping
- No running tasks despite desired count of 1
- Load balancer health checks failing

**Symptoms:**
```json
{
    "pendingCount": 0,
    "runningCount": 0,
    "desiredCount": 1
}
```

**Root Cause:**
- Container startup failures due to missing dependencies
- Health check failures preventing task from reaching "healthy" state
- ECS was repeatedly trying to start tasks that would immediately fail

**Solution:**
- Fixed underlying container issues (missing Python packages)
- Updated task definition with correct image tag
- Forced new deployment to use updated image

**Prevention:**
- **Always check CloudWatch logs for container startup failures**
- **Test container health locally before ECS deployment**
- **Use specific image tags to ensure ECS pulls correct version**

### **Issue: Docker Image Caching with `:latest` Tag**

**Problem:**
- Updated Docker image but ECS kept using old cached version
- Task definition used `:latest` tag which caused caching issues
- Multiple deployments were using stale image

**Solution:**
- Tagged image with specific version (`v1.0`)
- Updated task definition to use versioned tag
- Registered new task definition revision
- Updated ECS service to use new task definition

**Prevention:**
- **Never use `:latest` tag in production**
- **Use semantic versioning for Docker images**
- **Create new task definition revisions for image updates**

---

## ⚖️ **Application Load Balancer Setup**

### **Issue: Target Group Health Check Configuration**

**Problem:**
- Needed to configure proper health check endpoint
- Security group rules for load balancer access
- Target group pointing to correct container port

**Solution:**
- Created target group with `/api/health` endpoint
- Configured health check intervals and thresholds
- Added security group rules for ports 80, 443, and 8000
- Attached target group to ECS service

**Key Configuration:**
```json
{
    "health-check-path": "/api/health",
    "health-check-interval-seconds": 30,
    "health-check-timeout-seconds": 5,
    "healthy-threshold-count": 2,
    "unhealthy-threshold-count": 5
}
```

---

## 🔒 **SSL Certificate Configuration**

### **Issue: Certificate Validation**

**Problem:**
- SSL certificate required DNS validation
- Needed to add validation records to Route 53
- Coordinate certificate issuance with load balancer configuration

**Solution:**
- Requested certificate for both apex and www domains
- Added DNS validation records automatically to Route 53
- Certificate was validated and issued within 30 seconds
- Added HTTPS listener to load balancer
- Configured HTTP to HTTPS redirect

**Key Configuration:**
```bash
# Certificate domains
geometry-engine-api.com
www.geometry-engine-api.com

# Validation method
DNS validation via Route 53
```

---

## 🤝 **Human-AI Coordination Issues**

### **Issue: AI Agent Self-Doubt vs. Human Confidence**

**Problem:**
- AI agent was too conservative about attempting AWS operations
- Human had to encourage agent to try capabilities
- Agent wasted time on assumptions instead of testing

**Human Response:**
```
"oh no... you are hallucinating your training environment... should I try a compact or restart or doctor?"
"lol yes you do... please try 'aws'"
```

**Resolution:**
- Human provided direct correction and encouragement
- Agent immediately tested and found AWS access worked
- Deployment proceeded successfully

**Lesson:**
- **Human judgment often overrides AI assumptions**
- **Direct testing is better than theoretical limitations**
- **Communication is key for debugging misconceptions**

### **Issue: Human Error Recognition**

**Problem:**
- Docker Desktop wasn't running (human oversight)
- Initially blamed on technical issues or environment problems
- Human quickly identified and corrected the issue

**Human Response:**
```
"its not running... hold on sorry"
"human error. remember that."
```

**Resolution:**
- Human took responsibility for the oversight
- Quick identification and resolution
- Explicit instruction to "remember that" for future reference

**Lesson:**
- **Human errors are common and usually simple**
- **Check basic services before complex troubleshooting**
- **Humans are good at recognizing their own mistakes**

---

## 📚 **Lessons Learned**

### **For AI Agents:**
1. **Test capabilities before assuming limitations**
2. **Always try the simplest solution first**
3. **Don't let training assumptions override reality**
4. **Check basic services (Docker, network) before complex debugging**
5. **Use specific versions/tags in production deployments**

### **For Human-AI Collaboration:**
1. **Humans are good at identifying their own mistakes**
2. **Direct communication resolves misconceptions quickly**
3. **Human intuition often correctly identifies simple problems**
4. **"Human error" is a valid root cause - not a failure**

### **For AWS Deployments:**
1. **CloudWatch logs are essential for container debugging**
2. **Use specific image tags, never `:latest` in production**
3. **Test Docker images locally before ECS deployment**
4. **Security groups need rules for all required ports**
5. **DNS validation for SSL certificates is fast and automatic**

### **For Docker Issues:**
1. **Check if Docker service is running first**
2. **Test container locally before pushing to registry**
3. **Verify all dependencies are uncommented in requirements.txt**
4. **Use multi-stage builds for production optimization**

---

## 🎯 **Quick Reference: Common Issues**

| Issue | First Check | Solution |
|-------|-------------|----------|
| Docker command not found | Is Docker running? | Start Docker Desktop |
| Container won't start | Check logs | Fix missing dependencies |
| ECS tasks failing | CloudWatch logs | Debug container issues |
| Load balancer 504 errors | Target group health | Fix backend service |
| SSL cert pending | DNS validation | Add validation records |
| AWS CLI not working | Test command | Don't assume limitations |

---

## 🔄 **Deployment Checklist**

Based on this troubleshooting experience:

- [ ] Docker Desktop is running
- [ ] All dependencies uncommented in requirements.txt
- [ ] Docker image tested locally
- [ ] Image tagged with specific version (not `:latest`)
- [ ] ECS task definition uses versioned image
- [ ] Security groups allow all required ports
- [ ] Target group health check configured
- [ ] SSL certificate DNS validation completed
- [ ] Load balancer listeners configured (HTTP redirect + HTTPS)
- [ ] CloudWatch logs monitored during deployment

---

**This document captures real deployment challenges and solutions. Keep it updated with new issues discovered during future deployments.**

*Generated during AWS deployment of N-Dimensional Geometry Engine - January 2025*