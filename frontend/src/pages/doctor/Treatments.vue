<template>
    <div class="doctor-treatments">
        <div class="d-flex align-items-center mb-4">
            <router-link to="/doctor/appointments" class="text-decoration-none text-primary fw-bold me-3">
                <i class="bi bi-arrow-left"></i> Back
            </router-link>
            <h2 class="fw-bold text-dark mb-0">Treatment Details</h2>
        </div>

        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <div v-else class="row g-4">
            <!-- Appointment Info -->
            <div class="col-md-4">
                <div class="card border-0 shadow-sm h-100">
                    <div class="card-body p-4">
                        <h5 class="fw-bold border-bottom pb-3 mb-3 text-primary">Patient Info</h5>
                        <div class="vstack gap-3">
                            <div>
                                <label class="text-uppercase text-secondary small fw-bold">Patient Name</label>
                                <div class="fw-bold text-dark">{{ appointment.patient_name }}</div>
                            </div>
                            <div>
                                <label class="text-uppercase text-secondary small fw-bold">Date & Time</label>
                                <div class="fw-bold text-dark">{{ appointment.date }} at {{ appointment.time }}</div>
                            </div>
                            <div>
                                <label class="text-uppercase text-secondary small fw-bold">Reason for Visit</label>
                                <div class="fw-bold text-dark">{{ appointment.reason }}</div>
                            </div>
                            <div>
                                <label class="text-uppercase text-secondary small fw-bold">Status</label>
                                <div>
                                    <span :class="[
                                        'badge rounded-pill',
                                        appointment.status === 'BOOKED' ? 'bg-primary-subtle text-primary' :
                                            appointment.status === 'COMPLETED' ? 'bg-success-subtle text-success' :
                                                'bg-danger-subtle text-danger'
                                    ]">
                                        {{ appointment.status }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Treatment Form -->
            <div class="col-md-8">
                <div class="card border-0 shadow-sm">
                    <div class="card-body p-4">
                        <h5 class="fw-bold border-bottom pb-3 mb-3 text-primary">Diagnosis & Prescription</h5>

                        <form @submit.prevent="saveTreatment">
                            <div class="mb-3">
                                <label class="form-label fw-bold">Diagnosis</label>
                                <textarea v-model="form.diagnosis" rows="3" class="form-control"
                                    placeholder="Enter diagnosis..." required></textarea>
                            </div>

                            <div class="mb-3">
                                <label class="form-label fw-bold">Prescription</label>
                                <textarea v-model="form.prescription" rows="4" class="form-control"
                                    placeholder="Enter prescription details..." required></textarea>
                            </div>

                            <div class="mb-4">
                                <label class="form-label fw-bold">Notes</label>
                                <textarea v-model="form.notes" rows="3" class="form-control"
                                    placeholder="Additional notes..."></textarea>
                            </div>

                            <div class="d-flex justify-content-end">
                                <button type="submit" :disabled="saving" class="btn btn-primary px-4 fw-bold">
                                    <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status"
                                        aria-hidden="true"></span>
                                    {{ saving ? 'Saving...' : 'Save Treatment' }}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../../store/user'
import api from '../../services/api'
import { toast } from '../../utils/toastify'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const saving = ref(false)
const appointment = ref({})
const form = ref({
    diagnosis: '',
    prescription: '',
    notes: ''
})

const fetchData = async () => {
    const apptId = route.params.id
    try {
        // Fetch Appointment Details
        const apptRes = await api.get(`appointments/${apptId}`)
        appointment.value = apptRes.data

        // Fetch Existing Treatment (if any)
        const treatRes = await api.get(`treatments/${apptId}`)
        const data = treatRes.data
        if (data.treatment_id) {
            form.value = {
                diagnosis: data.diagnosis || '',
                prescription: data.prescription || '',
                notes: data.notes || ''
            }
        }
    } catch (e) {
        console.error(e)
        toast.error('Failed to load data')
    } finally {
        loading.value = false
    }
}

const saveTreatment = async () => {
    saving.value = true
    try {
        await api.post('treatments', {
            appointment_id: appointment.value.appointment_id,
            ...form.value
        })

        toast.success('Treatment saved successfully')
        // Optionally redirect back
        // router.push('/doctor/appointments')
    } catch (e) {
        console.error(e)
        toast.error('Error saving treatment')
    } finally {
        saving.value = false
    }
}

onMounted(() => {
    fetchData()
})
</script>
