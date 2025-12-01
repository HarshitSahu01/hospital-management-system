<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'
import { toast } from '../../utils/toastify'


const history = ref([])

onMounted(async () => {
  try {
    const response = await api.get('appointments')
    history.value = response.data.filter(a => a.status === 'COMPLETED' || a.status === 'CANCELLED')
  } catch (error) {
    toast.error('Failed to load history')
  }
})
</script>

<template>
  <div>
    <h2 class="fw-bold text-primary mb-4">Appointment History</h2>
    
    <div class="card border-0 shadow-sm">
        <div class="card-body p-0">
            <div v-if="history.length === 0" class="text-center text-muted py-5">
                <i class="bi bi-clock-history fs-1 d-block mb-3 text-light"></i>
                No history found.
            </div>
            <div v-else class="table-responsive">
                <table class="table table-hover mb-0 align-middle">
                    <thead class="bg-light">
                        <tr>
                            <th class="ps-4">Date</th>
                            <th>Doctor</th>
                            <th>Department</th>
                            <th>Status</th>
                            <th>Reason</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="appt in history" :key="appt.appointment_id">
                            <td class="ps-4 fw-bold text-dark">{{ appt.date }}</td>
                            <td>{{ appt.doctor_name }}</td>
                            <td><span class="badge bg-light text-dark border">{{ appt.doctor_dept }}</span></td>
                            <td>
                                <span :class="{
                                    'badge rounded-pill px-3 py-2': true,
                                    'bg-success-subtle text-success-emphasis': appt.status === 'COMPLETED',
                                    'bg-danger-subtle text-danger-emphasis': appt.status === 'CANCELLED'
                                }">{{ appt.status }}</span>
                            </td>
                            <td class="text-muted">{{ appt.reason }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
  </div>
</template>
