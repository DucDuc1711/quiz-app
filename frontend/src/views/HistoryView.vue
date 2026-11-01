<template>
  <div class="container">
    <nav class="navbar navbar-light bg-light mb-4">
      <div class="container">
        <router-link class="navbar-brand" to="/">← Quay lại trang chủ</router-link>
      </div>
    </nav>

    <h2 class="mb-4">Lịch sử làm bài của tôi</h2>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

    <div v-else-if="attempts.length === 0" class="text-center py-5">
      <p>Bạn chưa làm bài quiz nào.</p>
      <router-link to="/" class="btn btn-primary">Chọn một bộ quiz</router-link>
    </div>

    <div v-else>
      <div class="table-responsive">
        <table class="table table-striped table-hover align-middle">
          <thead class="table-dark">
            <tr>
              <th>Bộ quiz</th>
              <th>Điểm</th>
              <th>Đúng/Số câu</th>
              <th>Thời gian</th>
              <th>Ngày nộp</th>
              <th>Xem chi tiết</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in attempts" :key="item.id">
              <td>{{ item.quiz_title }}</td>
              <td class="fw-bold">{{ item.score }} / 10</td>
              <td>{{ item.correct_answers }} / {{ item.total_questions }}</td>
              <td>{{ formatTime(item.time_spent) }}</td>
              <td class="small text-muted">{{ new Date(item.submitted_at).toLocaleString('vi-VN') }}</td>
              <td>
                <router-link :to="{ name: 'QuizResult', params: { id: item.id } }" class="btn btn-sm btn-outline-primary">Xem</router-link>
              </td>
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

const attempts = ref([])
const loading = ref(true)
const error = ref(null)

const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

const loadAttempts = async () => {
  try {
    const res = await apiClient.get('/me/attempts')
    attempts.value = res.data.attempts
  } catch (e) {
    error.value = e.response?.data?.error || 'Không tải được lịch sử'
  } finally {
    loading.value = false
  }
}

onMounted(loadAttempts)
</script>
