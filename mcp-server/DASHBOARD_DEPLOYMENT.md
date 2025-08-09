# 📊 GeometryOracle Dashboard Deployment Guide

**Last Updated**: August 9, 2025  
**Status**: Ready for Public Deployment

## 🌐 Dashboard Overview

The GeometryOracle Dashboard provides real-time insights into how AI agents use the N-dimensional geometry MCP server. It's designed to be publicly accessible to showcase fascinating usage patterns and research data.

## 🚀 Quick Deployment

### **Local Development**
```bash
# From project root
cd mcp-server
source ../venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment for production data
export STAGE=prod

# Start dashboard (connects to AWS DynamoDB)
PYTHONPATH=src python -c "
import uvicorn
from src.dashboard import dashboard_app
uvicorn.run(dashboard_app, host='0.0.0.0', port=8002)
"
```

### **Production Deployment Options**

#### **Option 1: AWS Amplify**
```yaml
# amplify.yml
version: 1.0
backend:
  phases:
    preBuild:
      commands:
        - cd mcp-server
        - pip install -r requirements.txt
    build:
      commands:
        - PYTHONPATH=src uvicorn src.dashboard:dashboard_app --host 0.0.0.0 --port 8002
frontend:
  phases:
    build:
      commands:
        - echo "Dashboard available at /api/stats/overview"
```

#### **Option 2: Docker Container**
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY mcp-server/ .
RUN pip install -r requirements.txt

# Set environment
ENV STAGE=prod
ENV PYTHONPATH=src

EXPOSE 8002
CMD ["uvicorn", "src.dashboard:dashboard_app", "--host", "0.0.0.0", "--port", "8002"]
```

#### **Option 3: Serverless (Lambda)**
Deploy as additional Lambda function behind API Gateway for serverless dashboard.

## 📊 Dashboard Features

### **Real-Time Analytics**
- **Tool Usage Distribution**: Pie chart showing which MCP tools are most popular
- **Dimension Popularity**: Bar chart of preferred dimensions by AI agents  
- **Usage Timeline**: Historical usage patterns over time
- **Error Rates**: Success/failure statistics

### **Research Data Export**
- **JSON Export**: Structured data for programmatic analysis
- **CSV Export**: Spreadsheet-friendly format for research
- **Live Data Stream**: WebSocket connection for real-time monitoring
- **Filtered Views**: Filter by time period, tool type, dimensions

### **Public API Endpoints**

#### **GET /api/stats/overview**
```json
{
  "overview": {
    "total_queries": 1247,
    "unique_sessions": 89,
    "avg_execution_time_ms": 23.4,
    "most_popular_dimension": 3,
    "error_rate_percent": 2.1
  },
  "tool_usage": [
    {"tool_name": "calculate_hypersphere", "calls": 678},
    {"tool_name": "batch_geometry_calculations", "calls": 234}
  ],
  "dimension_popularity": [
    {"dimensions": 3, "calls": 456},
    {"dimensions": 4, "calls": 321}
  ]
}
```

#### **GET /api/charts/usage**
Returns Plotly JSON for interactive charts.

#### **GET /api/data/export?format=json|csv**
Export complete dataset for research purposes.

## 🔧 Configuration

### **Environment Variables**
```bash
# Data Source
STAGE=prod                    # Use 'prod' for AWS DynamoDB, 'dev' for SQLite

# AWS Configuration (auto-detected if available)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key    # Optional if using IAM roles
AWS_SECRET_ACCESS_KEY=your_secret

# Dashboard Settings
DASHBOARD_PORT=8002
DASHBOARD_HOST=0.0.0.0
LOG_LEVEL=info
```

### **Database Backend Auto-Detection**
The dashboard automatically detects the available backend:
- **AWS Available**: Uses DynamoDB table `geometry-oracle-mcp-prod-queries`
- **AWS Not Available**: Falls back to local SQLite database
- **Manual Override**: Set `use_dynamodb=True/False` in DatabaseManager

## 🎯 Public Value Proposition

### **Research Insights Available**
1. **AI Behavior Patterns**: How do different AI systems approach geometry?
2. **Dimensional Preferences**: What dimensions do AI agents explore most?
3. **Tool Usage Evolution**: How does usage change over time?
4. **Batch Processing Adoption**: Are AI agents using new batch tools?
5. **Performance Characteristics**: What's the computational load distribution?

### **Target Audiences**
- **AI Researchers**: Understanding AI behavior in mathematical domains
- **Educators**: Demonstrating real AI usage patterns to students
- **Developers**: Seeing practical MCP server adoption
- **General Public**: Fascination with AI exploring infinite dimensions

## 🔒 Privacy & Ethics

### **Data Collection Practices**
- ✅ **No Personal Data**: Only usage patterns, no user identification
- ✅ **Aggregated Statistics**: Individual requests not traceable
- ✅ **Transparent Collection**: All tracked data clearly documented
- ✅ **Research Purpose**: Data used for understanding AI behavior
- ✅ **Public Benefit**: Insights shared openly with research community

### **Data Retention**
- **DynamoDB TTL**: 90 days automatic cleanup
- **Aggregated Stats**: Retained indefinitely for research
- **Raw Data**: Available for research export before cleanup

## 🌐 Deployment URLs

### **Suggested Public URLs**
- **Primary**: `https://geometry-oracle-dashboard.com`
- **Alternative**: `https://ai-geometry-insights.com` 
- **AWS**: `https://dashboard.geometry-oracle.aws.dev`

### **Content Marketing**
- **Title**: "Live AI Geometry Behavior Analytics"
- **Subtitle**: "Watch AI Agents Explore N-Dimensional Space in Real-Time"
- **CTA**: "Explore how AI thinks about infinite dimensions"

## 🚀 Launch Checklist

### **Pre-Launch**
- [ ] Verify DynamoDB connection
- [ ] Test all dashboard endpoints
- [ ] Confirm data export functionality
- [ ] Set up monitoring and alerts
- [ ] Configure proper CORS headers

### **Launch**
- [ ] Deploy to chosen platform
- [ ] Configure custom domain
- [ ] Set up SSL certificate  
- [ ] Enable monitoring/logging
- [ ] Test public access

### **Post-Launch**
- [ ] Monitor usage and performance
- [ ] Gather user feedback
- [ ] Share on social media/research communities
- [ ] Document interesting findings
- [ ] Plan feature enhancements

## 🎉 Expected Impact

This dashboard will be the **first public window into AI agent behavior** in mathematical domains. The insights generated will be valuable for:

- Understanding how AI approaches geometric problems
- Identifying patterns in AI dimensional exploration
- Demonstrating practical MCP server adoption
- Contributing to AI behavior research
- Educating the public about AI capabilities

**Ready to show the world how AI agents think about infinite-dimensional geometry!** 🌌

---

**Technical Support**: See troubleshooting section in main README  
**Research Inquiries**: Contact for access to raw data exports  
**Community**: Join discussions about AI geometric behavior patterns