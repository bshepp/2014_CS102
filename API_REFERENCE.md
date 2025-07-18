# 🔌 N-Dimensional Geometry Engine API Reference

**Complete API Documentation for the N-Dimensional Geometry Engine**

## 📋 **Table of Contents**

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

## 🌐 **Overview**

The N-Dimensional Geometry Engine provides a RESTful API for creating, analyzing, and visualizing geometric shapes in N-dimensional space. The API supports mathematical operations, tiling patterns, and natural language queries.

### **Key Features**
- **N-Dimensional Support**: 1D to 100D+ geometric shapes
- **Mathematical Accuracy**: Verified to 1e-10 tolerance
- **Real-time Calculations**: Instant geometric computations
- **Visualization Data**: 3D/4D plotting coordinates
- **Natural Language Processing**: Intuitive geometry queries

---

## 🔐 **Authentication**

Currently, the API does not require authentication. All endpoints are publicly accessible.

**Future Enhancement**: Authentication will be added in v2.0 with API key support.

---

## 🌍 **Base URL**

```
http://localhost:8000
```

**Production URL**: TBD (when deployed)

---

## 📊 **Common Parameters**

### **Dimensional Parameters**
- `dimensions` (integer): Number of dimensions (1-100+)
- `radius` (float): Radius value for spherical shapes
- `side_length` (float): Side length for cubic shapes

### **Visualization Parameters**
- `include_visualization` (boolean): Include 3D/4D plot data
- `resolution` (integer): Visualization resolution (10-1000)

### **Precision Parameters**
- `precision` (integer): Decimal precision (1-15)
- `tolerance` (float): Calculation tolerance (default: 1e-10)

---

## 📄 **Response Format**

All API responses follow a consistent JSON structure:

```json
{
  "success": true,
  "data": {
    "shape_type": "hypersphere",
    "dimensions": 4,
    "properties": {
      "volume": 19.7392,
      "surface_area": 39.4784
    },
    "metadata": {
      "calculation_time": 0.001,
      "precision": 1e-10
    }
  },
  "visualization": {
    "coordinates": [...],
    "plot_data": {...}
  }
}
```

---

## ⚠️ **Error Handling**

