# kusho-capture

Kusho-capture is a lightweight HTTP traffic capture middleware for Python web applications. It seamlessly integrates with popular frameworks like FastAPI, Flask, and Django to record API traffic for testing, debugging, and monitoring purposes.

## Features

- 🔄 Automatic HTTP traffic capture for API endpoints
- 🎯 Configurable URL pattern matching
- 📦 Support for both WSGI and ASGI applications
- 🔍 Detailed request/response logging
- ⚡ Async support for modern web frameworks
- 🎛️ Configurable sampling rate for high-traffic applications
- 📊 Batch processing of captured events
- 🚀 Framework auto-detection

## Installation

```bash
pip install kusho-capture
```

For framework-specific dependencies:

```bash
pip install kusho-capture[fastapi]  # For FastAPI support
pip install kusho-capture[flask]    # For Flask support
pip install kusho-capture[django]   # For Django support
```

## Quick Start

### FastAPI Example

```python
from fastapi import FastAPI
from kusho_capture import EventCollector, setup_traffic_capture

app = FastAPI()
collector = EventCollector(
    collector_url="https://your-collector-endpoint.com",
    sample_rate=0.1,
    batch_size=100
)

app = setup_traffic_capture(app, collector, framework="fastapi")

@app.get("/api/items")
async def get_items():
    return {"items": ["item1", "item2"]}
```

### Flask Example

```python
from flask import Flask
from kusho_capture import EventCollector, setup_traffic_capture

app = Flask(__name__)
collector = EventCollector(
    collector_url="https://your-collector-endpoint.com",
    sample_rate=0.1,
    batch_size=100
)

app.wsgi_app = setup_traffic_capture(app.wsgi_app, collector, framework="flask")

@app.route("/api/items")
def get_items():
    return {"items": ["item1", "item2"]}
```

### Django Example

```python
# settings.py
MIDDLEWARE = [
    'kusho_capture.WSGIMiddleware',
    # ... other middleware
]

# somewhere in your configuration
from kusho_capture import EventCollector, setup_traffic_capture

collector = EventCollector(
    collector_url="https://your-collector-endpoint.com",
    sample_rate=0.1,
    batch_size=100
)

application = setup_traffic_capture(application, collector, framework="django")
```

## Configuration

### EventCollector Options

- `collector_url`: URL of your event collection endpoint
- `batch_size`: Number of events to batch before sending (default: 100)
- `flush_interval`: Maximum time to wait before sending a batch in seconds (default: 60)
- `max_queue_size`: Maximum number of events to queue (default: 10000)
- `sample_rate`: Percentage of requests to capture (default: 0.1 = 10%)

### Middleware Options

- `url_patterns`: List of URL patterns to match for capture (default: ['/api/'])
- `framework`: Auto-detected by default, can be explicitly set to 'fastapi', 'flask', or 'django'

## Event Data Structure

Captured events include:
- Timestamp
- Request path and method
- Request headers
- Query parameters
- Request body (for POST/PUT/PATCH requests)
- Response status and headers
- Response time

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.