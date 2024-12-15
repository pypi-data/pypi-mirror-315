import time
import json
import urllib.parse
from typing import List, Optional, Dict, Any
from .collector import EventCollector

def parse_query_params(environ):
    return dict(urllib.parse.parse_qs(environ.get('QUERY_STRING', '')))

def parse_request_body(environ):
    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        if content_length > 0:
            body = environ['wsgi.input'].read(content_length)
            return json.loads(body)
    except:
        pass
    return None

class WSGIMiddleware:
    def __init__(
        self, 
        app,
        collector: EventCollector,
        url_patterns: Optional[List[str]] = None
    ):
        self.app = app
        self.collector = collector
        self.url_patterns = url_patterns or ['/api/']

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        
        should_capture = any(pattern in path for pattern in self.url_patterns)
        if not should_capture:
            return self.app(environ, start_response)

        start_time = time.time()
        response_status = []
        response_headers = []
        
        def custom_start_response(status, headers, exc_info=None):
            response_status.append(status)
            response_headers.extend(headers)
            return start_response(status, headers, exc_info)

        response = self.app(environ, custom_start_response)
        duration = (time.time() - start_time) * 1000

        event = {
            'timestamp': start_time,
            'path': path,
            'method': environ.get('REQUEST_METHOD'),
            'headers': {k: v for k, v in environ.items() if k.startswith('HTTP_')},
            'path_params': environ.get('wsgiorg.routing_args', {}),
            'query_params': parse_query_params(environ),
            'request_body': parse_request_body(environ),
            'status': response_status[0] if response_status else None,
            'duration_ms': duration,
            'response_headers': dict(response_headers)
        }
        
        self.collector.capture(event)
        return response

class ASGIMiddleware:
    def __init__(
        self,
        app,
        collector: EventCollector,
        url_patterns: Optional[List[str]] = None
    ):
        self.app = app
        self.collector = collector
        self.url_patterns = url_patterns or ['/api/']

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)

        path = scope.get('path', '')
        should_capture = any(pattern in path for pattern in self.url_patterns)
        
        if not should_capture:
            return await self.app(scope, receive, send)

        start_time = time.time()
        response_status = []
        response_headers = []
        request_body = None

        # Capture request body
        if scope['method'] in ['POST', 'PUT', 'PATCH']:
            body_chunks = []
            async def wrapped_receive():
                message = await receive()
                if message['type'] == 'http.request':
                    body_chunks.append(message.get('body', b''))
                return message
            
            try:
                message = await wrapped_receive()
                if body_chunks:
                    request_body = json.loads(b''.join(body_chunks).decode())
            except:
                request_body = None
        else:
            message = await receive()

        # Capture response
        async def wrapped_send(message):
            if message['type'] == 'http.response.start':
                response_status.append(message.get('status'))
                response_headers.extend(message.get('headers', []))
            await send(message)

        await self.app(scope, receive, wrapped_send)
        duration = (time.time() - start_time) * 1000

        # Parse headers
        headers = {}
        for key, value in scope.get('headers', []):
            key = key.decode('utf-8')
            value = value.decode('utf-8')
            headers[f"HTTP_{key.upper().replace('-', '_')}"] = value

        # Parse query string
        query_string = scope.get('query_string', b'').decode()
        query_params = dict(urllib.parse.parse_qs(query_string))

        event = {
            'timestamp': start_time,
            'path': path,
            'method': scope.get('method'),
            'headers': headers,
            'path_params': dict(scope.get('path_params', {})),
            'query_params': query_params,
            'request_body': request_body,
            'status': response_status[0] if response_status else None,
            'duration_ms': duration,
            'response_headers': dict(response_headers)
        }
        
        self.collector.capture(event)

def setup_traffic_capture(
    app,
    collector: EventCollector,
    framework: str = 'auto',
    url_patterns: Optional[List[str]] = None
):
    """Helper function to set up the appropriate middleware based on framework."""
    if framework == 'auto':
        # Try to detect the framework
        if hasattr(app, 'router'):  # FastAPI/Starlette
            framework = 'fastapi'
        elif hasattr(app, 'wsgi_app'):  # Flask
            framework = 'flask'
        elif hasattr(app, 'get_response'):  # Django
            framework = 'django'
    
    if framework in ['fastapi', 'starlette']:
        return ASGIMiddleware(app, collector, url_patterns)
    else:  # flask, django, or unknown
        return WSGIMiddleware(app, collector, url_patterns)