import sqlite3
import json

class Ledger:
    def __init__(self, db_path):
        # Default mode with autocommit for general statements, manual for transactions
        self.conn = sqlite3.connect(db_path, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        try:
            self.conn.execute('BEGIN IMMEDIATE')
            with open('schema.sql', 'r') as f:
                self.conn.executescript(f.read())
            self.conn.execute('COMMIT')
        except sqlite3.OperationalError:
            # If the file schema already exists or there is no transaction active just pass
            try:
                self.conn.execute('ROLLBACK')
            except sqlite3.OperationalError:
                pass

    def record_reservation(self, task_id, seq, target_thread, message_type, message_hash, client_user_message_id):
        try:
            self.conn.execute('BEGIN IMMEDIATE')
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO requests (task_id, seq, target_thread, message_type, message_hash, client_user_message_id, state)
                VALUES (?, ?, ?, ?, ?, ?, 'RESERVED')
            """, (task_id, seq, target_thread, message_type, message_hash, client_user_message_id))
            req_id = cur.lastrowid
            self.conn.execute('COMMIT')
            return True, req_id
        except sqlite3.IntegrityError:
            self.conn.execute('ROLLBACK')
            cur = self.conn.cursor()
            cur.execute("""
                SELECT message_hash FROM requests WHERE task_id = ? AND seq = ? AND target_thread = ?
            """, (task_id, seq, target_thread))
            row = cur.fetchone()
            if row and row['message_hash'] != message_hash:
                return False, "MESSAGE_HASH_CONFLICT"
            return False, "DUPLICATE"
        except sqlite3.OperationalError: # Database locked (concurrency test)
             try:
                 self.conn.execute('ROLLBACK')
             except sqlite3.OperationalError:
                 pass
             return False, "DATABASE_LOCKED"

    def record_provenance_info(self, req_id, runner_path, runner_sha256, cwd, config_path, artifact_version):
        self.conn.execute('BEGIN IMMEDIATE')
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE requests SET
            runner_path = ?, runner_sha256 = ?, cwd = ?, config_path = ?, artifact_version = ?
            WHERE id = ?
        """, (runner_path, runner_sha256, cwd, config_path, artifact_version, req_id))
        self.conn.execute('COMMIT')

    def update_state(self, req_id, new_state, **kwargs):
        # Prevent backward transitions
        valid_transitions = {
            'RESERVED': ['PREFLIGHT_OK', 'BLOCKED'],
            'PREFLIGHT_OK': ['SENT', 'BLOCKED', 'FAILED', 'PREPARED'],
            'SENT': ['COMPLETED', 'UNKNOWN'],
            'COMPLETED': ['DELIVERED', 'UNKNOWN']
        }

        self.conn.execute('BEGIN IMMEDIATE')
        cur = self.conn.cursor()
        cur.execute("SELECT state FROM requests WHERE id = ?", (req_id,))
        row = cur.fetchone()
        if not row:
            self.conn.execute('ROLLBACK')
            return False

        current_state = row['state']

        # terminal states cannot be changed
        if current_state in ['DELIVERED', 'UNKNOWN', 'FAILED', 'BLOCKED', 'PREPARED']:
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

        query = f"UPDATE requests SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        cur.execute(query, update_values)
        self.conn.execute('COMMIT')
        return True
