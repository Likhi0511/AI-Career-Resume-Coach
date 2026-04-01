from sqlalchemy import text
from app.db.postgres import engine

def create_table():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                session_id TEXT,
                role TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))

def save_message(session_id, role, message):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO chat_history (session_id, role, message)
            VALUES (:session_id, :role, :message)
        """), {
            "session_id": session_id,
            "role": role,
            "message": message
        })

def get_history(session_id):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT role, message FROM chat_history
            WHERE session_id = :session_id
            ORDER BY created_at
        """), {"session_id": session_id})

        return result.fetchall()
