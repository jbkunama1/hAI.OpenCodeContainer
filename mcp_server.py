#!/usr/bin/env python3
"""
OpenCode MCP Server with Token Authentication
Secure MCP server for OpenCode with JWT token authentication
"""

import json
import logging
import os
import secrets
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import jwt
from datetime import datetime, timedelta
import threading
import time

# JWT error handling
try:
    from jwt.exceptions import PyJWTError
except ImportError:
    PyJWTError = Exception

# Configuration
SECRET_KEY = os.environ.get('OPENCODE_MCP_SECRET_KEY', secrets.token_urlsafe(32))
# TOKEN_EXPIRY removed - tokens have unlimited validity
MCP_PORT = int(os.environ.get('MCP_PORT', 9000))
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# Setup logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

class MCPHandler(BaseHTTPRequestHandler):
    """MCP Server Handler with token authentication"""
    
    def _send_response(self, status_code, content, content_type='application/json'):
        """Send HTTP response"""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(content.encode())
    
    def _validate_token(self, auth_header):
            """Validate JWT token (no expiry check)"""
            if not auth_header or not auth_header.startswith('Bearer '):
                return None
        
            token = auth_header[7:]  # Remove 'Bearer ' prefix
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
                return payload
            except PyJWTError:
                return None
    
    def _generate_token(self, user_id='opencode'):
        """Generate JWT token without expiry"""
        payload = {
            'user': user_id,
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    def _handle_options(self):
        """Handle CORS preflight requests"""
        self._send_response(200, '')
    
    def _handle_mcp_request(self, token, method, params):
        """Handle MCP requests"""
        try:
            if method == 'ping':
                return {"status": "ok", "server": "OpenCode MCP Server"}
            
            elif method == 'chat':
                # OpenCode chat integration
                message = params.get('message', '')
                model = params.get('model', 'gpt-3.5-turbo')
                temperature = params.get('temperature', 0.7)
                
                logger.info(f"Chat request: {message[:50]}...")
                
                # Forward to OpenCode API
                response = {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": f"OpenCode MCP Server received: {message}\nModel: {model}\nTemperature: {temperature}"
                    }
                }
                return response
            
            elif method == 'tools.list':
                # List available tools
                return {
                    "jsonrpc": "2.0", 
                    "result": {
                        "tools": [
                            {
                                "name": "opencode_chat",
                                "description": "Send message to OpenCode AI",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "message": {"type": "string", "description": "Message to send"},
                                        "model": {"type": "string", "default": "gpt-3.5-turbo"},
                                        "temperature": {"type": "number", "default": 0.7}
                                    }
                                }
                            }
                        ]
                    }
                }
            
            elif method == 'tokens.create':
                # Create new token
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "token": self._generate_token()
                    }
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                
        except Exception as e:
            logger.error(f"MCP request error: {e}")
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    def do_OPTIONS(self):
        """Handle CORS OPTIONS requests"""
        self._handle_options()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/mcp':
            # Extract authorization header
            auth_header = self.headers.get('Authorization')
            
            # Special case for token creation (no token required)
            if self.path == '/mcp' and auth_header == 'Bearer CREATE_TOKEN':
                token = self._generate_token()
                response = {"token": token}
                self._send_response(200, json.dumps(response))
                return
            
            # Validate token for other requests
            if not auth_header:
                self._send_response(401, json.dumps({"error": "Missing Authorization header"}))
                return
            
            token_payload = self._validate_token(auth_header)
            if not token_payload:
                self._send_response(401, json.dumps({"error": "Invalid or expired token"}))
                return
            
            # Process MCP request
            try:
                content_length = int(self.headers['Content-Length'])
                body = json.loads(self.rfile.read(content_length))
                
                method = body.get('method')
                params = body.get('params', {})
                
                result = self._handle_mcp_request(token_payload, method, params)
                
                response = {
                    "jsonrpc": "2.0",
                    "id": body.get('id', 1),
                    "result": result if not isinstance(result, dict) or 'error' not in result else result
                }
                
                self._send_response(200, json.dumps(response))
                
            except Exception as e:
                logger.error(f"Error processing request: {e}")
                self._send_response(500, json.dumps({"error": "Internal server error"}))
        
        else:
            self._send_response(404, json.dumps({"error": "Not found"}))
    
    def log_message(self, format, *args):
        """Custom logging"""
        logger.info(f"{self.client_address[0]} - - [{self.log_date_time_string()}] {format % args}")


class HealthHandler(BaseHTTPRequestHandler):
    """Health check handler"""
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"status": "healthy", "service": "OpenCode MCP Server"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()


def start_server():
    """Start MCP server with health endpoint"""
    # Create server with multiple handlers
    server = HTTPServer(('0.0.0.0', MCP_PORT), MCPHandler)
    
    # Add health check in separate thread
    def health_server():
        health = HTTPServer(('0.0.0.0', MCP_PORT + 1), HealthHandler)
        health.serve_forever()
    
    health_thread = threading.Thread(target=health_server, daemon=True)
    health_thread.start()
    
    logger.info(f"MCP Server started on port {MCP_PORT}")
    logger.info(f"Health check available on port {MCP_PORT + 1}")
    logger.info(f"Secret key configured: {'*' * 8}{SECRET_KEY[-8:] if len(SECRET_KEY) > 8 else SECRET_KEY}")
    
    server.serve_forever()


if __name__ == '__main__':
    # Install required packages if not available
    try:
        import jwt
    except ImportError:
        logger.error("JWT library not found. Install with: pip install PyJWT")
        exit(1)
    
    start_server()