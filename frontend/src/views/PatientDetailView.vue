<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import BaseBadge from '@/components/base/BaseBadge.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { listCarePlansForPatient, type CarePlan } from '@/services/care-plan.service'
import { getPatient } from '@/services/patient.service'
import type { PatientDetail } from '@/types/models'

const route = useRoute()
const router = useRouter()
const patient = ref<PatientDetail | null>(null)
const carePlans = ref<CarePlan[]>([])
const error = ref('')
const loading = ref(true)

async function load() {
  loading.value = true
  error.value = ''
  try {
    patient.value = await getPatient(route.params.mrn as string)
    carePlans.value = await listCarePlansForPatient(patient.value.id)
  } catch {
    error.value = 'You do not have access to this patient chart.'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div>
    <PageHeader :title="patient ? patient.fullName : 'Patient chart'">
      <template
        v-if="patient"
        #action
      >
        <BaseButton @click="router.push({ name: 'encounter-new', params: { mrn: patient.mrn } })">
          New Encounter
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
      v-else-if="patient"
      class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3"
    >
      <BaseCard title="Demographics">
        <p>MRN: {{ patient.mrn }}</p>
        <p>Date of birth: {{ patient.dateOfBirth }}</p>
      </BaseCard>
      <BaseCard title="Allergies">
        <ul
          v-if="patient.allergies.length"
          class="list-disc pl-4"
        >
          <li
            v-for="a in patient.allergies"
            :key="a.id"
          >
            {{ a.substance }} — {{ a.reaction }} ({{ a.severity }})
          </li>
        </ul>
        <p v-else>
          No known allergies recorded.
        </p>
      </BaseCard>
      <BaseCard title="Medications">
        <ul
          v-if="patient.medications.length"
          class="list-disc pl-4"
        >
          <li
            v-for="m in patient.medications"
            :key="m.id"
          >
            {{ m.name }} {{ m.dosage }} — {{ m.frequency }}
          </li>
        </ul>
        <p v-else>
          No active medications.
        </p>
      </BaseCard>
      <BaseCard title="Care Plans">
        <ul
          v-if="carePlans.length"
          class="list-disc pl-4"
        >
          <li
            v-for="plan in carePlans"
            :key="plan.id"
          >
            <RouterLink :to="{ name: 'care-plan-detail', params: { id: plan.id } }">
              {{ plan.title }}
            </RouterLink>
          </li>
        </ul>
        <p v-else>
          No care plans yet.
        </p>
      </BaseCard>
      <BaseCard title="Consents">
        <ul
          v-if="patient.consents.length"
          class="flex flex-col gap-2"
        >
          <li
            v-for="c in patient.consents"
            :key="c.id"
            class="flex items-center gap-2"
          >
            {{ c.consentType }}
            <BaseBadge
              :label="c.revokedAt ? 'Revoked' : 'Active'"
              :color="c.revokedAt ? '#c0392b' : '#2e9e6c'"
            />
          </li>
        </ul>
        <p v-else>
          No consent records.
        </p>
      </BaseCard>
    </div>
  </div>
</template>
