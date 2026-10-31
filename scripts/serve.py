"""Servidor local de desarrollo sin dependencias. Para móviles, servir con HTTPS."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
from urllib.parse import unquote,urlsplit
os.chdir(Path(__file__).resolve().parent.parent)
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if any(part.startswith('.') for part in unquote(urlsplit(self.path).path).split('/')):
            self.send_error(404)
            return
        super().do_GET()
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()
print('Jujuy: servidor de desarrollo en puerto ' + os.environ.get('PORT', '8000'), flush=True)
ThreadingHTTPServer(('127.0.0.1', int(os.environ.get('PORT', '8000'))), Handler).serve_forever()
