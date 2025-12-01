<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'
import { toast } from '../../utils/toastify'


const appointments = ref([])

onMounted(async () => {
    try {
        const response = await api.get('appointments')
        appointments.value = response.data.filter(a => a.status === 'BOOKED')
    } catch (error) {
        toast.error('Failed to load appointments')
    }
})

const updateStatus = async (id, status) => {
    try {
        await api.put(`appointments/${id}`, { status })
        toast.success('Appointment updated')
        appointments.value = appointments.value.filter(a => a.appointment_id !== id)
    } catch (error) {
        toast.error('Failed to update appointment')
    }
}
</script>

<template>
    <div>
        <h2 class="fw-bold text-primary mb-4">Doctor Dashboard</h2>

        <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom py-3 px-4 d-flex justify-content-between align-items-center">
                <h5 class="fw-bold mb-0 text-secondary"><i class="bi bi-calendar-event me-2"></i>Upcoming Appointments
                </h5>
                <div class="d-flex align-items-center">
                    <router-link to="/doctor/schedule" class="btn btn-outline-primary btn-sm me-3">
                        <i class="bi bi-clock me-1"></i> Manage Availability
                    </router-link>
                    <span class="badge bg-primary-subtle text-primary rounded-pill">{{ appointments.length }}
                        Pending</span>
                </div>
            </div>
            <div class="card-body p-0">
                <div v-if="appointments.length === 0" class="text-center text-muted py-5">
                    <i class="bi bi-calendar-x fs-1 d-block mb-3 text-light"></i>
                    No upcoming appointments.
                </div>
                <div v-else class="table-responsive">
                    <table class="table table-hover mb-0 align-middle">
                        <thead class="bg-light">
                            <tr>
                                <th class="ps-4">Date & Time</th>
                                <th>Patient</th>
                                <th>Reason</th>
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
                                    <div class="d-flex align-items-center">
                                        <div class="avatar-circle bg-primary-subtle text-primary me-2">
                                            {{ appt.patient_name.charAt(0) }}
                                        </div>
                                        <span class="fw-medium">{{ appt.patient_name }}</span>
                                    </div>
                                </td>
                                <td>{{ appt.reason }}</td>
                                <td class="text-end pe-4">
                                    <router-link :to="`/doctor/treatments/${appt.appointment_id}`"
                                        class="btn btn-sm btn-success me-2 rounded-pill px-3">
                                        <i class="bi bi-clipboard-pulse me-1"></i> Treat
                                    </router-link>
                                    <button class="btn btn-sm btn-outline-danger rounded-pill px-3"
                                        @click="updateStatus(appt.appointment_id, 'CANCELLED')">
                                        <i class="bi bi-x-lg me-1"></i> Cancel
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.avatar-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 0.8rem;
}
</style>
