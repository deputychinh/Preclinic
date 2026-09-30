<script setup lang="ts">
import { AlertTriangle, BarChart3, CalendarDays, Share2, Sparkles, Users } from '@lucide/vue'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import BaseBadge from '@/components/base/BaseBadge.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseStatCard from '@/components/base/BaseStatCard.vue'
import StatusBreakdownChart from '@/components/base/StatusBreakdownChart.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { AUDIT_ACTION_COLOR, ENCOUNTER_STATUS_COLOR, REFERRAL_STATUS_COLOR } from '@/constants/colors'
import {
  AUDIT_ACTION_LABEL,
  AuditAction,
  ENCOUNTER_STATUS_LABEL,
  REFERRAL_STATUS_LABEL,
  Role,
} from '@/enums'
import { getDashboardSummary, type DashboardSummary } from '@/services/dashboard.service'
import { useAuthStore } from '@/stores/auth.store'

const auth = useAuthStore()
const router = useRouter()
const summary = ref<DashboardSummary | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    summary.value = await getDashboardSummary()
  } catch {
    error.value = 'Could not load the dashboard.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <PageHeader :title="`Welcome, ${auth.currentUser?.fullName ?? ''}`">
      <template
        v-if="summary && summary.role !== 'COMPLIANCE_OFFICER'"
        #action
      >
        <BaseButton @click="router.push({ name: 'patients' })">
          Go to Patients
        </BaseButton>
      </template>
    </PageHeader>

    <p v-if="loading">
      Loading…
    </p>
    <p
      v-else-if="error"
      role="alert"
      class="text-danger"
    >
      {{ error }}
    </p>

    <div
      v-else-if="summary"
      class="flex flex-col gap-4"
    >
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <template v-if="summary.role !== 'COMPLIANCE_OFFICER'">
          <BaseStatCard
            label="Patients on my care team"
            :value="summary.patientCount"
            :icon="Users"
            color="primary"
          />
          <BaseStatCard
            label="Encounters this week"
            :value="summary.encountersThisWeek"
            :icon="CalendarDays"
            color="info"
          />
          <BaseStatCard
            label="AI drafts awaiting review"
            :value="summary.pendingAiDrafts"
            :icon="Sparkles"
            color="accent"
          />
          <BaseStatCard
            label="Open referrals"
            :value="summary.openReferrals"
            :icon="Share2"
            color="warning"
          />
        </template>
        <template v-else>
          <BaseStatCard
            label="Audit events today"
            :value="summary.eventsToday"
            :icon="BarChart3"
            color="info"
          />
          <BaseStatCard
            label="Break-glass events (7 days)"
            :value="summary.breakGlassThisWeek"
            :icon="AlertTriangle"
            color="danger"
          />
          <BaseStatCard
            label="Total events (7 days)"
            :value="summary.totalEventsThisWeek"
            :icon="BarChart3"
            color="primary"
          />
        </template>
      </div>

      <div class="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <BaseCard
          v-if="summary.role !== 'COMPLIANCE_OFFICER'"
          title="Encounters by status"
        >
          <StatusBreakdownChart
            :data="summary.encounterBreakdown"
            :color-map="ENCOUNTER_STATUS_COLOR"
            :label-map="ENCOUNTER_STATUS_LABEL"
          />
        </BaseCard>
        <BaseCard
          v-if="summary.role !== 'COMPLIANCE_OFFICER'"
          title="Referrals by status"
        >
          <StatusBreakdownChart
            :data="summary.referralBreakdown"
            :color-map="REFERRAL_STATUS_COLOR"
            :label-map="REFERRAL_STATUS_LABEL"
          />
        </BaseCard>
        <BaseCard
          v-if="summary.role === 'COMPLIANCE_OFFICER'"
          title="Audit events by action (7 days)"
          class="lg:col-span-2"
        >
          <StatusBreakdownChart
            :data="summary.actionBreakdown"
            :color-map="AUDIT_ACTION_COLOR"
            :label-map="AUDIT_ACTION_LABEL"
          />
        </BaseCard>
      </div>

      <BaseCard title="Recent activity">
        <ul
          v-if="summary.recentEvents.length"
          class="m-0 flex list-none flex-col gap-3 p-0"
        >
          <li
            v-for="event in summary.recentEvents"
            :key="event.id"
            class="flex flex-wrap items-center gap-3"
          >
            <BaseBadge
              :label="AUDIT_ACTION_LABEL[event.action as AuditAction] ?? event.action"
              :color="AUDIT_ACTION_COLOR[event.action as AuditAction] ?? '#6b7680'"
            />
            <span class="flex items-center gap-2 text-text">
              {{ event.resourceType }}<template v-if="event.patientId"> · patient #{{ event.patientId }}</template>
              <BaseBadge
                v-if="event.isBreakGlass"
                label="Break-glass"
                color="#c0392b"
              />
            </span>
            <span class="ml-auto text-sm text-text-muted">{{ new Date(event.createdAt).toLocaleString() }}</span>
          </li>
        </ul>
        <p v-else>
          No recent activity.
        </p>
      </BaseCard>

      <BaseCard
        v-if="summary.role !== 'COMPLIANCE_OFFICER'"
        title="Quick actions"
      >
        <div class="flex flex-wrap gap-3">
          <BaseButton
            variant="secondary"
            @click="router.push({ name: 'patients' })"
          >
            Search Patients
          </BaseButton>
          <BaseButton
            variant="secondary"
            @click="router.push({ name: 'referrals' })"
          >
            View Referrals
          </BaseButton>
          <BaseButton
            v-if="auth.role === Role.CARE_COORDINATOR"
            variant="secondary"
            @click="router.push({ name: 'lab-imports' })"
          >
            Import Lab Results
          </BaseButton>
        </div>
      </BaseCard>
    </div>
  </div>
</template>
