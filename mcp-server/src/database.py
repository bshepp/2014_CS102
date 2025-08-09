"""
Database layer for GeometryOracle MCP Server
Handles all data collection and logging functionality
Supports both SQLite (local) and DynamoDB (AWS) backends
"""

import sqlite3
import json
import asyncio
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager
import aiosqlite
import psutil
import time
import boto3
from botocore.exceptions import ClientError


class DatabaseManager:
    def __init__(
        self, db_path: str = "mcp_geometry_oracle.db", use_dynamodb: bool = None
    ):
        self.db_path = db_path

        # Auto-detect: use DynamoDB if AWS credentials available, otherwise SQLite
        if use_dynamodb is None:
            try:
                # Test if we can access AWS
                boto3.client("sts").get_caller_identity()
                self.use_dynamodb = True
                self.dynamodb_table = (
                    f"geometry-oracle-mcp-{os.environ.get('STAGE', 'prod')}-queries"
                )
                print(f"✅ Using DynamoDB: {self.dynamodb_table}")
            except Exception:
                self.use_dynamodb = False
                print("ℹ️ Using SQLite (AWS not available)")
        else:
            self.use_dynamodb = use_dynamodb
            if use_dynamodb:
                self.dynamodb_table = (
                    f"geometry-oracle-mcp-{os.environ.get('STAGE', 'prod')}-queries"
                )

        if not self.use_dynamodb:
            self._init_db()

    def _init_db(self):
        """Initialize database with schema"""
        with sqlite3.connect(self.db_path) as conn:
            # Read and execute schema
            with open("schemas/database.sql", "r") as f:
                schema = f.read()
            conn.executescript(schema)

    @asynccontextmanager
    async def get_connection(self):
        """Get async database connection"""
        conn = await aiosqlite.connect(self.db_path)
        try:
            yield conn
        finally:
            await conn.close()

    async def log_query(
        self,
        tool_name: str,
        input_parameters: Dict[str, Any],
        output_results: Optional[Dict[str, Any]] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        execution_time_ms: Optional[int] = None,
        session_id: Optional[str] = None,
        client_info: Optional[str] = None,
        ip_address: Optional[str] = None,
        dimensions: Optional[int] = None,
        shape_type: Optional[str] = None,
        visualization_requested: bool = False,
        memory_usage_mb: Optional[float] = None,
        cpu_time_ms: Optional[int] = None,
    ) -> int:
        """Log a query with comprehensive metadata"""

        async with self.get_connection() as conn:
            query = """
                INSERT INTO query_logs (
                    tool_name, input_parameters, output_results, success, error_message,
                    execution_time_ms, session_id, client_info, ip_address,
                    dimensions, shape_type, visualization_requested,
                    memory_usage_mb, cpu_time_ms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor = await conn.execute(
                query,
                (
                    tool_name,
                    json.dumps(input_parameters) if input_parameters else None,
                    json.dumps(output_results) if output_results else None,
                    success,
                    error_message,
                    execution_time_ms,
                    session_id,
                    client_info,
                    ip_address,
                    dimensions,
                    shape_type,
                    visualization_requested,
                    memory_usage_mb,
                    cpu_time_ms,
                ),
            )

            await conn.commit()
            return cursor.lastrowid

    async def log_error(
        self,
        tool_name: str,
        error_type: str,
        error_message: str,
        input_parameters: Optional[Dict[str, Any]] = None,
        stack_trace: Optional[str] = None,
    ):
        """Log an error with details"""

        async with self.get_connection() as conn:
            query = """
                INSERT INTO error_logs (tool_name, error_type, error_message, input_parameters, stack_trace)
                VALUES (?, ?, ?, ?, ?)
            """

            await conn.execute(
                query,
                (
                    tool_name,
                    error_type,
                    error_message,
                    json.dumps(input_parameters) if input_parameters else None,
                    stack_trace,
                ),
            )

            await conn.commit()

    async def log_visualization_request(
        self,
        query_log_id: int,
        visualization_type: str,
        parameters: Dict[str, Any],
        success: bool,
        generation_time_ms: int,
    ):
        """Log a visualization request"""

        async with self.get_connection() as conn:
            query = """
                INSERT INTO visualization_requests 
                (query_log_id, visualization_type, parameters, success, generation_time_ms)
                VALUES (?, ?, ?, ?, ?)
            """

            await conn.execute(
                query,
                (
                    query_log_id,
                    visualization_type,
                    json.dumps(parameters),
                    success,
                    generation_time_ms,
                ),
            )

            await conn.commit()

    async def update_tool_stats(
        self, tool_name: str, execution_time_ms: int, success: bool, session_id: str
    ):
        """Update aggregated tool usage statistics"""
        today = datetime.now().date()

        async with self.get_connection() as conn:
            # Check if record exists
            query = "SELECT * FROM tool_usage_stats WHERE tool_name = ? AND date = ?"
            cursor = await conn.execute(query, (tool_name, today))
            existing = await cursor.fetchone()

            if existing:
                # Update existing record
                update_query = """
                    UPDATE tool_usage_stats SET 
                        total_calls = total_calls + 1,
                        successful_calls = successful_calls + ?,
                        failed_calls = failed_calls + ?,
                        avg_execution_time_ms = 
                            ((avg_execution_time_ms * (total_calls - 1)) + ?) / total_calls
                    WHERE tool_name = ? AND date = ?
                """
                await conn.execute(
                    update_query,
                    (
                        1 if success else 0,
                        0 if success else 1,
                        execution_time_ms,
                        tool_name,
                        today,
                    ),
                )
            else:
                # Insert new record
                insert_query = """
                    INSERT INTO tool_usage_stats 
                    (tool_name, date, total_calls, successful_calls, failed_calls, avg_execution_time_ms, unique_sessions)
                    VALUES (?, ?, 1, ?, ?, ?, 1)
                """
                await conn.execute(
                    insert_query,
                    (
                        tool_name,
                        today,
                        1 if success else 0,
                        0 if success else 1,
                        execution_time_ms,
                    ),
                )

            await conn.commit()

    async def update_dimension_stats(
        self, dimensions: int, shape_type: str, execution_time_ms: int
    ):
        """Update dimension popularity statistics"""
        today = datetime.now().date()

        async with self.get_connection() as conn:
            query = """
                INSERT INTO dimension_stats (dimensions, shape_type, date, call_count, avg_execution_time_ms)
                VALUES (?, ?, ?, 1, ?)
                ON CONFLICT(dimensions, shape_type, date) DO UPDATE SET
                    call_count = call_count + 1,
                    avg_execution_time_ms = 
                        ((avg_execution_time_ms * (call_count - 1)) + ?) / call_count
            """

            await conn.execute(
                query,
                (dimensions, shape_type, today, execution_time_ms, execution_time_ms),
            )
            await conn.commit()

    async def get_usage_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get usage statistics for analysis"""

        if self.use_dynamodb:
            return await self._get_usage_stats_dynamodb(days)
        else:
            return await self._get_usage_stats_sqlite(days)

    async def _get_usage_stats_dynamodb(self, days: int = 30) -> Dict[str, Any]:
        """Get usage statistics from DynamoDB"""
        try:
            dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
            table = dynamodb.Table(self.dynamodb_table)

            # Get all items from the last N days
            from datetime import datetime, timedelta

            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

            response = table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr("timestamp").gte(
                    cutoff_date
                )
            )

            items = response.get("Items", [])

            # Process data similar to SQLite version
            tool_usage = {}
            dimension_popularity = {}

            for item in items:
                tool_name = item.get("tool_name")
                dimensions = item.get("dimensions")

                # Count tool usage
                if tool_name:
                    tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1

                # Count dimension popularity
                if dimensions:
                    dim_key = str(dimensions)
                    dimension_popularity[dim_key] = (
                        dimension_popularity.get(dim_key, 0) + 1
                    )

            return {
                "tool_usage": [
                    {"tool_name": k, "calls": v} for k, v in tool_usage.items()
                ],
                "dimension_popularity": [
                    {"dimensions": int(k), "calls": v}
                    for k, v in dimension_popularity.items()
                ],
                "error_rates": [],
                "total_queries": len(items),
                "data_source": "dynamodb",
            }

        except Exception as e:
            print(f"Error reading from DynamoDB: {e}")
            return {
                "tool_usage": [],
                "dimension_popularity": [],
                "error_rates": [],
                "total_queries": 0,
                "data_source": "dynamodb_error",
            }

    async def _get_usage_stats_sqlite(self, days: int = 30) -> Dict[str, Any]:
        """Get usage statistics from SQLite"""
        async with self.get_connection() as conn:
            # Tool usage over time
            query = """
                SELECT tool_name, COUNT(*) as calls, AVG(execution_time_ms) as avg_time
                FROM query_logs 
                WHERE timestamp >= datetime('now', '-{} days')
                GROUP BY tool_name
                ORDER BY calls DESC
            """.format(
                days
            )

            cursor = await conn.execute(query)
            tool_stats = await cursor.fetchall()

            # Dimension popularity
            dim_query = """
                SELECT dimensions, COUNT(*) as calls
                FROM query_logs 
                WHERE timestamp >= datetime('now', '-{} days') AND dimensions IS NOT NULL
                GROUP BY dimensions
                ORDER BY calls DESC
            """.format(
                days
            )

            cursor = await conn.execute(dim_query)
            dim_stats = await cursor.fetchall()

            # Error rates
            error_query = """
                SELECT tool_name, 
                       COUNT(*) as total_calls,
                       SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as errors
                FROM query_logs 
                WHERE timestamp >= datetime('now', '-{} days')
                GROUP BY tool_name
            """.format(
                days
            )

            cursor = await conn.execute(error_query)
            error_stats = await cursor.fetchall()

            return {
                "tool_usage": [
                    dict(zip([col[0] for col in cursor.description], row))
                    for row in tool_stats
                ],
                "dimension_popularity": [
                    dict(zip([col[0] for col in cursor.description], row))
                    for row in dim_stats
                ],
                "error_rates": [
                    dict(zip([col[0] for col in cursor.description], row))
                    for row in error_stats
                ],
            }


class PerformanceMonitor:
    """Monitor performance metrics for logging"""

    def __init__(self):
        self.start_time = None
        self.start_memory = None
        self.process = psutil.Process()

    def start_monitoring(self):
        """Start performance monitoring"""
        self.start_time = time.time()
        self.start_memory = self.process.memory_info().rss / 1024 / 1024  # MB

    def get_metrics(self) -> Dict[str, float]:
        """Get current performance metrics"""
        if self.start_time is None:
            return {}

        execution_time_ms = int((time.time() - self.start_time) * 1000)
        current_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        memory_usage_mb = current_memory - (self.start_memory or 0)

        return {
            "execution_time_ms": execution_time_ms,
            "memory_usage_mb": memory_usage_mb,
            "cpu_time_ms": int(self.process.cpu_times().user * 1000),
        }
