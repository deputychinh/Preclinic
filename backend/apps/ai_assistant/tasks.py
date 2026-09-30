from celery import shared_task
from django.conf import settings

from apps.ai_assistant.models import AIDraft
from apps.ai_assistant.providers import AnthropicProvider
from apps.ai_assistant.tools import build_read_only_tools
from apps.common.enums import AIDraftStatus

SYSTEM_PROMPT = (
    "You are a clinical documentation assistant. Draft a concise SOAP note for the patient using "
    "only the tools provided. Never invent information not returned by a tool call."
)


@shared_task
def generate_ai_draft(draft_id: int) -> None:
    draft = AIDraft.objects.select_related("encounter__patient").get(id=draft_id)
    provider = AnthropicProvider(api_key=settings.ANTHROPIC_API_KEY, model=settings.ANTHROPIC_MODEL)
    tools = build_read_only_tools(draft.encounter.patient)

    try:
        text, tool_log = provider.draft_note(system_prompt=SYSTEM_PROMPT, tools=tools)
        draft.content = text
        draft.tool_calls = tool_log
        draft.model_name = settings.ANTHROPIC_MODEL
        draft.status = AIDraftStatus.READY if text else AIDraftStatus.FAILED
    except Exception as exc:
        draft.status = AIDraftStatus.FAILED
        draft.error = str(exc)

    draft.save(update_fields=["content", "tool_calls", "model_name", "status", "error"])
