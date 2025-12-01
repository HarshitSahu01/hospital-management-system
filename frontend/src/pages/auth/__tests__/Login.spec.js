import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Login from '../Login.vue'
import { createTestingPinia } from '@pinia/testing'

// Mock router
const mockPush = vi.fn()
vi.mock('vue-router', () => ({
    useRouter: () => ({
        push: mockPush
    })
}))

describe('Login.vue', () => {
    it('renders login form', () => {
        const wrapper = mount(Login, {
            global: {
                plugins: [createTestingPinia()]
            }
        })
        expect(wrapper.find('h3').text()).toBe('Login')
        expect(wrapper.find('input[type="email"]').exists()).toBe(true)
        expect(wrapper.find('input[type="password"]').exists()).toBe(true)
        expect(wrapper.find('button').text()).toBe('Login')
    })

    it('updates v-model inputs', async () => {
        const wrapper = mount(Login, {
            global: {
                plugins: [createTestingPinia()]
            }
        })

        const emailInput = wrapper.find('input[type="email"]')
        await emailInput.setValue('test@example.com')
        expect(emailInput.element.value).toBe('test@example.com')

        const passwordInput = wrapper.find('input[type="password"]')
        await passwordInput.setValue('password')
        expect(passwordInput.element.value).toBe('password')
    })
})
