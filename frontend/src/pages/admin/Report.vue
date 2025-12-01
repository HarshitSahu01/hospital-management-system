<template>
    <div class="container-fluid py-4">
        <h2 class="mb-4">Admin Reports</h2>

        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <div v-else>
            <!-- Summary Cards -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h5 class="card-title">Doctors</h5>
                            <h2 class="mb-0">{{ stats.counts.doctors }}</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h5 class="card-title">Patients</h5>
                            <h2 class="mb-0">{{ stats.counts.patients }}</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h5 class="card-title">Appointments</h5>
                            <h2 class="mb-0">{{ stats.counts.appointments }}</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-dark">
                        <div class="card-body">
                            <h5 class="card-title">Departments</h5>
                            <h2 class="mb-0">{{ stats.counts.departments }}</h2>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Charts -->
            <div class="row">
                <div class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-header">Appointments by Department</div>
                        <div class="card-body">
                            <canvas id="deptChart"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-header">Appointment Status</div>
                        <div class="card-body">
                            <canvas id="statusChart"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-12 mb-4">
                    <div class="card">
                        <div class="card-header">Appointments (Last 7 Days)</div>
                        <div class="card-body">
                            <canvas id="trendChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';

const stats = ref(null);
const loading = ref(true);

const fetchStats = async () => {
    try {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://localhost:5000/api/admin/stats', {
            headers: { Authorization: `Bearer ${token}` }
        });
        stats.value = res.data;
        loading.value = false;

        await nextTick();
        renderCharts();
    } catch (error) {
        console.error("Error fetching stats:", error);
        loading.value = false;
    }
};

const renderCharts = () => {
    // 1. Department Chart (Bar)
    const deptCtx = document.getElementById('deptChart');
    new Chart(deptCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(stats.value.by_department),
            datasets: [{
                label: 'Appointments',
                data: Object.values(stats.value.by_department),
                backgroundColor: '#36A2EB'
            }]
        },
        options: { responsive: true }
    });

    // 2. Status Chart (Doughnut)
    const statusCtx = document.getElementById('statusChart');
    new Chart(statusCtx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(stats.value.by_status),
            datasets: [{
                data: Object.values(stats.value.by_status),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
            }]
        },
        options: { responsive: true }
    });

    // 3. Trend Chart (Line)
    // Fill in missing dates for last 7 days
    const dates = [];
    const counts = [];
    for (let i = 6; i >= 0; i--) {
        const d = new Date();
        d.setDate(d.getDate() - i);
        const dateStr = d.toISOString().split('T')[0];
        dates.push(dateStr);
        counts.push(stats.value.last_7_days[dateStr] || 0);
    }

    const trendCtx = document.getElementById('trendChart');
    new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Appointments',
                data: counts,
                borderColor: '#4BC0C0',
                tension: 0.1,
                fill: false
            }]
        },
        options: { responsive: true }
    });
};

onMounted(() => {
    fetchStats();
});
</script>
