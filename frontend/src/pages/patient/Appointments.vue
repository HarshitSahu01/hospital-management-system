<template>
    <div class="patient-appointments">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold text-primary mb-0">My Appointments</h2>
            <router-link to="/patient/book" class="btn btn-primary fw-bold">
                <i class="bi bi-plus-lg me-1"></i> Book New Appointment
            </router-link>
        </div>

        <!-- Appointments List -->
        <div class="card border-0 shadow-sm">
            <div class="card-body p-0">
                <div v-if="appointments.length === 0" class="p-5 text-center text-muted">
                    <i class="bi bi-calendar-x fs-1 mb-3 d-block"></i>
                    <p class="mb-0">No appointments found.</p>
                </div>
                <div v-else class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="bg-light">
                            <tr>
                                <th class="border-0 px-4 py-3 text-secondary text-uppercase small fw-bold">Date & Time
                                </th>
                                <th class="border-0 px-4 py-3 text-secondary text-uppercase small fw-bold">Doctor</th>
                                <th class="border-0 px-4 py-3 text-secondary text-uppercase small fw-bold">Department
                                </th>
                                <th class="border-0 px-4 py-3 text-secondary text-uppercase small fw-bold">Status</th>
                                <th class="border-0 px-4 py-3 text-secondary text-uppercase small fw-bold text-end">
                                    Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="appt in appointments" :key="appt.appointment_id">
                                <td class="px-4 py-3">
                                    <div class="fw-bold text-dark">{{ appt.date }}</div>
                                    <div class="small text-muted">{{ appt.time }}</div>
                                </td>
                                <td class="px-4 py-3">
                                    <router-link :to="`/doctor/profile/${appt.doctor_id}`"
                                        class="fw-bold text-decoration-none text-dark hover-link">
                                        {{ appt.doctor_name }}
                                    </router-link>
                                </td>
                                <td class="px-4 py-3">
                                    <span class="text-secondary">{{ appt.doctor_dept }}</span>
                                </td>
                                <td class="px-4 py-3">
                                    <span :class="[
                                        'badge rounded-pill',
                                        appt.status === 'BOOKED' ? 'bg-primary-subtle text-primary' :
                                            appt.status === 'COMPLETED' ? 'bg-success-subtle text-success' :
                                                'bg-danger-subtle text-danger'
                                    ]">
                                        {{ appt.status }}
                                    </span>
                                </td>
                                <td class="px-4 py-3 text-end">
                                    <button v-if="appt.status === 'BOOKED'"
                                        @click="cancelAppointment(appt.appointment_id)"
                                        class="btn btn-sm btn-outline-danger">
                                        Cancel
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

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'
import { toast } from '../../utils/toastify'

const appointments = ref([])

const fetchAppointments = async () => {
    try {
        const res = await api.get('appointments')
        appointments.value = res.data
    } catch (e) {
        console.error(e)
        toast.error('Failed to fetch appointments')
    }
}

const cancelAppointment = async (id) => {
    if (!confirm('Are you sure you want to cancel this appointment?')) return

    try {
        await api.put(`appointments/${id}`, { status: 'CANCELLED' })
        toast.success('Appointment cancelled')
        fetchAppointments()
    } catch (e) {
        console.error(e)
        toast.error('Error cancelling appointment')
    }
}

onMounted(() => {
    fetchAppointments()
})
</script>
