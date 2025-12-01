<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'
import { toast } from '../../utils/toastify'


const appointments = ref([])
const loading = ref(false)

onMounted(async () => {
    fetchAppointments()
})

const fetchAppointments = async () => {
    try {
        loading.value = true
        const response = await api.get('appointments')
        appointments.value = response.data
    } catch (error) {
        toast.error('Failed to load appointments')
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div>
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold text-primary mb-0">Appointments</h2>
        </div>

        <div class="card border-0 shadow-sm">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="bg-light">
                            <tr>
                                <th class="border-0 px-4 py-3">ID</th>
                                <th class="border-0 px-4 py-3">Patient</th>
                                <th class="border-0 px-4 py-3">Doctor</th>
                                <th class="border-0 px-4 py-3">Department</th>
                                <th class="border-0 px-4 py-3">Date & Time</th>
                                <th class="border-0 px-4 py-3">Status</th>
                                <th class="border-0 px-4 py-3">Reason</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="loading">
                                <td colspan="7" class="text-center py-5">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                </td>
                            </tr>
                            <tr v-else-if="appointments.length === 0">
                                <td colspan="7" class="text-center py-5 text-muted">
                                    No appointments found
                                </td>
                            </tr>
                            <tr v-else v-for="appt in appointments" :key="appt.appointment_id">
                                <td class="px-4 py-3">#{{ appt.appointment_id }}</td>
                                <td class="px-4 py-3 fw-bold">{{ appt.patient_name }}</td>
                                <td class="px-4 py-3">{{ appt.doctor_name }}</td>
                                <td class="px-4 py-3"><span class="badge bg-light text-dark border">{{ appt.doctor_dept
                                        }}</span></td>
                                <td class="px-4 py-3">
                                    <div>{{ appt.date }}</div>
                                    <small class="text-muted">{{ appt.time }}</small>
                                </td>
                                <td class="px-4 py-3">
                                    <span :class="{
                                        'badge': true,
                                        'bg-warning-subtle text-warning': appt.status === 'BOOKED',
                                        'bg-success-subtle text-success': appt.status === 'COMPLETED',
                                        'bg-danger-subtle text-danger': appt.status === 'CANCELLED'
                                    }">
                                        {{ appt.status }}
                                    </span>
                                </td>
                                <td class="px-4 py-3 text-muted small">{{ appt.reason }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>
