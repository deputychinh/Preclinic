import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import BaseBadge from '@/components/base/BaseBadge.vue'

describe('BaseBadge', () => {
  it('renders the label and applies the given color as a CSS variable', () => {
    const wrapper = mount(BaseBadge, { props: { label: 'SIGNED', color: '#2e9e6c' } })

    expect(wrapper.text()).toBe('SIGNED')
    expect(wrapper.attributes('style')).toContain('rgb(46, 158, 108)')
  })
})
