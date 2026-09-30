import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import SignDiffViewer from '@/components/encounter/SignDiffViewer.vue'

// DS-05: this is the one frontend test that directly protects the "no AI content becomes the
// legal record without human review" rule — the sign action must never be reachable before a
// diff has actually rendered.
describe('SignDiffViewer', () => {
  it('disables the sign button until there is content to review', () => {
    const wrapper = mount(SignDiffViewer, { props: { original: '', edited: '' } })

    expect(wrapper.find('button').attributes('disabled')).toBeDefined()
  })

  it('enables the sign button once a draft or edited note exists', () => {
    const wrapper = mount(SignDiffViewer, {
      props: { original: 'AI drafted text', edited: 'Clinician edited text' },
    })

    expect(wrapper.find('button').attributes('disabled')).toBeUndefined()
  })

  it('emits sign when the button is clicked', async () => {
    const wrapper = mount(SignDiffViewer, { props: { original: 'text', edited: 'text' } })

    await wrapper.find('button').trigger('click')

    expect(wrapper.emitted('sign')).toHaveLength(1)
  })
})
