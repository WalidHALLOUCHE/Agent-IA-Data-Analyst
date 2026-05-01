"""Comportement commun des agents alimentés par LLM."""

from __future__ import annotations

from agents.llm_client import LLMClient


class BaseAIAgent:
    name = "BaseAIAgent"
    role = "Agent IA"

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client or LLMClient()
        self.last_used_ai = False
        self.last_error: str | None = None

    def _generate(
        self,
        system_prompt: str,
        user_prompt: str,
        fallback: str,
        temperature: float = 0.2,
        max_tokens: int = 900,
    ) -> str:
        response = self.llm_client.complete(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        self.last_used_ai = response.used_ai
        self.last_error = response.error
        return response.content if response.used_ai and response.content else fallback

    def status(self) -> dict[str, str | bool | None]:
        return {
            "name": self.name,
            "role": self.role,
            "used_ai": self.last_used_ai,
            "error": self.last_error,
        }
