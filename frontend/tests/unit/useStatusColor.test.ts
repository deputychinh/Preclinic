import { ref } from 'vue'
import { describe, expect, it } from 'vitest'

import { useStatusColor } from '@/composables/useStatusColor'

describe('useStatusColor', () => {
  it('resolves the color for the current status and updates reactively', () => {
    const status = ref<'A' | 'B'>('A')
    const color = useStatusColor(status, { A: 'red', B: 'blue' })

    expect(color.value).toBe('red')

    status.value = 'B'

    expect(color.value).toBe('blue')
  })
})
