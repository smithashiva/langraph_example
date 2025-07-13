# history_store.py

import boto3
import time
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb", region_name="your-region")  # e.g., "us-east-1"
table = dynamodb.Table("conversation_history")

class HistoryStore:
    def get_user_history(self, user_id: str) -> list:
        response = table.query(
            KeyConditionExpression=Key("user_id").eq(user_id),
            ScanIndexForward=True
        )
        return [{"role": item["role"], "content": item["content"]} for item in response.get("Items", [])]

    def append_user_message(self, user_id: str, role: str, content: str):
        table.put_item(Item={
            "user_id": user_id,
            "timestamp": int(time.time() * 1000),
            "role": role,
            "content": content
        })
