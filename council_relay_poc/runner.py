import argparse
import hashlib
import json
import os
import sys

from src.ledger import Ledger
from src.validator import check_overrides
from src.parser import Parsers
from src.transport.mock import MockTransport
from src.transport.dry_run import DryRunTransport
from src.transport.prepare_live import PrepareLiveTransport
from src.transport.live import LiveTransport

def get_file_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def canonical_json(data):
    return json.dumps(data, separators=(',', ':'), sort_keys=True, ensure_ascii=False).encode('utf-8')

class Runner:
    def __init__(self, config_path, transport_mode, live_flag=False):
        self.config_path = config_path
        self.transport_mode = transport_mode
        self.live_flag = live_flag

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.ledger = Ledger(self.config['db_path'])

        self.runner_path = os.path.abspath(__file__)
        self.runner_sha256 = get_file_sha256(self.runner_path)
        self.cwd = os.getcwd()
        self.artifact_version = self.config.get('artifact_version', 'unknown')

    def check_provenance(self):
        if self.runner_path != self.config['runner_expected_path']:
            return False, "RUNNER_INTEGRITY_MISMATCH"
        if self.runner_sha256 != self.config['runner_expected_sha256']:
            return False, "RUNNER_INTEGRITY_MISMATCH"
        return True, None

    def execute(self, payload, task_id, seq, target_thread):
        # 1. Provenance
        prov_ok, prov_err = self.check_provenance()
        if not prov_ok:
            return "BLOCKED", prov_err

        # 2. Live Gates
        if self.live_flag or self.transport_mode == "live":
            if not self.config.get("live_enabled", False):
                return "BLOCKED", "LIVE_DISABLED"
            if not prov_ok:
                return "BLOCKED", prov_err
            if target_thread not in self.config.get("target_allowlist", []):
                return "BLOCKED", "TARGET_NOT_ALLOWED"
            if not self.config.get("metadata_pass", True):
                return "BLOCKED", "METADATA_MISMATCH"
            if self.config.get("busy", False):
                return "BLOCKED", "BUSY"

            # Since live is strictly prohibited in this POC:
            return "BLOCKED", "LIVE_EXECUTION_PROHIBITED_IN_POC"

        # Approval fail-closed
        if payload.get("method") == "approval/request" or "approval" in payload.get("method", ""):
            return "BLOCKED", "APPROVAL_FAIL_CLOSED"

        # Canonicalize and hash
        canonical_payload = canonical_json(payload)
        payload_hash = hashlib.sha256(canonical_payload).hexdigest()

        client_msg_id = payload.get("params", {}).get("clientUserMessageId", "unknown")

        # 3. Reservation
        res_ok, res_detail = self.ledger.record_reservation(
            task_id, seq, target_thread, payload.get("method", "unknown"), payload_hash, client_msg_id
        )

        if not res_ok:
            if res_detail == "MESSAGE_HASH_CONFLICT":
                return "BLOCKED", "MESSAGE_HASH_CONFLICT"
            return "DUPLICATE", "ALREADY_PROCESSED"

        req_id = res_detail

        # Log provenance
        self.ledger.record_provenance_info(
            req_id, self.runner_path, self.runner_sha256, self.cwd, self.config_path, self.artifact_version
        )

        # 4. Preflight Check
        valid, err = check_overrides(payload)
        if not valid:
            self.ledger.update_state(req_id, "BLOCKED", error_code=err)
            return "BLOCKED", err

        if self.config.get("preflight_fail", False):
             self.ledger.update_state(req_id, "BLOCKED", error_code="PREFLIGHT_FAIL")
             return "BLOCKED", "PREFLIGHT_FAIL"

        self.ledger.update_state(req_id, "PREFLIGHT_OK", request_sha256=payload_hash)

        # 5. Transport setup & execution
        if self.transport_mode == "mock":
            transport = MockTransport()
        elif self.transport_mode == "dry-run":
            transport = DryRunTransport()
        elif self.transport_mode == "prepare-live":
            transport = PrepareLiveTransport()
            # prepare-live stops here
            return "PREPARED", "PREPARE_LIVE_SUCCESS"
        else:
            self.ledger.update_state(req_id, "BLOCKED", error_code="INVALID_TRANSPORT")
            return "BLOCKED", "INVALID_TRANSPORT"

        # In mock/dry-run, we simulate SEND and COMPLETED
        self.ledger.update_state(req_id, "SENT", transport_mode=self.transport_mode)

        if self.config.get("crash_after_send", False):
            # simulate crash, no retry, lands in UNKNOWN
            return "UNKNOWN", "CRASH_AFTER_SEND"

        try:
            res = transport.send(payload)
        except Exception as e:
            self.ledger.update_state(req_id, "UNKNOWN", error_code="SEND_EXCEPTION")
            return "UNKNOWN", str(e)

        # Verify readback correlation simulation for DELIVERED state
        if self.transport_mode == "mock":
            if self.config.get("mock_backend_readback_fail", False):
                 self.ledger.update_state(req_id, "UNKNOWN", error_code="READBACK_FAIL")
                 return "UNKNOWN", "READBACK_FAIL"

        self.ledger.update_state(req_id, "COMPLETED")
        self.ledger.update_state(req_id, "DELIVERED", receipt=json.dumps(res))

        return "DELIVERED", "SUCCESS"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--mode", choices=["mock", "dry-run", "prepare-live", "live"], default="mock")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--payload", required=True, help="JSON string of payload")
    parser.add_argument("--task_id", required=True)
    parser.add_argument("--seq", type=int, required=True)
    parser.add_argument("--target_thread", required=True)

    args = parser.parse_args()

    payload = json.loads(args.payload)

    runner = Runner(args.config, args.mode, args.live)
    status, detail = runner.execute(payload, args.task_id, args.seq, args.target_thread)

    print(json.dumps({"status": status, "detail": detail}))
