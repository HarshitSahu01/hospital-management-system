<script setup>
import { ref } from 'vue'
import { useUserStore } from '../../store/user'
import { useRouter } from 'vue-router'
import { toast } from '../../utils/toastify'

const name = ref('')
const email = ref('')
const password = ref('')
const contact_no = ref('')
const gender = ref('Male')
const date_of_birth = ref('')
const address = ref('')
const city = ref('')
const state = ref('')
const zip_code = ref('')

const userStore = useUserStore()
const router = useRouter()
const isLoading = ref(false)

const handleRegister = async () => {
  isLoading.value = true
  const data = {
    name: name.value,
    email: email.value,
    password: password.value,
    contact_no: contact_no.value,
    gender: gender.value,
    date_of_birth: date_of_birth.value,
    address: address.value,
    city: city.value,
    state: state.value,
    zip_code: zip_code.value
  }
  
  const result = await userStore.register(data)
  isLoading.value = false
  
  if (result.success) {
    toast.success('Registration successful! Please login.')
    router.push('/login')
  } else {
    toast.error(result.message)
  }
}
</script>

<template>
  <div class="auth-container d-flex justify-content-center align-items-center min-vh-100 py-5">
    <div class="card auth-card shadow-lg border-0">
      <div class="card-body p-5">
        <div class="text-center mb-4">
            <h3 class="fw-bold text-primary mb-1">Create Account</h3>
            <p class="text-muted">Join AyurBase as a Patient</p>
        </div>
        
        <form @submit.prevent="handleRegister">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label small text-muted text-uppercase fw-bold">Full Name</label>
              <input type="text" class="form-control bg-light" v-model="name" required>
            </div>
            <div class="col-md-6">
              <label class="form-label small text-muted text-uppercase fw-bold">Email</label>
              <input type="email" class="form-control bg-light" v-model="email" required>
            </div>
            
            <div class="col-md-6">
              <label class="form-label small text-muted text-uppercase fw-bold">Password</label>
              <input type="password" class="form-control bg-light" v-model="password" required>
            </div>
            <div class="col-md-6">
              <label class="form-label small text-muted text-uppercase fw-bold">Contact No</label>
              <input type="text" class="form-control bg-light" v-model="contact_no">
            </div>

            <div class="col-md-6">
              <label class="form-label small text-muted text-uppercase fw-bold">Gender</label>
              <select class="form-select bg-light" v-model="gender">
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label small text-muted text-uppercase fw-bold">Date of Birth</label>
              <input type="date" class="form-control bg-light" v-model="date_of_birth">
            </div>

            <div class="col-12">
              <label class="form-label small text-muted text-uppercase fw-bold">Address</label>
              <input type="text" class="form-control bg-light" v-model="address">
            </div>

            <div class="col-md-4">
              <label class="form-label small text-muted text-uppercase fw-bold">City</label>
              <input type="text" class="form-control bg-light" v-model="city">
            </div>
            <div class="col-md-4">
              <label class="form-label small text-muted text-uppercase fw-bold">State</label>
              <input type="text" class="form-control bg-light" v-model="state">
            </div>
            <div class="col-md-4">
              <label class="form-label small text-muted text-uppercase fw-bold">Zip Code</label>
              <input type="number" maxlength="6" minlength="6" class="form-control bg-light" v-model="zip_code">
            </div>
          </div>

          <div class="d-grid mt-4">
            <button type="submit" class="btn btn-primary btn-lg shadow-sm" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                {{ isLoading ? 'Creating Account...' : 'Register' }}
            </button>
          </div>
        </form>
        <div class="text-center mt-4 pt-2 border-top">
          <small class="text-muted">Already have an account? <router-link to="/login" class="text-primary fw-bold text-decoration-none">Sign In</router-link></small>
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
    max-width: 700px;
    border-radius: 1.5rem;
}

.form-control:focus, .form-select:focus {
    background-color: #fff;
}
</style>
