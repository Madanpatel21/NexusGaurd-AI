# edge/edge-agent/src/command_listener.py
"""Lightweight command endpoint so JARVIS can drive edge self-healing."""
import json
import logging
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

logger = logging.getLogger("NexusGuard-Edge")


class CommandHandler(BaseHTTPRequestHandler):
    agent = None  # set by start()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        command = body.get("command", "")
        params = body.get("params", {})
        logger.info(f"Received command from JARVIS: '{command}' params={params}")

        if self.agent is not None:
            self.agent.remediate(command, params)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "executed", "command": command}).encode())

    def log_message(self, *args):
        pass  # silence default stderr logging


def start(agent, port=8001):
    CommandHandler.agent = agent
    server = ThreadingHTTPServer(("0.0.0.0", port), CommandHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    logger.info(f"Edge command listener on :{port}")
    return server
