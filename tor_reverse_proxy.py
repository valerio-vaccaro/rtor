from functools import wraps
from flask import request, Response, Flask
import requests
import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

# def check_auth(username, password):
#     """Verify credentials - replace with your own authentication logic"""
#     return username == 'admin' and password == 'your-secure-password'

# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(auth.username, auth.password):
#             return Response(
#                 'Could not verify your access level for that URL.\n'
#                 'You have to login with proper credentials', 401,
#                 {'WWW-Authenticate': 'Basic realm="Login Required"'})
#         return f(*args, **kwargs)
#     return decorated

def get_tor_session():
    """Create a requests session that routes through Tor"""
    session = requests.session()
    session.proxies = {
        'http': f'socks5h://{args.socks_host}:{args.socks_port}',
        'https': f'socks5h://{args.socks_host}:{args.socks_port}'
    }
    return session

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
# @requires_auth
def proxy(path):
    """Handle all incoming requests and proxy them to the Tor hidden service"""
    try:
        # Use the provided onion URL
        target_url = f"http://{args.onion_url}/{path}"
        
        session = get_tor_session()
        
        # Forward the request to the Tor hidden service
        resp = session.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )

        # Create the response
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                  if name.lower() not in excluded_headers]

        response = Response(resp.content, resp.status_code, headers)
        return response

    except Exception as e:
        logger.error(f"Proxy error: {str(e)}")
        return f"Error: {str(e)}", 500 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='rTor: Tor Reverse Proxy')
    parser.add_argument('--socks-port', type=int, default=9050,
                    help='Tor SOCKS port (default: 9050)')
    parser.add_argument('--socks-host', type=str, default='127.0.0.1',
                    help='Tor SOCKS host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8080,
                    help='Port to run the proxy server on (default: 8080)')
    parser.add_argument('--onion-url', type=str, required=True,
                    help='Target .onion URL (without http:// prefix)')
    
    args = parser.parse_args()
    
    # Run the Flask app with provided port
    app.run(host='0.0.0.0', port=args.port)
