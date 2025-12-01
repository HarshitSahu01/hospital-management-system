<script setup>
import { useUserStore } from '../store/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="navbar navbar-expand-lg sticky-top glass-nav">
    <div class="container-fluid px-4">
      <a class="navbar-brand fw-bold d-flex align-items-center" href="#">
        <div class="brand-icon me-2">
          <i class="bi bi-heart-pulse-fill text-white"></i>
        </div>
        <span class="text-white tracking-tight">AyurBase</span>
      </a>
      <button class="navbar-toggler border-0 text-white" type="button" data-bs-toggle="collapse"
        data-bs-target="#navbarNav">
        <i class="bi bi-list fs-4"></i>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center">
          <li class="nav-item" v-if="userStore.isAuthenticated">
            <div class="d-flex align-items-center text-white-50 me-3">
              <i class="bi bi-person-circle fs-5 me-2"></i>
              <span class="text-white fw-medium">{{ userStore.user?.name }}</span>
              <span class="badge bg-white text-primary ms-2 rounded-pill">{{ userStore.user?.role }}</span>
            </div>
          </li>
          <li class="nav-item" v-if="userStore.isAuthenticated">
            <button class="btn btn-light btn-sm rounded-pill px-3 fw-bold text-primary" @click="logout">
              Logout
            </button>
          </li>
          <li class="nav-item" v-else>
            <router-link to="/login"
              class="btn btn-light btn-sm rounded-pill px-4 fw-bold text-primary">Login</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.glass-nav {
  background: rgba(37, 99, 235, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  height: 64px;
  transition: all 0.3s ease;
  z-index: 1040;
}

.brand-icon {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tracking-tight {
  letter-spacing: -0.025em;
}
</style>
