<template>
    <div class="patient-profile">
        <div class="d-flex align-items-center mb-4">
            <button v-if="isReadOnly" @click="$router.go(-1)" class="btn btn-link text-decoration-none p-0 me-3">
                <i class="bi bi-arrow-left fs-4"></i>
            </button>
            <h2 class="fw-bold text-primary mb-0">{{ isReadOnly ? 'Patient Profile' : 'My Profile' }}</h2>
        </div>

        <div class="card border-0 shadow-sm">
            <div class="card-body p-4">
                <form @submit.prevent="updateProfile">
                    <!-- Personal Info -->
                    <h5 class="fw-bold text-secondary mb-3">Personal Information</h5>

                    <div class="row mb-4">
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Name</label>
                            <input v-model="profile.name" type="text" class="form-control" :disabled="isReadOnly"
                                required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Email</label>
                            <input v-model="profile.email" type="email" class="form-control bg-light" disabled>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Contact Number</label>
                            <input v-model="profile.contact_no" type="text" class="form-control" :disabled="isReadOnly">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Date of Birth</label>
                            <input v-model="profile.date_of_birth" type="date" class="form-control"
                                :disabled="isReadOnly">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Gender</label>
                            <select v-model="profile.gender" class="form-select" :disabled="isReadOnly">
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Blood Group</label>
                            <input v-model="profile.blood_group" type="text" class="form-control"
                                :disabled="isReadOnly">
                        </div>
                    </div>

                    <!-- Address -->
                    <h5 class="fw-bold text-secondary mb-3">Address</h5>

                    <div class="row mb-4">
                        <div class="col-12 mb-3">
                            <label class="form-label fw-bold">Address</label>
                            <input v-model="profile.address" type="text" class="form-control" :disabled="isReadOnly">
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">City</label>
                            <input v-model="profile.city" type="text" class="form-control" :disabled="isReadOnly">
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">State</label>
                            <input v-model="profile.state" type="text" class="form-control" :disabled="isReadOnly">
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">Zip Code</label>
                            <input v-model="profile.zip_code" type="text" class="form-control" :disabled="isReadOnly">
                        </div>
                    </div>

                    <!-- Medical Info -->
                    <h5 class="fw-bold text-secondary mb-3">Medical Information</h5>

                    <div class="mb-3">
                        <label class="form-label fw-bold">Allergies</label>
                        <textarea v-model="profile.allergies" rows="2" class="form-control"
                            :disabled="isReadOnly"></textarea>
                    </div>

                    <div class="mb-4">
                        <label class="form-label fw-bold">Medical History</label>
                        <textarea v-model="profile.medical_history" rows="3" class="form-control"
                            :disabled="isReadOnly"></textarea>
                    </div>

                    <div class="d-flex justify-content-end" v-if="!isReadOnly">
                        <button type="submit" :disabled="saving" class="btn btn-primary px-4">
                            <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status"
                                aria-hidden="true"></span>
                            {{ saving ? 'Saving...' : 'Update Profile' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '../../store/user'
import { useRoute } from 'vue-router'
import api from '../../services/api'
import { toast } from '../../utils/toastify'

const userStore = useUserStore()
const route = useRoute()
const profile = ref({})
const saving = ref(false)

const isReadOnly = computed(() => !!route.params.id)

const fetchProfile = async () => {
    try {
        if (isReadOnly.value) {
            // Fetch specific patient
            const res = await api.get(`patients/${route.params.id}`)
            profile.value = res.data
        } else {
            // Fetch own profile
            const res = await api.get('patients')
            const patients = res.data
            const myProfile = patients.find(p => p.email === userStore.user.email)

            if (myProfile) {
                // Fetch full details
                const detailRes = await api.get(`patients/${myProfile.patient_id}`)
                profile.value = detailRes.data
            }
        }
    } catch (e) {
        console.error(e)
        toast.error('Failed to load profile')
    }
}

const updateProfile = async () => {
    if (isReadOnly.value) return

    saving.value = true
    try {
        await api.put(`patients/${profile.value.patient_id}`, profile.value)
        toast.success('Profile updated successfully')
    } catch (e) {
        console.error(e)
        toast.error('Error updating profile')
    } finally {
        saving.value = false
    }
}

onMounted(() => {
    fetchProfile()
})
</script>
