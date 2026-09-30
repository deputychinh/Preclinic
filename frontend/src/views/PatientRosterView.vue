<script setup lang="ts">
import { Users } from '@lucide/vue'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import BaseInput from '@/components/base/BaseInput.vue'
import BasePagination from '@/components/base/BasePagination.vue'
import BaseStatCard from '@/components/base/BaseStatCard.vue'
import BaseTable from '@/components/base/BaseTable.vue'
import type { TableColumn } from '@/components/base/BaseTable.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { usePatientSearch } from '@/composables/usePatientSearch'

const { query, results, loading, error, hasNext, hasPrevious, goNext, goPrevious } = usePatientSearch()
const router = useRouter()

const columns: TableColumn[] = [
  { key: 'mrn', label: 'MRN' },
  { key: 'fullName', label: 'Name' },
  { key: 'dateOfBirth', label: 'Date of Birth' },
]

const rows = computed(() => results.value)
</script>

<template>
  <div>
    <PageHeader title="Patients" />
    <div class="mb-4 grid grid-cols-1 gap-4 sm:max-w-xs">
      <BaseStatCard
        label="Patients on this page"
        :value="results.length"
        :icon="Users"
      />
    </div>
    <BaseInput
      v-model="query"
      label="Search by name or MRN"
      hide-label
      placeholder="Search by name or MRN…"
      class="mb-4 max-w-[360px]"
    />
    <p
      v-if="error"
      role="alert"
      class="mb-4 text-danger"
    >
      {{ error }}
    </p>
    <BaseTable
      :columns="columns"
      :rows="rows"
      :loading="loading"
      empty-message="No patients found on your care team."
    >
      <template #actions="{ row }">
        <button
          type="button"
          class="text-sm font-medium text-primary hover:underline"
          @click="router.push({ name: 'patient-detail', params: { mrn: (row as any).mrn } })"
        >
          View
        </button>
      </template>
    </BaseTable>
    <BasePagination
      :has-previous="hasPrevious"
      :has-next="hasNext"
      :loading="loading"
      @previous="goPrevious"
      @next="goNext"
    />
  </div>
</template>
