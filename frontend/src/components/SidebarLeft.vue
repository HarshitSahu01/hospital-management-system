<script setup>
import { useUserStore } from '../store/user'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const userStore = useUserStore()
const route = useRoute()
const role = computed(() => userStore.user?.role)

const isActive = (path) => route.path.startsWith(path)
</script>

<template>
  <div class="sidebar-container d-flex flex-column flex-shrink-0 bg-white shadow-sm h-100">
    <div class="p-4">
      <small class="text-uppercase text-muted fw-bold ls-1">Menu</small>
    </div>
    <ul class="nav nav-pills flex-column px-3 mb-auto">

      <!-- Admin Links -->
      <template v-if="role === 'ADMIN'">
        <li class="nav-item mb-1">
          <router-link to="/admin" class="nav-link d-flex align-items-center"
            :class="{ active: route.path === '/admin' }">
            <i class="bi bi-grid-1x2-fill me-3"></i> Dashboard
          </router-link>
        </li>
        <li class="nav-item mb-1">
          <router-link to="/admin/doctors" class="nav-link d-flex align-items-center"
            :class="{ active: isActive('/admin/doctors') }">
            <i class="bi bi-person-badge-fill me-3"></i> Doctors
          </router-link>
        </li>
        <li class="nav-item mb-1">
          <router-link to="/admin/patients" class="nav-link d-flex align-items-center"
            :class="{ active: isActive('/admin/patients') }">
            <i class="bi bi-people-fill me-3"></i> Patients
          </router-link>
        </li>
        <li class="nav-item mb-1">
          <router-link to="/admin/departments" class="nav-link d-flex align-items-center"
            :class="{ active: isActive('/admin/departments') }">
            <i class="bi bi-building-fill me-3"></i> Departments
          </router-link>
        </li>
        <li class="nav-item mb-1">
          <router-link to="/admin/appointments" class="nav-link d-flex align-items-center"
            :class="{ active: isActive('/admin/appointments') }">
            <i class="bi bi-calendar-check-fill me-3"></i> Appointments
          </router-link>
        </li>
        <li class="nav-item mb-1">
          <router-link to="/admin/report" class="nav-link d-flex align-items-center"
            :class="{ active: isActive('/admin/report') }">
            <i class="bi bi-bar-chart-fill me-3"></i> Reports
          </router-link>
        </li>
      </template>

      <!-- Doctor Links -->
      <template v-if="role === 'DOCTOR'">
        <li class="nav-item mb-1">
          <router-link to="/doctor" class="nav-link d-flex align-items-center"
            :class="{ active: route.path === '/doctor' }">
            <i class="bi bi-grid-1x2-fill me-3"></i> Dashboard
          </router-link>
        </li>
        <li class="nav-item mb-1">
          <router-link to="/doctor/appointments" class="nav-link d-flex align-items-center"
            :class="{ active: isActive('/doctor/appointments') }">
            <i class="bi bi-calendar-check-fill me-3"></i> Appointments
          </router-link>
        </li>
        <li class="nav-item mb-1">
          <router-link to="/doctor/treatments" class="nav-link d-flex align-items-center"
            :class="{ active: isActive('/doctor/treatments') }">
            <i class="bi bi-clipboard-pulse me-3"></i> Treatments
          </router-link>
        </li>
        <li class="nav-item mb-1">
          <router-link to="/doctor/profile" class="nav-link d-flex align-items-center"
            :class="{ active: isActive('/doctor/profile') }">
            <i class="bi bi-person-circle me-3"></i> Profile
          </router-link>
        </li>
      </template>

      <!-- Patient Links -->
      <template v-if="role === 'PATIENT'">
        <li class="nav-item mb-1">
          <router-link to="/patient" class="nav-link d-flex align-items-center"
            :class="{ active: route.path === '/patient' }">
            <i class="bi bi-grid-1x2-fill me-3"></i> Dashboard
          </router-link>
        </li>
        <li class="nav-item mb-1">
          <router-link to="/patient/appointments" class="nav-link d-flex align-items-center"
            :class="{ active: isActive('/patient/appointments') }">
            <i class="bi bi-calendar-plus-fill me-3"></i> Appointments
          </router-link>
        </li>
        <li class="nav-item mb-1">
          <router-link to="/patient/treatments" class="nav-link d-flex align-items-center"
            :class="{ active: isActive('/patient/treatments') }">
            <i class="bi bi-clipboard-pulse me-3"></i> Treatments
          </router-link>
        </li>
        <li class="nav-item mb-1">
          <router-link to="/patient/profile" class="nav-link d-flex align-items-center"
            :class="{ active: isActive('/patient/profile') }">
            <i class="bi bi-person-circle me-3"></i> Profile
          </router-link>
        </li>
      </template>

    </ul>
    <div class="p-4 mt-auto border-top">
      <div class="d-flex align-items-center text-muted">
        <small>© 2025 HMS</small>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sidebar-container {
  width: 260px;
  position: fixed;
  top: 64px;
  /* Height of navbar */
  bottom: 0;
  left: 0;
  z-index: 100;
  border-right: 1px solid #e2e8f0;
}

.ls-1 {
  letter-spacing: 0.1em;
  font-size: 0.75rem;
}

.nav-link {
  color: var(--text-muted);
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background-color: #f1f5f9;
  color: var(--primary-color);
}

.nav-link.active {
  background-color: rgba(37, 99, 235, 0.1);
  color: var(--primary-color);
}

.nav-link i {
  font-size: 1.1rem;
}
</style>
