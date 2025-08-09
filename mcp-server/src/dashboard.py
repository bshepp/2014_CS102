"""
GeometryOracle MCP Server Dashboard
Web interface for viewing collected data and usage statistics
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from database import DatabaseManager
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.utils

dashboard_app = FastAPI(title="GeometryOracle MCP Dashboard")

# Setup templates and static files
templates = Jinja2Templates(directory="templates")

db = DatabaseManager()


@dashboard_app.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """Main dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@dashboard_app.get("/api/stats/overview")
async def get_overview_stats():
    """Get overview statistics for dashboard"""

    stats = await db.get_usage_stats(30)

    # Calculate additional overview metrics
    async with db.get_connection() as conn:
        # Total queries
        total_query = "SELECT COUNT(*) as total FROM query_logs"
        cursor = await conn.execute(total_query)
        total_queries = (await cursor.fetchone())[0]

        # Unique sessions
        session_query = "SELECT COUNT(DISTINCT session_id) as unique_sessions FROM query_logs WHERE session_id IS NOT NULL"
        cursor = await conn.execute(session_query)
        unique_sessions = (await cursor.fetchone())[0]

        # Average execution time
        avg_time_query = "SELECT AVG(execution_time_ms) as avg_time FROM query_logs WHERE execution_time_ms IS NOT NULL"
        cursor = await conn.execute(avg_time_query)
        avg_execution_time = (await cursor.fetchone())[0] or 0

        # Most popular dimension
        pop_dim_query = """
            SELECT dimensions, COUNT(*) as count 
            FROM query_logs 
            WHERE dimensions IS NOT NULL 
            GROUP BY dimensions 
            ORDER BY count DESC 
            LIMIT 1
        """
        cursor = await conn.execute(pop_dim_query)
        pop_dim_result = await cursor.fetchone()
        most_popular_dimension = pop_dim_result[0] if pop_dim_result else None

        # Error rate
        error_rate_query = """
            SELECT 
                COUNT(CASE WHEN success = 0 THEN 1 END) * 100.0 / COUNT(*) as error_rate
            FROM query_logs
        """
        cursor = await conn.execute(error_rate_query)
        error_rate = (await cursor.fetchone())[0] or 0

    return {
        "overview": {
            "total_queries": total_queries,
            "unique_sessions": unique_sessions,
            "avg_execution_time_ms": round(avg_execution_time, 2),
            "most_popular_dimension": most_popular_dimension,
            "error_rate_percent": round(error_rate, 2),
        },
        "tool_usage": stats["tool_usage"],
        "dimension_popularity": stats["dimension_popularity"],
        "error_rates": stats["error_rates"],
    }


@dashboard_app.get("/api/stats/timeline")
async def get_timeline_stats(days: int = 7):
    """Get usage timeline for charts"""

    async with db.get_connection() as conn:
        query = """
            SELECT 
                DATE(timestamp) as date,
                COUNT(*) as queries,
                COUNT(DISTINCT session_id) as unique_sessions,
                AVG(execution_time_ms) as avg_execution_time
            FROM query_logs 
            WHERE timestamp >= datetime('now', '-{} days')
            GROUP BY DATE(timestamp)
            ORDER BY date
        """.format(
            days
        )

        cursor = await conn.execute(query)
        timeline_data = await cursor.fetchall()

        # Convert to list of dicts
        timeline = []
        for row in timeline_data:
            timeline.append(
                {
                    "date": row[0],
                    "queries": row[1],
                    "unique_sessions": row[2],
                    "avg_execution_time": round(row[3] or 0, 2),
                }
            )

    return {"timeline": timeline}


