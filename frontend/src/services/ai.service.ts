import { API_ENDPOINTS } from '@/constants/api'
import { http } from '@/services/http'
import type { AIDraft } from '@/types/models'

function mapDraft(raw: any): AIDraft {
  return {
    id: raw.id,
    encounter: raw.encounter,
    status: raw.status,
    content: raw.content,
    modelName: raw.model_name,
    toolCalls: raw.tool_calls,
    error: raw.error,
  }
}

export async function requestAiDraft(encounterId: number | string): Promise<AIDraft> {
  const response = await http.post(API_ENDPOINTS.aiDraftRequest(encounterId))
  return mapDraft(response.data.data)
}

export async function getAiDraft(id: number | string): Promise<AIDraft> {
  const response = await http.get(API_ENDPOINTS.aiDraft(id))
  return mapDraft(response.data.data)
}

export async function approveAiDraft(id: number | string) {
  const response = await http.post(API_ENDPOINTS.aiDraftApprove(id))
  return response.data.data
}
