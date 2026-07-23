"""Serve the local card reviewer quietly, including under pythonw on Windows."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, _format, *_args):
        pass

if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 4173), QuietHandler).serve_forever()
