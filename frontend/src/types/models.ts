import type { AIDraftStatus, ConsentType, EncounterStatus, ImportJobStatus, NoteSource, ReferralStatus, Role } from '@/enums'

export interface CurrentUser {
  id: number
  email: string
  fullName: string
  role: Role
}

export interface PatientListItem {
  id: number
  mrn: string
  fullName: string
  dateOfBirth: string
}

export interface Allergy {
  id: number
  substance: string
  reaction: string
  severity: string
}

export interface Medication {
  id: number
  name: string
  dosage: string
  frequency: string
  active: boolean
}

export interface Consent {
  id: number
  consentType: ConsentType
  grantedAt: string
  revokedAt: string | null
}

export interface PatientDetail {
  id: number
  mrn: string
  fullName: string
  firstName: string
  lastName: string
  dateOfBirth: string
  allergies: Allergy[]
  medications: Medication[]
  consents: Consent[]
}

export interface EncounterNoteVersion {
  id: number
  version: number
  source: NoteSource
  content: string
  signedBy: number | null
  signedAt: string | null
  supersedes: number | null
}

export interface Encounter {
  id: number
  patient: number
  clinician: number
  status: EncounterStatus
  reason: string
  occurredAt: string
  diagnosisCodes: { id: number; code: string; description: string }[]
  noteVersions: EncounterNoteVersion[]
}

export interface AIDraft {
  id: number
  encounter: number
  status: AIDraftStatus
  content: string
  modelName: string
  toolCalls: { tool: string; input: Record<string, unknown> }[]
  error: string
}

export interface Referral {
  id: number
  patient: number
  specialty: string
  reason: string
  status: ReferralStatus
  referringClinician: number
}

export interface LabImportJob {
  id: number
  status: ImportJobStatus
  totalRows: number
  importedRows: number
  errorReport: { row: number; error: string }[]
  createdAt: string
}

export interface AuditEvent {
  id: number
  actorName: string
  actorEmail: string
  action: string
  resourceType: string
  resourceId: string
  patientId: string | null
  reason: string
  isBreakGlass: boolean
  metadata: Record<string, unknown>
  createdAt: string
}

export interface Paginated<T> {
  data: T[]
  meta: { next: string | null; previous: string | null }
}
