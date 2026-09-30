<script setup lang="ts">
export interface SelectOption {
  value: string
  label: string
}

const model = defineModel<string>({ default: '' })

withDefaults(
  defineProps<{
    label: string
    options: SelectOption[]
    placeholder?: string
    hideLabel?: boolean
  }>(),
  { placeholder: undefined, hideLabel: false },
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
    <select
      v-model="model"
      :aria-label="hideLabel ? label : undefined"
      class="w-full rounded-lg border border-border bg-white px-3 py-2 text-sm text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/30"
    >
      <option value="">
        {{ placeholder ?? 'All' }}
      </option>
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
  </label>
</template>
