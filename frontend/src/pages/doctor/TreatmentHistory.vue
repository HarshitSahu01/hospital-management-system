<template>
    <div class="doctor-treatment-history">
        <h2 class="fw-bold text-primary mb-4">Treatment History</h2>

        <div class="card border-0 shadow-sm">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="bg-light">
                            <tr>
                                <th class="border-0 px-4 py-3">Date</th>
                                <th class="border-0 px-4 py-3">Patient</th>
                                <th class="border-0 px-4 py-3">Diagnosis</th>
                                <th class="border-0 px-4 py-3">Prescription</th>
                                <th class="border-0 px-4 py-3 text-end">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="loading">
                                <td colspan="5" class="text-center py-5">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                </td>
                            </tr>
                            <tr v-else-if="treatments.length === 0">
                                <td colspan="5" class="text-center py-5 text-muted">
                                    No treatments found
                                </td>
                            </tr>
                            <tr v-else v-for="t in treatments" :key="t.appointment_id">
                                <td class="px-4 py-3">
                                    <div class="fw-bold">{{ t.date }}</div>
                                    <small class="text-muted">{{ t.time }}</small>
                                </td>
                                <td class="px-4 py-3">
                                    <div class="fw-bold">{{ t.patient_name }}</div>
                                </td>
                                <td class="px-4 py-3 text-truncate" style="max-width: 200px;">
                                    {{ t.treatment?.diagnosis || '-' }}
                                </td>
                                <td class="px-4 py-3 text-truncate" style="max-width: 200px;">
                                    {{ t.treatment?.prescription || '-' }}
                                </td>
                                <td class="px-4 py-3 text-end">
                                    <router-link :to="`/doctor/treatments/${t.appointment_id}`"
                                        class="btn btn-sm btn-outline-primary">
                                        <i class="bi bi-eye me-1"></i> View Details
                                    </router-link>
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
const treatments = ref([])
const loading = ref(false)

const fetchTreatments = async () => {
    try {
        loading.value = true
        const res = await api.get('appointments')
        const allAppointments = res.data
        // Filter for appointments that are completed or have treatment details
        treatments.value = allAppointments.filter(a => a.status === 'COMPLETED' || a.treatment)
    } catch (e) {
        console.error(e)
        toast.error('Failed to fetch treatments')
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchTreatments()
})
</script>
