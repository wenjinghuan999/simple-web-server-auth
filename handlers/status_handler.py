"""
Handler for the /api/status endpoint.
"""

import time
from flask import jsonify


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
