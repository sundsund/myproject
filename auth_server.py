from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class AuthHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/token':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'access_token': 'sample_token', 'token_type': 'bearer'}).encode())
        else:
            self.send_error(404)

httpd = HTTPServer(('localhost', 8081), AuthHandler)
httpd.serve_forever()
