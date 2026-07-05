from openai import OpenAI
import json
from config import LLM_PROVIDER, OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, OLLAMA_HOST, OLLAMA_MODEL


def create_client():
    if LLM_PROVIDER == "ollama":
        return OllamaClient(OLLAMA_HOST, OLLAMA_MODEL)
    return OpenAIClient(OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL)


class BaseLLMClient:
    def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        raise NotImplementedError


class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        kwargs = dict(
            model=self.model,
            messages=messages,
            temperature=0.1,
        )
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**kwargs)
        msg = response.choices[0].message

        result = {"content": msg.content}
        if msg.tool_calls:
            result["tool_calls"] = [
                {
                    "id": tc.id,
                    "name": tc.function.name,
                    "arguments": json.loads(tc.function.arguments),
                }
                for tc in msg.tool_calls
            ]
        return result


class OllamaClient(BaseLLMClient):
    def __init__(self, host: str, model: str):
        self.client = OpenAI(base_url=f"{host}/v1", api_key="ollama")
        self.model = model

    def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        kwargs = dict(
            model=self.model,
            messages=messages,
            temperature=0.1,
        )
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**kwargs)
        msg = response.choices[0].message

        result = {"content": msg.content}
        if msg.tool_calls:
            result["tool_calls"] = [
                {
                    "id": tc.id,
                    "name": tc.function.name,
                    "arguments": json.loads(tc.function.arguments),
                }
                for tc in msg.tool_calls
            ]
        return result