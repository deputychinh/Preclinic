import type { NavigationGuardWithThis } from 'vue-router'

import { Role } from '@/enums'
import { useAuthStore } from '@/stores/auth.store'

export const requireAuth: NavigationGuardWithThis<undefined> = async (to) => {
  const auth = useAuthStore()
  if (!auth.isAuthenticated) {
    return to.name === 'login' ? undefined : { name: 'login' }
  }
  // The access token survives a page reload (sessionStorage), but `currentUser` (role, name)
  // only gets set by login() — without this, every guard checking auth.role sees null right
  // after a reload, and requireRole below would wrongly bounce an authorized user to /patients.
  if (!auth.currentUser) {
    try {
      await auth.loadCurrentUser()
    } catch {
      auth.logout()
      return { name: 'login' }
    }
  }
}

export function requireRole(...roles: Role[]): NavigationGuardWithThis<undefined> {
  return () => {
    const auth = useAuthStore()
    if (!auth.role || !roles.includes(auth.role)) {
      return { name: 'patients' }
    }
  }
}
