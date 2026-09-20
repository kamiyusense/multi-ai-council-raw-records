from .base import Transport
from src.parser import Parsers

class TransportTimeoutError(Exception):
    pass

class LiveAppServerTransport(Transport):
    def __init__(self, config=None):
        self.config = config or {}
        self.client_factory_build_count = 0
        self.live_transport_executed = False
        self.model_executed = False
        self.is_initialized = False
        self.independent_subprocess_used = False

        self.client = None
        self.CodexClient = None
        self.CodexConfig = None

        self._rpc_timeout = self.config.get("rpc_timeout", 30)

    def _lazy_import_sdk(self):
        try:
             from openai_codex.client import CodexClient, CodexConfig
             self.CodexClient = CodexClient
             self.CodexConfig = CodexConfig
        except ImportError:
             pass

    def _approval_handler(self, request):
        # Fail-closed implementation: do not auto accept or auto deny.
        raise Exception("APPROVAL_FAIL_CLOSED: Human intervention required")

    def _build_client_factory(self):
        self._lazy_import_sdk()
        self.client_factory_build_count += 1

        runner_bin = self.config.get("codex_bin", "codex-app-server")

        if self.CodexClient and self.CodexConfig:
             # Exact signature as per official specs
             config = self.CodexConfig(codex_bin=runner_bin)

             return self.CodexClient(
                 config=config,
                 approval_handler=self._approval_handler
             )

        # If running in environment without real openai_codex package (e.g. test environment)
        # and live_execution_permitted is somehow True or testing live path fail-closed
        if not self.CodexClient or not self.CodexConfig:
            raise Exception("SDK_UNAVAILABLE: Real openai_codex SDK is not available. Fail-closed.")

        # We should never reach here in POC, but for completeness if it were available
        return self.CodexClient(
             config=self.CodexConfig(codex_bin=runner_bin),
             approval_handler=self._approval_handler
        )

    def start(self):
        if not self.config.get("live_execution_permitted", False):
            raise Exception("Live execution is STRICTLY PROHIBITED in this POC.")

        self.client = self._build_client_factory()

        # CodexClient.start() is STRICTLY PROHIBITED in this POC.
        # if self.client and hasattr(self.client, 'start'):
        #      self.client.start()

        self.is_initialized = True


    def send(self, payload):
        self.live_transport_executed = False
        self.model_executed = False

        method = payload.get("method")
        params = payload.get("params", {})

        if not self.config.get("live_execution_permitted", False):
            raise Exception("Live execution is STRICTLY PROHIBITED in this POC.")

        self.live_transport_executed = True
        if method == "turn/start":
            self.model_executed = True

        try:
             if method == "turn/start":
                 response = self.client.turn_start(**params)
             elif method == "thread/read":
                 response = self.client.thread_read(**params)
             elif method == "thread/start":
                 response = self.client.thread_start(**params)
             elif method == "thread/resume":
                 response = self.client.thread_resume(**params)
             else:
                 response = self.client.request(method, params)
        except Exception as e:
             raise Exception(f"POST_SEND_AMBIGUITY: {str(e)}")

        # DELIVERED 判定ロジック (Backend Correlation check on live path)
        if method == "turn/start":
             turn_id = response.get("result", {}).get("turn", {}).get("id")
             if not turn_id:
                 raise Exception("POST_SEND_AMBIGUITY: No turn.id in turn/start response")

             # Wait for turn completion using official SDK method
             try:
                 completed_msg = self.client.wait_for_turn_completed(turn_id, timeout=self._rpc_timeout)
             except Exception as e:
                 raise Exception("POST_SEND_AMBIGUITY: Timeout waiting for turn/completed notification")

             if completed_msg.get("params", {}).get("turn", {}).get("status") != "completed":
                  raise Exception("POST_SEND_AMBIGUITY: turn status != completed")

             thread_id = params.get("threadId")
             client_msg_id = params.get("clientUserMessageId")

             try:
                 read_res = self.client.thread_read(threadId=thread_id)
             except Exception as e:
                 raise Exception(f"POST_SEND_AMBIGUITY: thread/read failed: {str(e)}")

             if "result" not in read_res:
                 raise Exception("POST_SEND_AMBIGUITY: missing thread/read result")

             read_thread_id = Parsers.parse_thread_read(read_res)
             if not read_thread_id:
                  raise Exception("POST_SEND_AMBIGUITY: thread/read failed correlation or malformed")

             try:
                 list_res = self.client.request("thread/turns/list", {"itemsView": "full", "threadId": thread_id})
             except Exception as e:
                 raise Exception(f"POST_SEND_AMBIGUITY: thread/turns/list failed: {str(e)}")

             if "result" not in list_res:
                 raise Exception("POST_SEND_AMBIGUITY: missing thread/turns/list result")

             list_turn_id = Parsers.parse_thread_turns_list(list_res)
             if list_turn_id != turn_id:
                  raise Exception("POST_SEND_AMBIGUITY: thread/turns/list failed correlation or malformed")

             if not Parsers.correlate_backend(completed_msg, read_res, list_res, client_msg_id):
                  raise Exception("POST_SEND_AMBIGUITY: clientUserMessageId correlation failed")

        return response

    def shutdown(self):
        if self.client and hasattr(self.client, 'close'):
             try:
                 self.client.close()
             except Exception:
                 pass