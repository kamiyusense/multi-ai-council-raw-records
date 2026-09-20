import sqlite3
import json

class Ledger:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, isolation_level=None)
        # Apply standard schema statically for POC
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY,
                task_id TEXT,
                seq INTEGER,
                target_thread TEXT,
                message_type TEXT,
                state TEXT,
                client_user_message_id TEXT,
                error_code TEXT,
                error_detail TEXT,
                runner_path TEXT,
                runner_sha256 TEXT,
                cwd TEXT,
                config_path TEXT,
                artifact_version TEXT,
                request_sha256 TEXT,
                transport_mode TEXT,
                target_turn_id TEXT,
                receipt TEXT,
                recovery_required BOOLEAN,
                recovery_reason TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE UNIQUE INDEX IF NOT EXISTS idx_task_seq_thread
            ON requests(task_id, seq, target_thread);
        """)

    def begin_immediate(self):
        self.conn.execute('BEGIN IMMEDIATE')

    def insert_request(self, task_id, seq, thread, msg_type, state, **kwargs):
        fields = ["task_id", "seq", "target_thread", "message_type", "state"]
        values = [task_id, seq, thread, msg_type, state]

        for k, v in kwargs.items():
            fields.append(k)
            values.append(v)

        placeholders = ",".join(["?" for _ in fields])
        query = f"INSERT INTO requests ({','.join(fields)}) VALUES ({placeholders})"

        try:
            self.begin_immediate()
            cur = self.conn.cursor()
            cur.execute(query, values)
            req_id = cur.lastrowid
            self.conn.execute('COMMIT')
            return req_id
        except sqlite3.IntegrityError:
            self.conn.execute('ROLLBACK')
            raise ValueError("DUPLICATE_OR_CONFLICT")

    def update_state(self, req_id, new_state, **kwargs):
        valid_transitions = {
            'RESERVED': ['PREFLIGHT_OK', 'BLOCKED', 'UNKNOWN'],
            'PREFLIGHT_OK': ['SENT', 'PREPARED', 'BLOCKED', 'UNKNOWN'],
            'SENT': ['COMPLETED', 'UNKNOWN', 'FAILED', 'DRY_RUN_COMPLETED', 'SIMULATED_DELIVERED'],
            'COMPLETED': ['DELIVERED', 'UNKNOWN']
        }

        # Enforce that DELIVERED can ONLY be reached from COMPLETED (which requires verified live correlation)
        # DRY_RUN_COMPLETED and SIMULATED_DELIVERED are terminal simulated states

        self.conn.execute('BEGIN IMMEDIATE')
        cur = self.conn.cursor()
        cur.execute("SELECT state, transport_mode FROM requests WHERE id = ?", (req_id,))
        row = cur.fetchone()
        if not row:
            self.conn.execute('ROLLBACK')
            return False

        current_state, mode = row[0], row[1]

        # Safety constraint: Only real live mode can reach DELIVERED
        if new_state == 'DELIVERED' and mode != 'live':
             self.conn.execute('ROLLBACK')
             raise Exception(f"CRITICAL: mode '{mode}' cannot reach real DELIVERED state")

        # terminal states cannot be changed
        terminal_states = ['DELIVERED', 'UNKNOWN', 'FAILED', 'BLOCKED', 'PREPARED', 'DRY_RUN_COMPLETED', 'SIMULATED_DELIVERED']
        if current_state in terminal_states:
            self.conn.execute('ROLLBACK')
            return False

        if new_state not in valid_transitions.get(current_state, []):
            if new_state not in ['UNKNOWN', 'FAILED', 'BLOCKED']:
                self.conn.execute('ROLLBACK')
                return False

        update_fields = ["state = ?"]
        update_values = [new_state]

        for k, v in kwargs.items():
            update_fields.append(f"{k} = ?")
            update_values.append(v)

        update_values.append(req_id)

        query = f"UPDATE requests SET {', '.join(update_fields)}, updated_at=CURRENT_TIMESTAMP WHERE id = ?"
        cur.execute(query, update_values)
        self.conn.execute('COMMIT')
        return True

    def record_reservation(self, task_id, seq, thread, msg_type, msg_hash, client_msg_id):
        # Insert RESERVED record
        try:
            req_id = self.insert_request(
                task_id, seq, thread, msg_type, "RESERVED",
                request_sha256=msg_hash,
                client_user_message_id=client_msg_id
            )
            return True, req_id
        except ValueError as e:
            if str(e) == "DUPLICATE_OR_CONFLICT":
                # Check if hash matches
                cur = self.conn.cursor()
                cur.execute("SELECT request_sha256 FROM requests WHERE task_id = ? AND seq = ? AND target_thread = ?", (task_id, seq, thread))
                row = cur.fetchone()
                if row and row[0] == msg_hash:
                    return False, "DUPLICATE_NO_NEW_SEND"
                else:
                    return False, "MESSAGE_HASH_CONFLICT"
            return False, str(e)

    def record_provenance_info(self, req_id, runner_path, runner_sha256, cwd, config_path, artifact_version):
        self.conn.execute('BEGIN IMMEDIATE')
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE requests SET
                runner_path = ?,
                runner_sha256 = ?,
                cwd = ?,
                config_path = ?,
                artifact_version = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (runner_path, runner_sha256, cwd, config_path, artifact_version, req_id))
        self.conn.execute('COMMIT')
