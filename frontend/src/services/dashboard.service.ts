import { API_ENDPOINTS } from '@/constants/api'
import { http } from '@/services/http'

export interface DashboardActivityEvent {
  id: number
  action: string
  resourceType: string
  patientId: string | null
  isBreakGlass: boolean
  createdAt: string
}

export interface BreakdownRow {
  label: string
  count: number
}

export interface ClinicalDashboardSummary {
  role: 'CLINICIAN' | 'CARE_COORDINATOR'
  patientCount: number
  encountersThisWeek: number
  pendingAiDrafts: number
  openReferrals: number
  recentEvents: DashboardActivityEvent[]
  referralBreakdown: BreakdownRow[]
  encounterBreakdown: BreakdownRow[]
}

export interface ComplianceDashboardSummary {
  role: 'COMPLIANCE_OFFICER'
  eventsToday: number
  breakGlassThisWeek: number
  totalEventsThisWeek: number
  recentEvents: DashboardActivityEvent[]
  actionBreakdown: BreakdownRow[]
}

export type DashboardSummary = ClinicalDashboardSummary | ComplianceDashboardSummary

function mapEvent(raw: any): DashboardActivityEvent {
  return {
    id: raw.id,
    action: raw.action,
    resourceType: raw.resource_type,
    patientId: raw.patient_id,
    isBreakGlass: raw.is_break_glass,
    createdAt: raw.created_at,
  }
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  const response = await http.get(API_ENDPOINTS.dashboardSummary)
  const raw = response.data.data
  const recentEvents = raw.recent_events.map(mapEvent)

  if (raw.role === 'COMPLIANCE_OFFICER') {
    return {
      role: 'COMPLIANCE_OFFICER',
      eventsToday: raw.events_today,
      breakGlassThisWeek: raw.break_glass_this_week,
      totalEventsThisWeek: raw.total_events_this_week,
      recentEvents,
      actionBreakdown: raw.action_breakdown,
    }
  }
  return {
    role: raw.role,
    patientCount: raw.patient_count,
    encountersThisWeek: raw.encounters_this_week,
    pendingAiDrafts: raw.pending_ai_drafts,
    openReferrals: raw.open_referrals,
    recentEvents,
    referralBreakdown: raw.referral_breakdown,
    encounterBreakdown: raw.encounter_breakdown,
  }
}
