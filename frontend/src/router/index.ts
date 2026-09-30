import { createRouter, createWebHistory } from 'vue-router'

import { Role } from '@/enums'
import { requireAuth, requireRole } from '@/router/guards'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue') },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      beforeEnter: requireAuth,
    },
    {
      path: '/patients',
      name: 'patients',
      component: () => import('@/views/PatientRosterView.vue'),
      beforeEnter: requireAuth,
    },
    {
      path: '/patients/:mrn',
      name: 'patient-detail',
      component: () => import('@/views/PatientDetailView.vue'),
      beforeEnter: requireAuth,
    },
    {
      path: '/patients/:mrn/encounters/new',
      name: 'encounter-new',
      component: () => import('@/views/EncounterFormView.vue'),
      beforeEnter: requireAuth,
    },
    {
      path: '/patients/:mrn/encounters/:id',
      name: 'encounter-detail',
      component: () => import('@/views/EncounterDetailView.vue'),
      beforeEnter: requireAuth,
    },
    {
      path: '/care-plans/:id',
      name: 'care-plan-detail',
      component: () => import('@/views/CarePlanView.vue'),
      beforeEnter: requireAuth,
    },
    {
      path: '/referrals',
      name: 'referrals',
      component: () => import('@/views/ReferralsView.vue'),
      beforeEnter: requireAuth,
    },
    {
      path: '/lab-imports',
      name: 'lab-imports',
      component: () => import('@/views/LabImportsView.vue'),
      beforeEnter: [requireAuth, requireRole(Role.CARE_COORDINATOR)],
    },
    {
      path: '/audit',
      name: 'audit',
      component: () => import('@/views/AuditLogView.vue'),
      beforeEnter: [requireAuth, requireRole(Role.COMPLIANCE_OFFICER)],
    },
    { path: '/', redirect: '/dashboard' },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/views/NotFoundView.vue') },
  ],
})

export default router
