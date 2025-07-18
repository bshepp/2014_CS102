#!/usr/bin/env python3
"""
FastAPI Web API for the N-Dimensional Geometry Engine
Exposes the geometry engine capabilities through REST endpoints
"""

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import json
import math

# Import our geometry engine
from geometry_engine import GeometryAgent, HyperSphere, HyperCube, HyperEllipsoid, Simplex, HyperPyramid, OriginalSphere, JavaBridge, RegularTiling, HexagonalTiling, VoronoiTiling, TilingAnalyzer

# FastAPI app setup
app = FastAPI(
    title="N-Dimensional Geometry Engine API",
    description="Transform your CS102 sphere calculator into infinite dimensions with AI-powered natural language queries",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize geometry agent
geometry_agent = GeometryAgent()

# Pydantic models for request/response
class SphereRequest(BaseModel):
    dimensions: int = Field(..., ge=1, le=100, description="Number of dimensions (1-100)")
    radius: float = Field(..., gt=0, description="Sphere radius")

class CubeRequest(BaseModel):
    dimensions: int = Field(..., ge=1, le=100, description="Number of dimensions (1-100)")
    side_length: float = Field(..., gt=0, description="Cube side length")

class EllipsoidRequest(BaseModel):
    dimensions: int = Field(..., ge=1, le=100, description="Number of dimensions (1-100)")
    semi_axes: List[float] = Field(..., description="Semi-axes lengths (must match dimensions)")

class SimplexRequest(BaseModel):
    dimensions: int = Field(..., ge=1, le=100, description="Number of dimensions (1-100)")
    side_length: float = Field(..., gt=0, description="Simplex side length")

class PyramidRequest(BaseModel):
    dimensions: int = Field(..., ge=1, le=100, description="Number of dimensions (1-100)")
    base_side_length: float = Field(..., gt=0, description="Base side length")
    height: float = Field(..., gt=0, description="Pyramid height")

class TilingRequest(BaseModel):
    tiling_type: str = Field(..., description="Type of tiling: 'regular', 'hexagonal', 'voronoi'")
    dimensions: int = Field(..., ge=1, le=100, description="Number of dimensions (1-100)")
    bounds: List[List[float]] = Field(..., description="Bounds for each dimension [[min, max], ...]")
    density: float = Field(1.0, gt=0, description="Tiling density (default: 1.0)")
    # Regular tiling parameters
    shape_type: Optional[str] = Field(None, description="For regular tiling: 'cube', 'sphere', 'simplex'")
    parameter: Optional[float] = Field(None, gt=0, description="Shape parameter (side length, radius, etc.)")
    # Hexagonal tiling parameters
    side_length: Optional[float] = Field(None, gt=0, description="For hexagonal tiling: side length")
    # Voronoi tiling parameters
    seed_points: Optional[List[List[float]]] = Field(None, description="For voronoi: seed points")
    num_random_seeds: Optional[int] = Field(None, ge=1, description="For voronoi: number of random seeds")

class TilingResponse(BaseModel):
    tiling_type: str
    dimensions: int
    tile_count: int
    coverage_efficiency: float
    pattern_properties: Dict[str, Any]
    tiles: List[Dict[str, Any]]
    analysis: Optional[Dict[str, Any]] = None

class ShapeResponse(BaseModel):
    dimensions: int
    parameter: float
    parameter_name: str
    volume: float
    surface_area: float
    volume_formula: str
    surface_area_formula: str
    shape_type: str
    additional_properties: Optional[Dict[str, Any]] = None

# Keep backwards compatibility
SphereResponse = ShapeResponse

class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language geometry query")

class QueryResponse(BaseModel):
    query: str
    response: str
    success: bool

class ComparisonRequest(BaseModel):
    dimensions: int = Field(..., ge=1, le=100)
    parameter: float = Field(..., gt=0)

class ComparisonResponse(BaseModel):
    dimensions: int
    parameter: float
    sphere_volume: float
    sphere_surface: float
    comparison_data: Dict[str, Any]

class VisualizationRequest(BaseModel):
    dimensions: int = Field(..., ge=1, le=4, description="Dimensions for visualization (1-4)")
    parameter: float = Field(..., gt=0, description="Shape parameter (radius for sphere, side length for cube)")
    shape_type: str = Field("sphere", description="Shape type: 'sphere' or 'cube'")
    cross_section: Optional[float] = Field(None, description="Cross-section distance from center")

# API Endpoints

@app.get("/demo", response_class=HTMLResponse)
async def demo():
    """Serve the interactive demo page"""
    with open("demo.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main web interface"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>N-Dimensional Geometry Engine</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 1200px; margin: 0 auto; background: rgba(0,0,0,0.3); padding: 40px; border-radius: 15px; }
            h1 { text-align: center; font-size: 2.5em; margin-bottom: 10px; }
            .subtitle { text-align: center; font-size: 1.2em; margin-bottom: 30px; opacity: 0.9; }
            .section { margin: 30px 0; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 10px; }
            .btn { display: inline-block; padding: 12px 25px; margin: 10px; background: #4CAF50; color: white; text-decoration: none; border-radius: 5px; transition: all 0.3s; }
            .btn:hover { background: #45a049; transform: translateY(-2px); }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
            .feature { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center; }
            .api-link { background: #2196F3; }
            .api-link:hover { background: #1976D2; }
            .demo-link { background: #FF9800; }
            .demo-link:hover { background: #F57C00; }
            .code { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; font-family: monospace; overflow-x: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌌 N-Dimensional Geometry Engine</h1>
            <p class="subtitle">From CS102 (2014) to Infinite Dimensions • AI-Powered • Web-Enabled</p>
            
            <div class="section">
                <h2>🚀 Quick Start</h2>
                <p>Transform your original CS102 sphere calculator into a powerful n-dimensional geometry engine!</p>
                <div>
                    <a href="/api/docs" class="btn api-link">📚 API Documentation</a>
                    <a href="/demo" class="btn demo-link">🎮 Interactive Demo</a>
                    <a href="/visualize" class="btn">📊 3D Visualizations</a>
                </div>
            </div>

            <div class="section">
                <h2>✨ Features</h2>
                <div class="features">
                    <div class="feature">
                        <h3>🔢 N-Dimensional Shapes</h3>
                        <p>Spheres, cubes, ellipsoids, simplices, and pyramids from 1D to 100D+</p>
                    </div>
                    <div class="feature">
                        <h3>🔲 Tiling & Tessellations</h3>
                        <p>Regular tilings, hexagonal patterns, Voronoi diagrams, and space-filling</p>
                    </div>
                    <div class="feature">
                        <h3>🤖 AI Interface</h3>
                        <p>Natural language queries like "create a 5D ellipsoid with axes 1 2 3 4 5"</p>
                    </div>
                    <div class="feature">
                        <h3>☕ Original Java Integration</h3>
                        <p>Your CS102 code from 2014 is preserved and executable</p>
                    </div>
                    <div class="feature">
                        <h3>📈 Interactive Visualizations</h3>
                        <p>Real-time 3D rendering and cross-sectional analysis</p>
                    </div>
                    <div class="feature">
                        <h3>🔍 Pattern Analysis</h3>
                        <p>Symmetry analysis, coverage efficiency, and mathematical properties</p>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>🔬 Try It Now</h2>
                <p>Example API calls:</p>
                <div class="code">
                    # Create a 4D hypersphere
                    curl -X POST "http://localhost:8000/api/sphere" \\
                         -H "Content-Type: application/json" \\
                         -d '{"dimensions": 4, "radius": 1.5}'
                    
                    # Create a 3D ellipsoid
                    curl -X POST "http://localhost:8000/api/ellipsoid" \\
                         -H "Content-Type: application/json" \\
                         -d '{"dimensions": 3, "semi_axes": [1.0, 2.0, 3.0]}'
                    
                    # Create a 4D pyramid
                    curl -X POST "http://localhost:8000/api/pyramid" \\
                         -H "Content-Type: application/json" \\
                         -d '{"dimensions": 4, "base_side_length": 2.0, "height": 3.0}'
                    
                    # Create hexagonal tiling
                    curl -X POST "http://localhost:8000/api/tiling" \\
                         -H "Content-Type: application/json" \\
                         -d '{"tiling_type": "hexagonal", "dimensions": 2, "bounds": [[0, 10], [0, 10]], "side_length": 1.0}'
                    
                    # Create Voronoi diagram
                    curl -X POST "http://localhost:8000/api/tiling" \\
                         -H "Content-Type: application/json" \\
                         -d '{"tiling_type": "voronoi", "dimensions": 2, "bounds": [[0, 10], [0, 10]], "num_random_seeds": 8}'
                    
                    # Natural language query
                    curl -X POST "http://localhost:8000/api/query" \\
                         -H "Content-Type: application/json" \\
                         -d '{"query": "create a 5D simplex with side 2"}'
                </div>
            </div>

            <div class="section">
                <h2>📊 Mathematical Insights</h2>
                <p>Explore how geometry behaves in higher dimensions:</p>
                <ul>
                    <li>Volume peaks around 5-6 dimensions for unit spheres</li>
                    <li>Surface area scales as n × volume / radius</li>
                    <li>Most volume concentrates near the surface in high dimensions</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """)

@app.post("/api/sphere", response_model=ShapeResponse)
async def create_sphere(request: SphereRequest):
    """Create an n-dimensional sphere and return its properties"""
    try:
        sphere = HyperSphere(request.dimensions, request.radius)
        
        return ShapeResponse(
            dimensions=request.dimensions,
            parameter=request.radius,
            parameter_name="radius",
            volume=sphere.get_volume(),
            surface_area=sphere.get_surface_area(),
            volume_formula=sphere.get_volume_formula(),
            surface_area_formula=sphere.get_surface_area_formula(),
            shape_type=sphere.get_shape_type(),
            additional_properties={
                "diameter": 2 * request.radius
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/cube", response_model=ShapeResponse)
async def create_cube(request: CubeRequest):
    """Create an n-dimensional cube and return its properties"""
    try:
        cube = HyperCube(request.dimensions, request.side_length)
        
        return ShapeResponse(
            dimensions=request.dimensions,
            parameter=request.side_length,
            parameter_name="side_length",
            volume=cube.get_volume(),
            surface_area=cube.get_surface_area(),
            volume_formula=cube.get_volume_formula(),
            surface_area_formula=cube.get_surface_area_formula(),
            shape_type=cube.get_shape_type(),
            additional_properties={
                "vertices": cube.get_vertex_count(),
                "edges": cube.get_edge_count(),
                "diagonal": cube.get_diagonal_length(),
                "cross_section_volume": cube.get_cross_section(request.side_length / 2)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/ellipsoid", response_model=ShapeResponse)
async def create_ellipsoid(request: EllipsoidRequest):
    """Create an n-dimensional ellipsoid and return its properties"""
    try:
        if len(request.semi_axes) != request.dimensions:
            raise ValueError(f"Number of semi-axes ({len(request.semi_axes)}) must match dimensions ({request.dimensions})")
        
        ellipsoid = HyperEllipsoid(request.dimensions, *request.semi_axes)
        
        return ShapeResponse(
            dimensions=request.dimensions,
            parameter=max(request.semi_axes),  # Use largest semi-axis as primary parameter
            parameter_name="max_semi_axis",
            volume=ellipsoid.get_volume(),
            surface_area=ellipsoid.get_surface_area(),
            volume_formula=ellipsoid.get_volume_formula(),
            surface_area_formula=ellipsoid.get_surface_area_formula(),
            shape_type=ellipsoid.get_shape_type(),
            additional_properties={
                "semi_axes": request.semi_axes,
                "axis_ratio": ellipsoid.get_axis_ratio(),
                "is_sphere": ellipsoid.is_sphere(),
                "eccentricity": ellipsoid.get_eccentricity() if request.dimensions == 2 else None
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/simplex", response_model=ShapeResponse)
async def create_simplex(request: SimplexRequest):
    """Create an n-dimensional simplex and return its properties"""
    try:
        simplex = Simplex(request.dimensions, request.side_length)
        
        return ShapeResponse(
            dimensions=request.dimensions,
            parameter=request.side_length,
            parameter_name="side_length",
            volume=simplex.get_volume(),
            surface_area=simplex.get_surface_area(),
            volume_formula=simplex.get_volume_formula(),
            surface_area_formula=simplex.get_surface_area_formula(),
            shape_type=simplex.get_shape_type(),
            additional_properties={
                "vertices": simplex.get_vertex_count(),
                "edges": simplex.get_edge_count(),
                "circumradius": simplex.get_circumradius(),
                "inradius": simplex.get_inradius(),
                "height": simplex.get_height()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/pyramid", response_model=ShapeResponse)
async def create_pyramid(request: PyramidRequest):
    """Create an n-dimensional pyramid and return its properties"""
    try:
        pyramid = HyperPyramid(request.dimensions, request.base_side_length, request.height)
        
        return ShapeResponse(
            dimensions=request.dimensions,
            parameter=request.base_side_length,
            parameter_name="base_side_length",
            volume=pyramid.get_volume(),
            surface_area=pyramid.get_surface_area(),
            volume_formula=pyramid.get_volume_formula(),
            surface_area_formula=pyramid.get_surface_area_formula(),
            shape_type=pyramid.get_shape_type(),
            additional_properties={
                "height": request.height,
                "vertices": pyramid.get_vertex_count(),
                "edges": pyramid.get_edge_count(),
                "slant_height": pyramid.get_slant_height(),
                "lateral_edge_length": pyramid.get_lateral_edge_length(),
                "base_volume": pyramid.get_base_volume(),
                "base_surface_area": pyramid.get_base_surface_area()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/query", response_model=QueryResponse)
async def natural_language_query(request: QueryRequest):
    """Process natural language geometry queries"""
    try:
        response = geometry_agent.process_query(request.query)
        return QueryResponse(
            query=request.query,
            response=response,
            success=True
        )
    except Exception as e:
        return QueryResponse(
            query=request.query,
            response=f"Error processing query: {str(e)}",
            success=False
        )

@app.post("/api/original-java")
async def run_original_java(diameter: float = Query(..., description="Sphere diameter")):
    """Execute the original CS102 Java code"""
    try:
        result = geometry_agent.java_bridge.run_original_multisphere(diameter)
        return JSONResponse(content={
            "diameter": diameter,
            "java_available": geometry_agent.java_bridge.java_available,
            "result": result,
            "success": True
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/compare", response_model=ComparisonResponse)
async def compare_shapes(request: ComparisonRequest):
    """Compare different geometric shapes"""
    try:
        sphere = HyperSphere(request.dimensions, request.parameter)
        cube = HyperCube(request.dimensions, request.parameter)
        
        sphere_volume = sphere.get_volume()
        cube_volume = cube.get_volume()
        sphere_surface = sphere.get_surface_area()
        cube_surface = cube.get_surface_area()
        
        return ComparisonResponse(
            dimensions=request.dimensions,
            parameter=request.parameter,
            sphere_volume=sphere_volume,
            sphere_surface=sphere_surface,
            comparison_data={
                "sphere": {
                    "volume": sphere_volume,
                    "surface_area": sphere_surface,
                    "volume_formula": sphere.get_volume_formula(),
                    "surface_formula": sphere.get_surface_area_formula()
                },
                "cube": {
                    "volume": cube_volume,
                    "surface_area": cube_surface,
                    "volume_formula": cube.get_volume_formula(),
                    "surface_formula": cube.get_surface_area_formula(),
                    "vertices": cube.get_vertex_count(),
                    "edges": cube.get_edge_count(),
                    "diagonal": cube.get_diagonal_length()
                },
                "ratios": {
                    "volume_ratio_sphere_cube": sphere_volume / cube_volume,
                    "surface_ratio_sphere_cube": sphere_surface / cube_surface
                },
                "insights": {
                    "volume_comparison": "sphere" if sphere_volume > cube_volume else "cube",
                    "surface_comparison": "sphere" if sphere_surface > cube_surface else "cube"
                }
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/visualize")
async def create_visualization(request: VisualizationRequest):
    """Create interactive 3D visualizations"""
    try:
        if request.shape_type == "sphere":
            shape = HyperSphere(request.dimensions, request.parameter)
        else:  # cube
            shape = HyperCube(request.dimensions, request.parameter)
        
        if request.dimensions == 1:
            # 1D visualization
            fig = go.Figure()
            if request.shape_type == "sphere":
                # 1D sphere: line segment
                fig.add_trace(go.Scatter(
                    x=[-request.parameter, request.parameter],
                    y=[0, 0],
                    mode='lines+markers',
                    name='1D Sphere (Line)',
                    line=dict(width=5, color='blue')
                ))
                title = f"1D Sphere (Line Segment) - Radius: {request.parameter}"
            else:
                # 1D cube: line segment
                fig.add_trace(go.Scatter(
                    x=[0, request.parameter],
                    y=[0, 0],
                    mode='lines+markers',
                    name='1D Cube (Line)',
                    line=dict(width=5, color='red')
                ))
                title = f"1D Cube (Line Segment) - Side: {request.parameter}"
            
            fig.update_layout(
                title=title,
                xaxis_title="X",
                yaxis_title="Y",
                showlegend=False
            )
            
        elif request.dimensions == 2:
            # 2D: Circle
            theta = np.linspace(0, 2*np.pi, 100)
            x = request.radius * np.cos(theta)
            y = request.radius * np.sin(theta)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x, y=y,
                mode='lines',
                name='2D Sphere (Circle)',
                line=dict(width=3, color='green')
            ))
            fig.update_layout(
                title=f"2D Sphere (Circle) - Radius: {request.radius}",
                xaxis_title="X",
                yaxis_title="Y",
                showlegend=False,
                width=600,
                height=600
            )
            
        elif request.dimensions == 3:
            # 3D: Sphere
            u = np.linspace(0, 2 * np.pi, 50)
            v = np.linspace(0, np.pi, 50)
            x = request.radius * np.outer(np.cos(u), np.sin(v))
            y = request.radius * np.outer(np.sin(u), np.sin(v))
            z = request.radius * np.outer(np.ones(np.size(u)), np.cos(v))
            
            fig = go.Figure(data=[go.Surface(
                x=x, y=y, z=z,
                colorscale='Viridis',
                showscale=False,
                opacity=0.8
            )])
            fig.update_layout(
                title=f"3D Sphere - Radius: {request.radius}",
                scene=dict(
                    xaxis_title="X",
                    yaxis_title="Y",
                    zaxis_title="Z",
                    aspectmode='cube'
                ),
                width=700,
                height=700
            )
            
        elif request.dimensions == 4:
            # 4D: Cross-section visualization
            if request.cross_section is None:
                request.cross_section = 0.0
            
            # Calculate 3D cross-section
            if abs(request.cross_section) < request.radius:
                cross_radius = np.sqrt(request.radius**2 - request.cross_section**2)
                
                u = np.linspace(0, 2 * np.pi, 50)
                v = np.linspace(0, np.pi, 50)
                x = cross_radius * np.outer(np.cos(u), np.sin(v))
                y = cross_radius * np.outer(np.sin(u), np.sin(v))
                z = cross_radius * np.outer(np.ones(np.size(u)), np.cos(v))
                
                fig = go.Figure(data=[go.Surface(
                    x=x, y=y, z=z,
                    colorscale='Plasma',
                    showscale=False,
                    opacity=0.8
                )])
                fig.update_layout(
                    title=f"4D Sphere Cross-section at w={request.cross_section:.2f}<br>Cross-section radius: {cross_radius:.3f}",
                    scene=dict(
                        xaxis_title="X",
                        yaxis_title="Y",
                        zaxis_title="Z",
                        aspectmode='cube'
                    ),
                    width=700,
                    height=700
                )
            else:
                # Cross-section outside sphere
                fig = go.Figure()
                fig.add_annotation(
                    text="Cross-section outside sphere bounds",
                    x=0.5, y=0.5,
                    showarrow=False,
                    font=dict(size=20)
                )
                fig.update_layout(
                    title=f"4D Sphere - Cross-section at w={request.cross_section:.2f} (outside bounds)",
                    width=700,
                    height=700
                )
        
        # Add mathematical info
        fig.add_annotation(
            text=f"Volume: {sphere.get_volume():.6f}<br>Surface Area: {sphere.get_surface_area():.6f}",
            x=0.02, y=0.98,
            xref="paper", yref="paper",
            showarrow=False,
            bgcolor="rgba(255,255,255,0.8)",
            font=dict(size=12)
        )
        
        return JSONResponse(content={
            "plot_json": fig.to_json(),
            "dimensions": request.dimensions,
            "radius": request.radius,
            "volume": sphere.get_volume(),
            "surface_area": sphere.get_surface_area(),
            "cross_section": request.cross_section
        })
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/dimensions/{dimensions}")
async def get_dimension_info(dimensions: int = Path(..., ge=1, le=100)):
    """Get information about spheres in specific dimensions"""
    try:
        # Create unit sphere for reference
        unit_sphere = HyperSphere(dimensions, 1.0)
        
        # Calculate some interesting properties
        volume = unit_sphere.get_volume()
        surface = unit_sphere.get_surface_area()
        
        return {
            "dimensions": dimensions,
            "unit_sphere": {
                "volume": volume,
                "surface_area": surface,
                "volume_formula": unit_sphere.get_volume_formula(),
                "surface_formula": unit_sphere.get_surface_area_formula()
            },
            "insights": {
                "volume_peaks_at": "5-6 dimensions for unit spheres",
                "surface_to_volume_ratio": surface / volume if volume > 0 else float('inf'),
                "mathematical_note": f"In {dimensions}D, most volume is concentrated near the surface"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/tiling", response_model=TilingResponse)
async def create_tiling(request: TilingRequest):
    """Create tiling patterns and tessellations"""
    try:
        # Validate bounds match dimensions
        if len(request.bounds) != request.dimensions:
            raise ValueError(f"Number of bounds ({len(request.bounds)}) must match dimensions ({request.dimensions})")
        
        # Convert bounds to the expected format
        bounds = [(bound[0], bound[1]) for bound in request.bounds]
        
        # Create tiling based on type
        if request.tiling_type == "regular":
            if not request.shape_type or not request.parameter:
                raise ValueError("Regular tiling requires 'shape_type' and 'parameter'")
            
            # Create the base shape
            if request.shape_type == "cube":
                base_shape = HyperCube(request.dimensions, request.parameter)
            elif request.shape_type == "sphere":
                base_shape = HyperSphere(request.dimensions, request.parameter)
            elif request.shape_type == "simplex":
                base_shape = Simplex(request.dimensions, request.parameter)
            else:
                raise ValueError(f"Unsupported shape type: {request.shape_type}")
            
            tiling = RegularTiling(request.dimensions, base_shape)
            
        elif request.tiling_type == "hexagonal":
            if request.dimensions != 2:
                raise ValueError("Hexagonal tiling is only supported in 2D")
            if not request.side_length:
                raise ValueError("Hexagonal tiling requires 'side_length'")
            
            tiling = HexagonalTiling(request.side_length)
            
        elif request.tiling_type == "voronoi":
            if request.dimensions != 2:
                raise ValueError("Voronoi tiling is currently only supported in 2D")
            
            if request.seed_points:
                seed_points = request.seed_points
            elif request.num_random_seeds:
                # Generate random seed points within bounds
                import random
                seed_points = []
                for _ in range(request.num_random_seeds):
                    point = []
                    for bound in bounds:
                        point.append(random.uniform(bound[0], bound[1]))
                    seed_points.append(point)
            else:
                raise ValueError("Voronoi tiling requires either 'seed_points' or 'num_random_seeds'")
            
            tiling = VoronoiTiling(request.dimensions, seed_points)
            
        else:
            raise ValueError(f"Unsupported tiling type: {request.tiling_type}")
        
        # Generate the pattern
        tiles = tiling.generate_pattern(bounds, request.density)
        
        # Analyze the pattern
        analyzer = TilingAnalyzer(tiling)
        analysis = analyzer.analyze_pattern()
        
        return TilingResponse(
            tiling_type=request.tiling_type,
            dimensions=request.dimensions,
            tile_count=len(tiles),
            coverage_efficiency=tiling.get_coverage_efficiency(),
            pattern_properties=tiling.get_pattern_properties(),
            tiles=tiles,
            analysis=analysis
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "geometry_engine": "operational",
        "java_available": geometry_agent.java_bridge.java_available,
        "supported_dimensions": "1-100",
        "supported_shapes": ["sphere", "cube", "ellipsoid", "simplex", "pyramid"],
        "supported_tilings": ["regular", "hexagonal", "voronoi"],
        "features": [
            "n-dimensional spheres",
            "n-dimensional cubes", 
            "n-dimensional ellipsoids",
            "n-dimensional simplices",
            "n-dimensional pyramids",
            "regular tiling patterns",
            "hexagonal tessellations",
            "voronoi diagrams",
            "n-dimensional space filling",
            "tiling pattern analysis",
            "shape comparisons",
            "natural language queries",
            "original java integration",
            "interactive visualizations"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting N-Dimensional Geometry Engine Web API...")
    print("📊 Access the web interface at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/api/docs")
    print("🎮 Interactive Demo at: http://localhost:8000/demo")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)