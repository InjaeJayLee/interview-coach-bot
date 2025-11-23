import os
from typing import Literal, Any

from dotenv import load_dotenv


load_dotenv()

ProviderName = Literal["openai", "anthropic"]

LLM_PROVIDER: ProviderName = os.getenv("LLM_PROVIDER", "openai").lower()


class LLMClient:
    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> str:
        raise NotImplementedError


class OpenAILLMClient(LLMClient):
    def __init__(self) -> None:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 2500,
        **kwargs: Any,
    ) -> str:
        params: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            **kwargs,
        }

        if self.model.startswith("gpt-5"):
            params.pop("temperature", None)
            params["max_completion_tokens"] = max_tokens
        else:
            params["max_tokens"] = max_tokens

        resp = self.client.chat.completions.create(**params)
        return resp.choices[0].message.content or ""


class AnthropicLLMClient(LLMClient):
    def __init__(self) -> None:
        from anthropic import Anthropic
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set.")
        self.client = Anthropic(api_key=api_key)
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")

    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 2500,
        **kwargs: Any,
    ) -> str:
        system_prompts = []
        content_blocks: list[dict[str, str]] = []

        for m in messages:
            role = m["role"]
            content = m["content"]
            if role == "system":
                system_prompts.append(content)
            elif role in ("user", "assistant"):
                content_blocks.append({"type": "text", "text": content})
        system_prompt = "\n\n".join(system_prompts) if system_prompts else None

        resp = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or None,
            messages=[
                {
                    "role": "user",
                    "content": content_blocks,
                }
            ],
        )

        parts = resp.content
        texts = [p.text for p in parts if getattr(p, "type", "") == "text"]
        return "\n".join(texts).strip()


def _create_llm() -> LLMClient:
    if LLM_PROVIDER == "openai":
        return OpenAILLMClient()
    elif LLM_PROVIDER == "anthropic":
        return AnthropicLLMClient()
    else:
        raise ValueError(f"지원하지 않는 LLM_PROVIDER: {LLM_PROVIDER}")


llm: LLMClient = _create_llm()