### **Error Response Format**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_DIMENSIONS",
    "message": "Dimensions must be between 1 and 100",
    "details": {
      "provided_value": 150,
      "valid_range": [1, 100]
    }
  }
}
```

### **HTTP Status Codes**
- **200 OK**: Successful request
- **400 Bad Request**: Invalid input parameters
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error

### **Error Codes**
- `INVALID_DIMENSIONS`: Invalid dimension count
- `INVALID_RADIUS`: Invalid radius value
- `CALCULATION_ERROR`: Mathematical computation failed
- `VISUALIZATION_ERROR`: Visualization generation failed
- `QUERY_PARSING_ERROR`: Natural language query parsing failed

---

## 🎯 **Endpoints**

### **1. Create Hypersphere**

Create and analyze an N-dimensional hypersphere.

```http
POST /api/sphere
```

**Request Body:**
```json
{
  "radius": 2.5,
  "dimensions": 4,
  "include_visualization": true,
  "precision": 6
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "shape_type": "hypersphere",
    "dimensions": 4,
    "radius": 2.5,
    "properties": {
      "volume": 19.7392,
      "surface_area": 39.4784,
      "diameter": 5.0,
      "circumference": 15.7080
    },
    "formulas": {
      "volume": "π² * r⁴ / 2",
      "surface_area": "2π² * r³"
    }
  }
}
```

### **2. Create Hypercube**

Generate and analyze an N-dimensional hypercube.

```http
POST /api/cube
```

**Request Body:**
```json
{
  "side_length": 3.0,
  "dimensions": 5,
  "include_edges": true,
  "include_vertices": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "shape_type": "hypercube",
    "dimensions": 5,
    "side_length": 3.0,
    "properties": {
      "volume": 243.0,
      "surface_area": 486.0,
      "vertices": 32,
      "edges": 80,
      "faces": 80
    },
    "vertex_coordinates": [...],
    "edge_list": [...]
  }
}
```

### **3. Create Hyperellipsoid**

Create an N-dimensional hyperellipsoid with custom axis lengths.

```http
POST /api/ellipsoid
```

**Request Body:**
```json
{
  "axis_lengths": [2.0, 3.0, 1.5],
  "dimensions": 3,
  "include_eccentricity": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "shape_type": "hyperellipsoid",
    "dimensions": 3,
    "axis_lengths": [2.0, 3.0, 1.5],
    "properties": {
      "volume": 18.8496,
      "surface_area": 45.2389,
      "eccentricity": 0.8165,
      "semi_axes": [2.0, 3.0, 1.5]
    }
  }
}
```

### **4. Create Simplex**

Generate an N-dimensional simplex (generalized triangle).

```http
POST /api/simplex
```

**Request Body:**
```json
{
  "dimensions": 4,
  "edge_length": 2.0,
  "include_coordinates": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "shape_type": "simplex",
    "dimensions": 4,
    "edge_length": 2.0,
    "properties": {
      "volume": 0.9428,
      "surface_area": 6.9282,
      "vertices": 5,
      "circumradius": 1.5811,
      "inradius": 0.3953
    },
    "vertex_coordinates": [...]
  }
}
```

### **5. Create Hyperpyramid**

Create an N-dimensional hyperpyramid.

```http
POST /api/pyramid
```

**Request Body:**
```json
{
  "base_dimensions": 3,
  "height": 4.0,
  "base_side_length": 2.0
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "shape_type": "hyperpyramid",
    "base_dimensions": 3,
    "height": 4.0,
    "base_side_length": 2.0,
    "properties": {
      "volume": 2.3094,
      "surface_area": 15.4641,
      "slant_height": 4.2426,
      "lateral_edges": 4.4721
    }
  }
}
```

### **6. Generate Tiling Pattern**

Create tiling and tessellation patterns.

```http
POST /api/tiling
```

**Request Body:**
```json
{
  "pattern_type": "hexagonal",
  "dimensions": 2,
  "size": [10, 10],
  "tile_size": 1.0,
  "include_analysis": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "pattern_type": "hexagonal",
    "dimensions": 2,
    "tile_count": 100,
    "properties": {
      "coverage_efficiency": 0.9069,
      "coordination_number": 6,
      "symmetry_group": "p6m"
    },
    "tiles": [
      {
        "id": 1,
        "center": [0.5, 0.866],
        "vertices": [...]
      }
    ]
  }
}
```

### **7. Natural Language Query**

Process natural language geometry queries.

```http
POST /api/query
```

**Request Body:**
```json
{
  "query": "What is the volume of a 4D sphere with radius 3?",
  "include_explanation": true,
  "include_visualization": false
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "query": "What is the volume of a 4D sphere with radius 3?",
    "parsed_intent": {
      "shape_type": "hypersphere",
      "dimensions": 4,
      "radius": 3.0,
      "requested_property": "volume"
    },
    "result": {
      "volume": 111.2654,
      "formula": "π² * r⁴ / 2",
      "calculation_steps": [
        "π² ≈ 9.8696",
        "r⁴ = 3⁴ = 81",
        "Volume = 9.8696 * 81 / 2 = 111.2654"
      ]
    },
    "explanation": "A 4D hypersphere with radius 3 has a volume of approximately 111.27 cubic units."
  }
}
```

### **8. Compare Shapes**

Compare properties of multiple geometric shapes.

```http
POST /api/compare
```

**Request Body:**
```json
{
  "shapes": [
    {
      "type": "sphere",
      "radius": 2.0,
      "dimensions": 3
    },
    {
      "type": "cube",
      "side_length": 2.0,
      "dimensions": 3
    }
  ],
  "comparison_properties": ["volume", "surface_area"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "comparison": [
      {
        "shape": "sphere",
        "properties": {
          "volume": 33.5103,
          "surface_area": 50.2655
        }
      },
      {
        "shape": "cube",
        "properties": {
          "volume": 8.0,
          "surface_area": 24.0
        }
      }
    ],
    "analysis": {
      "volume_ratio": 4.1888,
      "surface_area_ratio": 2.0944
    }
  }
}
```

### **9. Health Check**

Check API health and status.

```http
GET /api/health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "uptime": "2h 34m 12s",
    "capabilities": {
      "max_dimensions": 100,
      "supported_shapes": ["sphere", "cube", "ellipsoid", "simplex", "pyramid"],
      "tiling_patterns": ["regular", "hexagonal", "voronoi"]
    }
  }
}
```

### **10. Get Supported Dimensions**

Retrieve information about supported dimensions for each shape type.

```http
GET /api/dimensions
```

**Response:**
```json
{
  "success": true,
  "data": {
    "supported_dimensions": {
      "sphere": {"min": 1, "max": 100, "optimal": 20},
      "cube": {"min": 1, "max": 50, "optimal": 10},
      "ellipsoid": {"min": 2, "max": 50, "optimal": 10},
      "simplex": {"min": 1, "max": 30, "optimal": 10},
      "pyramid": {"min": 2, "max": 30, "optimal": 8}
    },
    "performance_notes": {
      "high_dimensions": "Dimensions > 20 may have increased computation time",
      "memory_usage": "Memory usage scales exponentially with dimensions"
    }
  }
}
```

---

## 💡 **Examples**

### **Example 1: Basic Hypersphere**
```bash
curl -X POST "http://localhost:8000/api/sphere" \
  -H "Content-Type: application/json" \
  -d '{
    "radius": 1.0,
    "dimensions": 3
  }'
