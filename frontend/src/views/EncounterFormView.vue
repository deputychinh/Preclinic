<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import BaseButton from '@/components/base/BaseButton.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { createEncounter } from '@/services/encounter.service'
import { getPatient } from '@/services/patient.service'

const route = useRoute()
const router = useRouter()
const reason = ref('')
const occurredAt = ref(new Date().toISOString().slice(0, 16))
const error = ref('')
const saving = ref(false)

async function onSubmit() {
  saving.value = true
  error.value = ''
  try {
    const patient = await getPatient(route.params.mrn as string)
    const encounter = await createEncounter(patient.id, reason.value, new Date(occurredAt.value).toISOString())
    router.push({ name: 'encounter-detail', params: { mrn: patient.mrn, id: encounter.id } })
  } catch {
    error.value = 'Could not create the encounter.'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div>
    <PageHeader title="New Encounter" />
    <form
      class="flex max-w-[480px] flex-col gap-4 rounded-2xl bg-white p-6 shadow-sm"
      @submit.prevent="onSubmit"
    >
      <BaseInput
        v-model="reason"
        label="Reason for visit"
        required
      />
      <BaseInput
        v-model="occurredAt"
        label="Date & time"
        type="datetime-local"
        required
      />
      <p
        v-if="error"
        role="alert"
        class="m-0 text-danger"
      >
        {{ error }}
      </p>
      <BaseButton
        type="submit"
        :disabled="saving"
      >
        {{ saving ? 'Saving…' : 'Create Encounter' }}
      </BaseButton>
    </form>
  </div>
</template>
