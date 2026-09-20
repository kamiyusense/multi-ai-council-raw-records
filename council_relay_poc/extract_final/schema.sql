-- schema.sql

CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    seq INTEGER NOT NULL,
    source_thread TEXT,
    target_thread TEXT NOT NULL,
    message_type TEXT NOT NULL,
    message_hash TEXT NOT NULL,
    client_user_message_id TEXT NOT NULL,
    state TEXT NOT NULL,
    target_turn_id TEXT,
    receipt TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    error_code TEXT,
    error_detail TEXT,
    recovery_required BOOLEAN DEFAULT 0,
    recovery_reason TEXT,
    runner_path TEXT,
    runner_sha256 TEXT,
    cwd TEXT,
    config_path TEXT,
    artifact_version TEXT,
    request_sha256 TEXT,
    transport_mode TEXT,

    UNIQUE(task_id, seq, target_thread)
);
