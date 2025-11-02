# 🔍 Amplify Deployment Deep Analysis - gengine.darkforestlabs.com
**Date**: September 7, 2025  
**Analysis**: Complete re-examination of what's actually deployed

## Executive Summary

The website at `gengine.darkforestlabs.com` **IS loading successfully** and serving content, but it's **fundamentally broken** due to a critical API mismatch. The page loads but cannot perform any actual geometry calculations.

---

## ✅ What's Actually Working

### 1. **Amplify Deployment IS Successful**
- **Last Successful Deploy**: Sept 6, 2025 at 8:20 PM PST
- **Commit**: `43d4edf` (docs: comprehensive session wrap-up)
- **Build Status**: SUCCEED
- **Files Served**: `demo.html` copied to `index.html` during build

### 2. **Content IS Being Served Correctly**
- **Source File**: `/demo.html` in repository root
- **Live Site**: Exact match - files are identical (verified with diff)
- **CloudFront**: `d2dnv1za149q6w.cloudfront.net` (via Route53 CNAME)
- **Custom Domain**: `gengine.darkforestlabs.com` → CloudFront → Amplify

### 3. **Frontend HTML/CSS/JS Loads Fine**
- Beautiful gradient UI displays
- Forms and buttons render correctly  
- Plotly.js loads for visualizations
- All static content works

---

## 🔴 The Critical Problem: Complete API Mismatch

### **The Fundamental Issue**

The demo.html file expects a **FastAPI web server** but is trying to connect to a **Lambda MCP server** with completely incompatible APIs:

#### **What demo.html Expects (FastAPI endpoints):**
```javascript
API_BASE = 'https://s6ngc23inj.execute-api.us-east-1.amazonaws.com/prod'

// Then tries to call:
- ${API_BASE}/sphere         // POST sphere calculations
- ${API_BASE}/query          // POST natural language queries  
- ${API_BASE}/original-java  // GET Java integration
- ${API_BASE}/dimensions     // GET dimension info
- ${API_BASE}/visualize      // POST visualization data
```

#### **What Actually Exists (MCP Lambda):**
```
- /prod/mcp    // JSON-RPC 2.0 MCP protocol ONLY
```

### **Why Nothing Works:**

1. **Wrong Protocol**: 
   - Frontend sends REST API calls
   - Backend expects JSON-RPC 2.0 MCP format

2. **Wrong Endpoints**:
   - Frontend calls `/sphere`, `/query`, etc.
   - Backend only has `/mcp`

3. **Wrong Payload Format**:
   - Frontend sends: `{"dimensions": 3, "radius": 2}`
   - Backend expects: `{"jsonrpc": "2.0", "method": "tool/call", "params": {...}}`

4. **Authentication Issues**:
   - API Gateway returns "Missing Authentication Token" for non-existent routes

---

## 📊 The Architecture Confusion

### **Two Separate Systems Were Built:**

#### **System 1: Local FastAPI Server** (`web_api.py`)
- Runs locally on port 8000
- Has all the endpoints demo.html expects
- Never deployed to AWS
- This is what the frontend was designed for

#### **System 2: AWS MCP Server** (Lambda)
- Deployed to AWS Lambda
- JSON-RPC protocol for Claude Desktop
- Completely different API structure
- This is what's actually deployed

### **The Mismatch:**
The frontend (`demo.html`) was written for System 1 but deployed pointing to System 2's URL.

---

## 🎯 Why It Appears "Incredibly Inaccurate"

When users visit `gengine.darkforestlabs.com`:

1. **Page loads beautifully** ✅
2. **User enters geometry parameters** ✅
3. **Clicks "Calculate"** ✅
4. **JavaScript makes API call** ✅
5. **API returns 403/404 error** ❌
6. **Error displayed to user** ❌
7. **Nothing works** ❌

The site **looks professional** but **does nothing** - hence "incredibly inaccurate."

---

## 🔧 The Solution Options

### **Option 1: Deploy FastAPI to AWS (Recommended)**
Deploy the actual `web_api.py` to AWS Lambda or ECS:
```bash
# Package FastAPI app
# Deploy to Lambda with API Gateway
# Update demo.html to use new endpoint
```

### **Option 2: Rewrite Frontend for MCP**
Modify demo.html to use JSON-RPC format:
```javascript
// Change all API calls to MCP format
const response = await fetch(`${API_BASE}/mcp`, {
    method: 'POST',
    body: JSON.stringify({
        jsonrpc: "2.0",
        method: "tool/call",
        params: {
            name: "calculate_hypersphere",
            arguments: { dimensions: 3, radius: 2 }
        },
        id: 1
    })
});
```

### **Option 3: Create API Gateway Proxy**
Add Lambda functions to translate REST → MCP:
- `/sphere` → translates to MCP calculate_hypersphere
- `/query` → translates to MCP process
- etc.

---

## 📈 Amplify Configuration Details

### **What's Configured:**
- **App ID**: `d2vt3koij47dy3`
- **Repository**: `https://github.com/bshepp/2014_cs102`
- **Branch**: `main` (production)
- **Build Spec**: Copies `demo.html` to `index.html`
- **Auto Build**: Disabled (manual deployments)

### **What's Missing:**
- Custom domain not configured in Amplify (uses Route53 → CloudFront instead)
- Amplify default domain returns 404 (not configured properly)

### **CloudFront Mystery:**
- `d2dnv1za149q6w.cloudfront.net` serves the site
- Not listed in CloudFront distributions (might be Amplify-managed)
- Works via Route53 CNAME

---

## 🎯 Immediate Fix Recommendations

### **Quick Fix (Today):**
1. Update `demo.html` to show a message: "API integration coming soon"
2. OR: Point to local development for now

### **Proper Fix (This Week):**
1. **Deploy FastAPI to AWS**:
   ```bash
   # Use SAM or Serverless Framework
   # Deploy web_api.py as Lambda function
   # Configure API Gateway with all routes
   ```

2. **Update demo.html** with new endpoint

3. **Test everything** before pushing

### **Long-term Fix:**
1. Consolidate to single API approach
2. Full Infrastructure as Code
3. Automated testing of API endpoints
4. Monitoring and alerts

---

## ✅ The Good News

1. **Amplify IS working** - deployment pipeline is fine
2. **CloudFront IS working** - content delivery is fine  
3. **Frontend IS working** - HTML/CSS/JS is fine
4. **CI/CD IS working** - GitHub Actions are fine

**The ONLY problem**: Wrong backend API deployed for this frontend

---

## 📝 Summary

`gengine.darkforestlabs.com` loads successfully but is a **beautiful, non-functional shell** because:
- Frontend expects FastAPI endpoints
- Backend provides MCP endpoints
- They speak different languages

This is a **classic deployment mismatch** - two different systems were developed (local FastAPI and AWS MCP) and the wrong combination got deployed.

**Fix Priority**: HIGH - The site looks professional but does nothing, which is worse than being obviously broken.

---

*Analysis Complete: September 7, 2025*
*Recommendation: Deploy FastAPI to AWS immediately*