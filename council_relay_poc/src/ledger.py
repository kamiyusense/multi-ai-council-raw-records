import sqlite3
import json

class Ledger:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        with open('schema.sql', 'r') as f:
            self.conn.executescript(f.read())

    def record_reservation(self, task_id, seq, target_thread, message_type, message_hash, client_user_message_id):
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO requests (task_id, seq, target_thread, message_type, message_hash, client_user_message_id, state)
                VALUES (?, ?, ?, ?, ?, ?, 'RESERVED')
            """, (task_id, seq, target_thread, message_type, message_hash, client_user_message_id))
            self.conn.commit()
            return True, cur.lastrowid
        except sqlite3.IntegrityError:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT message_hash FROM requests WHERE task_id = ? AND seq = ? AND target_thread = ?
            """, (task_id, seq, target_thread))
            row = cur.fetchone()
            if row and row['message_hash'] != message_hash:
                return False, "MESSAGE_HASH_CONFLICT"
            return False, "DUPLICATE"

    def update_state(self, req_id, new_state, **kwargs):
        # Prevent backward transitions
        valid_transitions = {
            'RESERVED': ['PREFLIGHT_OK', 'BLOCKED'],
            'PREFLIGHT_OK': ['SENT', 'BLOCKED', 'FAILED'],
            'SENT': ['COMPLETED', 'UNKNOWN'],
            'COMPLETED': ['DELIVERED', 'UNKNOWN']
        }

        cur = self.conn.cursor()
        cur.execute("SELECT state FROM requests WHERE id = ?", (req_id,))
        row = cur.fetchone()
        if not row:
            return False

        current_state = row['state']

        # terminal states cannot be changed
        if current_state in ['DELIVERED', 'UNKNOWN', 'FAILED', 'BLOCKED']:
            return False

        if new_state not in valid_transitions.get(current_state, []):
             if new_state not in ['UNKNOWN', 'FAILED', 'BLOCKED']:
                 return False

        update_fields = ["state = ?"]
        update_values = [new_state]

        for k, v in kwargs.items():
            update_fields.append(f"{k} = ?")
            update_values.append(v)

        update_values.append(req_id)

        query = f"UPDATE requests SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        cur.execute(query, update_values)
        self.conn.commit()
        return True


    def record_provenance_info(self, req_id, runner_path, runner_sha256, cwd, config_path, artifact_version):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE requests SET
            runner_path = ?, runner_sha256 = ?, cwd = ?, config_path = ?, artifact_version = ?
            WHERE id = ?
        """, (runner_path, runner_sha256, cwd, config_path, artifact_version, req_id))
        self.conn.commit()
