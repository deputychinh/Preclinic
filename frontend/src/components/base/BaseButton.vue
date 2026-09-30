<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    variant?: 'primary' | 'secondary' | 'danger'
    type?: 'button' | 'submit'
    disabled?: boolean
  }>(),
  { variant: 'primary', type: 'button', disabled: false },
)

const variantClass = computed(() => {
  switch (props.variant) {
    case 'secondary':
      return 'border border-border bg-white text-secondary hover:bg-bg-soft'
    case 'danger':
      return 'bg-danger text-white hover:opacity-90'
    default:
      return 'bg-primary text-white hover:bg-primary-dark'
  }
})
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    class="inline-flex items-center justify-center gap-1.5 rounded-xl px-4 py-2 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40"
    :class="variantClass"
  >
    <slot />
  </button>
</template>
