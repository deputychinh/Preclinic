import { API_ENDPOINTS } from '@/constants/api'
import { http } from '@/services/http'
import type { Paginated, Referral } from '@/types/models'

function mapReferral(raw: any): Referral {
  return {
    id: raw.id,
    patient: raw.patient,
    specialty: raw.specialty,
    reason: raw.reason,
    status: raw.status,
    referringClinician: raw.referring_clinician,
  }
}

export async function listReferrals(patientId?: number | string): Promise<Paginated<Referral>> {
  const response = await http.get(API_ENDPOINTS.referrals, { params: { patient_id: patientId || undefined } })
  return { data: response.data.data.map(mapReferral), meta: response.data.meta }
}

export async function createReferral(patientId: number, specialty: string, reason: string): Promise<Referral> {
  const response = await http.post(API_ENDPOINTS.referrals, { patient: patientId, specialty, reason })
  return mapReferral(response.data.data)
}
