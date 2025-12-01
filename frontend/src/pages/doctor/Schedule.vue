<template>
    <div class="doctor-schedule">
        <h2 class="fw-bold text-primary mb-4">Manage Availability</h2>

        <div class="card border-0 shadow-sm mb-4">
            <div class="card-body p-4">
                <label class="form-label fw-bold mb-3">Select Date</label>
                <div class="d-flex gap-2 overflow-auto pb-2">
                    <button v-for="day in nextDays" :key="day.dateStr" @click="selectDate(day.dateStr)"
                        :class="['btn', selectedDate === day.dateStr ? 'btn-primary' : 'btn-outline-secondary']"
                        style="min-width: 120px;">
                        {{ day.display }}
                    </button>
                </div>
            </div>
        </div>

        <div v-if="selectedDate" class="card border-0 shadow-sm">
            <div class="card-body p-4">
                <h4 class="fw-bold mb-4">Slots for {{ formatDate(selectedDate) }}</h4>

                <div class="row g-3">
                    <div v-for="slot in availableSlots" :key="slot.time" class="col-6 col-md-4 col-lg-3">
                        <button @click="toggleSlot(slot.time)" :disabled="slot.isBooked" :class="[
                            'btn w-100 py-3 d-flex flex-column align-items-center justify-content-center h-100',
                            slot.isBooked
                                ? 'btn-danger opacity-75'
                                : (slot.isSelected
                                    ? 'btn-success'
                                    : 'btn-outline-secondary')
                        ]">
                            <span class="fs-5 fw-bold mb-1">{{ slot.time }}</span>
                            <span class="small text-uppercase">
                                <i v-if="slot.isBooked" class="bi bi-x-circle-fill me-1"></i>
                                <i v-else-if="slot.isSelected" class="bi bi-check-circle-fill me-1"></i>
                                <i v-else class="bi bi-circle me-1"></i>
                                {{ slot.isBooked ? 'Booked' : (slot.isSelected ? 'Available' : 'Unavailable') }}
                            </span>
                        </button>
                    </div>
                </div>

                <div class="d-flex justify-content-end mt-4 pt-3 border-top">
                    <button @click="saveAvailability" :disabled="saving" class="btn btn-primary px-4 fw-bold">
                        <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status"
                            aria-hidden="true"></span>
                        {{ saving ? 'Saving...' : 'Save Changes' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../../store/user'
import api from '../../services/api'

const userStore = useUserStore()
const selectedDate = ref(null)
const saving = ref(false)
const availabilityData = ref([]) // Stores fetched availability from backend

// Generate next 7 days
const nextDays = computed(() => {
    const days = []
    const today = new Date()
    for (let i = 0; i < 7; i++) {
        const d = new Date(today)
        d.setDate(today.getDate() + i)
        days.push({
            dateStr: d.toISOString().split('T')[0],
            display: d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
        })
    }
    return days
})

// Standard slots 9am - 6pm
const standardSlots = [
    { time: '09:00', label: '09:00 - 10:00' },
    { time: '10:00', label: '10:00 - 11:00' },
    { time: '11:00', label: '11:00 - 12:00' },
    { time: '12:00', label: '12:00 - 13:00' },
    { time: '13:00', label: '13:00 - 14:00' },
    { time: '14:00', label: '14:00 - 15:00' },
    { time: '15:00', label: '15:00 - 16:00' },
    { time: '16:00', label: '16:00 - 17:00' },
    { time: '17:00', label: '17:00 - 18:00' }
]

// Computed slots for the selected date combining standard slots with fetched data
const availableSlots = computed(() => {
    if (!selectedDate.value) return []

    // Filter fetched data for selected date
    const dayData = availabilityData.value.filter(a => a.date === selectedDate.value)

    return standardSlots.map(slot => {
        // Check if this slot exists in fetched data
        // Note: backend returns slot_from as "HH:MM:SS", we need to match "HH:MM"
        const existing = dayData.find(d => d.slot_from.startsWith(slot.time))

        return {
            ...slot,
            isSelected: !!existing, // If it exists in DB, it's selected (Available)
            isBooked: existing ? existing.is_booked === 1 : false
        }
    })
})

const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
}

const selectDate = (dateStr) => {
    selectedDate.value = dateStr
}

const toggleSlot = (time) => {
    // We can't directly mutate computed property items.
    // Instead, we should update the local state that drives the computed property.
    // But here, we are deriving from 'availabilityData'.
    // So we need to simulate the change in 'availabilityData'.

    const currentSlots = [...availabilityData.value]
    const existingIndex = currentSlots.findIndex(a => a.date === selectedDate.value && a.slot_from.startsWith(time))

    if (existingIndex >= 0) {
        // Remove it(Deselect)
        // Check if booked first ? The UI disables booked slots, so we assume we can remove.
        currentSlots.splice(existingIndex, 1)
    } else {
        // Add it(Select)
        currentSlots.push({
            date: selectedDate.value,
            slot_from: time + ':00',
            slot_to: '', // Backend calculates this
            is_booked: 0
        })
    }

    availabilityData.value = currentSlots
}

const fetchAvailability = async () => {
    try {
        const res = await api.get('doctor/availability')
        availabilityData.value = res.data
    } catch (e) {
        console.error('Failed to fetch availability', e)
    }
}

const saveAvailability = async () => {
    saving.value = true
    try {
        // Get all selected slots for the current date
        const slotsToSend = availableSlots.value
            .filter(s => s.isSelected)
            .map(s => s.time)

        await api.post('doctor/availability', {
            date: selectedDate.value,
            slots: slotsToSend
        })

        // Refresh data
        await fetchAvailability()
        alert('Availability saved successfully')
    } catch (e) {
        console.error('Error saving', e)
        alert('Error saving availability')
    } finally {
        saving.value = false
    }
}

onMounted(() => {
    if (nextDays.value.length > 0) {
        selectedDate.value = nextDays.value[0].dateStr
    }
    fetchAvailability()
})
</script>
