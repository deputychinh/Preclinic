// Mirrors backend/apps/common/enums.py. Kept hand-written for now (small, stable set); a future
// pass can generate this from the OpenAPI schema the same way types/api.generated.ts is generated.

export enum Role {
  CLINICIAN = 'CLINICIAN',
  CARE_COORDINATOR = 'CARE_COORDINATOR',
  COMPLIANCE_OFFICER = 'COMPLIANCE_OFFICER',
}

export const ROLE_LABEL: Record<Role, string> = {
  [Role.CLINICIAN]: 'Clinician',
  [Role.CARE_COORDINATOR]: 'Care Coordinator',
  [Role.COMPLIANCE_OFFICER]: 'Compliance Officer',
}

export enum EncounterStatus {
  DRAFT = 'DRAFT',
  PENDING_SIGNATURE = 'PENDING_SIGNATURE',
  SIGNED = 'SIGNED',
  AMENDED = 'AMENDED',
}

export const ENCOUNTER_STATUS_LABEL: Record<EncounterStatus, string> = {
  [EncounterStatus.DRAFT]: 'Draft',
  [EncounterStatus.PENDING_SIGNATURE]: 'Pending Signature',
  [EncounterStatus.SIGNED]: 'Signed',
  [EncounterStatus.AMENDED]: 'Amended',
}

export enum NoteSource {
  CLINICIAN = 'CLINICIAN',
  AI_DRAFT = 'AI_DRAFT',
}

export enum ReferralStatus {
  REQUESTED = 'REQUESTED',
  ACCEPTED = 'ACCEPTED',
  DECLINED = 'DECLINED',
  COMPLETED = 'COMPLETED',
}

export const REFERRAL_STATUS_LABEL: Record<ReferralStatus, string> = {
  [ReferralStatus.REQUESTED]: 'Requested',
  [ReferralStatus.ACCEPTED]: 'Accepted',
  [ReferralStatus.DECLINED]: 'Declined',
  [ReferralStatus.COMPLETED]: 'Completed',
}

export enum ConsentType {
  TREATMENT = 'TREATMENT',
  DATA_SHARING = 'DATA_SHARING',
  RESEARCH = 'RESEARCH',
}

export enum ImportJobStatus {
  PENDING = 'PENDING',
  RUNNING = 'RUNNING',
  SUCCEEDED = 'SUCCEEDED',
  FAILED_PARTIAL = 'FAILED_PARTIAL',
}

export enum AuditAction {
  READ = 'READ',
  CREATE = 'CREATE',
  UPDATE = 'UPDATE',
  EXPORT = 'EXPORT',
  BREAK_GLASS = 'BREAK_GLASS',
}

export const AUDIT_ACTION_LABEL: Record<AuditAction, string> = {
  [AuditAction.READ]: 'Read',
  [AuditAction.CREATE]: 'Create',
  [AuditAction.UPDATE]: 'Update',
  [AuditAction.EXPORT]: 'Export',
  [AuditAction.BREAK_GLASS]: 'Break-glass',
}

export enum AIDraftStatus {
  PENDING = 'PENDING',
  READY = 'READY',
  APPROVED = 'APPROVED',
  FAILED = 'FAILED',
}
