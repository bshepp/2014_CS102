# Branch Protection Rules Setup

## Required GitHub Settings

To complete the GitFlow pipeline setup, configure these branch protection rules in GitHub:

### 1. Main Branch Protection
Navigate to: `Settings` → `Branches` → `Add rule`

**Branch name pattern**: `main`

**Protect matching branches**:
- [x] Require a pull request before merging
  - [x] Require approvals: 1
  - [x] Dismiss stale PR approvals when new commits are pushed  
  - [x] Require review from code owners
- [x] Require status checks to pass before merging
  - [x] Require branches to be up to date before merging
  - Required status checks:
    - `🔬 Production Validation Suite`
    - `🧪 Test Results Summary` 
    - `🌐 Web Standards Validation`
- [x] Require conversation resolution before merging
- [x] Require signed commits
- [x] Include administrators
- [x] Restrict pushes that create files
- [x] Allow force pushes: OFF
- [x] Allow deletions: OFF

### 2. Develop Branch Protection  
Navigate to: `Settings` → `Branches` → `Add rule`

**Branch name pattern**: `develop`

**Protect matching branches**:
- [x] Require a pull request before merging
  - [x] Require approvals: 1
- [x] Require status checks to pass before merging
  - Required status checks:
    - `🔍 Develop Branch Validation`
    - `🧪 Python Tests (Develop)`
    - `🌐 API Tests (Develop)`
- [x] Require conversation resolution before merging
- [x] Include administrators
- [x] Allow force pushes: OFF
- [x] Allow deletions: OFF

## GitHub Secrets Required

Add these secrets in: `Settings` → `Secrets and variables` → `Actions`

### Repository Secrets
- `AWS_ACCESS_KEY_ID`: AWS access key for deployment
- `AWS_SECRET_ACCESS_KEY`: AWS secret access key

### Environment Secrets (Production)
Create environment: `Settings` → `Environments` → `New environment`
- Name: `production`
- Protection rules: Require reviewers (recommended)
- Environment secrets:
  - `AWS_ACCESS_KEY_ID`: Production AWS credentials
  - `AWS_SECRET_ACCESS_KEY`: Production AWS secret

## Manual Setup Commands

Run these commands after configuring GitHub settings:

```bash
# Set develop as default branch for PRs (optional)
gh repo edit --default-branch develop

# Enable branch protection via CLI (if preferred)
gh api repos/bshepp/2014_CS102/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["🔬 Production Validation Suite"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null
```

## Verification

After setup, verify with:
```bash
gh api repos/bshepp/2014_CS102/branches/main/protection
gh api repos/bshepp/2014_CS102/branches/develop/protection
```