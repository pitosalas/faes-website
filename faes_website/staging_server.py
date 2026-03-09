#!/usr/bin/env python3
# staging_server.py — generates site to staging/ and serves it locally
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import base64
import os
import http.server
from pathlib import Path
from faes_website.site_generator import SiteGenerator

PORT = 8000
PASSWORD = "xyzzy"


class BasicAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self._authorized():
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="FAES Private"')
            self.end_headers()
            return
        super().do_GET()

    def _authorized(self) -> bool:
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Basic "):
            return False
        credentials = base64.b64decode(auth[6:]).decode(errors="replace")
        password = credentials.split(":", 1)[-1]
        return password == PASSWORD

    def log_message(self, format, *args):
        pass  # suppress per-request logging to keep console output clean


class StagingServer:
    def __init__(self, root: Path):
        self.content_dir = root / "content"
        self.staging_dir = root / "staging"

    def run(self, private: bool):
        self.staging_dir.mkdir(exist_ok=True)
        written = SiteGenerator(self.content_dir, self.staging_dir).generate(include_private=private)
        for filename in written:
            print(f"  wrote {filename}")
        print(f"Staging site ready — {len(written)} files in {self.staging_dir}")
        print(f"Serving at http://localhost:{PORT}/index.html")
        if private:
            print(f"Password protected — enter password '{PASSWORD}' when prompted.")
        print("Press Ctrl-C to stop.")
        os.chdir(self.staging_dir)
        handler = BasicAuthHandler if private else http.server.SimpleHTTPRequestHandler
        with http.server.HTTPServer(("", PORT), handler) as server:
            server.serve_forever()
