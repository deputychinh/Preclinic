<script setup lang="ts">
import { LayoutDashboard, Share2, ShieldCheck, UploadCloud, Users } from '@lucide/vue'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import { Role } from '@/enums'
import { useAuthStore } from '@/stores/auth.store'
import { useUiStore } from '@/stores/ui.store'

const ui = useUiStore()
const auth = useAuthStore()
const route = useRoute()

const navItems = computed(() => [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, visible: true },
  { to: '/patients', label: 'Patients', icon: Users, visible: true },
  { to: '/referrals', label: 'Referrals', icon: Share2, visible: true },
  {
    to: '/lab-imports',
    label: 'Lab Imports',
    icon: UploadCloud,
    visible: auth.role === Role.CARE_COORDINATOR,
  },
  {
    to: '/audit',
    label: 'Audit Log',
    icon: ShieldCheck,
    visible: auth.role === Role.COMPLIANCE_OFFICER,
  },
].filter((item) => item.visible))

function isActive(to: string) {
  return route.path === to || route.path.startsWith(`${to}/`)
}
</script>

<template>
  <nav
    class="flex shrink-0 flex-col bg-secondary text-white transition-all duration-200"
    :class="ui.sidebarCollapsed ? 'w-[76px]' : 'w-[260px]'"
  >
    <div class="flex h-16 items-center px-4">
      <span class="text-lg font-bold tracking-tight">
        {{ ui.sidebarCollapsed ? 'CP' : 'CarePath' }}
      </span>
    </div>
    <ul class="flex flex-col gap-1 px-3 py-2">
      <li
        v-for="item in navItems"
        :key="item.to"
      >
        <RouterLink
          :to="item.to"
          class="flex items-center gap-3 rounded-xl border-l-4 px-3 py-2.5 text-sm font-medium transition"
          :class="
            isActive(item.to)
              ? 'border-accent bg-white/10 text-white'
              : 'border-transparent text-white/70 hover:bg-white/5 hover:text-white'
          "
        >
          <component
            :is="item.icon"
            :size="18"
            class="shrink-0"
          />
          <span v-if="!ui.sidebarCollapsed">{{ item.label }}</span>
        </RouterLink>
      </li>
    </ul>
  </nav>
</template>
