"""
Handler for the /api/status endpoint.
"""

import time
from flask import jsonify


def handle_query(request, query):
    """
    Handle the request based on natural language query.
    Returns response if handled, None otherwise.
    """
    if not query:
        return None
        
    query_lower = query.lower()
    if 'status' in query_lower or '状态' in query_lower:
        return handle(request)
    
    return None


def handle(request):
    """
    Handle status endpoint request.
    
    Args:
        request: Flask request object
        
    Returns:
        JSON response
    """
    return jsonify({
        'status': 'ok',
        'timestamp': int(time.time()),
        'server': 'simple-web-server-auth',
        'path': request.path
    })
