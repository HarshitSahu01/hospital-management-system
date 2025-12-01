<script setup>
import { ref } from 'vue'
import { useUserStore } from '../../store/user'
import { useRouter } from 'vue-router'
import { toast } from '../../utils/toastify'

const email = ref('')
const password = ref('')
const userStore = useUserStore()
const router = useRouter()
const isLoading = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  const result = await userStore.login(email.value, password.value)
  isLoading.value = false
  
  if (result.success) {
    toast.success('Welcome back!')
    const role = userStore.user.role
    if (role === 'ADMIN') router.push('/admin')
    else if (role === 'DOCTOR') router.push('/doctor')
    else router.push('/patient')
  } else {
    toast.error(result.message)
  }
}
</script>

<template>
  <div class="auth-container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card auth-card shadow-lg border-0">
      <div class="card-body p-5">
        <div class="text-center mb-5">
            <div class="icon-circle bg-primary-subtle text-primary mx-auto mb-3">
                <i class="bi bi-heart-pulse-fill fs-3"></i>
            </div>
            <h3 class="fw-bold text-primary mb-1">Welcome Back</h3>
            <p class="text-muted">Sign in to your account</p>
        </div>
        
        <form @submit.prevent="handleLogin">
          <div class="mb-4">
            <label for="email" class="form-label fw-medium text-muted small text-uppercase ls-1">Email address</label>
            <div class="input-group">
                <span class="input-group-text bg-light border-end-0 text-muted"><i class="bi bi-envelope"></i></span>
                <input type="email" class="form-control bg-light border-start-0 ps-0" id="email" v-model="email" placeholder="name@example.com" required>
            </div>
          </div>
          <div class="mb-4">
            <label for="password" class="form-label fw-medium text-muted small text-uppercase ls-1">Password</label>
            <div class="input-group">
                <span class="input-group-text bg-light border-end-0 text-muted"><i class="bi bi-lock"></i></span>
                <input type="password" class="form-control bg-light border-start-0 ps-0" id="password" v-model="password" placeholder="••••••••" required>
            </div>
          </div>
          <div class="d-grid pt-2">
            <button type="submit" class="btn btn-primary btn-lg shadow-sm" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                {{ isLoading ? 'Signing in...' : 'Sign In' }}
            </button>
          </div>
        </form>
        <div class="text-center mt-4 pt-2 border-top">
          <small class="text-muted">Don't have an account? <router-link to="/register" class="text-primary fw-bold text-decoration-none">Create Account</router-link></small>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
}

.auth-card {
    width: 100%;
    max-width: 420px;
    border-radius: 1.5rem;
}

.icon-circle {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.ls-1 {
    letter-spacing: 0.05em;
}

.form-control:focus {
    box-shadow: none;
    background-color: #fff;
}

.input-group-text {
    border-color: #cbd5e1;
}

.form-control {
    border-color: #cbd5e1;
}

.input-group:focus-within .input-group-text,
.input-group:focus-within .form-control {
    border-color: var(--primary-color);
    background-color: #fff;
}
</style>
