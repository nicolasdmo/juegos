#!/usr/bin/env python3
"""Mini servidor estático para probar localmente.

Uso:
    python serve.py
Después abrí http://localhost:8000 en el navegador.

Por qué no se puede abrir el index.html con doble clic:
    fetch() de un archivo local (file://) está bloqueado por CORS en todos los
    navegadores modernos. Hay que servir los archivos por HTTP.
"""
import http.server
import socketserver
import os

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".gbc": "application/octet-stream",
        ".gb":  "application/octet-stream",
    }

    def end_headers(self):
        # Sin caché para que los cambios se vean al recargar
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Servidor corriendo en http://localhost:{PORT}")
    print("Ctrl+C para detener.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
