"""
Handler for the /api/hello endpoint.
"""

from flask import jsonify


def handle_query(request, query):
    """
    Handle the request based on natural language query.
    Returns response if handled, None otherwise.
    """
    if not query:
        return None
        
    query_lower = query.lower()
    if 'hello' not in query_lower and '你好' not in query_lower:
        return None

    name = query_lower.replace('hello', '').replace('你好', '').strip()
    if not name:
        name = None
    return handle(request, name)


def handle(request, name=None):
    """
    Handle hello endpoint request.
    
    Args:
        request: Flask request object
        name: Optional name override
        
    Returns:
        JSON response
    """
    if name is None:
        name = request.args.get('name', 'World')
    
    return jsonify({
        'message': f'Hello, {name}!',
        'path': request.path,
        'method': request.method
    })
