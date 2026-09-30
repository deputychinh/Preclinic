import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import BaseButton from '@/components/base/BaseButton.vue'

describe('BaseButton', () => {
  it('renders slot content and defaults to a primary, enabled button', () => {
    const wrapper = mount(BaseButton, { slots: { default: 'Save' } })

    expect(wrapper.text()).toBe('Save')
    expect(wrapper.element.tagName).toBe('BUTTON')
    expect(wrapper.classes()).toContain('bg-primary')
    expect(wrapper.attributes('disabled')).toBeUndefined()
  })

  it('disables the button when the disabled prop is true', () => {
    const wrapper = mount(BaseButton, { props: { disabled: true } })

    expect(wrapper.attributes('disabled')).toBeDefined()
  })
})
