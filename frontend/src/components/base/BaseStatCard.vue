<script setup lang="ts">
import type { Component } from 'vue'
import { computed } from 'vue'

import BaseIconBadge, { type IconBadgeColor } from '@/components/base/BaseIconBadge.vue'

const props = withDefaults(
  defineProps<{
    label: string
    value: number | string
    icon?: Component
    color?: IconBadgeColor
  }>(),
  { icon: undefined, color: 'primary' },
)

// Static lookup table (not `border-${color}` interpolation) so Tailwind's build-time class
// scanner keeps every literal class name it needs.
const BORDER_CLASSES: Record<IconBadgeColor, string> = {
  primary: 'border-primary',
  accent: 'border-accent',
  success: 'border-success',
  warning: 'border-warning',
  danger: 'border-danger',
  info: 'border-info',
}

const borderClass = computed(() => BORDER_CLASSES[props.color])
</script>

<template>
  <div
    class="flex items-center gap-4 rounded-2xl border-l-4 bg-white p-5 shadow-sm"
    :class="borderClass"
  >
    <BaseIconBadge
      v-if="icon"
      :icon="icon"
      :color="color"
    />
    <div>
      <div class="text-xl font-bold text-secondary">
        {{ value }}
      </div>
      <div class="text-sm text-text-muted">
        {{ label }}
      </div>
    </div>
  </div>
</template>
