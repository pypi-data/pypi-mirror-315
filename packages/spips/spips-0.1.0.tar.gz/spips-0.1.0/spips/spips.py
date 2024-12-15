from jinja2 import Template
from http.server import HTTPServer, BaseHTTPRequestHandler
import re

class Spips:
    def __init__(self):
        self.routes = {}  # Menyimpan semua route dan handler-nya
        self.output = ""  # Hasil render HTML
    
    def route(self, path, method):
        """Dekorator untuk mendefinisikan route."""
        def decorator(func):
            self.routes[(path, method.lower())] = func
            return func
        return decorator

    def render(self, template_file, **kwargs):
        """Fungsi untuk merender template HTML."""
        try:
            with open(f"views/{template_file}", 'r') as file:
                template_content = file.read()
            template = Template(template_content)
            self.output = template.render(**kwargs)
        except FileNotFoundError:
            self.output = f"<h1>Error: File '{template_file}' not found.</h1>"

    def serve(self, port=8000):
        """Menjalankan server HTTP."""
        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(handler_self):
                route_key = (handler_self.path, 'get')
                if route_key in self.routes:
                    self.routes[route_key]()  # Panggil handler yang sesuai
                else:
                    self.output = "<h1>404 Not Found</h1>"
                handler_self.send_response(200)
                handler_self.send_header('Content-type', 'text/html')
                handler_self.end_headers()
                handler_self.wfile.write(self.output.encode('utf-8'))

        # Jalankan server HTTP
        server = HTTPServer(('localhost', port), RequestHandler)
        from colorama import Fore, Style

        print()
        print(Fore.GREEN + "    Spips server running on the " + Fore.CYAN + f"http://localhost:{port}" + Style.RESET_ALL)
        print()
        print(Fore.YELLOW + "    ctrl + c to stop the server" + Style.RESET_ALL)

        server.serve_forever()


class Router:
    """Dummy class untuk routing."""
    @staticmethod
    def register_routes(app):
        """Template untuk mengatur routes di file terpisah."""
        pass


class Modeler:
    """Dummy class untuk model/database."""
    @staticmethod
    def describe_model():
        """Template untuk definisi model di file terpisah."""
        pass