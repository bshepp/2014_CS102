# GeometryOracle MCP Tools Reference

**Complete MCP Tools Documentation for the GeometryOracle MCP Server**

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Base URL](#base-url)
- [Common Parameters](#common-parameters)
- [Response Format](#response-format)
- [Error Handling](#error-handling)
- [Endpoints](#endpoints)
- [Examples](#examples)
- [Rate Limiting](#rate-limiting)
- [SDKs and Libraries](#sdks-and-libraries)

---

## Overview

The GeometryOracle MCP Server provides Model Context Protocol (MCP) tools for creating, analyzing, and processing geometric shapes in N-dimensional space. The tools support mathematical operations, batch processing, and AI-focused analysis capabilities.

### **Key Features**
- **N-Dimensional Support**: 1D to 100D+ geometric shapes
- **Mathematical Accuracy**: Verified to 1e-10 tolerance
- **Real-time Calculations**: Instant geometric computations
- **Batch Processing**: Efficient multi-shape analysis
- **AI-Focused Tools**: Optimized for Claude Desktop integration

---

## 🔐 **Authentication**

MCP tools communicate through the Model Context Protocol. Authentication is handled by Claude Desktop's MCP client.

**Security**: Tools operate within Claude Desktop's sandbox environment.

---

## 🌍 **MCP Server Connection**

```
python geometry_oracle_mcp_server.py
```

**Production Server**: AWS Lambda (auto-scaling, serverless)

---

## 🛠️ **Available MCP Tools**

### **Core Geometry Tools**
- `calculate_shape_properties`: Calculate geometric properties for any N-dimensional shape
- `compare_shapes`: Compare multiple shapes and analyze relationships
- `generate_tiling_pattern`: Create tessellation patterns with mathematical analysis

### **AI-Focused Tools**  
- `batch_process_shapes`: Efficient processing of multiple geometric calculations
- `analyze_dimensional_scaling`: Study how properties scale across dimensions
- `geometry_insights`: Generate mathematical insights and pattern analysis

---

## 📄 **Tool Response Format**

All MCP tool responses follow a consistent structure:

```json
{
  "shape_type": "hypersphere",
  "dimensions": 4,
  "properties": {
    "volume": 19.7392,
    "surface_area": 39.4784
  },
  "metadata": {
    "calculation_time": 0.001,
    "precision": 1e-10
  },
  "analysis": {
    "mathematical_insights": "...",
    "scaling_behavior": "..."
  }
}
```

---

## ⚠️ **Error Handling**

### **MCP Tool Errors**
MCP tools return detailed error information when validation fails:

```
Error: Invalid dimensions value
Details: Dimensions must be between 1 and 100 (provided: 150)
Suggestion: Try using dimensions between 1-50 for optimal performance
```

### **Common Error Types**
- **Validation Errors**: Invalid parameter values
- **Calculation Errors**: Mathematical computation failures  
- **Resource Errors**: Memory or computation limits exceeded
- **Input Errors**: Malformed or missing required parameters

### **Error Recovery**
All tools provide suggestions for fixing invalid inputs and alternative approaches.

---

## 🛠️ **MCP Tools Documentation**

### **1. calculate_shape_properties**

Calculate geometric properties for any N-dimensional shape.

**Usage:**
```
Calculate the volume of a 4D sphere with radius 2.5
```

**Parameters:**
- `shape_type`: "sphere", "cube", "ellipsoid", "simplex", or "pyramid"
- `dimensions`: Number of dimensions (1-100)
- `size_parameters`: Radius, side length, or axis lengths
- `analysis_level`: "basic", "detailed", or "comprehensive"

**Example Response:**
```
Shape: 4D Hypersphere
Dimensions: 4
Radius: 2.5
Volume: 19.7392 cubic units
Surface Area: 39.4784 square units
Formula: V = π²r⁴/2
Scaling: Volume grows as r⁴ in 4D space
```

### **2. compare_shapes**

Compare multiple shapes and analyze their relationships.

**Usage:**
```
Compare a 3D sphere (radius 2) with a 3D cube (side 2)
```

**Parameters:**
- `shapes`: List of shape definitions to compare
- `comparison_metrics`: Properties to compare (volume, surface area, etc.)
- `include_ratios`: Calculate ratios between shapes
- `analysis_depth`: Level of mathematical analysis

**Example Response:**
```
Shape Comparison Analysis:

3D Sphere (r=2):
- Volume: 33.51 cubic units
- Surface Area: 50.27 square units

3D Cube (s=2):
- Volume: 8.00 cubic units  
- Surface Area: 24.00 square units

Comparison:
- Sphere volume is 4.19× larger
- Sphere surface area is 2.09× larger
- Sphere has optimal volume-to-surface ratio
```

### **3. generate_tiling_pattern**

Create tessellation patterns with mathematical analysis.

**Usage:**
```
Generate a hexagonal tiling pattern for a 10×10 area
```

**Parameters:**
- `pattern_type`: "regular", "hexagonal", "voronoi", or "custom"
- `dimensions`: Spatial dimensions for tiling
- `area_size`: Dimensions of the area to tile
- `tile_parameters`: Size and spacing parameters
- `include_analysis`: Mathematical properties analysis

**Example Response:**
```
Hexagonal Tiling Pattern:

Pattern: Regular Hexagonal
Area: 10×10 square units
Tile Count: 87 hexagons
Coverage Efficiency: 90.69%
Coordination Number: 6
Symmetry Group: p6m

Properties:
- Optimal 2D space-filling pattern
- Maximum area-to-perimeter ratio
- 6-fold rotational symmetry
- Used in nature (honeycomb, basalt columns)
```

### **4. batch_process_shapes**

Efficient processing of multiple geometric calculations.

**Usage:**
```
Calculate volumes for spheres with radii 1,2,3,4,5 in dimensions 2,3,4
```

**Parameters:**
- `shape_configurations`: List of shapes to process
- `processing_mode`: "parallel", "sequential", or "optimized"
- `output_format`: "table", "summary", or "detailed"
- `include_statistics`: Statistical analysis of results

**Example Response:**
```
Batch Processing Results:

Processed: 15 shapes (5 radii × 3 dimensions)
Execution Time: 0.023 seconds
Success Rate: 100%

Results Summary:
┌─────────┬──────┬──────┬──────┐
│ Radius  │  2D  │  3D  │  4D  │
├─────────┼──────┼──────┼──────┤
│    1    │ 3.14 │ 4.19 │ 4.93 │
│    2    │12.57 │33.51 │78.96 │
│    3    │28.27 │113.1 │445.1 │
└─────────┴──────┴──────┴──────┘

Trends: Volume scales as r^n where n = dimensions
```

### **5. analyze_dimensional_scaling**

Study how geometric properties scale across dimensions.

**Usage:**
```
Analyze how sphere volume scales from 1D to 10D with unit radius
```

**Parameters:**
- `shape_type`: Shape to analyze across dimensions
- `dimension_range`: Range of dimensions to study
- `scaling_parameter`: Property to track (volume, surface area, etc.)
- `analysis_type`: "scaling", "optimization", or "comparison"

**Example Response:**
```
Dimensional Scaling Analysis: Unit Sphere Volume

Dimension Range: 1D to 10D
Parameter: Volume
Radius: 1.0 (constant)

Scaling Pattern:
1D: Length = 2.000
2D: Area = 3.142 (π)
3D: Volume = 4.189 (4π/3)
4D: Hypervolume = 4.935 (π²/2)
5D: Hypervolume = 5.264
6D: Hypervolume = 5.168
7D: Hypervolume = 4.725
8D: Hypervolume = 4.059
9D: Hypervolume = 3.299
10D: Hypervolume = 2.550

Key Insight: Unit sphere volume peaks at 5D!
Phenomenon: "Curse of dimensionality" - volume concentrates near surface in high dimensions
```

### **6. geometry_insights**

Generate mathematical insights and pattern analysis.

**Usage:**
```
Provide insights about the relationship between cube and sphere volumes in 3D
```

**Parameters:**
- `topic`: Geometric concept or relationship to analyze
- `context_shapes`: Relevant shapes for the analysis
- `insight_type`: "mathematical", "historical", "applications", or "connections"
- `depth_level`: "overview", "detailed", or "research"

**Example Response:**
```
Geometric Insights: Cube vs Sphere Volume Relationship

Mathematical Relationship:
- Sphere inscribed in unit cube: Volume ratio = π/6 ≈ 0.524
- Cube inscribed in unit sphere: Volume ratio = 6/π ≈ 1.910
- Maximum sphere in unit cube fills ~52.4% of space

Historical Context:
- Archimedes (3rd century BC) first calculated sphere volume
- Relationship appears in sphere packing problems
- Connected to isoperimetric inequality

Applications:
- Sphere packing in crystallography
- Optimal container design
- Error analysis in high-dimensional data

Mathematical Beauty:
"The sphere is nature's solution to maximizing volume while minimizing surface area - the isoperimetric champion of geometry."
```





---

## 💡 **Usage Examples**

### **Example 1: Basic Shape Calculation**
```
User: Calculate the volume of a 3D sphere with radius 5
Claude: I'll use the calculate_shape_properties tool to find that.

[Tool Result: Volume = 523.6 cubic units, Formula: V = (4/3)πr³]
```

### **Example 2: Dimensional Analysis**
```
User: How does sphere volume change as we go from 2D to 6D?
Claude: I'll analyze dimensional scaling for you.

[Tool Result: Shows volume peaks at 5D, then decreases - demonstrates curse of dimensionality]
```

### **Example 3: Complex Comparison**
```
User: Compare packing efficiency of spheres vs cubes in 3D space
Claude: I'll compare these shapes and analyze their packing properties.

[Tool Result: Sphere packing ~74% (face-centered cubic), cube packing 100%, with trade-offs]
```

---

## 🚦 **Performance and Limits**

**MCP Tool Performance**:
- Sub-millisecond calculations for dimensions 1-20
- Automatic optimization for high-dimensional computations
- Efficient batch processing for multiple shapes

**Computational Limits**:
- Maximum dimensions: 100 (with performance warnings >20)
- Batch processing: Up to 1000 shapes per request
- Memory usage scales with dimension complexity

---

## 🔧 **Integration and Setup**

### **Claude Desktop Configuration**
Add to your Claude Desktop MCP settings:
```json
{
  "mcpServers": {
    "geometry-oracle": {
      "command": "python",
      "args": ["/path/to/geometry_oracle_mcp_server.py"],
      "env": {}
    }
  }
}
```

### **Local Development**
```bash
# Install dependencies
pip install -r requirements-production.txt

# Start MCP server
python geometry_oracle_mcp_server.py

# Connect Claude Desktop to use tools
```

---

## 📖 **Documentation and Resources**

- **Tool Testing**: Use Claude Desktop's MCP inspector
- **Source Code**: geometry_oracle_mcp_server.py
- **Examples**: Available in Claude Desktop chat interface

---

## Support and Feedback

- **GitHub Issues**: [Report bugs or request features](https://github.com/bshepp/2014_CS102/issues)
- **Documentation**: See [TESTING.md](TESTING.md) for testing examples
- **Architecture**: See [CLAUDE.md](CLAUDE.md) for system details

---

## 🔄 **Version History**

### **v2.0.0** (Current - MCP Architecture)
- Complete transformation to MCP-only architecture
- 6 specialized MCP tools for Claude Desktop
- AI-focused batch processing capabilities
- Dimensional scaling analysis tools
- Mathematical insights generation
- AWS Lambda production deployment

### **v1.0.0** (Legacy - Web API)
- Previous REST API implementation
- Deprecated in favor of MCP architecture
- Archived for reference

---

*This reference covers all available MCP tools and functionality of the GeometryOracle MCP Server.*