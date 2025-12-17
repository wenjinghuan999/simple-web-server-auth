#!/usr/bin/env python3
"""
Example client for the simple web server with authorization.
Demonstrates how to calculate signatures and make authenticated requests.
"""

import hashlib
import time
import sys


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
    signature_string = f"{secret_key}{access_key}{timestamp}{path}"
    return hashlib.sha1(signature_string.encode('utf-8')).hexdigest()


def make_request(server_url, path, access_key, secret_key, extra_params=None):
    """
    Make an authenticated request to the server.
    
    Args:
        server_url: Base URL of the server (e.g., http://localhost:5000)
        path: Request path (e.g., /api/hello)
        access_key: Your access key
        secret_key: Your secret key
        extra_params: Dictionary of additional query parameters
        
    Returns:
        Response object
    """
    try:
        import requests
    except ImportError:
        print("Error: requests library not installed.")
        print("Install it with: pip install requests")
        sys.exit(1)
    
    # Generate authentication parameters
    timestamp = str(int(time.time()))
    signature = calculate_signature(secret_key, access_key, timestamp, path)
    
    # Build parameters
    params = {
        'accesskey': access_key,
        'timestamp': timestamp,
        'signature': signature
    }
    
    if extra_params:
        params.update(extra_params)
    
    # Make request
    url = f"{server_url}{path}"
    print(f"\nRequest URL: {url}")
    print(f"Parameters: {params}")
    
    response = requests.get(url, params=params)
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    return response


def main():
    """
    Main function demonstrating client usage.
    """
    # Configuration
    server_url = "http://localhost:5000"
    access_key = "test-key-1"
    secret_key = "test-secret-1"
    
    print("=" * 60)
    print("Simple Web Server Auth - Client Example")
    print("=" * 60)
    
    # Test 1: Index endpoint (now protected)
    print("\n[Test 1] Accessing index endpoint with query dispatching")
    print("-" * 60)
    
    # 1a. Query for 'hello'
    print("\n--- Query: q=hello ---")
    try:
        make_request(server_url, "/", access_key, secret_key, {'q': 'hello'})
    except Exception as e:
        print(f"Error: {e}")

    # 1b. Query for 'status'
    print("\n--- Query: q=status ---")
    try:
        make_request(server_url, "/", access_key, secret_key, {'q': 'status'})
    except Exception as e:
        print(f"Error: {e}")

    # 1c. Query for '你好' (Chinese)
    print("\n--- Query: q=你好 ---")
    try:
        make_request(server_url, "/", access_key, secret_key, {'q': '你好'})
    except Exception as e:
        print(f"Error: {e}")

    # 1d. Query with parameter 'hello Alice'
    print("\n--- Query: q=hello Alice ---")
    try:
        make_request(server_url, "/", access_key, secret_key, {'q': 'hello Alice'})
    except Exception as e:
        print(f"Error: {e}")

    # 1e. Unknown query
    print("\n--- Query: q=unknown ---")
    try:
        make_request(server_url, "/", access_key, secret_key, {'q': 'unknown'})
    except Exception as e:
        print(f"Error: {e}")

    # 1f. No query
    print("\n--- No Query ---")
    try:
        make_request(server_url, "/", access_key, secret_key)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Protected endpoint with valid auth (Direct access)
    print("\n[Test 2] Accessing protected endpoint with valid authentication")
    print("-" * 60)
    try:
        make_request(server_url, "/api/hello", access_key, secret_key, {'name': 'User'})
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Status endpoint
    print("\n[Test 3] Accessing status endpoint")
    print("-" * 60)
    try:
        make_request(server_url, "/api/status", access_key, secret_key)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Invalid signature (for demonstration)
    print("\n[Test 4] Attempting access with invalid signature")
    print("-" * 60)
    try:
        import requests
        timestamp = str(int(time.time()))
        params = {
            'accesskey': access_key,
            'timestamp': timestamp,
            'signature': 'invalid_signature'
        }
        response = requests.get(f"{server_url}/api/hello", params=params)
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
    except ImportError:
        print("Skipping - requests library not installed")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
