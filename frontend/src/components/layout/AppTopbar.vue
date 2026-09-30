<script setup lang="ts">
import { LogOut, Menu } from '@lucide/vue'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { ROLE_LABEL } from '@/enums'
import { useAuthStore } from '@/stores/auth.store'
import { useUiStore } from '@/stores/ui.store'

const auth = useAuthStore()
const ui = useUiStore()
const route = useRoute()
const router = useRouter()

const breadcrumb = computed(() => (route.name ? String(route.name).replace(/-/g, ' ') : ''))

const initials = computed(() => {
  const name = auth.currentUser?.fullName ?? ''
  return name
    .split(' ')
    .filter(Boolean)
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
})

function onLogout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <header class="flex h-16 shrink-0 items-center gap-4 border-b border-border bg-white px-6">
    <button
      type="button"
      aria-label="Toggle sidebar"
      class="rounded-lg p-2 text-text-muted transition hover:bg-bg-soft hover:text-text"
      @click="ui.toggleSidebar()"
    >
      <Menu :size="20" />
    </button>
    <span class="text-sm capitalize text-text-muted">{{ breadcrumb }}</span>

    <div class="ml-auto flex items-center gap-3">
      <span
        v-if="auth.role"
        class="rounded-full bg-primary-soft px-3 py-1 text-xs font-semibold text-primary"
      >
        {{ ROLE_LABEL[auth.role] }}
      </span>
      <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary-soft text-xs font-bold text-primary">
        {{ initials }}
      </div>
      <span class="text-sm text-text">{{ auth.currentUser?.fullName }}</span>
      <button
        type="button"
        class="inline-flex items-center rounded-lg border border-border px-3 py-1.5 text-sm font-medium text-secondary transition hover:bg-bg-soft"
        @click="onLogout"
      >
        <LogOut
          :size="16"
          class="mr-1"
        />
        Log out
      </button>
    </div>
  </header>
</template>
