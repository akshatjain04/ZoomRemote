import unittest
from http.server import SimpleHTTPRequestHandler
from unittest.mock import Mock
from io import BytesIO

class TestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='./', **kwargs)

    def send_simple_response(self, content, ctype):
        self.send_response(200)
        self.send_header("Content-type", ctype)
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content.encode())

class TestRequestHandler(unittest.TestCase):
    def setUp(self):
        self.handler = TestHandler(Mock(), ('localhost', 8080), Mock())
        self.handler.wfile = BytesIO()

    def test_send_simple_response_text(self):
        self.handler.send_simple_response('Hello, World!', 'text/plain')
        headers = self.handler.wfile.getvalue()
        self.assertIn(b'Content-type: text/plain', headers)
        self.assertIn(b'Content-Length: 13', headers)
        self.assertIn(b'Hello, World!', headers)

    def test_send_simple_response_html(self):
        self.handler.send_simple_response('<h1>Hello, World!</h1>', 'text/html')
        headers = self.handler.wfile.getvalue()
        self.assertIn(b'Content-type: text/html', headers)
        self.assertIn(b'Content-Length: 22', headers)
        self.assertIn(b'<h1>Hello, World!</h1>', headers)

if __name__ == '__main__':
    unittest.main()
