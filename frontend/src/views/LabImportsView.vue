<script setup lang="ts">
import { ref } from 'vue'

import BaseButton from '@/components/base/BaseButton.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { getLabImportJob, uploadLabImport } from '@/services/lab-import.service'
import type { LabImportJob } from '@/types/models'

// eslint-disable-next-line no-undef -- DOM lib type, not an undefined value reference
const file = ref<File | null>(null)
const job = ref<LabImportJob | null>(null)
const uploading = ref(false)
const error = ref('')

// eslint-disable-next-line no-undef -- DOM lib type
function onFileChange(event: Event) {
  file.value = (event.target as HTMLInputElement).files?.[0] ?? null // eslint-disable-line no-undef -- DOM lib type
}

async function onUpload() {
  if (!file.value) return
  uploading.value = true
  error.value = ''
  try {
    const { job: created } = await uploadLabImport(file.value)
    job.value = created
    poll(created.id)
  } catch {
    error.value = 'Upload failed.'
  } finally {
    uploading.value = false
  }
}

function poll(id: number) {
  // eslint-disable-next-line no-undef -- browser global, valid at runtime and in the DOM lib
  const timer = setInterval(async () => {
    const updated = await getLabImportJob(id)
    job.value = updated
    if (updated.status === 'SUCCEEDED' || updated.status === 'FAILED_PARTIAL') {
      // eslint-disable-next-line no-undef -- browser global
      clearInterval(timer)
    }
  }, 2000)
}
</script>

<template>
  <div>
    <PageHeader title="Lab Result Import" />
    <BaseCard class="max-w-[480px]">
      <div class="flex flex-col gap-3">
        <input
          type="file"
          accept=".csv"
          class="text-sm"
          @change="onFileChange"
        >
        <BaseButton
          :disabled="!file || uploading"
          @click="onUpload"
        >
          {{ uploading ? 'Uploading…' : 'Upload CSV' }}
        </BaseButton>
        <p
          v-if="error"
          role="alert"
          class="text-danger"
        >
          {{ error }}
        </p>
        <div v-if="job">
          <p>Status: {{ job.status }}</p>
          <p>Imported {{ job.importedRows }} / {{ job.totalRows }} rows</p>
          <ul
            v-if="job.errorReport.length"
            class="list-disc pl-4"
          >
            <li
              v-for="e in job.errorReport"
              :key="e.row"
            >
              Row {{ e.row }}: {{ e.error }}
            </li>
          </ul>
        </div>
      </div>
    </BaseCard>
  </div>
</template>
