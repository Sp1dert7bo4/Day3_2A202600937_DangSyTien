# -*- coding: utf-8 -*-
"""
OPTC Strategy System — Zero-Dependency Live Web Server
Hosts the interactive dashboard and bridges browser chat directly with the ReAct Agent.
"""
import os
import sys
import json
import time
import webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.core.gemini_provider import GeminiProvider
from src.core.openai_provider import OpenAIProvider
from src.agent.agent import ReActAgent
from src.tools.tool_registry import TOOLS
from src.telemetry.logger import logger

# Thread-safe local storage for capturing logs during a request
captured_events = []
original_log_event = logger.log_event

# Intercept logger events to collect them for the API response
def custom_log_event(event_type: str, data: Dict[str, Any]):
    payload = {
        "event": event_type,
        "data": data
    }
    captured_events.append(payload)
    original_log_event(event_type, data)

logger.log_event = custom_log_event


class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default server logs in console to keep output clean
        pass

    def do_GET(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Serve the HTML dashboard at the root URL
        if self.path == "/" or self.path == "/index.html":
            demo_path = os.path.join(current_dir, "demo.html")
            try:
                with open(demo_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except Exception as e:
                self.send_error(500, f"Error reading demo.html: {e}")
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        # REST API endpoint to chat with the ReAct Agent
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            
            try:
                request_json = json.loads(post_data.decode("utf-8"))
                query = request_json.get("query", "").strip()
                
                if not query:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Empty query"}).encode("utf-8"))
                    return

                # Initialize LLM dynamically based on .env configuration
                provider = os.getenv("DEFAULT_PROVIDER", "google").lower()
                model = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
                
                if provider == "google":
                    llm = GeminiProvider(model_name=model)
                else:
                    llm = OpenAIProvider(model_name=model)
                
                agent = ReActAgent(llm=llm, tools=TOOLS, max_steps=8)
                
                # Clear and capture ReAct loop event trace
                global captured_events
                captured_events = []
                
                print(f"🌐 [Web Demo] Query received: {query}")
                answer = agent.run(query)
                print(f"✅ [Web Demo] Strategy proposal generated successfully.")

                # Package the final answer along with step-by-step logs
                response_payload = {
                    "answer": answer,
                    "steps": captured_events,
                    "provider": provider,
                    "model": model
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(response_payload).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")


def run(port=8000):
    server_address = ("", port)
    httpd = ThreadingHTTPServer(server_address, DashboardHandler)
    
    print("=" * 60)
    print("🚀 OPTC STRATEGY SYSTEM — LIVE INTERACTIVE WEB SERVER")
    print("=" * 60)
    print(f"🌐 Server is running at: http://localhost:{port}/")
    print(f"📁 Dashboard template: src/demo.html")
    print(f"Press Ctrl+C to terminate.")
    print("=" * 60)
    
    # Auto-open browser window after a tiny delay
    time.sleep(1)
    webbrowser.open(f"http://localhost:{port}/")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()


if __name__ == "__main__":
    run()
