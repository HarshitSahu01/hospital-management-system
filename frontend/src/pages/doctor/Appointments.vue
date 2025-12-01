<template>
    <div class="doctor-appointments">
        <h2 class="fw-bold text-primary mb-4">My Appointments</h2>

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
                                <th class="border-0 px-4 py-3 text-secondary text-uppercase small fw-bold">Patient</th>
                                <th class="border-0 px-4 py-3 text-secondary text-uppercase small fw-bold">Reason</th>
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
                                    <router-link :to="`/patient/profile/${appt.patient_id}`"
                                        class="fw-bold text-decoration-none text-dark hover-link">
                                        {{ appt.patient_name }}
                                    </router-link>
                                </td>
                                <td class="px-4 py-3">
                                    <div class="text-secondary text-truncate" style="max-width: 200px;">{{ appt.reason
                                    }}</div>
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
                                    <router-link v-if="appt.status !== 'CANCELLED'"
                                        :to="`/doctor/treatments/${appt.appointment_id}`"
                                        class="btn btn-sm btn-outline-success me-2">
                                        Treat
                                    </router-link>
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
import { useUserStore } from '../../store/user'
import api from '../../services/api'
import { toast } from '../../utils/toastify'

const userStore = useUserStore()
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
