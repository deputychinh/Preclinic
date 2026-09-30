"""Strategy pattern for the drafting LLM: `AnthropicProvider` is the real implementation, and a
test/local `providers.py` swap-in is possible without touching services.py or tasks.py."""

from abc import ABC, abstractmethod
from typing import Any, Protocol

import anthropic


class DraftTool(Protocol):
    name: str
    description: str
    input_schema: dict[str, Any]

    def __call__(self, **kwargs: Any) -> Any: ...


class LLMProvider(ABC):
    @abstractmethod
    def draft_note(self, *, system_prompt: str, tools: list[DraftTool]) -> tuple[str, list[dict]]:
        """Returns (draft_text, tool_call_log)."""


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model = model

    def draft_note(self, *, system_prompt: str, tools: list[DraftTool]) -> tuple[str, list[dict]]:
        client = anthropic.Anthropic(api_key=self._api_key)
        tool_specs = [
            {"name": t.name, "description": t.description, "input_schema": t.input_schema} for t in tools
        ]
        tools_by_name = {t.name: t for t in tools}
        tool_call_log: list[dict] = []

        messages: list[dict] = [{"role": "user", "content": "Draft a SOAP note for this encounter."}]
        for _ in range(6):  # bounded agent loop: never let a runaway tool-call chain hang the worker
            # Plain dicts here (not the SDK's exact TypedDict variants) keep this module decoupled
            # from the SDK's type surface — DraftTool is our own Protocol, not the SDK's ToolParam.
            response = client.messages.create(
                model=self._model,
                max_tokens=2000,
                system=system_prompt,
                tools=tool_specs,  # type: ignore[arg-type]
                messages=messages,  # type: ignore[arg-type]
            )
            if response.stop_reason != "tool_use":
                text = "".join(block.text for block in response.content if block.type == "text")
                return text, tool_call_log

            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                tool = tools_by_name[block.name]
                result = tool(**block.input)
                tool_call_log.append({"tool": block.name, "input": block.input})
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": str(result)}
                )
            messages.append({"role": "user", "content": tool_results})

        return "", tool_call_log
