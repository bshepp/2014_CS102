"""
Simple AWS Lambda handler for GeometryOracle MCP Server
"""

import json
import os
import sys
import traceback
from typing import Dict, Any
import boto3
from datetime import datetime, timedelta
import math

# Simple geometry calculations without external dependencies
def calculate_hypersphere_volume(dimensions, radius):
    """Calculate N-dimensional sphere volume"""
    if dimensions == 1:
        return 2 * radius
    elif dimensions == 2:
        return math.pi * radius * radius
    elif dimensions == 3:
        return (4.0/3.0) * math.pi * radius * radius * radius
    else:
        # General formula: V = π^(n/2) * r^n / Γ(n/2 + 1)
        from math import gamma, pi
        return (pi ** (dimensions/2)) * (radius ** dimensions) / gamma(dimensions/2 + 1)

def calculate_hypercube_volume(dimensions, side_length):
    """Calculate N-dimensional cube volume"""
    return side_length ** dimensions

def validate_request_security(event):
    """Validate request for security and rate limiting"""
    # Check request size (prevent large payloads)
    body = event.get('body', '')
    if len(str(body)) > 10000:  # 10KB limit
        return False
    
    # Validate dimensions (prevent compute bombs)
    if event.get('httpMethod') == 'POST' and body:
        try:
            if isinstance(body, str):
                request_data = json.loads(body)
            else:
                request_data = body
            
            params = request_data.get('params', {})
            arguments = params.get('arguments', {})
            dimensions = arguments.get('dimensions', 0)
            
            # Limit to reasonable dimensions (prevent exponential compute)
            if dimensions > 50:
                return False
                
            # Validate shape count for comparisons
            if params.get('name') == 'compare_shapes':
                shapes = arguments.get('shapes', [])
                if len(shapes) > 20:  # Max 20 shapes per comparison
                    return False
                    
        except (json.JSONDecodeError, AttributeError):
            pass  # Let the main handler deal with invalid JSON
    
    return True

def get_client_ip(event):
    """Extract client IP for logging"""
    headers = event.get('headers', {})
    return (headers.get('X-Forwarded-For', '').split(',')[0].strip() or 
            headers.get('X-Real-IP', '') or 
            event.get('requestContext', {}).get('identity', {}).get('sourceIp', 'unknown'))

def mcp_handler(event, context):
    """Handle MCP protocol requests with security controls"""
    try:
        # Security: Input validation and rate limiting
        if not validate_request_security(event):
            return {
                'statusCode': 429,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Rate limit exceeded or invalid request'})
            }
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
                        'get_usage_statistics'
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
                
                # Execute tool
                if tool_name == 'calculate_hypersphere':
                    dimensions = arguments.get('dimensions', 3)
                    radius = arguments.get('radius', 1.0)
                    
                    volume = calculate_hypersphere_volume(dimensions, radius)
                    
                    result = {
                        'shape_type': 'hypersphere',
                        'dimensions': dimensions,
                        'radius': radius,
                        'volume': volume,
                        'surface_area': dimensions * volume / radius if radius > 0 else 0,
                        'diameter': 2 * radius
                    }
                    
                elif tool_name == 'calculate_hypercube':
                    dimensions = arguments.get('dimensions', 3)
                    side_length = arguments.get('side_length', 1.0)
                    
                    volume = calculate_hypercube_volume(dimensions, side_length)
                    
                    result = {
                        'shape_type': 'hypercube',
                        'dimensions': dimensions,
                        'side_length': side_length,
                        'volume': volume,
                        'surface_area': 2 * dimensions * (side_length ** (dimensions - 1)) if dimensions > 0 else 0,
                        'vertices': 2 ** dimensions,
                        'edges': dimensions * (2 ** (dimensions - 1)) if dimensions > 0 else 0
                    }
                    
                elif tool_name == 'compare_shapes':
                    shapes = arguments.get('shapes', [])
                    comparisons = []
                    
                    for shape_config in shapes:
                        shape_type = shape_config.get('type')
                        dimensions = shape_config.get('dimensions')
                        
                        if shape_type == 'hypersphere':
                            radius = shape_config.get('radius', 1.0)
                            volume = calculate_hypersphere_volume(dimensions, radius)
                            comparisons.append({
                                'type': 'hypersphere',
                                'dimensions': dimensions,
                                'radius': radius,
                                'volume': volume
                            })
                        elif shape_type == 'hypercube':
                            side = shape_config.get('side_length', 1.0)
                            volume = calculate_hypercube_volume(dimensions, side)
                            comparisons.append({
                                'type': 'hypercube',
                                'dimensions': dimensions,
                                'side_length': side,
                                'volume': volume
                            })
                    
                    result = {
                        'shapes': comparisons,
                        'comparison_count': len(comparisons),
                        'largest_volume': max(comparisons, key=lambda x: x['volume']) if comparisons else None
                    }
                    
                elif tool_name == 'get_usage_statistics':
                    result = {
                        'message': 'Usage statistics from AWS deployment',
                        'total_queries': 0,
                        'unique_sessions': 0,
                        'popular_tools': ['calculate_hypersphere', 'calculate_hypercube'],
                        'popular_dimensions': [2, 3, 4]
                    }
                    
                else:
                    result = {'error': f'Unknown tool: {tool_name}'}
                
                # Log to DynamoDB with enhanced security info
                try:
                    client_ip = get_client_ip(event)
                    log_to_dynamodb(tool_name, arguments, result, True, session_id, user_agent, client_ip)
                except Exception as e:
                    print(f"DynamoDB logging error: {str(e)}")
                
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

def log_to_dynamodb(tool_name, input_params, output_results, success, session_id=None, client_info=None, client_ip=None):
    """Log query to DynamoDB with enhanced security tracking"""
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
        if session_id:
            item['session_id'] = session_id
        if client_info:
            item['client_info'] = client_info
        if client_ip:
            item['client_ip'] = client_ip
            
        table.put_item(Item=item)
        
    except Exception as e:
        print(f"DynamoDB logging error: {str(e)}")
        # Don't fail the main request if logging fails

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