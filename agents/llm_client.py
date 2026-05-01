"""Client LLM léger utilisé par les agents IA.

Le pipeline analytique doit fonctionner sans clé API. Quand aucune clé
n'est configurée, les agents retournent des réponses déterministes.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any

from dotenv import load_dotenv


@dataclass(frozen=True)
class LLMResponse:
    content: str
    used_ai: bool
    error: str | None = None


class LLMClient:
    """OpenAI-backed text generation with graceful fallback behavior."""

    def __init__(
        self,
        provider: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        enabled: bool | None = None,
    ) -> None:
        load_dotenv()
        self.provider = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        env_enabled = os.getenv("ENABLE_AI_AGENTS", "true").lower() in {"1", "true", "yes"}
        self.enabled = env_enabled if enabled is None else enabled

    @property
    def is_available(self) -> bool:
        return self.enabled and self.provider == "openai" and bool(self.api_key)

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 900,
    ) -> LLMResponse:
        if not self.enabled:
            return LLMResponse("", used_ai=False, error="Les agents IA sont désactivés.")
        if self.provider != "openai":
            return LLMResponse("", used_ai=False, error=f"Provider non supporté : {self.provider}")
        if not self.api_key:
            return LLMResponse("", used_ai=False, error="OPENAI_API_KEY n'est pas configurée.")

        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)
            response: Any = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = response.choices[0].message.content or ""
            return LLMResponse(content.strip(), used_ai=True)
        except Exception as exc:  # pragma: no cover - network/provider errors vary
            return LLMResponse("", used_ai=False, error=str(exc))
