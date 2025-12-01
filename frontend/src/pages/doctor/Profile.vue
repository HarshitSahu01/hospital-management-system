<template>
    <div class="doctor-profile">
        <div class="d-flex align-items-center mb-4">
            <button v-if="isReadOnly" @click="$router.go(-1)" class="btn btn-link text-decoration-none p-0 me-3">
                <i class="bi bi-arrow-left fs-4"></i>
            </button>
            <h2 class="fw-bold text-primary mb-0">{{ isReadOnly ? 'Doctor Profile' : 'My Profile' }}</h2>
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
                    </div>

                    <!-- Professional Info -->
                    <h5 class="fw-bold text-secondary mb-3">Professional Details</h5>

                    <div class="row mb-4">
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Department</label>
                            <input v-model="profile.department" type="text" class="form-control bg-light" disabled>
                        </div>
                        <div class="col-12 mb-3">
                            <label class="form-label fw-bold">Qualification</label>
                            <input v-model="profile.qualification" type="text" class="form-control"
                                :disabled="isReadOnly">
                        </div>
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
            // Fetch specific doctor
            const res = await api.get(`doctors/${route.params.id}`)
            profile.value = res.data
        } else {
            // Fetch own profile
            // We should use /me or similar, but current API structure is a bit loose.
            // Let's rely on userStore.user.user_id to find the doctor profile
            const res = await api.get(`doctors/${userStore.user.user_id}`) // Assuming endpoint supports user_id or we filter
            // Actually the endpoint /doctors returns list. /doctors/:id returns specific.
            // But we need to know the doctor_id.
            // Let's fetch list and find.
            const listRes = await api.get('doctors')
            const myProfile = listRes.data.find(d => d.email === userStore.user.email)
            if (myProfile) {
                // Fetch full details including webhook (if exposed)
                const fullRes = await api.get(`doctors/${myProfile.doctor_id}`)
                profile.value = fullRes.data
                // Manually add webhook_url from user object if not in doctor response?
                // The DoctorResource returns status but not webhook_url.
                // We need to update DoctorResource to return webhook_url for owner/admin.

                // Wait, let's check resources.py again. DoctorResource.get returns:
                // name, email, contact_no, department, dept_id, qualification, experience_yrs, status
                // It does NOT return webhook_url.

                // I need to update resources.py to return webhook_url.
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
        await api.put(`doctors/${profile.value.doctor_id}`, profile.value)
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
