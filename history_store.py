import time
import psycopg2
from psycopg2.extras import Json
import uuid
from datetime import datetime

class HistoryStore:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="finagent.cfm8ykkm0s84.ap-south-1.rds.amazonaws.com",
            dbname="postgres",
            user="postgres",
            password="Capstone2025$"
        )

    def get_user_history(self, user_id: str) -> list:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT state
                FROM agent.langgraph_sessions
                WHERE user_id = %s AND is_active = TRUE
                ORDER BY last_accessed_at DESC
                LIMIT 1
            """, (user_id,))
            row = cur.fetchone()
            if row:
                print(f"Fetched user_id: {user_id} history: {row[0].get('history', [])}")

                return row[0].get("history", [])
            return []
        

    # def get_user_history_old(self, user_id: str) -> list:
    #     response = table.query(
    #         KeyConditionExpression=Key("user_id").eq(user_id),
    #         ScanIndexForward=True
    #     )
    #     return [{"role": item["role"], "content": item["content"]} for item in response.get("Items", [])]

    def insert_new_session(self, user_id: str, state: dict, metadata: dict = None):
        with self.conn.cursor() as cur:
            session_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO agent.langgraph_sessions (
                    session_id, user_id, session_name, state, metadata,
                    is_active, created_at, last_accessed_at
                )
                VALUES (%s, %s, %s, %s, %s, TRUE, %s, %s)
            """, (
                session_id,
                user_id,
                "default_session",
                Json(state),
                Json(metadata or {}),
                datetime.utcnow(),
                datetime.utcnow()
            ))
            self.conn.commit()
            print(f"[DB] New session inserted for user {user_id}")


    
    # Append a new message to the user's history for storage
    def append_user_message(self, user_id: str, role: str, content: str):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT session_id, state
                FROM agent.langgraph_sessions
                WHERE user_id = %s AND is_active = TRUE
                ORDER BY last_accessed_at DESC
                LIMIT 1
            """, (user_id,))
            result = cur.fetchone()
            print(f"[DB] append_user_message: Retrieved session for {user_id}: {result}")

            if result:
                session_id, state = result
                history = state.get("history", [])
                history.append({
                    "id": str(uuid.uuid4()),
                    "role": role,
                    "content": content,
                    "timestamp": datetime.utcnow().isoformat()
                })
                state["history"] = history

                cur.execute("""
                    UPDATE agent.langgraph_sessions
                    SET state = %s,
                        last_accessed_at = %s
                    WHERE session_id = %s
                """, (Json(state), datetime.utcnow(), session_id))
                print(f"[DB] Updated session {session_id} with new message.")
                self.conn.commit()
                return True
            else:
                print(f"[DB] No active session found for user {user_id}. Cannot append message.")
                return False

    def update_session_state(self, user_id: str, state: dict):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT session_id
                FROM agent.langgraph_sessions
                WHERE user_id = %s AND is_active = TRUE
                ORDER BY last_accessed_at DESC
                LIMIT 1
            """, (user_id,))
            result = cur.fetchone()

            if result:
                session_id = result[0]
                cur.execute("""
                    UPDATE agent.langgraph_sessions
                    SET state = %s,
                        last_accessed_at = %s
                    WHERE session_id = %s
                """, (Json(state), datetime.utcnow(), session_id))
                self.conn.commit()
