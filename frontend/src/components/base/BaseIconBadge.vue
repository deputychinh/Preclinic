<script setup lang="ts">
import type { Component } from 'vue'
import { computed } from 'vue'

export type IconBadgeColor = 'primary' | 'accent' | 'success' | 'warning' | 'danger' | 'info'

const props = withDefaults(
  defineProps<{
    icon: Component
    color?: IconBadgeColor
    size?: 'sm' | 'md'
  }>(),
  { color: 'primary', size: 'md' },
)

// Written as a static lookup table (not `bg-${color}-soft` string interpolation) so Tailwind's
// build-time class scanner can see every literal class name it needs to keep.
const COLOR_CLASSES: Record<IconBadgeColor, string> = {
  primary: 'bg-primary-soft text-primary',
  accent: 'bg-accent-soft text-accent',
  success: 'bg-success-soft text-success',
  warning: 'bg-warning-soft text-warning',
  danger: 'bg-danger-soft text-danger',
  info: 'bg-info-soft text-info',
}

const colorClass = computed(() => COLOR_CLASSES[props.color])
const sizeClass = computed(() => (props.size === 'sm' ? 'h-8 w-8' : 'h-12 w-12'))
const iconSize = computed(() => (props.size === 'sm' ? 16 : 22))
</script>

<template>
  <div
    class="flex shrink-0 items-center justify-center rounded-lg"
    :class="[colorClass, sizeClass]"
  >
    <component
      :is="icon"
      :size="iconSize"
    />
  </div>
</template>
