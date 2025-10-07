"""OpenAI client helper for structured outputs."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from openai import OpenAI

from .settings import settings

logger = logging.getLogger(__name__)


class TKPOpenAIClient:
    """Wrapper around OpenAI Responses API for TKP generation."""

    def __init__(self, schema_path: Optional[Path] = None) -> None:
        self._schema_path = schema_path or settings.schema_path
        self._client: Optional[OpenAI] = None
        if settings.openai_api_key:
            self._client = OpenAI(api_key=settings.openai_api_key)
        else:
            logger.warning("OPENAI_API_KEY is not set. Structured completion will be skipped.")

    def _load_schema(self) -> Dict[str, Any]:
        with self._schema_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def collect_structured_data(self, prompt: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Call OpenAI Responses API to extract structured TKP data."""

        if not self._client:
            return {}

        schema = self._load_schema()
        try:
            response = self._client.responses.create(
                model=settings.openai_model,
                input=self._build_prompt(prompt, state),
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "tkp_schema",
                        "schema": schema,
                        "strict": True,
                    },
                },
            )
        except Exception as exc:  # pragma: no cover - network errors not covered
            logger.error("OpenAI structured completion failed: %s", exc)
            return {}

        try:
            content = response.output[0].content[0].text  # type: ignore[attr-defined]
            data = json.loads(content)
            if not isinstance(data, dict):
                raise ValueError("Structured response is not a dictionary")
            return data
        except Exception as exc:  # pragma: no cover
            logger.error("Failed to parse structured response: %s", exc)
            return {}

    @staticmethod
    def _build_prompt(message: str, state: Dict[str, Any]) -> str:
        base_instructions = (
            "Ты помощник по составлению ТКП. На основе сообщения пользователя и текущего "
            "состояния собери недостающие поля. Возвращай только JSON, соответствующий схеме."
        )
        state_json = json.dumps(state, ensure_ascii=False, indent=2)
        return (
            f"{base_instructions}\n\n"  # noqa: E501
            f"Текущее состояние:\n{state_json}\n\n"
            f"Сообщение пользователя:\n{message}"
        )


openai_client = TKPOpenAIClient()
