import json
from typing import Callable, Tuple

# Simple WSGI application without external dependencies

def _json_response(data: dict, status: str = "200 OK") -> Tuple[bytes, list, str]:
    body = json.dumps(data).encode("utf-8")
    headers = [("Content-Type", "application/json"), ("Content-Length", str(len(body)))]
    return body, headers, status


def health(environ, start_response):
    body, headers, status = _json_response({"status": "ok"}, "200 OK")
    start_response(status, headers)
    return [body]


def template(environ, start_response):
    sample_template = {
        "industry": "Technology",
        "region": "EU",
        "checklist": [
            {"id": 1, "question": "Does the company disclose carbon emissions?", "required": True},
            {"id": 2, "question": "Is there a board-level ESG oversight?", "required": False},
        ],
    }
    body, headers, status = _json_response(sample_template, "200 OK")
    start_response(status, headers)
    return [body]

# Route dispatch table
_ROUTES = {
    "/health": health,
    "/template": template,
}


def application(environ, start_response):
    path = environ.get("PATH_INFO", "")
    handler = _ROUTES.get(path)
    if handler:
        return handler(environ, start_response)
    # 404 response
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not Found"]

# Export a name expected by tests
app = application

if __name__ == "__main__":
    # Run a simple development server
    from wsgiref.simple_server import make_server

    with make_server("0.0.0.0", 8000, application) as httpd:
        print("Serving on http://0.0.0.0:8000 ...")
        httpd.serve_forever()
