import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../store/user'

import Login from '../pages/auth/Login.vue'
import Register from '../pages/auth/Register.vue'
import AdminDashboard from '../pages/admin/Dashboard.vue'
import DoctorDashboard from '../pages/doctor/Dashboard.vue'
import PatientDashboard from '../pages/patient/Dashboard.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
            meta: { hideSidebar: true }
        },
        {
            path: '/register',
            name: 'register',
            component: Register,
            meta: { hideSidebar: true }
        },
        {
            path: '/admin',
            name: 'admin-dashboard',
            component: AdminDashboard,
            meta: { requiresAuth: true, role: 'ADMIN' }
        },
        {
            path: '/doctor',
            name: 'doctor-dashboard',
            component: DoctorDashboard,
            meta: { requiresAuth: true, role: 'DOCTOR' }
        },
        {
            path: '/doctor/schedule',
            name: 'doctor-schedule',
            component: () => import('../pages/doctor/Schedule.vue'),
            meta: { requiresAuth: true, role: 'DOCTOR' }
        },
        {
            path: '/doctor/appointments',
            name: 'doctor-appointments',
            component: () => import('../pages/doctor/Appointments.vue'),
            meta: { requiresAuth: true, role: 'DOCTOR' }
        },
        {
            path: '/doctor/treatments',
            name: 'doctor-treatments',
            component: () => import('../pages/doctor/TreatmentHistory.vue'),
            meta: { requiresAuth: true, role: 'DOCTOR' }
        },
        {
            path: '/doctor/treatments/:id',
            name: 'doctor-treatment-detail',
            component: () => import('../pages/doctor/Treatments.vue'),
            meta: { requiresAuth: true, role: 'DOCTOR' }
        },
        {
            path: '/doctor/profile',
            name: 'doctor-profile',
            component: () => import('../pages/doctor/Profile.vue'),
            meta: { requiresAuth: true, role: 'DOCTOR' }
        },
        {
            path: '/doctor/profile/:id',
            name: 'doctor-profile-view',
            component: () => import('../pages/doctor/Profile.vue'),
            meta: { requiresAuth: true } // Accessible by Patient and Doctor
        },
        {
            path: '/patient',
            name: 'patient-dashboard',
            component: PatientDashboard,
            meta: { requiresAuth: true, role: 'PATIENT' }
        },
        {
            path: '/patient/appointments',
            name: 'patient-appointments',
            component: () => import('../pages/patient/Appointments.vue'),
            meta: { requiresAuth: true, role: 'PATIENT' }
        },
        {
            path: '/patient/treatments',
            name: 'patient-treatments',
            component: () => import('../pages/patient/Treatments.vue'),
            meta: { requiresAuth: true, role: 'PATIENT' }
        },
        {
            path: '/patient/profile',
            name: 'patient-profile',
            component: () => import('../pages/patient/Profile.vue'),
            meta: { requiresAuth: true, role: 'PATIENT' }
        },
        {
            path: '/patient/profile/:id',
            name: 'patient-profile-view',
            component: () => import('../pages/patient/Profile.vue'),
            meta: { requiresAuth: true, role: 'DOCTOR' } // Only Doctor/Admin can view patient profile
        },
        {
            path: '/patient/book',
            name: 'patient-book-appointment',
            component: () => import('../pages/patient/BookAppointment.vue'),
            meta: { requiresAuth: true, role: 'PATIENT' }
        }
        // Add more routes as we create pages
        ,
        {
            path: '/admin/doctors',
            name: 'admin-doctors',
            component: () => import('../pages/admin/Doctors.vue'),
            meta: { requiresAuth: true, role: 'ADMIN' }
        },
        {
            path: '/admin/patients',
            name: 'admin-patients',
            component: () => import('../pages/admin/Patients.vue'),
            meta: { requiresAuth: true, role: 'ADMIN' }
        },
        {
            path: '/admin/departments',
            name: 'admin-departments',
            component: () => import('../pages/admin/Departments.vue'),
            meta: { requiresAuth: true, role: 'ADMIN' }
        },
        {
            path: '/admin/appointments',
            name: 'admin-appointments',
            component: () => import('../pages/admin/Appointments.vue'),
            meta: { requiresAuth: true, role: 'ADMIN' }
        },
        {
            path: '/admin/report',
            name: 'admin-report',
            component: () => import('../pages/admin/Report.vue'),
            meta: { requiresAuth: true, role: 'ADMIN' }
        }
    ]
})

router.beforeEach((to, from, next) => {
    const userStore = useUserStore()
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    const requiredRole = to.meta.role

    if (requiresAuth && !userStore.isAuthenticated) {
        next('/login')
    } else if (requiresAuth && requiredRole && userStore.user.role !== requiredRole) {
        // Redirect to appropriate dashboard if role mismatch
        if (userStore.user.role === 'ADMIN') next('/admin')
        else if (userStore.user.role === 'DOCTOR') next('/doctor')
        else if (userStore.user.role === 'PATIENT') next('/patient')
        else next('/login')
    } else if (userStore.isAuthenticated && (to.name === 'login' || to.name === 'register')) {
        // Redirect logged-in users away from login/register
        if (userStore.user.role === 'ADMIN') next('/admin')
        else if (userStore.user.role === 'DOCTOR') next('/doctor')
        else if (userStore.user.role === 'PATIENT') next('/patient')
        else next('/')
    } else {
        next()
    }
})

export default router
