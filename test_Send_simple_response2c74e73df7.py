import unittest
from unittest.mock import Mock, MagicMock, patch
from http.server import SimpleHTTPRequestHandler
from io import BytesIO

class TestHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.rfile = request
        self.wfile = BytesIO()
        self.client_address = client_address
        self.server = server

    def send_error(self, code, message=None):
        self.send_response_only(code, message)

class TestSend_simple_response2c74e73df7(unittest.TestCase):
    def setUp(self):
        self.request = BytesIO(b'GET / HTTP/1.0\r\n')
        self.client_address = ("localhost", 8000)
        self.server = MagicMock()
        self.handler = TestHandler(self.request, self.client_address, self.server)
        self.handler.send_response = Mock()
        self.handler.send_header = Mock()
        self.handler.end_headers = Mock()

    def test_send_simple_response(self):
        content = "Hello, World!"
        ctype = "text/html"

        self.handler.send_simple_response(content, ctype)

        self.handler.send_response.assert_called_once_with(200)
        self.handler.send_header.assert_any_call("Content-type", ctype)
        self.handler.send_header.assert_any_call("Content-Length", len(content))
        self.handler.end_headers.assert_called_once()
        self.assertEqual(self.handler.wfile.getvalue(), content.encode())

    def test_send_simple_response_empty_content(self):
        content = ""
        ctype = "text/html"

        self.handler.send_simple_response(content, ctype)

        self.handler.send_response.assert_called_once_with(200)
        self.handler.send_header.assert_any_call("Content-type", ctype)
        self.handler.send_header.assert_any_call("Content-Length", len(content))
        self.handler.end_headers.assert_called_once()
        self.assertEqual(self.handler.wfile.getvalue(), content.encode())

if __name__ == '__main__':
    unittest.main()
