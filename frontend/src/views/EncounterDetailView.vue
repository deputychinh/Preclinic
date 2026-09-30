<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import BaseBadge from '@/components/base/BaseBadge.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import SignDiffViewer from '@/components/encounter/SignDiffViewer.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { ENCOUNTER_STATUS_COLOR } from '@/constants/colors'
import { AI_DRAFT_POLL_INTERVAL_MS, AI_DRAFT_POLL_TIMEOUT_MS } from '@/constants/app'
import { usePolling } from '@/composables/usePolling'
import { approveAiDraft, getAiDraft, requestAiDraft } from '@/services/ai.service'
import { getEncounter, signEncounterNote } from '@/services/encounter.service'
import type { AIDraft, Encounter } from '@/types/models'

const route = useRoute()
const encounter = ref<Encounter | null>(null)
const editedNote = ref('')
const requestingDraft = ref(false)
const signing = ref(false)
const activeDraft = ref<AIDraft | null>(null)

const { result: polledDraft, start } = usePolling<AIDraft>(
  () => getAiDraft(activeDraft.value!.id),
  (draft) => draft.status === 'READY' || draft.status === 'FAILED',
  AI_DRAFT_POLL_INTERVAL_MS,
  AI_DRAFT_POLL_TIMEOUT_MS,
)

const latestNote = computed(() => encounter.value?.noteVersions[0] ?? null)
const draftContent = computed(() => polledDraft.value?.content ?? '')

async function load() {
  encounter.value = await getEncounter(route.params.id as string)
}

async function onRequestAiDraft() {
  if (!encounter.value) return
  requestingDraft.value = true
  activeDraft.value = await requestAiDraft(encounter.value.id)
  start()
  requestingDraft.value = false
}

async function onSign() {
  if (!encounter.value) return
  signing.value = true
  try {
    if (activeDraft.value?.status === 'READY') {
      await approveAiDraft(activeDraft.value.id)
    }
    await load()
    const note = encounter.value!.noteVersions[0]
    await signEncounterNote(encounter.value!.id, note.id)
    await load()
  } finally {
    signing.value = false
  }
}

onMounted(load)
</script>

<template>
  <div v-if="encounter">
    <PageHeader :title="`Encounter — ${encounter.reason}`">
      <template #action>
        <BaseBadge
          :label="encounter.status"
          :color="ENCOUNTER_STATUS_COLOR[encounter.status]"
        />
      </template>
    </PageHeader>

    <div
      v-if="encounter.status !== 'SIGNED'"
      class="mb-4"
    >
      <BaseButton
        variant="secondary"
        :disabled="requestingDraft"
        @click="onRequestAiDraft"
      >
        {{ requestingDraft ? 'Requesting…' : 'Draft with AI' }}
      </BaseButton>
    </div>

    <SignDiffViewer
      v-if="latestNote"
      :original="draftContent"
      :edited="editedNote || latestNote.content"
      :signing="signing"
      @sign="onSign"
    />
  </div>
</template>
