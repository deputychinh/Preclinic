<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import BaseBadge from '@/components/base/BaseBadge.vue'
import BaseTable from '@/components/base/BaseTable.vue'
import type { TableColumn } from '@/components/base/BaseTable.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { REFERRAL_STATUS_COLOR } from '@/constants/colors'
import type { ReferralStatus } from '@/enums'
import { listReferrals } from '@/services/referral.service'
import type { Referral } from '@/types/models'

const referrals = ref<Referral[]>([])
const loading = ref(true)

const columns: TableColumn[] = [
  { key: 'specialty', label: 'Specialty' },
  { key: 'reason', label: 'Reason' },
]

const rows = computed(() =>
  referrals.value.map((r) => ({ specialty: r.specialty, reason: r.reason, status: r.status })),
)

onMounted(async () => {
  try {
    const page = await listReferrals()
    referrals.value = page.data
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <PageHeader title="Referrals" />
    <BaseTable
      :columns="columns"
      :rows="rows"
      :loading="loading"
      empty-message="No referrals yet."
    >
      <template #actions="{ row }">
        <BaseBadge
          :label="String(row.status)"
          :color="REFERRAL_STATUS_COLOR[row.status as ReferralStatus]"
        />
      </template>
    </BaseTable>
  </div>
</template>
