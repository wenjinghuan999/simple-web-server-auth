# simple-web-server-auth

A simple web server based on Flask with signature-based authorization.

## Features

- **Flask-based web server**: Lightweight and easy to extend
- **HTTPS support**: Can be configured to run with SSL/TLS
- **Basic routing**: Modular route handling with separate handler files
- **Signature-based authentication**: Secure request signing using SHA1 hash
- **Configurable access keys**: Static access-key/secret-key pairs
- **Timestamp validation**: Prevents replay attacks (5-minute window)

## How It Works

The authentication system requires three parameters with each request:

1. **accesskey**: Your access key identifier
2. **timestamp**: Unix timestamp (current time)
3. **signature**: SHA1 hash calculated as: `sha1(secret_key + access_key + timestamp + path)`

The signature calculation ensures that:
- Only clients with valid secret keys can generate valid signatures
- Each request is timestamped to prevent replay attacks
- The signature includes the request path to prevent request manipulation

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.py` to configure:

- **ACCESS_KEYS**: Add your access-key/secret-key pairs
- **HOST/PORT**: Server binding address and port
- **USE_HTTPS**: Enable/disable HTTPS
- **SSL_CERT/SSL_KEY**: Paths to SSL certificate files

## Running the Server

```bash
python server.py
```

For HTTPS, first generate certificates:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

Then set `USE_HTTPS = True` in `config.py`.

## API Endpoints

### Public Endpoints

- `GET /` - Server information (no authentication required)

### Protected Endpoints

- `GET /api/hello` - Hello world endpoint (requires authentication)
- `GET /api/status` - Server status endpoint (requires authentication)

## Usage Examples

### Python Client Example

```python
import hashlib
import time
import requests

def calculate_signature(secret_key, access_key, timestamp, path):
    signature_string = f"{secret_key}{access_key}{timestamp}{path}"
    return hashlib.sha1(signature_string.encode('utf-8')).hexdigest()

# Configuration
server_url = "http://localhost:5000"
access_key = "test-key-1"
secret_key = "test-secret-1"
path = "/api/hello"

# Generate authentication parameters
timestamp = str(int(time.time()))
signature = calculate_signature(secret_key, access_key, timestamp, path)

# Make request
response = requests.get(
    f"{server_url}{path}",
    params={
        'accesskey': access_key,
        'timestamp': timestamp,
        'signature': signature,
        'name': 'User'
    }
)

print(response.json())
```

### JavaScript Client Example

```javascript
const crypto = require('crypto');

function calculateSignature(secretKey, accessKey, timestamp, path) {
    const signatureString = `${secretKey}${accessKey}${timestamp}${path}`;
    return crypto.createHash('sha1').update(signatureString).digest('hex');
}

// Configuration
const serverUrl = "http://localhost:5000";
const accessKey = "test-key-1";
const secretKey = "test-secret-1";
const path = "/api/hello";

// Generate authentication parameters
const timestamp = Math.floor(Date.now() / 1000).toString();
const signature = calculateSignature(secretKey, accessKey, timestamp, path);

// Make request
const url = `${serverUrl}${path}?accesskey=${accessKey}&timestamp=${timestamp}&signature=${signature}&name=User`;

fetch(url)
    .then(response => response.json())
    .then(data => console.log(data));
```

### cURL Example

```bash
# Calculate signature (using bash)
SECRET_KEY="test-secret-1"
ACCESS_KEY="test-key-1"
PATH="/api/hello"
TIMESTAMP=$(date +%s)
SIGNATURE=$(echo -n "${SECRET_KEY}${ACCESS_KEY}${TIMESTAMP}${PATH}" | sha1sum | cut -d' ' -f1)

# Make request
curl "http://localhost:5000${PATH}?accesskey=${ACCESS_KEY}&timestamp=${TIMESTAMP}&signature=${SIGNATURE}&name=User"
```

## Adding New Routes

To add a new route:

1. Create a new handler file in the `handlers/` directory:

```python
# handlers/my_handler.py
from flask import jsonify

def handle(request):
    return jsonify({'message': 'My custom endpoint'})
```

2. Add the route in `server.py`:

```python
@app.route('/api/myendpoint')
@require_auth
def my_endpoint():
    from handlers import my_handler
    return my_handler.handle(request)
```

## Authentication Parameters

Authentication parameters can be passed either as:

- **Query parameters**: `?accesskey=...&timestamp=...&signature=...`
- **HTTP headers**: `X-Access-Key`, `X-Timestamp`, `X-Signature`

## Security Notes

- **Keep your secret keys secure**: Never commit them to version control. In production, load them from environment variables or a secure secrets management system
- **Use HTTPS in production**: This prevents credential and data interception
- **SHA1 Note**: This implementation uses SHA1 as specified in the requirements. While SHA1 is considered cryptographically weak for collision resistance, it's acceptable for HMAC-like signature verification when combined with proper timestamp validation and HTTPS
- **Timing attack protection**: The implementation uses constant-time comparison for signature verification
- **Timestamp validation**: The default 5-minute window prevents replay attacks
- **Each request requires a fresh signature** with current timestamp
- **Consider implementing rate limiting** for production use
- **Debug mode**: Set `DEBUG = False` in production to avoid exposing sensitive information

## Project Structure

```
.
├── server.py              # Main Flask application with auth
├── config.py              # Configuration and access keys
├── requirements.txt       # Python dependencies
├── handlers/              # Route handlers
│   ├── __init__.py
│   ├── hello_handler.py   # Handler for /api/hello
│   └── status_handler.py  # Handler for /api/status
└── README.md
```

## License

See LICENSE file for details.
