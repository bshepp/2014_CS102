-- GeometryOracle MCP Server Database Schema
-- Comprehensive logging for data collection and analysis

-- Main query log table
CREATE TABLE IF NOT EXISTS query_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Timing data
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    execution_time_ms INTEGER,
    
    -- Request metadata
    tool_name VARCHAR(100) NOT NULL,
    session_id VARCHAR(100),
    client_info TEXT, -- User-Agent, MCP client type if available
    ip_address VARCHAR(45), -- IPv4/IPv6 compatible
    
    -- Request data
    input_parameters TEXT, -- JSON blob of all parameters
    
    -- Response data  
    output_results TEXT, -- JSON blob of results
    success BOOLEAN NOT NULL,
    error_message TEXT,
    
    -- Geometry-specific metadata
    dimensions INTEGER,
    shape_type VARCHAR(50),
    visualization_requested BOOLEAN DEFAULT FALSE,
    
    -- Performance metrics
    memory_usage_mb REAL,
    cpu_time_ms INTEGER
);

-- Index for fast queries
CREATE INDEX IF NOT EXISTS idx_query_logs_timestamp ON query_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_query_logs_tool ON query_logs(tool_name);
CREATE INDEX IF NOT EXISTS idx_query_logs_dimensions ON query_logs(dimensions);
CREATE INDEX IF NOT EXISTS idx_query_logs_session ON query_logs(session_id);

-- Tool usage statistics (aggregated data)
CREATE TABLE IF NOT EXISTS tool_usage_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    total_calls INTEGER DEFAULT 0,
    successful_calls INTEGER DEFAULT 0,
    failed_calls INTEGER DEFAULT 0,
    avg_execution_time_ms REAL,
    unique_sessions INTEGER DEFAULT 0,
    UNIQUE(tool_name, date)
);

-- Dimension popularity tracking
CREATE TABLE IF NOT EXISTS dimension_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dimensions INTEGER NOT NULL,
    shape_type VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    call_count INTEGER DEFAULT 0,
    avg_execution_time_ms REAL,
    UNIQUE(dimensions, shape_type, date)
);

-- Error tracking
CREATE TABLE IF NOT EXISTS error_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    tool_name VARCHAR(100),
    error_type VARCHAR(100),
    error_message TEXT,
    input_parameters TEXT,
    stack_trace TEXT
);

-- Visualization requests tracking
CREATE TABLE IF NOT EXISTS visualization_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_log_id INTEGER,
    visualization_type VARCHAR(100),
    parameters TEXT,
    success BOOLEAN,
    generation_time_ms INTEGER,
    FOREIGN KEY(query_log_id) REFERENCES query_logs(id)
);