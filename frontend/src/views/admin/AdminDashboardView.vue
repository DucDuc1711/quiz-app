<template>
  <div class="container">
    <nav class="navbar navbar-light bg-light mb-4">
      <div class="container">
        <router-link class="navbar-brand" to="/">← Về trang chủ</router-link>
      </div>
    </nav>

    <h2 class="mb-4">Bảng điều khiển Quản trị</h2>

    <div class="row g-4 mb-4">
      <div class="col-md-3">
        <div class="card bg-primary text-white shadow-sm">
          <div class="card-body">
            <div class="small opacity-75">Tổng người dùng</div>
            <h3 class="mb-0">{{ stats.total_users }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-success text-white shadow-sm">
          <div class="card-body">
            <div class="small opacity-75">Tổng bộ quiz</div>
            <h3 class="mb-0">{{ stats.total_quizzes }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-info text-white shadow-sm">
          <div class="card-body">
            <div class="small opacity-75">Tổng câu hỏi</div>
            <h3 class="mb-0">{{ stats.total_questions }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-warning text-dark shadow-sm">
          <div class="card-body">
            <div class="small opacity-75">Tổng lượt làm bài</div>
            <h3 class="mb-0">{{ stats.total_attempts }}</h3>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow">
      <div class="card-header bg-dark text-white">
        <h5 class="mb-0">Các lượt làm bài gần đây</h5>
      </div>
      <div class="card-body">
        <div v-if="stats.recent_attempts.length === 0" class="text-muted text-center py-3">
          Chưa có lượt làm bài nào.
        </div>
        <table v-else class="table table-sm table-hover align-middle">
          <thead>
            <tr>
              <th>Người chơi</th>
              <th>Bộ quiz</th>
              <th>Điểm</th>
              <th>Thời gian</th>
              <th>Ngày nộp</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in stats.recent_attempts" :key="a.id">
              <td>{{ a.username }}</td>
              <td>{{ a.quiz_title }}</td>
              <td class="fw-bold">{{ a.score }} / 10</td>
              <td>{{ formatTime(a.time_spent) }}</td>
              <td class="small text-muted">{{ new Date(a.submitted_at).toLocaleString('vi-VN') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/axios'

const stats = ref({
  total_users: 0,
  total_quizzes: 0,
  total_questions: 0,
  total_attempts: 0,
  recent_attempts: []
})
const loading = ref(true)
const error = ref(null)

const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

const loadStats = async () => {
  try {
    const res = await apiClient.get('/admin/stats')
    stats.value = res.data.stats
  } catch (e) {
    error.value = e.response?.data?.error || 'Không tải được thống kê'
  } finally {
    loading.value = false
  }
}

onMounted(loadStats)
</script>
