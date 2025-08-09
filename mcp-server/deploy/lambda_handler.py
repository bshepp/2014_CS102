"""
AWS Lambda handlers for GeometryOracle MCP Server
"""

import json
import os
import sys
import traceback
from typing import Dict, Any
import boto3
from datetime import datetime, timedelta

# Add the src directory to path - Lambda deployment structure
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.dirname(__file__))

from src.mcp_server import GeometryOracleMCP
from src.dashboard import dashboard_app  
from geometry_engine import HyperSphere, HyperCube
import asyncio

# Initialize MCP server
mcp_server = None

def get_mcp_server():
    global mcp_server
    if mcp_server is None:
        mcp_server = GeometryOracleMCP()
    return mcp_server

def mcp_handler(event, context):
    """Handle MCP protocol requests"""
    try:
        # Extract request data
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization, Mcp-Session-Id',
                    'Access-Control-Max-Age': '3600'
                },
                'body': ''
            }
        
        if event.get('httpMethod') == 'GET':
            # Health check for MCP server
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({
                    'status': 'healthy',
                    'service': 'GeometryOracle MCP Server',
                    'version': '1.0.0',
                    'timestamp': datetime.utcnow().isoformat(),
                    'tools_available': [
                        'calculate_hypersphere',
                        'calculate_hypercube', 
                        'compare_shapes',
                        'get_usage_statistics',
                        'batch_geometry_calculations',
                        'analyze_dimension_scaling'
                    ]
                })
            }
        
        # Handle POST requests (MCP calls)
        if event.get('httpMethod') == 'POST':
            body = event.get('body', '{}')
            if isinstance(body, str):
                request_data = json.loads(body)
            else:
                request_data = body
            
            # Extract session info
            headers = event.get('headers', {})
            session_id = headers.get('Mcp-Session-Id') or headers.get('mcp-session-id')
            user_agent = headers.get('User-Agent', 'Unknown')
            
            # Route to appropriate tool
            method = request_data.get('method', '')
            params = request_data.get('params', {})
            
            if method == 'tools/call':
                tool_name = params.get('name', '')
                arguments = params.get('arguments', {})
                
                # Add session info to arguments
                arguments['session_id'] = session_id
                arguments['client_info'] = user_agent
                
                # Execute tool
                if tool_name == 'calculate_hypersphere':
                    result = asyncio.run(execute_hypersphere(arguments))
                elif tool_name == 'calculate_hypercube':
                    result = asyncio.run(execute_hypercube(arguments))
                elif tool_name == 'compare_shapes':
                    result = asyncio.run(execute_compare_shapes(arguments))
                elif tool_name == 'get_usage_statistics':
                    result = asyncio.run(execute_usage_stats(arguments))
                else:
                    result = {'error': f'Unknown tool: {tool_name}'}
                
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                    },
                    'body': json.dumps({
                        'jsonrpc': '2.0',
                        'id': request_data.get('id'),
                        'result': result
                    })
                }
            
            elif method == 'tools/list':
                tools = [
                    {
                        'name': 'calculate_hypersphere',
                        'description': 'Calculate volume and surface area of N-dimensional hypersphere',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {
                                'dimensions': {'type': 'integer', 'minimum': 1},
                                'radius': {'type': 'number', 'minimum': 0}
                            },
                            'required': ['dimensions', 'radius']
                        }
                    },
                    {
                        'name': 'calculate_hypercube',
                        'description': 'Calculate volume and surface area of N-dimensional hypercube',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {
                                'dimensions': {'type': 'integer', 'minimum': 1},
                                'side_length': {'type': 'number', 'minimum': 0}
                            },
                            'required': ['dimensions', 'side_length']
                        }
                    },
                    {
                        'name': 'compare_shapes',
                        'description': 'Compare volumes and properties of multiple N-dimensional shapes',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {
                                'shapes': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'type': {'type': 'string'},
                                            'dimensions': {'type': 'integer'},
                                            'radius': {'type': 'number'},
                                            'side_length': {'type': 'number'}
                                        }
                                    }
                                }
                            },
                            'required': ['shapes']
                        }
                    },
                    {
                        'name': 'get_usage_statistics',
                        'description': 'Get usage statistics for the MCP server',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {
                                'days': {'type': 'integer', 'minimum': 1, 'maximum': 365}
                            }
                        }
                    }
                ]
                
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                    },
                    'body': json.dumps({
                        'jsonrpc': '2.0',
                        'id': request_data.get('id'),
                        'result': {'tools': tools}
                    })
                }
        
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Invalid request method'})
        }
        
    except Exception as e:
        print(f"MCP Handler Error: {str(e)}")
        print(traceback.format_exc())
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'jsonrpc': '2.0',
                'id': None,
                'error': {
                    'code': -32603,
                    'message': 'Internal error',
                    'data': str(e)
                }
            })
        }

async def execute_hypersphere(args):
    """Execute hypersphere calculation"""
    try:
        dimensions = args['dimensions']
        radius = args['radius']
        
        sphere = HyperSphere(dimensions, radius)
        
        result = {
            'shape_type': 'hypersphere',
            'dimensions': dimensions,
            'radius': radius,
            'volume': sphere.get_volume(),
            'surface_area': sphere.get_surface_area(),
            'diameter': sphere.get_diameter(),
            'volume_formula': sphere.get_volume_formula(),
            'surface_area_formula': sphere.get_surface_area_formula()
        }
        
        # Log to DynamoDB
        await log_to_dynamodb('calculate_hypersphere', args, result, True)
        
        return result
        
    except Exception as e:
        await log_to_dynamodb('calculate_hypersphere', args, None, False, str(e))
        raise

