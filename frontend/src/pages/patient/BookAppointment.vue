<template>
    <div class="book-appointment">
        <h2 class="fw-bold text-primary mb-4">Book New Appointment</h2>

        <div class="card border-0 shadow-sm">
            <div class="card-body p-4">
                <!-- Search Section -->
                <div class="mb-4">
                    <label class="form-label fw-bold">Search Doctor</label>
                    <input v-model="searchQuery" type="text" placeholder="Search by name or department..."
                        class="form-control">
                </div>

                <!-- Doctor List (Tabular) -->
                <div v-if="!selectedDoctor">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead class="bg-light">
                                <tr>
                                    <th class="border-0 px-3 py-3">Doctor</th>
                                    <th class="border-0 px-3 py-3">Department</th>
                                    <th class="border-0 px-3 py-3">Experience</th>
                                    <th class="border-0 px-3 py-3">Qualification</th>
                                    <th class="border-0 px-3 py-3 text-end">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="filteredDoctors.length === 0">
                                    <td colspan="5" class="text-center py-4 text-muted">
                                        No doctors found matching your search.
                                    </td>
                                </tr>
                                <tr v-else v-for="doc in filteredDoctors" :key="doc.doctor_id">
                                    <td class="px-3 py-3">
                                        <div class="d-flex align-items-center">
                                            <div class="avatar-circle bg-primary-subtle text-primary me-3">
                                                {{ doc.name.charAt(0) }}
                                            </div>
                                            <router-link :to="`/doctor/profile/${doc.doctor_id}`"
                                                class="fw-bold text-decoration-none text-dark hover-link">
                                                {{ doc.name }}
                                            </router-link>
                                        </div>
                                    </td>
                                    <td class="px-3 py-3">{{ doc.department }}</td>
                                    <td class="px-3 py-3">{{ doc.experience_yrs }} years</td>
                                    <td class="px-3 py-3">{{ doc.qualification }}</td>
                                    <td class="px-3 py-3 text-end">
                                        <button class="btn btn-sm btn-outline-primary" @click="selectDoctor(doc)">
                                            Select
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Booking Form -->
                <div v-else>
                    <div class="d-flex align-items-center justify-content-between mb-4 border-bottom pb-3">
                        <div class="d-flex align-items-center">
                            <button @click="selectedDoctor = null"
                                class="btn btn-link text-decoration-none text-secondary p-0 me-3">
                                <i class="bi bi-arrow-left fs-4"></i>
                            </button>
                            <div>
                                <h4 class="fw-bold mb-0">Booking with {{ selectedDoctor.name }}</h4>
                                <small class="text-muted">{{ selectedDoctor.department }}</small>
                            </div>
                        </div>
                    </div>

                    <form @submit.prevent="bookAppointment">
                        <div class="row mb-4">
                            <div class="col-md-6">
                                <label class="form-label fw-bold">Select Date</label>
                                <input v-model="booking.date" type="date" class="form-control" required :min="minDate"
                                    @change="fetchSlots">
                            </div>
                        </div>

                        <!-- Slots Grid -->
                        <div v-if="booking.date" class="mb-4">
                            <label class="form-label fw-bold">Select Time Slot</label>
                            <div v-if="loadingSlots" class="text-center py-3">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </div>
                            <div v-else-if="availableSlots.length === 0" class="alert alert-warning py-2">
                                No slots available for this date.
                            </div>
                            <div v-else class="d-flex flex-wrap gap-2">
                                <button type="button" v-for="slot in availableSlots" :key="slot.time"
                                    @click="booking.time = slot.time" :disabled="!slot.available" :class="['btn',
                                        !slot.available ? 'btn-light text-muted border-0' :
                                            (booking.time === slot.time ? 'btn-primary' : 'btn-outline-primary')]"
                                    style="width: 100px;">
                                    {{ slot.time }}
                                </button>
                            </div>
                        </div>

                        <div class="mb-4">
                            <label class="form-label fw-bold">Reason for Visit</label>
                            <textarea v-model="booking.reason" class="form-control" rows="3" required></textarea>
                        </div>

                        <div class="d-flex justify-content-end">
                            <button type="submit" :disabled="!isValidBooking || bookingLoading"
                                class="btn btn-primary px-5 py-2 fw-bold">
                                {{ bookingLoading ? 'Booking...' : 'Confirm Appointment' }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'
import { toast } from '../../utils/toastify'

const router = useRouter()
const doctors = ref([])
const searchQuery = ref('')
const selectedDoctor = ref(null)
const availableSlots = ref([])
const loadingSlots = ref(false)
const bookingLoading = ref(false)

const booking = ref({
    date: '',
    time: '',
    reason: ''
})

const minDate = computed(() => {
    const today = new Date()
    return today.toISOString().split('T')[0]
})

const filteredDoctors = computed(() => {
    if (!searchQuery.value) return doctors.value
    const query = searchQuery.value.toLowerCase()
    return doctors.value.filter(doc =>
        doc.name.toLowerCase().includes(query) ||
        doc.department.toLowerCase().includes(query)
    )
})

const isValidBooking = computed(() => {
    return booking.value.date && booking.value.time && booking.value.reason
})

onMounted(async () => {
    try {
        const res = await api.get('doctors')
        doctors.value = res.data
    } catch (e) {
        console.error(e)
        toast.error('Failed to load doctors')
    }
})

const selectDoctor = (doc) => {
    selectedDoctor.value = doc
    booking.value = { date: '', time: '', reason: '' }
    availableSlots.value = []
}

const fetchSlots = async () => {
    if (!booking.value.date || !selectedDoctor.value) return

    loadingSlots.value = true
    booking.value.time = '' // Reset selected time

    try {
        const res = await api.get('doctor/slots', {
            params: {
                doctor_id: selectedDoctor.value.doctor_id,
                date: booking.value.date
            }
        })

        let slots = res.data

        // Filter past slots if date is today
        const today = new Date()
        const selectedDate = new Date(booking.value.date)

        if (selectedDate.toDateString() === today.toDateString()) {
            const currentHour = today.getHours()
            const currentMinute = today.getMinutes()

            slots = slots.map(slot => {
                const [slotHour, slotMinute] = slot.time.split(':').map(Number)
                if (slotHour < currentHour || (slotHour === currentHour && slotMinute <= currentMinute)) {
                    return { ...slot, available: false } // Mark past slots as unavailable
                }
                return slot
            })
        }

        availableSlots.value = slots
    } catch (e) {
        console.error(e)
        toast.error('Failed to load slots')
    } finally {
        loadingSlots.value = false
    }
}

const bookAppointment = async () => {
    if (!isValidBooking.value) return

    bookingLoading.value = true
    try {
        await api.post('appointments', {
            doctor_id: selectedDoctor.value.doctor_id,
            date: booking.value.date,
            time: booking.value.time,
            reason: booking.value.reason
        })

        toast.success('Appointment booked successfully')
        router.push('/patient/appointments')
    } catch (e) {
        console.error(e)
        toast.error(e.response?.data?.msg || 'Error booking appointment')
    } finally {
        bookingLoading.value = false
    }
}
</script>

<style scoped>
.avatar-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 14px;
}
</style>
