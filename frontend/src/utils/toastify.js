import { reactive } from 'vue'

export const toastState = reactive({
    toasts: []
})

let toastId = 0

export const toast = {
    add(type, message, duration = 3000) {
        const id = toastId++
        toastState.toasts.push({ id, type, message })
        if (duration > 0) {
            setTimeout(() => {
                this.remove(id)
            }, duration)
        }
        return id
    },
    remove(id) {
        const index = toastState.toasts.findIndex(t => t.id === id)
        if (index !== -1) {
            toastState.toasts.splice(index, 1)
        }
    },
    success(message, duration) {
        return this.add('success', message, duration)
    },
    error(message, duration) {
        return this.add('danger', message, duration)
    },
    warning(message, duration) {
        return this.add('warning', message, duration)
    },
    info(message, duration) {
        return this.add('info', message, duration)
    }
}
