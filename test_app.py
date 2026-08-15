import json
from app import app
from wsgiref.util import setup_testing_defaults


def _call_app(path: str):
    environ = {}
    setup_testing_defaults(environ)
    environ["REQUEST_METHOD"] = "GET"
    environ["PATH_INFO"] = path
    result = {}
    def start_response(status, headers):
        result["status"] = status
        result["headers"] = headers
    response_body = b"".join(app(environ, start_response))
    return result["status"], response_body


def test_health_endpoint():
    status, body = _call_app('/health')
    assert status.startswith('200')
    data = json.loads(body)
    assert data == {"status": "ok"}


def test_template_endpoint():
    status, body = _call_app('/template')
    assert status.startswith('200')
    data = json.loads(body)
    assert data["industry"] == "Technology"
    assert isinstance(data["checklist"], list)
    assert len(data["checklist"]) == 2
