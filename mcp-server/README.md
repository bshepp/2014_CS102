# 🌌 GeometryOracle MCP Server

**Model Context Protocol server for N-dimensional geometry calculations with comprehensive data collection**

Transform your AI systems with N-dimensional geometry capabilities while contributing to research on AI mathematical query patterns.

## 🎯 What This Does

- **MCP Server**: Any AI system can call GeometryOracle for N-dimensional calculations
- **Data Collection**: Every query is logged for research into AI geometry usage patterns  
- **Research Dashboard**: Beautiful web interface showing usage analytics and trends
- **Open Dataset**: Anonymized data available for computational geometry research

## 🚀 Features

### **MCP Tools Available:**
- `calculate_hypersphere(dimensions, radius)` - N-dimensional sphere calculations
- `calculate_hypercube(dimensions, side_length)` - N-dimensional cube calculations  
- `compare_shapes(shapes)` - Multi-shape volume/area comparisons
- `get_usage_statistics(days)` - Meta-tool for server statistics

### **Data Collection:**
- Query parameters and results
- Execution timing and performance metrics
- Session tracking and client information
- Error logging and analysis
- Dimension popularity tracking
- Visualization request patterns

### **Research Dashboard:**
- Real-time usage statistics
- Interactive charts and graphs
- Data export (JSON/CSV) for research
- Performance analytics
- Error rate monitoring

## 📋 Quick Start

### **1. Setup**
```bash
cd mcp-server

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from src.database import DatabaseManager; DatabaseManager()"
```

### **2. Run MCP Server**
```bash
# Start MCP server (port 8001)
python src/mcp_server.py

# Start dashboard (port 8002) 
python src/dashboard.py
```

### **3. View Dashboard**
Open http://localhost:8002 to see real-time usage data and analytics.

### **4. Connect AI Systems**
Configure your AI systems to use the MCP server at `http://localhost:8001/mcp`

## 🔧 Configuration

### **MCP Client Configuration**
```json
{
  "mcpServers": {
    "geometry-oracle": {
      "command": "python",
      "args": ["src/mcp_server.py"],
      "env": {
        "DB_PATH": "geometry_oracle.db"
      }
    }
  }
}
```

### **Environment Variables**
- `DB_PATH`: Database file path (default: `mcp_geometry_oracle.db`)
- `PORT`: MCP server port (default: 8001)
- `DASHBOARD_PORT`: Dashboard port (default: 8002)

## 💡 Example Usage

### **From Claude/ChatGPT/AI Systems:**
```
User: "What's the volume of a 5-dimensional sphere with radius 3?"

AI: Let me use GeometryOracle to calculate that...
→ Calls calculate_hypersphere(5, 3)
→ Returns: Volume: 1436.76 cubic units

All queries logged to database for research! 📊
```

### **Direct API Calls:**
```python
import requests

response = requests.post("http://localhost:8001/mcp", json={
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "calculate_hypersphere",
        "arguments": {
            "dimensions": 4,
            "radius": 2.5
        }
    },
    "id": 1
})
```

## 📊 Research Value

### **Data Collected:**
- **Query Patterns**: What dimensions do AIs find most interesting?
- **Tool Usage**: Which geometry operations are most common?
- **Performance Metrics**: How does complexity scale with dimensions?
- **Error Analysis**: What mathematical operations fail and why?
- **Session Analytics**: How do different AI systems use geometry tools?

### **Research Applications:**
- AI mathematical reasoning patterns
- Computational geometry usage studies  
- N-dimensional visualization research
- Educational AI tool development
- Mathematical query optimization

## 🏗️ Architecture

```
AI System (Claude/ChatGPT/etc.)
    ↓ MCP Protocol (JSON-RPC 2.0)
FastMCP Server (port 8001)
    ↓ 
GeometryEngine + Database Logger
    ↓
SQLite Database + Analytics Dashboard (port 8002)
```

### **Components:**
- **`mcp_server.py`**: Main MCP protocol server
- **`database.py`**: Comprehensive logging and analytics  
- **`dashboard.py`**: Web dashboard for data visualization
- **`schemas/database.sql`**: Database schema with research-focused tables

## 🌐 Deployment Options

### **Local Development**
```bash
python src/mcp_server.py  # MCP server
python src/dashboard.py   # Dashboard
```

### **AWS Lambda (Planned)**
- Serverless MCP server deployment
- API Gateway integration
- DynamoDB for logging
- CloudWatch analytics

### **Docker**
```dockerfile
# Dockerfile coming soon!
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8001 8002
CMD ["python", "src/mcp_server.py"]
```

## 📈 Dashboard Features

**Real-time Analytics:**
- Total queries processed
- Unique AI sessions  
- Average response times
- Most popular dimensions
- Error rates

**Interactive Charts:**
- Tool usage distribution
- Dimension popularity trends
- Performance over time
- Session analytics

**Data Export:**
- JSON format for research
- CSV for spreadsheet analysis
- Real-time data streaming
- Anonymized datasets

## 🤝 Contributing to Research

### **Using the Data:**
1. Visit the dashboard at http://localhost:8002
2. Export data in JSON/CSV format
3. Analyze AI geometry query patterns
4. Publish research findings (please cite!)

### **Research Questions to Explore:**
- Do different AI models prefer different dimensions?
- What geometric operations are most computationally expensive?
- How do AI systems use geometry for problem-solving?
- What visualization types are most requested?

## 📄 License & Citation

**MIT License** - Use freely for research and education.

**Please cite as:**
```
GeometryOracle MCP Server: A Data Collection Platform for AI Geometry Research
https://github.com/your-username/geometry-oracle
```

## 🔗 Related Projects

- **GeometryOracle Main**: The original N-dimensional geometry engine
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Computational Geometry Research**: Educational applications and N-dimensional visualization

---

**🌌 Transform AI mathematical reasoning, one dimension at a time!**

*From a 2014 CS102 sphere calculator to AI research infrastructure - the journey continues...*