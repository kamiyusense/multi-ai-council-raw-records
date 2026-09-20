from .base import Transport
import subprocess
import json
import sys

class LiveAppServerTransport(Transport):
    def __init__(self, config=None):
        self.config = config or {}
        self.client_factory_build_count = 0
        self.app_server_process_started = False
        self.live_transport_executed = False
        self.model_executed = False

        self.client = None
        self.process = None
        self.codex_module = None

    def _lazy_import_sdk(self):
        try:
             import openai
             self.codex_module = openai
        except ImportError:
             pass

    def _build_client_factory(self):
        self._lazy_import_sdk()
        self.client_factory_build_count += 1

        if self.codex_module:
             return self.codex_module.Client(api_key="poc-key", base_url="http://localhost/v1")
        return None

    def _build_stdio_process(self):
        runner_bin = self.config.get("codex_bin_path", "codex-app-server")
        cmd = [runner_bin, "--listen", "stdio://"]

        if self.config.get("live_execution_permitted", False):
            self.app_server_process_started = True

        return cmd

    # JSON-RPC request builders
    def _build_initialize_request(self):
        return {"method": "initialize", "params": {}}

    def _build_thread_start_request(self):
        return {"method": "thread/start", "params": {}}

    def _build_thread_resume_request(self, thread_id):
        return {"method": "thread/resume", "params": {"threadId": thread_id}}

    def _build_thread_read_request(self, thread_id):
        return {"method": "thread/read", "params": {"threadId": thread_id}}

    def _build_thread_turns_list_request(self, thread_id):
        return {"method": "thread/turns/list", "params": {"itemsView": "full", "threadId": thread_id}}

    def _build_turn_start_request(self, thread_id, inputs, client_msg_id):
        return {
            "method": "turn/start",
            "params": {
                "clientUserMessageId": client_msg_id,
                "input": inputs,
                "threadId": thread_id
            }
        }

    # Notification handling
    def _handle_initialized(self, payload):
        pass # Handle initialized confirmation

    def _handle_turn_completed(self, payload):
        pass # Handle turn/completed streaming end

    def start(self):
        # Structurally setup the environment
        self.client = self._build_client_factory()
        self.process = self._build_stdio_process()

        # Enforce POC block
        if not self.config.get("live_execution_permitted", False):
            raise Exception("Live execution is STRICTLY PROHIBITED in this POC.")

    def send(self, payload):
        self.live_transport_executed = True
        method = payload.get("method")

        if method == "turn/start":
            self.model_executed = True

        # Dispatch table
        if method == "initialize":
            pass
        elif method == "initialized":
            self._handle_initialized(payload)
        elif method == "thread/start":
            pass
        elif method == "thread/resume":
            pass
        elif method == "thread/read":
            pass
        elif method == "thread/turns/list":
            pass
        elif method == "turn/completed":
            self._handle_turn_completed(payload)

        if not self.config.get("live_execution_permitted", False):
            raise Exception("Live execution is STRICTLY PROHIBITED in this POC.")

        return {"result": {"routed": True}}

    def shutdown(self):
        if self.process and hasattr(self.process, 'terminate'):
            self.process.terminate()
