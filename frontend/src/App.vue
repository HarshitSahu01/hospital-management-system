<script setup>
import { RouterView, useRoute } from 'vue-router'
import NavbarTop from './components/NavbarTop.vue'
import SidebarLeft from './components/SidebarLeft.vue'
import Toast from './components/Toast.vue'
import { useUserStore } from './store/user'

const userStore = useUserStore()
const route = useRoute()
</script>

<template>
  <NavbarTop />
  <div class="container-fluid">
    <div class="row">
      <div v-if="userStore.isAuthenticated && !route.meta.hideSidebar" class="col-auto d-none d-md-block p-0">
        <SidebarLeft />
      </div>
      <main :class="[
        'col px-md-4 py-4 main-content',
        { 'offset-md-sidebar': userStore.isAuthenticated && !route.meta.hideSidebar }
      ]">
        <div class="fade-enter-active">
          <RouterView />
        </div>
      </main>
    </div>
  </div>
  <Toast />
</template>

<style>
.main-content {
  min-height: calc(100vh - 64px);
  transition: margin-left 0.3s ease;
}

@media (min-width: 768px) {
  .offset-md-sidebar {
    margin-left: 260px;
    /* Sidebar width */
    width: calc(100% - 260px);
  }
}

/* Page Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
