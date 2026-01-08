from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.llm.client import llm
from app.memory.memory_store import get_history, save_history
from dotenv import load_dotenv
from langfuse import observe
from app.core.observability import score_trace
from app.evals.basic import (
    eval_persona_consistency,
    eval_response_length,
    eval_question_answering,
)
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

GLOBAL_PROMPT = load_prompt(os.getenv("PROMPT_GLOBAL"))
PERSONA_PROMPT = load_prompt(os.getenv("PROMPT_PERSONA_1"))

@observe(name="chat_service")
def chat_service(user_id: str, message: str) -> str:
    history = get_history(user_id)

    messages = [
        SystemMessage(content=GLOBAL_PROMPT),
        SystemMessage(content=PERSONA_PROMPT),
    ] + history + [HumanMessage(content=message)]

    response = llm.invoke(messages)
    response_text = response.content

    # =========================
    # EVALUATIONS (REAL)
    # =========================

    score_trace(
        name="persona_consistency",
        value=eval_persona_consistency(response_text),
        data_type="NUMERIC",
        comment="Checks warmth & feminine tone alignment",
    )

    score_trace(
        name="response_length_ok",
        value=eval_response_length(response_text),
        data_type="BOOLEAN",
        comment="Response length within acceptable range",
    )

    score_trace(
        name="answers_user",
        value=eval_question_answering(message, response_text),
        data_type="BOOLEAN",
        comment="Does the response actually address the user input",
    )

    save_history(
        user_id,
        history + [
            HumanMessage(content=message),
            AIMessage(content=response_text)
        ]
    )

    return response_text
