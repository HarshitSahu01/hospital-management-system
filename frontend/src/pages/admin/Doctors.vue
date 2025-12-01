<script setup>
import { ref, onMounted, reactive } from 'vue'
import api from '../../services/api'
import { toast } from '../../utils/toastify'
import { Modal } from 'bootstrap'


const doctors = ref([])
const departments = ref([])
const loading = ref(false)
let modalInstance = null

const form = reactive({
    name: '',
    email: '',
    password: '',
    contact_no: '',
    dept_id: '',
    qualification: '',
    experience_yrs: '',
    isDisabled: false
})

const isEditing = ref(false)
const currentDoctorId = ref(null)

onMounted(async () => {
    fetchDoctors()
    fetchDepartments()
    modalInstance = new Modal(document.getElementById('addDoctorModal'))

    // Reset form when modal is closed
    document.getElementById('addDoctorModal').addEventListener('hidden.bs.modal', () => {
        resetForm()
    })
})

const fetchDoctors = async () => {
    try {
        loading.value = true
        const response = await api.get('doctors')
        doctors.value = response.data
    } catch (error) {
        toast.error('Failed to load doctors')
    } finally {
        loading.value = false
    }
}

const fetchDepartments = async () => {
    try {
        const response = await api.get('departments')
        departments.value = response.data
    } catch (error) {
        console.error('Failed to load departments')
    }
}

const submitForm = async () => {
    try {
        const payload = { ...form }
        if (isEditing.value) {
            payload.status = form.isDisabled ? 'DISABLED' : 'ACTIVE'
            delete payload.isDisabled

            await api.put(`doctors/${currentDoctorId.value}`, payload)
            toast.success('Doctor updated successfully')
        } else {
            await api.post('doctors', form)
            toast.success('Doctor added successfully')
        }
        modalInstance.hide()
        fetchDoctors()
    } catch (error) {
        toast.error(error.response?.data?.msg || (isEditing.value ? 'Failed to update doctor' : 'Failed to add doctor'))
    }
}

const editDoctor = (doc) => {
    isEditing.value = true
    currentDoctorId.value = doc.doctor_id
    form.name = doc.name
    form.email = doc.email
    form.password = '' // Keep blank or handle as needed, usually don't populate password
    form.contact_no = doc.contact_no
    form.dept_id = doc.dept_id
    form.qualification = doc.qualification
    form.experience_yrs = doc.experience_yrs
    form.isDisabled = doc.status && doc.status.toUpperCase() === 'DISABLED'
    modalInstance.show()
}

const deleteDoctor = async (id) => {
    if (!confirm('Are you sure you want to delete this doctor?')) return

    try {
        await api.delete(`doctors/${id}`)
        toast.success('Doctor deleted')
        fetchDoctors()
    } catch (error) {
        toast.error('Failed to delete doctor')
    }
}

const resetForm = () => {
    isEditing.value = false
    currentDoctorId.value = null
    Object.keys(form).forEach(key => form[key] = '')
}
</script>

<template>
    <div>
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold text-primary mb-0">Doctors</h2>
            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addDoctorModal">
                <i class="bi bi-plus-lg me-2"></i> Add Doctor
            </button>
        </div>

        <div class="card border-0 shadow-sm">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="bg-light">
                            <tr>
                                <th class="border-0 px-4 py-3">Name</th>
                                <th class="border-0 px-4 py-3">Department</th>
                                <th class="border-0 px-4 py-3">Qualification</th>
                                <th class="border-0 px-4 py-3">Experience</th>
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
                            <tr v-else-if="doctors.length === 0">
                                <td colspan="6" class="text-center py-5 text-muted">
                                    No doctors found
                                </td>
                            </tr>
                            <tr v-else v-for="doc in doctors" :key="doc.doctor_id">
                                <td class="px-4 py-3">
                                    <div class="d-flex align-items-center">
                                        <div class="avatar-circle bg-primary-subtle text-primary me-3">
                                            {{ doc.name.charAt(0) }}
                                        </div>
                                        <div>
                                            <div class="fw-bold">{{ doc.name }}</div>
                                            <small class="text-muted">ID: {{ doc.doctor_id }}</small>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-4 py-3"><span class="badge bg-light text-dark border">{{ doc.department
                                }}</span></td>
                                <td class="px-4 py-3">{{ doc.qualification }}</td>
                                <td class="px-4 py-3">{{ doc.experience_yrs }} years</td>
                                <td class="px-4 py-3">
                                    <span
                                        :class="['badge', doc.status && doc.status.toUpperCase() === 'ACTIVE' ? 'bg-success-subtle text-success' : 'bg-danger-subtle text-danger']">
                                        {{ doc.status ? doc.status.toUpperCase() : 'UNKNOWN' }}
                                    </span>
                                </td>
                                <td class="px-4 py-3 text-end">
                                    <button class="btn btn-sm btn-outline-primary me-2" @click="editDoctor(doc)">
                                        <i class="bi bi-pencil me-1"></i> Edit
                                    </button>
                                    <button class="btn btn-sm btn-outline-danger" @click="deleteDoctor(doc.doctor_id)">
                                        <i class="bi bi-trash me-1"></i> Delete
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Add Doctor Modal -->
        <div class="modal fade" id="addDoctorModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content border-0 shadow">
                    <div class="modal-header border-0 pb-0">
                        <h5 class="modal-title fw-bold">{{ isEditing ? 'Edit Doctor' : 'Add New Doctor' }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="submitForm">
                            <div class="mb-3">
                                <label class="form-label">Full Name</label>
                                <input type="text" class="form-control" v-model="form.name" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-control" v-model="form.email" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Password</label>
                                <input type="password" class="form-control" v-model="form.password"
                                    :required="!isEditing">
                                <div v-if="isEditing" class="form-text">Leave blank to keep current password</div>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Contact Number</label>
                                <input type="tel" class="form-control" v-model="form.contact_no" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Department</label>
                                <select class="form-select" v-model="form.dept_id" required>
                                    <option value="" disabled>Select Department</option>
                                    <option v-for="dept in departments" :key="dept.dept_id" :value="dept.dept_id">
                                        {{ dept.name }}
                                    </option>
                                </select>
                            </div>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Qualification</label>
                                    <input type="text" class="form-control" v-model="form.qualification" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Experience (Yrs)</label>
                                    <input type="number" class="form-control" v-model="form.experience_yrs" required>
                                </div>
                            </div>
                            <div class="mb-3 form-check" v-if="isEditing">
                                <input type="checkbox" class="form-check-input" id="disableUser"
                                    v-model="form.isDisabled">
                                <label class="form-check-label text-danger fw-bold" for="disableUser">Disable User
                                    (Block Login)</label>
                            </div>
                            <div class="d-grid mt-4">
                                <button type="submit" class="btn btn-primary">{{ isEditing ? 'Update Doctor' :
                                    'CreateDoctor Account' }}</button>
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
