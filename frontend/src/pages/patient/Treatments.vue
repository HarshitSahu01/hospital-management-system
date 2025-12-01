<template>
    <div class="patient-treatments">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold text-primary mb-0">My Treatments</h2>
            <button @click="exportTreatments" class="btn btn-outline-primary">
                <i class="bi bi-download me-2"></i> Export CSV
            </button>
        </div>

        <div class="vstack gap-4">
            <div v-if="treatments.length === 0" class="card border-0 shadow-sm">
                <div class="card-body p-5 text-center text-muted">
                    <i class="bi bi-clipboard-pulse fs-1 mb-3 d-block"></i>
                    <p class="mb-0">No treatments found.</p>
                </div>
            </div>

            <div v-else v-for="t in treatments" :key="t.treatment_id" class="card border-0 shadow-sm">
                <div
                    class="card-header bg-primary-subtle border-0 py-3 d-flex justify-content-between align-items-center">
                    <div>
                        <span class="fw-bold text-primary">Date: {{ t.date }}</span>
                        <span class="mx-2 text-secondary">|</span>
                        <span class="text-dark fw-bold">Dr. {{ t.doctor_name }}</span>
                    </div>
                    <span class="badge bg-white text-primary border border-primary-subtle">ID: #{{ t.treatment_id
                        }}</span>
                </div>

                <div class="card-body p-4">
                    <div class="row g-4">
                        <div class="col-md-6">
                            <h6 class="text-uppercase text-secondary small fw-bold mb-2">Diagnosis</h6>
                            <p class="text-dark mb-0">{{ t.diagnosis }}</p>
                        </div>

                        <div class="col-md-6">
                            <h6 class="text-uppercase text-secondary small fw-bold mb-2">Prescription</h6>
                            <p class="text-dark mb-0" style="white-space: pre-line;">{{ t.prescription }}</p>
                        </div>

                        <div v-if="t.notes" class="col-12">
                            <div class="border-top pt-3 mt-2">
                                <h6 class="text-uppercase text-secondary small fw-bold mb-2">Notes</h6>
                                <p class="text-muted fst-italic mb-0">{{ t.notes }}</p>
                            </div>
                        </div>
                    </div>
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

const fetchTreatments = async () => {
    try {
        // We need to fetch appointments first, then for each completed appointment, fetch treatment.
        // Ideally backend should have an endpoint /api/patient/treatments.
        // But we only have /api/treatments/:appointment_id
        // Let's fetch all appointments for patient, filter COMPLETED, then fetch treatments.

        const apptRes = await api.get('appointments')
        const appointments = apptRes.data
        const completedAppts = appointments.filter(a => a.status === 'COMPLETED')

        const treatmentPromises = completedAppts.map(async (appt) => {
            try {
                const tRes = await api.get(`treatments/${appt.appointment_id}`)
                const tData = tRes.data
                if (tData.treatment_id) {
                    return {
                        ...tData,
                        date: appt.date,
                        doctor_name: appt.doctor_name
                    }
                }
            } catch (e) {
                // Ignore 404s or other errors for individual treatments
                return null
            }
            return null
        })

        const results = await Promise.all(treatmentPromises)
        treatments.value = results.filter(t => t !== null)
    } catch (e) {
        console.error(e)
        toast.error('Failed to fetch treatments')
    }
}

const exportTreatments = async () => {
    try {
        await api.post('export/treatments')
        toast.success('Export started! You will receive a link via Google Chat.')
    } catch (e) {
        console.error(e)
        toast.error('Failed to start export')
    }
}

onMounted(() => {
    fetchTreatments()
})
</script>
