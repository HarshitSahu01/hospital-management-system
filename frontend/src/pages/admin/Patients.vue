<script setup>
import { ref, onMounted, reactive } from 'vue'
import api from '../../services/api'
import { toast } from '../../utils/toastify'
import { Modal } from 'bootstrap'


const patients = ref([])
const loading = ref(false)
let modalInstance = null

const form = reactive({
    name: '',
    email: '',
    password: '',
    gender: '',
    blood_group: '',
    contact_no: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    dob: '',
    isDisabled: false
})

const isEditing = ref(false)
const currentPatientId = ref(null)

onMounted(async () => {
    fetchPatients()
    modalInstance = new Modal(document.getElementById('editPatientModal'))

    document.getElementById('editPatientModal').addEventListener('hidden.bs.modal', () => {
        resetForm()
    })
})

const fetchPatients = async () => {
    try {
        loading.value = true
        const response = await api.get('patients')
        patients.value = response.data
    } catch (error) {
        toast.error('Failed to load patients')
    } finally {
        loading.value = false
    }
}

const submitForm = async () => {
    try {
        if (isEditing.value) {
            const payload = { ...form }
            payload.status = form.isDisabled ? 'DISABLED' : 'ACTIVE'
            delete payload.isDisabled

            await api.put(`patients/${currentPatientId.value}`, payload)
            toast.success('Patient updated successfully')
            modalInstance.hide()
            fetchPatients()
        }
    } catch (error) {
        toast.error(error.response?.data?.msg || 'Failed to update patient')
    }
}

const editPatient = (pat) => {
    isEditing.value = true
    currentPatientId.value = pat.patient_id
    form.name = pat.name
    form.email = pat.email
    form.password = ''
    form.gender = pat.gender
    form.blood_group = pat.blood_group
    form.contact_no = pat.contact_no
    form.address = pat.address
    form.city = pat.city
    form.state = pat.state
    form.zip_code = pat.zip_code
    form.dob = pat.dob
    form.isDisabled = pat.status && pat.status.toUpperCase() === 'DISABLED'
    modalInstance.show()
}

const deletePatient = async (id) => {
    if (!confirm('Are you sure you want to delete this patient?')) return

    try {
        await api.delete(`patients/${id}`)
        toast.success('Patient deleted')
        fetchPatients()
    } catch (error) {
        toast.error('Failed to delete patient')
    }
}

const resetForm = () => {
    isEditing.value = false
    currentPatientId.value = null
    Object.keys(form).forEach(key => form[key] = '')
}
</script>

<template>
    <div>
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold text-primary mb-0">Patients</h2>
        </div>

        <div class="card border-0 shadow-sm">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="bg-light">
                            <tr>
                                <th class="border-0 px-4 py-3">Name</th>
                                <th class="border-0 px-4 py-3">Email</th>
                                <th class="border-0 px-4 py-3">Gender</th>
                                <th class="border-0 px-4 py-3">Blood Group</th>
                                <th class="border-0 px-4 py-3">Status</th>
                                <th class="border-0 px-4 py-3 text-end">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="loading">
                                <td colspan="6" class="text-center py-5">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                </td>
                            </tr>
                            <tr v-else-if="patients.length === 0">
                                <td colspan="6" class="text-center py-5 text-muted">
                                    No patients found
                                </td>
                            </tr>
                            <tr v-else v-for="pat in patients" :key="pat.patient_id">
                                <td class="px-4 py-3">
                                    <div class="d-flex align-items-center">
                                        <div class="avatar-circle bg-success-subtle text-success me-3">
                                            {{ pat.name.charAt(0) }}
                                        </div>
                                        <div>
                                            <div class="fw-bold">{{ pat.name }}</div>
                                            <small class="text-muted">ID: {{ pat.patient_id }}</small>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-4 py-3">{{ pat.email }}</td>
                                <td class="px-4 py-3">{{ pat.gender }}</td>
                                <td class="px-4 py-3"><span class="badge bg-light text-dark border">{{ pat.blood_group
                                }}</span></td>
                                <td class="px-4 py-3">
                                    <span
                                        :class="['badge', pat.status && pat.status.toUpperCase() === 'ACTIVE' ? 'bg-success-subtle text-success' : 'bg-danger-subtle text-danger']">
                                        {{ pat.status ? pat.status.toUpperCase() : 'UNKNOWN' }}
                                    </span>
                                </td>
                                <td class="px-4 py-3 text-end">
                                    <button class="btn btn-sm btn-outline-primary me-2" @click="editPatient(pat)">
                                        <i class="bi bi-pencil me-1"></i> Edit
                                    </button>
                                    <button class="btn btn-sm btn-outline-danger"
                                        @click="deletePatient(pat.patient_id)">
                                        <i class="bi bi-trash me-1"></i> Delete
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>


        <!-- Edit Patient Modal -->
        <div class="modal fade" id="editPatientModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content border-0 shadow">
                    <div class="modal-header border-0 pb-0">
                        <h5 class="modal-title fw-bold">Edit Patient</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="submitForm">
                            <h6 class="fw-bold text-secondary mb-3">Personal Information</h6>
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <label class="form-label">Name</label>
                                    <input type="text" class="form-control" v-model="form.name" required>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Email</label>
                                    <input type="email" class="form-control bg-light" v-model="form.email" disabled>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <label class="form-label">Contact Number</label>
                                    <input type="text" class="form-control" v-model="form.contact_no">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Date of Birth</label>
                                    <input type="date" class="form-control" v-model="form.dob">
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <label class="form-label">Gender</label>
                                    <select class="form-select" v-model="form.gender">
                                        <option value="Male">Male</option>
                                        <option value="Female">Female</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Blood Group</label>
                                    <input type="text" class="form-control" v-model="form.blood_group">
                                </div>
                            </div>

                            <h6 class="fw-bold text-secondary mb-3 mt-4">Address</h6>
                            <div class="mb-3">
                                <label class="form-label">Address</label>
                                <input type="text" class="form-control" v-model="form.address">
                            </div>
                            <div class="row mb-3">
                                <div class="col-md-4">
                                    <label class="form-label">Pincode</label>
                                    <input type="text" class="form-control" v-model="form.zip_code">
                                </div>
                            </div>

                            <div class="mb-3 form-check" v-if="isEditing">
                                <input type="checkbox" class="form-check-input" id="disableUser"
                                    v-model="form.isDisabled">
                                <label class="form-check-label text-danger fw-bold" for="disableUser">Disable User
                                    (Block Login)</label>
                            </div>

                            <div class="d-grid mt-4">
                                <button type="submit" class="btn btn-primary">Update Patient</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.avatar-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}
</style>