```

### **Example 2: Complex Tiling Pattern**
```bash
curl -X POST "http://localhost:8000/api/tiling" \
  -H "Content-Type: application/json" \
  -d '{
    "pattern_type": "voronoi",
    "dimensions": 2,
    "size": [20, 20],
    "seed_points": 50,
    "include_analysis": true
  }'
```

### **Example 3: Natural Language Query**
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Compare the volume of a 4D cube with side length 2 to a 4D sphere with radius 2",
    "include_explanation": true
  }'
```

---

## 🚦 **Rate Limiting**

**Current Status**: No rate limiting implemented.

**Future Implementation**: 
- 1000 requests per hour per IP
- Premium tier: 10,000 requests per hour
- Burst limit: 100 requests per minute

---

## 📚 **SDKs and Libraries**

### **Python SDK** (Planned)
```python
from geometry_engine import GeometryAPI

client = GeometryAPI(base_url="http://localhost:8000")
sphere = client.create_sphere(radius=2.0, dimensions=4)
print(f"Volume: {sphere.volume}")
```

### **JavaScript SDK** (Planned)
```javascript
import { GeometryAPI } from 'geometry-engine-js';

const client = new GeometryAPI('http://localhost:8000');
const sphere = await client.createSphere({
  radius: 2.0,
  dimensions: 4
});
console.log(`Volume: ${sphere.volume}`);
```

---

## 🔧 **Interactive Documentation**

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Spec**: http://localhost:8000/api/openapi.json

---

## 📞 **Support and Feedback**

- **GitHub Issues**: [Report bugs or request features](https://github.com/bshepp/2014_CS102/issues)
- **Documentation**: See [TESTING.md](TESTING.md) for testing examples
- **Architecture**: See [CLAUDE.md](CLAUDE.md) for system details

---

## 🔄 **Changelog**

### **v1.0.0** (Current)
- Initial API release
- 10 core endpoints
- N-dimensional geometry support
- Natural language processing
- Tiling pattern generation

### **v1.1.0** (Planned)
- Authentication system
- Rate limiting
- Enhanced visualization
- Batch processing
- Python/JavaScript SDKs

---

*This API reference is comprehensive and covers all available endpoints and functionality of the N-Dimensional Geometry Engine.*