# Production Dockerfile for GeometryOracle N-Dimensional Geometry Engine
# Multi-stage build optimized for AWS deployment with MCP server support

# Build stage
FROM python:3.11-slim AS builder

# Set build environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
COPY requirements-dev.txt .

# Install Python dependencies (main and dev packages for MCP server)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir httpx mcp

# Production stage
FROM python:3.11-slim AS production

# Set production environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PORT=8000
ENV STAGE=prod

# Install runtime dependencies (use Debian default JDK for current release)
RUN apt-get update && apt-get install -y \
    default-jdk-headless \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Java tools (javac/java) are on PATH via alternatives; JAVA_HOME not required

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create app directory
WORKDIR /app

# Copy application code
COPY geometry_engine.py .
COPY geometry_oracle_mcp_server.py .

# Copy Java source files from their actual locations to both root and source directory
COPY src/java/original/Sphere.java .
COPY src/java/original/MultiSphere.java .
COPY src/java/ src/java/

# MCP server is geometry_oracle_mcp_server.py (already copied above)

# Compile Java files in root directory (for JavaBridge)
RUN javac Sphere.java MultiSphere.java

# Also compile Java files in source directory (backup)
RUN cd src/java/original && javac Sphere.java MultiSphere.java

# Change ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port for MCP server
EXPOSE 8000

# Health check for MCP server (check if process is running)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import geometry_oracle_mcp_server; print('MCP server available')" || exit 1

# Default: Run the MCP server
CMD ["python", "geometry_oracle_mcp_server.py"]