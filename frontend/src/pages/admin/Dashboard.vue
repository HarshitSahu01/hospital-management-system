<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'
import { toast } from '../../utils/toastify'
import Chart from 'chart.js/auto'


const stats = ref({ doctors: 0, patients: 0, appointments: 0, departments: 0 })

onMounted(async () => {
  try {
    const response = await api.get('admin/stats')
    stats.value = response.data

    renderChart()
  } catch (error) {
    toast.error('Failed to load stats')
  }
})

const renderChart = () => {
  const ctx = document.getElementById('statsChart')
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Doctors', 'Patients', 'Appointments', 'Departments'],
      datasets: [{
        data: [stats.value.doctors, stats.value.patients, stats.value.appointments, stats.value.departments],
        backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#6366f1'],
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            usePointStyle: true,
            padding: 20
          }
        }
      },
      cutout: '70%'
    }
  })
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold text-primary mb-0">Admin Dashboard</h2>
      <span class="text-muted">{{ new Date().toLocaleDateString() }}</span>
    </div>

    <div class="row g-4 mb-4">
      <div class="col-md-3">
        <div class="card h-100 border-0 shadow-sm stat-card">
          <div class="card-body d-flex align-items-center">
            <div class="icon-box bg-blue-100 text-blue-600 me-3">
              <i class="bi bi-person-badge-fill fs-4"></i>
            </div>
            <div>
              <h6 class="text-muted text-uppercase small fw-bold mb-1">Doctors</h6>
              <h3 class="fw-bold mb-0">{{ stats.doctors }}</h3>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card h-100 border-0 shadow-sm stat-card">
          <div class="card-body d-flex align-items-center">
            <div class="icon-box bg-green-100 text-green-600 me-3">
              <i class="bi bi-people-fill fs-4"></i>
            </div>
            <div>
              <h6 class="text-muted text-uppercase small fw-bold mb-1">Patients</h6>
              <h3 class="fw-bold mb-0">{{ stats.patients }}</h3>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card h-100 border-0 shadow-sm stat-card">
          <div class="card-body d-flex align-items-center">
            <div class="icon-box bg-yellow-100 text-yellow-600 me-3">
              <i class="bi bi-calendar-check-fill fs-4"></i>
            </div>
            <div>
              <h6 class="text-muted text-uppercase small fw-bold mb-1">Appointments</h6>
              <h3 class="fw-bold mb-0">{{ stats.appointments }}</h3>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card h-100 border-0 shadow-sm stat-card">
          <div class="card-body d-flex align-items-center">
            <div class="icon-box bg-indigo-100 text-indigo-600 me-3">
              <i class="bi bi-building-fill fs-4"></i>
            </div>
            <div>
              <h6 class="text-muted text-uppercase small fw-bold mb-1">Departments</h6>
              <h3 class="fw-bold mb-0">{{ stats.departments }}</h3>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-8">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-0 pt-4 px-4">
            <h5 class="fw-bold mb-0">Hospital Overview</h5>
          </div>
          <div class="card-body p-4">
            <div style="height: 300px;">
              <canvas id="statsChart"></canvas>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100 bg-primary text-white position-relative overflow-hidden">
          <div class="card-body p-4 d-flex flex-column justify-content-center">
            <h4 class="fw-bold mb-3">Quick Actions</h4>
            <div class="d-grid gap-2">
              <router-link to="/admin/doctors" class="btn btn-light text-primary fw-bold text-start"><i
                  class="bi bi-plus-circle me-2"></i> Add Doctor</router-link>
              <router-link to="/admin/departments" class="btn btn-light text-primary fw-bold text-start"><i
                  class="bi bi-building-add me-2"></i> Add Department</router-link>
              <router-link to="/admin/appointments" class="btn btn-outline-light fw-bold text-start"><i
                  class="bi bi-file-earmark-text me-2"></i> View Reports</router-link>
            </div>
          </div>
          <i class="bi bi-hospital position-absolute text-white-50"
            style="font-size: 10rem; right: -2rem; bottom: -2rem; opacity: 0.2;"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.icon-box {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-blue-100 {
  background-color: #dbeafe;
}

.text-blue-600 {
  color: #2563eb;
}

.bg-green-100 {
  background-color: #d1fae5;
}

.text-green-600 {
  color: #059669;
}

.bg-yellow-100 {
  background-color: #fef3c7;
}

.text-yellow-600 {
  color: #d97706;
}

.bg-indigo-100 {
  background-color: #e0e7ff;
}

.text-indigo-600 {
  color: #4f46e5;
}

.stat-card {
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-5px);
}
</style>
