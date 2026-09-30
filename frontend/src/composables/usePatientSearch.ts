import { computed, ref, watch } from 'vue'

import { SEARCH_DEBOUNCE_MS } from '@/constants/app'
import { extractCursor } from '@/lib/cursor'
import { searchPatients } from '@/services/patient.service'
import type { PatientListItem } from '@/types/models'

export function usePatientSearch() {
  const query = ref('')
  const results = ref<PatientListItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const nextCursor = ref<string | undefined>(undefined)
  const previousCursor = ref<string | undefined>(undefined)
  let debounceTimer: ReturnType<typeof setTimeout>

  async function runSearch(cursor?: string) {
    loading.value = true
    error.value = null
    try {
      const page = await searchPatients(query.value, cursor)
      results.value = page.data
      nextCursor.value = extractCursor(page.meta.next)
      previousCursor.value = extractCursor(page.meta.previous)
    } catch {
      error.value = 'Could not load patients. Please try again.'
    } finally {
      loading.value = false
    }
  }

  watch(query, () => {
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => runSearch(), SEARCH_DEBOUNCE_MS)
  })

  function goNext() {
    if (nextCursor.value) runSearch(nextCursor.value)
  }

  function goPrevious() {
    runSearch(previousCursor.value)
  }

  runSearch()

  return {
    query,
    results,
    loading,
    error,
    hasNext: computed(() => Boolean(nextCursor.value)),
    hasPrevious: computed(() => Boolean(previousCursor.value)),
    goNext,
    goPrevious,
    refresh: () => runSearch(),
  }
}