@dashboard_app.get("/api/stats/dimensions")
async def get_dimension_analysis():
    """Get detailed dimension usage analysis"""

    async with db.get_connection() as conn:
        # Dimension distribution by shape type
        dim_shape_query = """
            SELECT dimensions, shape_type, COUNT(*) as count
            FROM query_logs 
            WHERE dimensions IS NOT NULL AND shape_type IS NOT NULL
            GROUP BY dimensions, shape_type
            ORDER BY dimensions, count DESC
        """
        cursor = await conn.execute(dim_shape_query)
        dim_shape_data = await cursor.fetchall()

        # Dimension performance
        dim_perf_query = """
            SELECT dimensions, 
                   AVG(execution_time_ms) as avg_time,
                   COUNT(*) as count
            FROM query_logs 
            WHERE dimensions IS NOT NULL AND execution_time_ms IS NOT NULL
            GROUP BY dimensions
            ORDER BY dimensions
        """
        cursor = await conn.execute(dim_perf_query)
        dim_perf_data = await cursor.fetchall()

    return {
        "dimension_shape_distribution": [
            {"dimensions": row[0], "shape_type": row[1], "count": row[2]}
            for row in dim_shape_data
        ],
        "dimension_performance": [
            {
                "dimensions": row[0],
                "avg_execution_time": round(row[1], 2),
                "count": row[2],
            }
            for row in dim_perf_data
        ],
    }


@dashboard_app.get("/api/data/export")
async def export_research_data(format: str = "json"):
    """Export collected data for research purposes"""

    async with db.get_connection() as conn:
        # Get all query logs (anonymized)
        query = """
            SELECT 
                timestamp,
                tool_name,
                dimensions,
                shape_type,
                success,
                execution_time_ms,
                visualization_requested
            FROM query_logs
            ORDER BY timestamp DESC
        """
        cursor = await conn.execute(query)
        data = await cursor.fetchall()

        # Convert to research-friendly format
        research_data = []
        for row in data:
            research_data.append(
                {
                    "timestamp": row[0],
                    "tool": row[1],
                    "dimensions": row[2],
                    "shape_type": row[3],
                    "success": bool(row[4]),
                    "execution_time_ms": row[5],
                    "visualization_requested": (
                        bool(row[6]) if row[6] is not None else False
                    ),
                }
            )

    return {
        "metadata": {
            "export_date": datetime.now().isoformat(),
            "total_records": len(research_data),
            "description": "GeometryOracle MCP Server usage data for research purposes",
            "fields": [
                "timestamp: Query execution time",
                "tool: MCP tool name called",
                "dimensions: N-dimensional parameter used",
                "shape_type: Geometry type (hypersphere, hypercube, etc.)",
                "success: Whether query succeeded",
                "execution_time_ms: Processing time in milliseconds",
                "visualization_requested: Whether visualization was requested",
            ],
        },
        "data": research_data,
    }


@dashboard_app.get("/api/charts/usage")
async def get_usage_charts():
    """Generate usage charts for dashboard"""

    stats = await get_overview_stats()

    # Tool usage pie chart
    tool_data = stats["tool_usage"]
    if tool_data:
        tool_fig = go.Figure(
            data=[
                go.Pie(
                    labels=[item["tool_name"] for item in tool_data],
                    values=[item["calls"] for item in tool_data],
                    title="Tool Usage Distribution",
                )
            ]
        )
        tool_chart = json.dumps(tool_fig, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        tool_chart = json.dumps({"data": [], "layout": {"title": "No data available"}})

    # Dimension popularity bar chart
    dim_data = stats["dimension_popularity"]
    if dim_data:
        dim_fig = go.Figure(
            data=[
                go.Bar(
                    x=[f"{item['dimensions']}D" for item in dim_data],
                    y=[item["calls"] for item in dim_data],
                    title="Dimension Popularity",
                )
            ]
        )
        dim_chart = json.dumps(dim_fig, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        dim_chart = json.dumps({"data": [], "layout": {"title": "No data available"}})

    return {"tool_usage_chart": tool_chart, "dimension_chart": dim_chart}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(dashboard_app, host="0.0.0.0", port=8002)
