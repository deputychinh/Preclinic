<script setup lang="ts">
import { AlertTriangle, ShieldCheck } from '@lucide/vue'
import { computed, ref, watch } from 'vue'

import BaseBadge from '@/components/base/BaseBadge.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import BasePagination from '@/components/base/BasePagination.vue'
import BaseSelect from '@/components/base/BaseSelect.vue'
import type { SelectOption } from '@/components/base/BaseSelect.vue'
import BaseStatCard from '@/components/base/BaseStatCard.vue'
import BaseTable from '@/components/base/BaseTable.vue'
import type { TableColumn } from '@/components/base/BaseTable.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { AUDIT_ACTION_LABEL, AuditAction } from '@/enums'
import { extractCursor } from '@/lib/cursor'
import { searchAuditEvents } from '@/services/audit.service'
import type { AuditEvent } from '@/types/models'

const events = ref<AuditEvent[]>([])
const loading = ref(true)
const actionFilter = ref('')
const patientIdFilter = ref('')
const breakGlassOnly = ref(false)
const nextCursor = ref<string | undefined>(undefined)
const previousCursor = ref<string | undefined>(undefined)
// eslint-disable-next-line no-undef -- browser global
let debounceTimer: ReturnType<typeof setTimeout>

const columns: TableColumn[] = [
  { key: 'createdAt', label: 'When' },
  { key: 'actorName', label: 'Actor' },
  { key: 'action', label: 'Action' },
  { key: 'resourceType', label: 'Resource' },
  { key: 'reason', label: 'Reason' },
]

// AuditAction.BREAK_GLASS is excluded: no service ever writes it as an `action` value — a
// break-glass access is recorded as its real action (usually READ) plus the separate
// `is_break_glass` flag, which the checkbox below already filters on. Offering it here would let
// a compliance officer select a filter that always returns zero rows.
const actionOptions: SelectOption[] = Object.values(AuditAction)
  .filter((action) => action !== AuditAction.BREAK_GLASS)
  .map((action) => ({ value: action, label: AUDIT_ACTION_LABEL[action] }))

const breakGlassCount = computed(() => events.value.filter((e) => e.isBreakGlass).length)

async function load(cursor?: string) {
  loading.value = true
  try {
    const page = await searchAuditEvents({
      action: actionFilter.value || undefined,
      patientId: patientIdFilter.value || undefined,
      breakGlassOnly: breakGlassOnly.value,
      cursor,
    })
    events.value = page.data
    nextCursor.value = extractCursor(page.meta.next)
    previousCursor.value = extractCursor(page.meta.previous)
  } finally {
    loading.value = false
  }
}

watch([actionFilter, patientIdFilter, breakGlassOnly], () => {
  // eslint-disable-next-line no-undef -- browser global
  clearTimeout(debounceTimer)
  // eslint-disable-next-line no-undef -- browser global
  debounceTimer = setTimeout(() => load(), 300)
})

function goNext() {
  if (nextCursor.value) load(nextCursor.value)
}

function goPrevious() {
  load(previousCursor.value)
}

load()
</script>

<template>
  <div>
    <PageHeader title="Audit Log" />
    <div class="mb-4 grid grid-cols-1 gap-4 sm:grid-cols-2 md:max-w-lg">
      <BaseStatCard
        label="Events (this page)"
        :value="events.length"
        :icon="ShieldCheck"
        color="info"
      />
      <BaseStatCard
        label="Break-glass events (this page)"
        :value="breakGlassCount"
        :icon="AlertTriangle"
        color="danger"
      />
    </div>

    <div class="mb-4 flex flex-wrap items-end gap-4">
      <BaseSelect
        v-model="actionFilter"
        label="Action"
        :options="actionOptions"
        placeholder="All actions"
      />
      <BaseInput
        v-model="patientIdFilter"
        label="Patient ID"
        placeholder="Filter by patient ID…"
      />
      <label class="flex h-[42px] cursor-pointer items-center gap-2 text-sm text-text">
        <input
          v-model="breakGlassOnly"
          type="checkbox"
        >
        Break-glass only
      </label>
    </div>

    <BaseTable
      :columns="columns"
      :rows="events"
      :loading="loading"
      empty-message="No audit events found."
    >
      <template #actions="{ row }">
        <BaseBadge
          v-if="(row as any).isBreakGlass"
          label="Break-glass"
          color="#c0392b"
        />
      </template>
    </BaseTable>
    <BasePagination
      :has-previous="Boolean(previousCursor)"
      :has-next="Boolean(nextCursor)"
      :loading="loading"
      @previous="goPrevious"
      @next="goNext"
    />
  </div>
</template>
