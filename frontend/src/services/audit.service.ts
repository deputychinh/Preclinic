import { API_ENDPOINTS } from '@/constants/api'
import { http } from '@/services/http'
import type { AuditEvent, Paginated } from '@/types/models'

function mapEvent(raw: any): AuditEvent {
  return {
    id: raw.id,
    actorName: raw.actor_name,
    actorEmail: raw.actor_email,
    action: raw.action,
    resourceType: raw.resource_type,
    resourceId: raw.resource_id,
    patientId: raw.patient_id,
    reason: raw.reason,
    isBreakGlass: raw.is_break_glass,
    metadata: raw.metadata,
    createdAt: raw.created_at,
  }
}

export async function searchAuditEvents(filters: {
  patientId?: string
  actorId?: string
  action?: string
  breakGlassOnly?: boolean
  cursor?: string
}): Promise<Paginated<AuditEvent>> {
  const response = await http.get(API_ENDPOINTS.auditEvents, {
    params: {
      patient_id: filters.patientId,
      actor_id: filters.actorId,
      action: filters.action,
      break_glass_only: filters.breakGlassOnly || undefined,
      cursor: filters.cursor,
    },
  })
  return { data: response.data.data.map(mapEvent), meta: response.data.meta }
}
