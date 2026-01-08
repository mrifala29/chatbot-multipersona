from langchain_openai import ChatOpenAI
from app.core.config import OPENROUTER_API_KEY

llm = ChatOpenAI(
    model="qwen/qwen3-vl-8b-instruct",
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.5,
    max_tokens=100,
    extra_body={
        "provider": {
            "order": ["alibaba"]
        }
    }
)
