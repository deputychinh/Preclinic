import { API_ENDPOINTS } from '@/constants/api'
import { http } from '@/services/http'
import type { Paginated, PatientDetail, PatientListItem } from '@/types/models'

function mapListItem(raw: any): PatientListItem {
  return { id: raw.id, mrn: raw.mrn, fullName: raw.full_name, dateOfBirth: raw.date_of_birth }
}

function mapDetail(raw: any): PatientDetail {
  return {
    id: raw.id,
    mrn: raw.mrn,
    fullName: raw.full_name,
    firstName: raw.first_name,
    lastName: raw.last_name,
    dateOfBirth: raw.date_of_birth,
    allergies: raw.allergies.map((a: any) => ({ id: a.id, substance: a.substance, reaction: a.reaction, severity: a.severity })),
    medications: raw.medications.map((m: any) => ({ id: m.id, name: m.name, dosage: m.dosage, frequency: m.frequency, active: m.active })),
    consents: raw.consents.map((c: any) => ({ id: c.id, consentType: c.consent_type, grantedAt: c.granted_at, revokedAt: c.revoked_at })),
  }
}

export async function searchPatients(query: string, cursor?: string): Promise<Paginated<PatientListItem>> {
  const response = await http.get(API_ENDPOINTS.patients, { params: { q: query || undefined, cursor } })
  return { data: response.data.data.map(mapListItem), meta: response.data.meta }
}

export async function getPatient(id: number | string, breakGlassReason?: string): Promise<PatientDetail> {
  const response = await http.get(API_ENDPOINTS.patient(id), {
    params: breakGlassReason ? { break_glass_reason: breakGlassReason } : undefined,
  })
  return mapDetail(response.data.data)
}
