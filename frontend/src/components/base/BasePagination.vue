<script setup lang="ts">
import { ChevronLeft, ChevronRight } from '@lucide/vue'

defineProps<{
  hasPrevious: boolean
  hasNext: boolean
  loading?: boolean
}>()

const emit = defineEmits<{ previous: []; next: [] }>()
</script>

<template>
  <div class="mt-3 flex justify-end gap-2">
    <button
      type="button"
      class="inline-flex items-center rounded-lg border border-border bg-white px-3 py-1.5 text-sm font-medium text-secondary transition hover:bg-bg-soft disabled:cursor-not-allowed disabled:opacity-50"
      :disabled="!hasPrevious || loading"
      @click="emit('previous')"
    >
      <ChevronLeft
        :size="16"
        class="mr-1"
      />
      Previous
    </button>
    <button
      type="button"
      class="inline-flex items-center rounded-lg border border-border bg-white px-3 py-1.5 text-sm font-medium text-secondary transition hover:bg-bg-soft disabled:cursor-not-allowed disabled:opacity-50"
      :disabled="!hasNext || loading"
      @click="emit('next')"
    >
      Next
      <ChevronRight
        :size="16"
        class="ml-1"
      />
    </button>
  </div>
</template>
