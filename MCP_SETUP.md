# 🌌 GeometryOracle MCP Server Setup

**Transform Claude Desktop into an N-dimensional geometry powerhouse!**

This MCP server bridges Claude Desktop to your live AWS GeometryOracle infrastructure, enabling natural language geometry calculations.

## 🚀 Quick Setup

### 1. **Verify Server Works**
```bash
source venv/bin/activate
python geometry_oracle_mcp_server.py
# Should show: ✅ AWS connectivity verified
# Then wait for MCP client connection via stdio
```

### 2. **Claude Desktop Configuration**

**Location of config file:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Add this configuration:**
```json
{
  "mcpServers": {
    "geometry-oracle": {
      "command": "python",
      "args": ["/mnt/f/ensemble_project/2014_CS102/geometry_oracle_mcp_server.py"],
      "env": {
        "AWS_ENDPOINT": "https://s6ngc23inj.execute-api.us-east-1.amazonaws.com/prod/mcp",
        "PYTHONPATH": "/mnt/f/ensemble_project/2014_CS102/venv/lib/python3.12/site-packages"
      }
    }
  }
}
```

**⚠️ Important:** Update the absolute path in `args` to match your system!

### 3. **Restart Claude Desktop**

After adding the configuration, completely restart Claude Desktop to load the MCP server.

## 🎯 **Available Tools**

Once connected, Claude Desktop will have access to:

### **🔮 calculate_hypersphere**
Calculate N-dimensional sphere properties
- **Input**: dimensions (1-100+), radius
- **Output**: volume, surface_area, diameter, formulas

### **📦 calculate_hypercube** 
Calculate N-dimensional cube properties
- **Input**: dimensions (1-100+), side_length
- **Output**: volume, surface_area, vertices, edges, diagonal

### **⚖️ compare_shapes**
Compare multiple geometric shapes
- **Input**: list of shapes with types and parameters
- **Output**: volume ratios, largest shape, comparisons

### **📊 get_usage_statistics**
Get server analytics
- **Input**: days (1-365)
- **Output**: usage stats, popular dimensions, tool usage

## 🗣️ **Example Usage in Claude Desktop**

Once setup is complete, you can chat naturally:

```
You: "What's the volume of a 5-dimensional sphere with radius 3?"

Claude: Let me calculate that for you using the geometry tools...
→ [Calls calculate_hypersphere(5, 3) via MCP]
→ The volume of a 5-dimensional sphere with radius 3 is 1436.76 cubic units.

You: "Compare that to a 5D cube with side length 6"

Claude: I'll compare these shapes...
→ [Calls compare_shapes with both shapes]
→ The 5D cube (volume: 7776) is 5.4x larger than the 5D sphere.
```

## 🔧 **Troubleshooting**

### **Server Not Starting**
```bash
# Check dependencies
source venv/bin/activate
python -c "import mcp, httpx; print('Dependencies OK')"

# Test AWS connectivity
curl -X POST "https://s6ngc23inj.execute-api.us-east-1.amazonaws.com/prod/mcp" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

### **Claude Desktop Not Seeing Tools**
1. **Check config file location** (see paths above)
2. **Verify JSON syntax** (use a JSON validator)
3. **Check absolute paths** in the `args` field
4. **Restart Claude Desktop** completely
5. **Check Claude Desktop logs** for error messages

### **Permission Issues**
```bash
# Make server executable
chmod +x geometry_oracle_mcp_server.py

# Ensure Python path is correct
which python
```

## 📈 **Monitoring**

### **Server Logs**
The MCP server logs to stderr, so you'll see connection info when Claude Desktop connects.

### **AWS Usage**
All calculations hit your AWS infrastructure:
- **Lambda**: `geometry-oracle-mcp` function
- **DynamoDB**: `geometry-oracle-mcp-prod-queries` table
- **API Gateway**: Real-time request logging

### **Cost Tracking**
Your AWS usage will increase with MCP usage, but should remain minimal (estimated $1-5/month for typical usage).

## 🌟 **What This Enables**

- **Natural Language Geometry**: Just ask Claude for calculations
- **Infinite Dimensions**: 1D to 100D+ shape calculations  
- **Research Data**: All queries logged to your AWS analytics
- **Seamless Integration**: No APIs, no JSON, just conversation
- **Production Infrastructure**: Backed by your scalable AWS deployment

## 🔗 **Architecture**

```
Claude Desktop User
    ↓ Natural language
Claude Desktop (with MCP client)
    ↓ stdio/JSON-RPC 2.0
geometry_oracle_mcp_server.py (Local proxy)
    ↓ HTTPS
AWS API Gateway (s6ngc23inj.execute-api.us-east-1.amazonaws.com)
    ↓ Invoke
AWS Lambda (geometry-oracle-mcp)
    ↓ Logs to
DynamoDB (geometry-oracle-mcp-prod-queries)
```

---

**🌌 Ready to explore infinite dimensions through natural conversation!**

*From a 2014 CS102 sphere calculator to Claude Desktop integration - the journey continues...*