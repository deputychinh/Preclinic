import { API_ENDPOINTS } from '@/constants/api'
import { http } from '@/services/http'
import type { Encounter, EncounterNoteVersion } from '@/types/models'

function mapNoteVersion(raw: any): EncounterNoteVersion {
  return {
    id: raw.id,
    version: raw.version,
    source: raw.source,
    content: raw.content,
    signedBy: raw.signed_by,
    signedAt: raw.signed_at,
    supersedes: raw.supersedes,
  }
}

function mapEncounter(raw: any): Encounter {
  return {
    id: raw.id,
    patient: raw.patient,
    clinician: raw.clinician,
    status: raw.status,
    reason: raw.reason,
    occurredAt: raw.occurred_at,
    diagnosisCodes: raw.diagnosis_codes,
    noteVersions: raw.note_versions.map(mapNoteVersion),
  }
}

export async function createEncounter(patientId: number, reason: string, occurredAt: string): Promise<Encounter> {
  const response = await http.post(API_ENDPOINTS.encounters, { patient: patientId, reason, occurred_at: occurredAt })
  return mapEncounter(response.data.data)
}

export async function getEncounter(id: number | string): Promise<Encounter> {
  const response = await http.get(API_ENDPOINTS.encounter(id))
  return mapEncounter(response.data.data)
}

export async function signEncounterNote(encounterId: number | string, noteId: number): Promise<EncounterNoteVersion> {
  const response = await http.post(API_ENDPOINTS.signEncounterNote(encounterId), { note_id: noteId })
  return mapNoteVersion(response.data.data)
}
