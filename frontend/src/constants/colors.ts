// Kept in sync with assets/styles/_tokens.scss by convention (checked in code review, docs/plan.md §9).
import { AIDraftStatus, AuditAction, EncounterStatus, ImportJobStatus, ReferralStatus } from '@/enums'

export const COLORS = {
  primary: '#2f6690',
  secondary: '#16324f',
  accent: '#3a8891',
  success: '#2e9e6c',
  warning: '#d98e04',
  danger: '#c0392b',
  info: '#4a90c4',
} as const

export const ENCOUNTER_STATUS_COLOR: Record<EncounterStatus, string> = {
  [EncounterStatus.DRAFT]: COLORS.warning,
  [EncounterStatus.PENDING_SIGNATURE]: COLORS.info,
  [EncounterStatus.SIGNED]: COLORS.success,
  [EncounterStatus.AMENDED]: COLORS.accent,
}

export const REFERRAL_STATUS_COLOR: Record<ReferralStatus, string> = {
  [ReferralStatus.REQUESTED]: COLORS.warning,
  [ReferralStatus.ACCEPTED]: COLORS.success,
  [ReferralStatus.DECLINED]: COLORS.danger,
  [ReferralStatus.COMPLETED]: COLORS.info,
}

export const IMPORT_JOB_STATUS_COLOR: Record<ImportJobStatus, string> = {
  [ImportJobStatus.PENDING]: COLORS.warning,
  [ImportJobStatus.RUNNING]: COLORS.info,
  [ImportJobStatus.SUCCEEDED]: COLORS.success,
  [ImportJobStatus.FAILED_PARTIAL]: COLORS.danger,
}

export const AI_DRAFT_STATUS_COLOR: Record<AIDraftStatus, string> = {
  [AIDraftStatus.PENDING]: COLORS.warning,
  [AIDraftStatus.READY]: COLORS.info,
  [AIDraftStatus.APPROVED]: COLORS.success,
  [AIDraftStatus.FAILED]: COLORS.danger,
}

export const AUDIT_ACTION_COLOR: Record<AuditAction, string> = {
  [AuditAction.READ]: COLORS.info,
  [AuditAction.CREATE]: COLORS.success,
  [AuditAction.UPDATE]: COLORS.warning,
  [AuditAction.EXPORT]: COLORS.accent,
  [AuditAction.BREAK_GLASS]: COLORS.danger,
}
