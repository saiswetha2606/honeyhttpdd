import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from termcolor import colored
import requests
import urllib.parse

# Dynamically determine the base directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define log file paths relative to the script's directory
LOG_FILE = os.path.join(BASE_DIR, "logs", "access_log.txt")
FAKE_LOGIN_FILE = os.path.join(BASE_DIR, "logs", "fake_logins.txt")

# Placeholder API Key for AbuseIPDB (Replace with your API Key)
ABUSE_IPDB_API_KEY = "1d6d14c544acebb439cb71bb99fb40c159397c137658925f362be7f2cef5f2d3ed56b98b1a26aed8"

def check_ip_reputation(ip):
    """
    Check IP reputation using AbuseIPDB API.
    """
    if not ABUSE_IPDB_API_KEY:
        return {"error": "No API Key Provided"}
    try:
        url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
        headers = {
            "Accept": "application/json",
            "Key": ABUSE_IPDB_API_KEY,
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

class EnhancedHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Log visitor details
            client_ip = self.client_address[0]
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user_agent = self.headers.get('User-Agent', 'Unknown')
            request_path = self.path

            # Log headers
            headers = "\n".join(f"{key}: {value}" for key, value in self.headers.items())
            log_entry = (
                f"[{timestamp}] IP: {client_ip}, Path: {request_path}, "
                f"User-Agent: {user_agent}\nHeaders:\n{headers}\n"
            )

            # Write to log file
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)  # Ensure logs directory exists
            with open(LOG_FILE, 'a') as log_file:
                log_file.write(log_entry)

            # Check IP reputation
            ip_info = check_ip_reputation(client_ip)
            if ip_info.get("error"):
                print(f"Error checking IP reputation for {client_ip}: {ip_info['error']}")
            else:
                print(f"Reputation info for {client_ip}: {ip_info}")

            # Serve pages based on the path
            if request_path == "/":
                self._serve_default_page()
            elif request_path == "/login":
                self._serve_login_page()
            elif request_path == "/admin":
                self._serve_admin_page()
            else:
                self._serve_404()

        except Exception as e:
            print(f"Error processing request: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"<html><body><h1>500 Internal Server Error</h1></body></html>")

    def do_POST(self):
        if self.path == "/login":
            try:
                # Handle fake login POST request
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                parsed_data = urllib.parse.parse_qs(post_data)

                Email = parsed_data.get('Email', [''])[0]
                Password = parsed_data.get('Password', [''])[0]

                # Log fake credentials
                os.makedirs(os.path.dirname(FAKE_LOGIN_FILE), exist_ok=True)  # Ensure logs directory exists
                with open(FAKE_LOGIN_FILE, 'a') as fake_logins:
                    fake_logins.write(f"Email: {Email}, Password: {Password}\n")

                # Send thank-you page
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Thank you for logging in!</h1></body></html>")
            except Exception as e:
                print(f"Error processing POST request: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"<html><body><h1>500 Internal Server Error</h1></body></html>")
        else:
            self._serve_404()

    def _serve_default_page(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'''
            <html><body>
            <h1>Welcome to HoneyHTTPd!</h1>
            <p>This is a secure area. Unauthorized access is prohibited.</p>
            <a href="/login">Go to Login Page</a>
            </body></html>
        ''')

    def _serve_login_page(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'''
            <html><body>
            <h1>Login Page</h1>
            <form method="POST" action="/login">
                <label for="Email">Email:</label>
                <input type="text" id="Email" name="Email"><br><br>
                <label for="Password">Password:</label>
                <input type="password" id="Password" name="Password"><br><br>
                <button type="submit">Login</button>
            </form>
            </body></html>
        ''')

    def _serve_admin_page(self):
        self.send_response(403)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>403 Forbidden</h1><p>Access Denied</p></body></html>")

    def _serve_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")

    def log_message(self, format, *args):
        return

def start_server(domain, port):
    server = HTTPServer((domain, port), EnhancedHTTPRequestHandler)
    print(colored(f"Server running on {domain}:{port}", "green"))
    server.serve_forever()

if __name__ == "__main__":
    try:
        print(colored("Starting HoneyHTTPd server...", "yellow"))
        threading.Thread(target=start_server, args=("0.0.0.0", 8080), daemon=True).start()
        print(colored("Press Ctrl+C to stop the server", "yellow"))
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        exit(0)
