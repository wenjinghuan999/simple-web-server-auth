"""
Configuration file for the web server.
Contains access keys and server settings.
"""

# Access keys configuration
# Format: 'access_key': 'secret_key'
ACCESS_KEYS = {
    'test-key-1': 'test-secret-1',
    'test-key-2': 'test-secret-2',
    'admin-key': 'admin-secret-123',
}

# Server configuration
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# HTTPS configuration
USE_HTTPS = False
SSL_CERT = 'cert.pem'
SSL_KEY = 'key.pem'
