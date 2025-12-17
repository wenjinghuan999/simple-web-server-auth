#!/usr/bin/env python3
"""
Simple web server with authorization based on Flask.
Supports HTTPS and signature-based authentication.
"""

import hashlib
import time
from functools import wraps
from flask import Flask, request, jsonify
import config

app = Flask(__name__)


def calculate_signature(secret_key, access_key, timestamp, path):
    """
    Calculate signature using SHA1 hash.
    
    Args:
        secret_key: The secret key for the access key
        access_key: The access key identifier
        timestamp: Unix timestamp of the request
        path: The requested path
        
    Returns:
        Hexadecimal string of the SHA1 hash
    """
    # Create signature string: secret_key + access_key + timestamp + path
    signature_string = f"{secret_key}{access_key}{timestamp}{path}"
    return hashlib.sha1(signature_string.encode('utf-8')).hexdigest()


def verify_signature(access_key, timestamp, signature, path):
    """
    Verify the request signature.
    
    Args:
        access_key: The access key from the request
        timestamp: The timestamp from the request
        signature: The signature from the request
        path: The requested path
        
    Returns:
        Tuple of (is_valid: bool, error_message: str or None)
    """
    # Check if access key exists
    if access_key not in config.ACCESS_KEYS:
        return False, "Invalid access key"
    
    # Get the secret key
    secret_key = config.ACCESS_KEYS[access_key]
    
    # Verify timestamp is within acceptable range (5 minutes)
    try:
        request_time = int(timestamp)
        current_time = int(time.time())
        time_diff = abs(current_time - request_time)
        
        if time_diff > 300:  # 5 minutes
            return False, "Timestamp expired"
    except (ValueError, TypeError):
        return False, "Invalid timestamp"
    
    # Calculate expected signature
    expected_signature = calculate_signature(secret_key, access_key, timestamp, path)
    
    # Compare signatures
    if signature != expected_signature:
        return False, "Invalid signature"
    
    return True, None


def require_auth(f):
    """
    Decorator to require authentication for routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get authentication parameters from request
        access_key = request.args.get('accesskey') or request.headers.get('X-Access-Key')
        timestamp = request.args.get('timestamp') or request.headers.get('X-Timestamp')
        signature = request.args.get('signature') or request.headers.get('X-Signature')
        
        # Check if all required parameters are present
        if not all([access_key, timestamp, signature]):
            return jsonify({
                'error': 'Missing authentication parameters',
                'required': ['accesskey', 'timestamp', 'signature']
            }), 401
        
        # Verify the signature
        is_valid, error_message = verify_signature(
            access_key, timestamp, signature, request.path
        )
        
        if not is_valid:
            return jsonify({'error': error_message}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


@app.route('/')
def index():
    """Public endpoint - no authentication required."""
    return jsonify({
        'message': 'Simple Web Server with Authorization',
        'version': '1.0',
        'endpoints': {
            '/': 'Public endpoint',
            '/api/hello': 'Protected endpoint - requires authentication',
            '/api/status': 'Protected endpoint - requires authentication'
        }
    })


@app.route('/api/hello')
@require_auth
def hello():
    """Protected endpoint."""
    from handlers import hello_handler
    return hello_handler.handle(request)


@app.route('/api/status')
@require_auth
def status():
    """Protected endpoint."""
    from handlers import status_handler
    return status_handler.handle(request)


if __name__ == '__main__':
    # For development, run without HTTPS
    # For production, use HTTPS with proper certificates
    ssl_context = None
    
    if config.USE_HTTPS:
        ssl_context = (config.SSL_CERT, config.SSL_KEY)
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
        ssl_context=ssl_context
    )
