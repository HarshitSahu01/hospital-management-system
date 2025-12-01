<script setup>
import { ref, onMounted, reactive } from 'vue'
import api from '../../services/api'
import { toast } from '../../utils/toastify'
import { Modal } from 'bootstrap'


const departments = ref([])
const loading = ref(false)
let modalInstance = null

const form = reactive({
    name: '',
    description: ''
})

const isEditing = ref(false)
const currentDeptId = ref(null)

onMounted(async () => {
    fetchDepartments()
    modalInstance = new Modal(document.getElementById('addDeptModal'))

    // Reset form when modal is closed
    document.getElementById('addDeptModal').addEventListener('hidden.bs.modal', () => {
        resetForm()
    })
})

const fetchDepartments = async () => {
    try {
        loading.value = true
        const response = await api.get('departments')
        departments.value = response.data
    } catch (error) {
        toast.error('Failed to load departments')
    } finally {
        loading.value = false
    }
}

const submitForm = async () => {
    try {
        if (isEditing.value) {
            await api.put(`departments/${currentDeptId.value}`, form)
            toast.success('Department updated successfully')
        } else {
            await api.post('departments', form)
            toast.success('Department added successfully')
        }
        modalInstance.hide()
        fetchDepartments()
    } catch (error) {
        toast.error(error.response?.data?.msg || (isEditing.value ? 'Failed to update department' : 'Failed to add department'))
    }
}

const editDept = (dept) => {
    isEditing.value = true
    currentDeptId.value = dept.dept_id
    form.name = dept.name
    form.description = dept.description
    modalInstance.show()
}

const resetForm = () => {
    isEditing.value = false
    currentDeptId.value = null
    form.name = ''
    form.description = ''
}

const deleteDept = async (id) => {
    if (!confirm('Are you sure you want to delete this department?')) return

    try {
        await api.delete(`departments/${id}`)
        toast.success('Department deleted')
        fetchDepartments()
    } catch (error) {
        toast.error('Failed to delete department')
    }
}
</script>

<template>
    <div>
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold text-primary mb-0">Departments</h2>
            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addDeptModal">
                <i class="bi bi-plus-lg me-2"></i> Add Department
            </button>
        </div>

        <div class="row g-4">
            <div v-if="loading" class="col-12 text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            <div v-else-if="departments.length === 0" class="col-12 text-center py-5 text-muted">
                No departments found
            </div>
            <div v-else v-for="dept in departments" :key="dept.dept_id" class="col-md-4">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <div class="icon-box bg-indigo-100 text-indigo-600">
                                <i class="bi bi-building-fill fs-5"></i>
                            </div>
                            <div class="d-flex">
                                <button class="btn btn-sm btn-outline-primary me-2" @click.prevent="editDept(dept)"
                                    title="Edit">
                                    <i class="bi bi-pencil"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-danger" @click.prevent="deleteDept(dept.dept_id)"
                                    title="Delete">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </div>
                        </div>
                        <h5 class="fw-bold mb-2">{{ dept.name }}</h5>
                        <p class="text-muted small mb-3">{{ dept.description }}</p>
                        <div class="d-flex align-items-center text-muted small">
                            <i class="bi bi-people-fill me-2"></i>
                            <span>{{ dept.doctors_registered }} Doctors</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add Department Modal -->
        <div class="modal fade" id="addDeptModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content border-0 shadow">
                    <div class="modal-header border-0 pb-0">
                        <h5 class="modal-title fw-bold">{{ isEditing ? 'Edit Department' : 'Add New Department' }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="submitForm">
                            <div class="mb-3">
                                <label class="form-label">Department Name</label>
                                <input type="text" class="form-control" v-model="form.name" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Description</label>
                                <textarea class="form-control" v-model="form.description" rows="3" required></textarea>
                            </div>
                            <div class="d-grid mt-4">
                                <button type="submit" class="btn btn-primary">{{ isEditing ? 'Update Department' :
                                    'Create Department' }}</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.icon-box {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.bg-indigo-100 {
    background-color: #e0e7ff;
}

.text-indigo-600 {
    color: #4f46e5;
}
</style>
