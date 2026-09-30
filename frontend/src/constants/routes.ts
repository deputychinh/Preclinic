export const ROUTES = {
  login: '/login',
  patients: '/patients',
  patientDetail: (mrn: string) => `/patients/${mrn}`,
  newEncounter: (mrn: string) => `/patients/${mrn}/encounters/new`,
  encounterDetail: (mrn: string, id: number | string) => `/patients/${mrn}/encounters/${id}`,
  carePlan: (id: number | string) => `/care-plans/${id}`,
  referrals: '/referrals',
  labImports: '/lab-imports',
  audit: '/audit',
} as const
