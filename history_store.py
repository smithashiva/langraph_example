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
                FROM langgraph_sessions
                WHERE user_id = %s AND is_active = TRUE
                ORDER BY last_accessed_at DESC
                LIMIT 1
            """, (user_id,))
            row = cur.fetchone()
            if row:
                return row[0].get("history", [])
            return []
        

    # def get_user_history_old(self, user_id: str) -> list:
    #     response = table.query(
    #         KeyConditionExpression=Key("user_id").eq(user_id),
    #         ScanIndexForward=True
    #     )
    #     return [{"role": item["role"], "content": item["content"]} for item in response.get("Items", [])]



    

    def append_user_message(self, user_id: str, role: str, content: str):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT session_id, state
                FROM langgraph_sessions
                WHERE user_id = %s AND is_active = TRUE
                ORDER BY last_accessed_at DESC
                LIMIT 1
            """, (user_id,))
            result = cur.fetchone()

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
                    UPDATE langgraph_sessions
                    SET state = %s,
                        last_accessed_at = %s
                    WHERE session_id = %s
                """, (Json(state), datetime.utcnow(), session_id))
                self.conn.commit()

    def update_session_state(self, user_id: str, state: dict):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT session_id
                FROM langgraph_sessions
                WHERE user_id = %s AND is_active = TRUE
                ORDER BY last_accessed_at DESC
                LIMIT 1
            """, (user_id,))
            result = cur.fetchone()

            if result:
                session_id = result[0]
                cur.execute("""
                    UPDATE langgraph_sessions
                    SET state = %s,
                        last_accessed_at = %s
                    WHERE session_id = %s
                """, (Json(state), datetime.utcnow(), session_id))
                self.conn.commit()
