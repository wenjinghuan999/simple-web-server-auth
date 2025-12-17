"""
Handler for the /api/hello endpoint.
"""

from flask import jsonify


def handle(request):
    """
    Handle hello endpoint request.
    
    Args:
        request: Flask request object
        
    Returns:
        JSON response
    """
    name = request.args.get('name', 'World')
    
    return jsonify({
        'message': f'Hello, {name}!',
        'path': request.path,
        'method': request.method
    })
