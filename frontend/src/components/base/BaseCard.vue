<script setup lang="ts">
import type { Component } from 'vue'

withDefaults(
  defineProps<{
    title?: string
    icon?: Component
  }>(),
  { title: undefined, icon: undefined },
)
</script>

<template>
  <section class="rounded-2xl bg-white p-6 shadow-sm">
    <div
      v-if="title"
      class="mb-4 flex items-center gap-3"
    >
      <div
        v-if="icon"
        class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary-soft text-primary"
      >
        <component
          :is="icon"
          :size="18"
        />
      </div>
      <h2 class="text-base font-bold text-secondary">
        {{ title }}
      </h2>
      <div class="ml-auto">
        <slot name="action" />
      </div>
    </div>
    <slot />
  </section>
</template>
