<script setup>
import { toastState, toast } from '../utils/toastify'
</script>

<template>
  <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 1055">
    <div
      v-for="t in toastState.toasts"
      :key="t.id"
      class="toast show align-items-center border-0 mb-2"
      :class="`text-bg-${t.type}`"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div class="d-flex">
        <div class="toast-body">
          {{ t.message }}
        </div>
        <button
          type="button"
          class="btn-close btn-close-white me-2 m-auto"
          @click="toast.remove(t.id)"
          aria-label="Close"
        ></button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.toast-container {
  pointer-events: none;
}
.toast {
  pointer-events: auto;
}
</style>
