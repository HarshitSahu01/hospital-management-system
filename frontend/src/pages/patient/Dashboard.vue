<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'
import { toast } from '../../utils/toastify'


const appointments = ref([])

onMounted(async () => {
  try {
    const response = await api.get('appointments')
    appointments.value = response.data
  } catch (error) {
    toast.error('Failed to load appointments')
  }
})

const cancelAppointment = async (id) => {
    if(!confirm('Are you sure you want to cancel this appointment?')) return
    try {
        await api.put(`appointments/${id}`, { status: 'CANCELLED' })
        toast.success('Appointment cancelled')
        const appt = appointments.value.find(a => a.appointment_id === id)
        if(appt) appt.status = 'CANCELLED'
    } catch (error) {
        toast.error('Failed to cancel appointment')
    }
}
</script>

<template>
  <div>
    <h2 class="fw-bold text-primary mb-4">Patient Dashboard</h2>
    
    <div class="row mb-4">
        <div class="col-md-12">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-white border-bottom py-3 px-4 d-flex justify-content-between align-items-center">
                    <h5 class="fw-bold mb-0 text-secondary">My Appointments</h5>
                    <router-link to="/patient/book" class="btn btn-primary rounded-pill px-4 shadow-sm">
                        <i class="bi bi-plus-lg me-2"></i>Book New
                    </router-link>
                </div>
                <div class="card-body p-0">
                    <div v-if="appointments.length === 0" class="text-center text-muted py-5">
                         <i class="bi bi-journal-medical fs-1 d-block mb-3 text-light"></i>
                        No appointments found.
                    </div>
                    <div v-else class="table-responsive">
                        <table class="table table-hover mb-0 align-middle">
                            <thead class="bg-light">
                                <tr>
                                    <th class="ps-4">Date & Time</th>
                                    <th>Doctor</th>
                                    <th>Department</th>
                                    <th>Status</th>
                                    <th class="text-end pe-4">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="appt in appointments" :key="appt.appointment_id">
                                    <td class="ps-4">
                                        <div class="fw-bold text-dark">{{ appt.date }}</div>
                                        <small class="text-muted">{{ appt.time }}</small>
                                    </td>
                                    <td>
                                        <div class="fw-medium text-primary">{{ appt.doctor_name }}</div>
                                    </td>
                                    <td>
                                        <span class="badge bg-light text-dark border">{{ appt.doctor_dept }}</span>
                                    </td>
                                    <td>
                                        <span :class="{
                                            'badge rounded-pill px-3 py-2': true,
                                            'bg-warning-subtle text-warning-emphasis': appt.status === 'BOOKED',
                                            'bg-success-subtle text-success-emphasis': appt.status === 'COMPLETED',
                                            'bg-danger-subtle text-danger-emphasis': appt.status === 'CANCELLED'
                                        }">{{ appt.status }}</span>
                                    </td>
                                    <td class="text-end pe-4">
                                        <button 
                                            v-if="appt.status === 'BOOKED'" 
                                            class="btn btn-sm btn-outline-danger rounded-pill px-3" 
                                            @click="cancelAppointment(appt.appointment_id)"
                                        >Cancel</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>
