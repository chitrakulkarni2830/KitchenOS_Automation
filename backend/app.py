import http.server
import json
import logging
import urllib.parse
import os
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.config import Config
from backend.database.db_manager import DatabaseManager
from backend.services.business_services import BusinessServices
from backend.routes.auth import handle_auth_routes
from backend.routes.inventory import handle_inventory_routes
from backend.routes.recipes import handle_recipe_routes
from backend.routes.pos import handle_pos_routes
from backend.utils.helpers import decode_jwt, error_response, standard_response

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("kitchen_os")

# Initialize Shared Managers
db_manager = DatabaseManager(Config.DB_PATH)
services = BusinessServices(db_manager)

class KitchenOSHTTPHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logger.info(f"{self.address_string()} - - {format%args}")

    def end_headers(self):
        # Enforce CORS rules
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def handle_static_file(self):
        """Serves static frontend HTML/JS/CSS assets if route is not an API."""
        path = self.path.split("?")[0]
        if path == "/":
            path = "/index.html"
            
        # Try to resolve filepath
        file_path = os.path.abspath(os.path.join(Config.STATIC_FOLDER, path.lstrip("/")))
        
        # Security boundaries check
        root_dir = os.path.abspath(Config.STATIC_FOLDER)
        if not file_path.startswith(root_dir):
            self.send_error_json("FORBIDDEN", "Path access out of bounds.", 403)
            return

        if os.path.exists(file_path) and not os.path.isdir(file_path):
            # Resolve content type
            content_type = "text/plain"
            if file_path.endswith(".html"):
                content_type = "text/html"
            elif file_path.endswith(".js"):
                content_type = "application/javascript"
            elif file_path.endswith(".css"):
                content_type = "text/css"
            elif file_path.endswith(".json"):
                content_type = "application/json"
            elif file_path.endswith(".svg"):
                content_type = "image/svg+xml"

            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                logger.error(f"Error reading file: {e}")
                self.send_error_json("FILE_READ_ERROR", f"Error rendering page: {str(e)}", 500)
        else:
            self.send_error_json("NOT_FOUND", "Resource file not found.", 404)

    def send_error_json(self, code, message, status_code):
        response, code_status = error_response(code, message, status_code=status_code)
        self.send_response(code_status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def get_request_user(self):
        """Extracts and verifies authorization credentials from headers."""
        auth_header = self.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ")[1]
        return decode_jwt(token)

    def process_api_route(self):
        """Main routing controller parsing bodies, queries, permissions and dispatches."""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)
        method = self.command

        # Read JSON body payload if provided
        body = {}
        content_length = self.headers.get('Content-Length')
        if content_length:
            try:
                body_data = self.rfile.read(int(content_length)).decode('utf-8')
                if body_data:
                    body = json.loads(body_data)
            except Exception as e:
                logger.error(f"Failed to parse request JSON body: {e}")
                self.send_error_json("MALFORMED_JSON", "Request body must be valid JSON.", 400)
                return

        # 1. Open Health check route (No authentication needed)
        if method == "GET" and path == "/api/v1/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(standard_response(data={"status": "healthy"})).encode())
            return

        # 2. Authentications endpoints (No authorization token checking needed)
        if path.startswith("/api/v1/auth"):
            try:
                res_data, status_code = handle_auth_routes(method, path, body, services, self.headers)
                self.send_response(status_code)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(res_data).encode())
            except Exception as e:
                logger.error(f"Auth route error: {e}")
                self.send_error_json("INTERNAL_SERVER_ERROR", str(e), 500)
            return

        # 3. Secure Endpoints requiring JWT checks
        user = self.get_request_user()
        if not user:
            self.send_error_json("UNAUTHORIZED", "Missing or expired authorization credentials.", 401)
            return

        # Inject logged-in user details to headers dictionary
        self.headers['X-User-Role'] = user.get("role")
        self.headers['X-User-Email'] = user.get("email")

        try:
            res_data, status_code = None, 404
            
            # Route dispatches
            if path.startswith("/api/v1/ingredients") or path.startswith("/api/v1/pantry"):
                res_data, status_code = handle_inventory_routes(method, path, body, services, self.headers, query_params)
            elif path.startswith("/api/v1/recipes"):
                res_data, status_code = handle_recipe_routes(method, path, body, services, self.headers)
            elif path.startswith("/api/v1/pos"):
                # Role control: only allow POS webhooks to be called
                res_data, status_code = handle_pos_routes(method, path, body, services, self.headers)

            if res_data is not None:
                self.send_response(status_code)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(res_data).encode())
            else:
                self.send_error_json("ROUTE_NOT_FOUND", f"Route {method} {path} not found.", 404)
        except Exception as e:
            logger.error(f"Global route exception: {e}")
            self.send_error_json("INTERNAL_SERVER_ERROR", f"An internal server exception occurred: {str(e)}", 500)

    def do_GET(self):
        if self.path.startswith("/api"):
            self.process_api_route()
        else:
            self.handle_static_file()

    def do_POST(self):
        if self.path.startswith("/api"):
            self.process_api_route()
        else:
            self.send_error_json("METHOD_NOT_ALLOWED", "Static assets do not support POST requests.", 405)

    def do_PUT(self):
        if self.path.startswith("/api"):
            self.process_api_route()
        else:
            self.send_error_json("METHOD_NOT_ALLOWED", "Static assets do not support PUT requests.", 405)

    def do_DELETE(self):
        if self.path.startswith("/api"):
            self.process_api_route()
        else:
            self.send_error_json("METHOD_NOT_ALLOWED", "Static assets do not support DELETE requests.", 405)

def run_server():
    server_address = ('', Config.PORT)
    httpd = http.server.HTTPServer(server_address, KitchenOSHTTPHandler)
    logger.info(f"KitchenOS Server running on port {Config.PORT}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("KitchenOS Server shutting down...")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
