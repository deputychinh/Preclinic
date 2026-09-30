export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

export const API_ENDPOINTS = {
  login: '/auth/login',
  refresh: '/auth/refresh',
  me: '/auth/me',
  patients: '/patients',
  patient: (id: number | string) => `/patients/${id}`,
  encounters: '/encounters',
  encounter: (id: number | string) => `/encounters/${id}`,
  signEncounterNote: (id: number | string) => `/encounters/${id}/sign`,
  aiDraftRequest: (encounterId: number | string) => `/encounters/${encounterId}/ai-drafts`,
  aiDraft: (id: number | string) => `/ai-drafts/${id}`,
  aiDraftApprove: (id: number | string) => `/ai-drafts/${id}/approve`,
  carePlans: '/care-plans',
  referrals: '/referrals',
  labImports: '/lab-imports',
  labImport: (id: number | string) => `/lab-imports/${id}`,
  auditEvents: '/audit-events',
  health: '/health',
  dashboardSummary: '/dashboard/summary',
} as const
