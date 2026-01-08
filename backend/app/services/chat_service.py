from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.llm.client import llm
from app.memory.redis_store import get_history, save_history
from app.core.observability import langfuse
from dotenv import load_dotenv
import os


load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
PROMPT_DIR = os.path.join(BASE_DIR, "prompts")

def load_prompt(filename: str) -> str:
    path = os.path.join(PROMPT_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

GLOBAL_PROMPT = load_prompt(
    os.getenv("PROMPT_GLOBAL")
)

PERSONA_PROMPT = load_prompt(
    os.getenv("PROMPT_PERSONA_1")
)

def chat_service(user_id: str, message: str) -> str:
    trace = langfuse.trace(
        name="chat",
        user_id=user_id,
        input=message
    )

    history = get_history(user_id)

    messages = [
        SystemMessage(content="GLOBAL PROMPT"),
        SystemMessage(content="PERSONA PROMPT"),
    ] + history + [HumanMessage(content=message)]

    trace.span(
        name="build_prompt",
        input={
            "history": [m.content for m in history],
            "user": message
        }
    )

    response = llm.invoke(messages)

    trace.span(
        name="llm_call",
        output=response.content
    )

    save_history(
        user_id,
        history + [
            HumanMessage(content=message),
            AIMessage(content=response.content)
        ]
    )

    trace.update(output=response.content)

    return response.content
