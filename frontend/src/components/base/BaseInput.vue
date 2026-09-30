<script setup lang="ts">
const model = defineModel<string>({ default: '' })

withDefaults(
  defineProps<{
    label: string
    type?: string
    placeholder?: string
    required?: boolean
    hideLabel?: boolean
    autocomplete?: string
  }>(),
  { type: 'text', placeholder: undefined, required: false, hideLabel: false, autocomplete: undefined },
)
</script>

<template>
  <label class="block">
    <span
      class="mb-1.5 block text-sm font-medium text-secondary"
      :class="{ 'sr-only': hideLabel }"
    >
      {{ label }}
    </span>
    <input
      v-model="model"
      :type="type"
      :placeholder="placeholder"
      :required="required"
      :autocomplete="autocomplete"
      :aria-label="hideLabel ? label : undefined"
      class="w-full rounded-lg border border-border px-3 py-2 text-sm text-text placeholder:text-text-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/30"
    >
  </label>
</template>
