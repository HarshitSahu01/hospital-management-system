import { defineStore } from 'pinia'
import api from '../services/api'
import axios from 'axios' // Still needed for initial login if we want to avoid circular dep issues or just use api?
// Actually, we can use api for login too.

export const useUserStore = defineStore('user', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: JSON.parse(localStorage.getItem('user')) || null,
        isAuthenticated: !!localStorage.getItem('token')
    }),
    actions: {
        async login(email, password) {
            try {
                // We use a direct axios call for login to avoid interceptor loops if something is weird, 
                // but using 'api' is also fine as long as we don't have a token yet.
                // However, to be safe and clean, let's use the api instance.
                const response = await api.post('auth/login', { email, password })
                this.token = response.data.access_token
                this.user = response.data.user
                this.isAuthenticated = true

                localStorage.setItem('token', this.token)
                localStorage.setItem('refresh_token', response.data.refresh_token)
                localStorage.setItem('user', JSON.stringify(this.user))

                return { success: true }
            } catch (error) {
                return { success: false, message: error.response?.data?.msg || 'Login failed' }
            }
        },
        async register(data) {
            try {
                await api.post('auth/register', data)
                return { success: true }
            } catch (error) {
                return { success: false, message: error.response?.data?.msg || 'Registration failed' }
            }
        },
        async refreshToken() {
            try {
                const refreshToken = localStorage.getItem('refresh_token')
                if (!refreshToken) return false

                // We need to make a call WITHOUT the access token interceptor potentially interfering,
                // or we need to manually set the Authorization header to the refresh token?
                // The backend expects: @jwt_required(refresh=True) which looks for Authorization: Bearer <refresh_token>

                // We can create a temporary axios instance or just override headers
                const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/auth/refresh`, {}, {
                    headers: {
                        'Authorization': `Bearer ${refreshToken}`
                    }
                })

                this.token = response.data.access_token
                localStorage.setItem('token', this.token)
                return true
            } catch (error) {
                this.logout()
                return false
            }
        },
        logout() {
            this.token = null
            this.user = null
            this.isAuthenticated = false
            localStorage.removeItem('token')
            localStorage.removeItem('refresh_token')
            localStorage.removeItem('user')
        }
    }
})

