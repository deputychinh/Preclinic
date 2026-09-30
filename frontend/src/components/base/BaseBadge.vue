<script setup lang="ts">
defineProps<{ label: string; color: string }>()
</script>

<template>
  <span
    class="inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold"
    :style="{ color, backgroundColor: `${color}26` }"
  >
    {{ label }}
  </span>
</template>
