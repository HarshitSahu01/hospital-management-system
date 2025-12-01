import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Toast from '../Toast.vue'
import { toast } from '../../utils/toastify'

describe('Toast.vue', () => {
    it('renders nothing initially', () => {
        const wrapper = mount(Toast)
        expect(wrapper.findAll('.toast').length).toBe(0)
    })

    it('renders a toast when added', async () => {
        const wrapper = mount(Toast)
        toast.success('Test Message')
        await wrapper.vm.$nextTick()
        expect(wrapper.text()).toContain('Test Message')
        expect(wrapper.findAll('.toast').length).toBe(1)
    })
})
