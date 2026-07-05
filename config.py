import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5")

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", BASE_DIR / "output"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_TOOL_CALLS = int(os.getenv("MAX_TOOL_CALLS", "10"))