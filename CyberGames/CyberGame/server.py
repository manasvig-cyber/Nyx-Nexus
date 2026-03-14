"""
Simple HTTP server for the CyberGame project.
Serves all files from the project directory, including static assets.

Usage:
    python server.py

Then open http://localhost:8080 in your browser.
"""

import http.server
import socketserver
import os

PORT = 8080

# Change to the directory where the script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler

# Add proper MIME types for image files
Handler.extensions_map.update({
    '.webp': 'image/webp',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.html': 'text/html',
})

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"=== CyberGame Server ===")
    print(f"Serving at http://localhost:{PORT}")
    print(f"Open http://localhost:{PORT}/index.html to play")
    print(f"Press Ctrl+C to stop")
    httpd.serve_forever()
