<script setup lang="ts">
import { computed } from 'vue'

import BaseButton from '@/components/base/BaseButton.vue'

const props = defineProps<{
  original: string
  edited: string
  signing?: boolean
}>()

const emit = defineEmits<{ sign: [] }>()

// DS-05: the sign action must never be reachable before a diff has actually rendered — this is the
// one frontend guarantee that backs the "no AI content becomes the record without human review" rule.
const hasDiff = computed(() => props.original.trim().length > 0 || props.edited.trim().length > 0)
const isUnchanged = computed(() => props.original === props.edited)
</script>

<template>
  <div class="flex flex-col gap-3">
    <div class="rounded-lg bg-bg-soft p-3">
      <h3 class="mb-2 text-sm text-text-muted">
        AI draft (original)
      </h3>
      <pre class="m-0 whitespace-pre-wrap font-sans">{{ original || '(no draft)' }}</pre>
    </div>
    <div class="rounded-lg bg-bg-soft p-3">
      <h3 class="mb-2 text-sm text-text-muted">
        Clinician version (to be signed)
      </h3>
      <pre class="m-0 whitespace-pre-wrap font-sans">{{ edited }}</pre>
    </div>
    <p
      v-if="isUnchanged && original"
      class="m-0 text-sm text-warning"
    >
      No edits made to the AI draft.
    </p>
    <BaseButton
      :disabled="!hasDiff || signing"
      @click="emit('sign')"
    >
      {{ signing ? 'Signing…' : 'Sign and finalize' }}
    </BaseButton>
  </div>
</template>
