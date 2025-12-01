import axios from 'axios'
import { useUserStore } from '../store/user'
import router from '../router'

const api = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_URL
})

// Request interceptor to add token
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
}, error => {
    return Promise.reject(error)
})

// Response interceptor to handle 401 and refresh token
api.interceptors.response.use(response => {
    return response
}, async error => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true

        try {
            const userStore = useUserStore()
            const success = await userStore.refreshToken()

            if (success) {
                // Update header with new token
                originalRequest.headers.Authorization = `Bearer ${localStorage.getItem('token')}`
                return api(originalRequest)
            }
        } catch (refreshError) {
            // Refresh failed, redirect to login
            const userStore = useUserStore()
            userStore.logout()
            router.push('/login')
        }
    }

    return Promise.reject(error)
})

export default api
