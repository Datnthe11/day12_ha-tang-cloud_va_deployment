import logging
from openai import OpenAI
from app.config import settings
from utils.mock_llm import ask as mock_ask

logger = logging.getLogger(__name__)

# Initialize OpenAI client if API key is provided
client = None
if settings.openai_api_key:
    client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """You are a helpful DevOps and Cloud Infrastructure assistant.
You help users understand concepts like Docker, FastAPI, Redis, Cloud Deployment, Rate Limiting, and Cost Guard.
Keep your answers concise, clear, and focused on production-ready engineering practices.
"""

def ask_agent(question: str) -> str:
    """
    Call OpenAI API to answer the user's question.
    If OPENAI_API_KEY is not set, fallback to mock LLM.
    """
    if not client:
        logger.warning("No OPENAI_API_KEY found, falling back to mock LLM.")
        return mock_ask(question)
    
    try:
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return f"Sorry, I encountered an error while processing your request: {str(e)}"
