from typing import Dict, List
from langchain_core.messages import BaseMessage

memory_store: Dict[str, List[BaseMessage]] = {}
MAX_MESSAGES = 6

def get_history(user_id: str):
    return memory_store.get(user_id, [])

def save_history(user_id: str, messages: list):
    memory_store[user_id] = messages[-MAX_MESSAGES:]