async def execute_hypercube(args):
    """Execute hypercube calculation"""
    try:
        dimensions = args['dimensions']
        side_length = args['side_length']
        
        cube = HyperCube(dimensions, side_length)
        
        result = {
            'shape_type': 'hypercube',
            'dimensions': dimensions,
            'side_length': side_length,
            'volume': cube.get_volume(),
            'surface_area': cube.get_surface_area(),
            'vertices': 2 ** dimensions,
            'edges': dimensions * (2 ** (dimensions - 1)) if dimensions > 0 else 0
        }
        
        # Log to DynamoDB
        await log_to_dynamodb('calculate_hypercube', args, result, True)
        
        return result
        
    except Exception as e:
        await log_to_dynamodb('calculate_hypercube', args, None, False, str(e))
        raise

async def execute_compare_shapes(args):
    """Execute shape comparison"""
    try:
        shapes = args['shapes']
        comparisons = []
        
        for shape_config in shapes:
            shape_type = shape_config.get('type')
            dimensions = shape_config.get('dimensions')
            
            if shape_type == 'hypersphere':
                radius = shape_config.get('radius', 1.0)
                shape = HyperSphere(dimensions, radius)
                comparisons.append({
                    'type': 'hypersphere',
                    'dimensions': dimensions,
                    'radius': radius,
                    'volume': shape.get_volume(),
                    'surface_area': shape.get_surface_area()
                })
            elif shape_type == 'hypercube':
                side = shape_config.get('side_length', 1.0)
                shape = HyperCube(dimensions, side)
                comparisons.append({
                    'type': 'hypercube',
                    'dimensions': dimensions,
                    'side_length': side,
                    'volume': shape.get_volume(),
                    'surface_area': shape.get_surface_area()
                })
        
        result = {
            'shapes': comparisons,
            'comparison_count': len(comparisons),
            'largest_volume': max(comparisons, key=lambda x: x['volume']) if comparisons else None
        }
        
        # Log to DynamoDB
        await log_to_dynamodb('compare_shapes', args, result, True)
        
        return result
        
    except Exception as e:
        await log_to_dynamodb('compare_shapes', args, None, False, str(e))
        raise

async def execute_usage_stats(args):
    """Execute usage statistics"""
    try:
        # For now, return mock stats - would integrate with DynamoDB queries
        result = {
            'message': 'Usage statistics from AWS deployment',
            'total_queries': 0,
            'unique_sessions': 0,
            'popular_tools': [],
            'popular_dimensions': []
        }
        
        # Log to DynamoDB
        await log_to_dynamodb('get_usage_statistics', args, result, True)
        
        return result
        
    except Exception as e:
        await log_to_dynamodb('get_usage_statistics', args, None, False, str(e))
        raise

async def log_to_dynamodb(tool_name, input_params, output_results, success, error_message=None):
    """Log query to DynamoDB"""
    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table_name = f"geometry-oracle-mcp-{os.environ.get('STAGE', 'dev')}-queries"
        table = dynamodb.Table(table_name)
        
        item = {
            'id': f"{tool_name}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{hash(str(input_params)) % 10000}",
            'timestamp': datetime.utcnow().isoformat(),
            'tool_name': tool_name,
            'input_parameters': json.dumps(input_params),
            'success': success,
            'ttl': int((datetime.utcnow() + timedelta(days=90)).timestamp())  # Auto-delete after 90 days
        }
        
        if output_results:
            item['output_results'] = json.dumps(output_results)
        if error_message:
            item['error_message'] = error_message
        if input_params.get('session_id'):
            item['session_id'] = input_params['session_id']
        if input_params.get('client_info'):
            item['client_info'] = input_params['client_info']
            
        table.put_item(Item=item)
        
    except Exception as e:
        print(f"DynamoDB logging error: {str(e)}")
        # Don't fail the main request if logging fails


def dashboard_handler(event, context):
    """Handle dashboard requests"""
    try:
        # Simple dashboard response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html',
                'Access-Control-Allow-Origin': '*',
            },
            'body': '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>GeometryOracle MCP Server</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
                    .header { text-align: center; margin-bottom: 40px; }
                    .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
                    .code { background: #eee; padding: 10px; font-family: monospace; margin: 10px 0; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🌌 GeometryOracle MCP Server</h1>
                    <p>AWS Lambda Deployment - Ready for AI Systems</p>
                </div>
                
                <div class="endpoint">
                    <h3>MCP Endpoint</h3>
                    <div class="code">POST /mcp</div>
                    <p>Send JSON-RPC 2.0 requests for geometry calculations</p>
                </div>
                
                <div class="endpoint">
                    <h3>Health Check</h3>
                    <div class="code">GET /health</div>
                    <p>Server health and available tools</p>
                </div>
                
                <div class="endpoint">
                    <h3>Available Tools</h3>
                    <ul>
                        <li><code>calculate_hypersphere</code> - N-dimensional spheres</li>
                        <li><code>calculate_hypercube</code> - N-dimensional cubes</li>
                        <li><code>compare_shapes</code> - Multi-shape comparisons</li>
                        <li><code>get_usage_statistics</code> - Server statistics</li>
                    </ul>
                </div>
                
                <div class="endpoint">
                    <h3>Example Usage</h3>
                    <div class="code">
{
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
}
                    </div>
                </div>
            </body>
            </html>
            '''
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

def health_handler(event, context):
    """Health check endpoint"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({
            'status': 'healthy',
            'service': 'GeometryOracle MCP Server',
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat(),
            'aws_region': os.environ.get('AWS_REGION'),
            'stage': os.environ.get('STAGE', 'dev')
        })
    }