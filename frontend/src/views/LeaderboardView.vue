<template>
  <div class="container">
    <nav class="navbar navbar-light bg-light mb-4">
      <div class="container">
        <router-link class="navbar-brand" to="/">← Quay lại danh sách</router-link>
      </div>
    </nav>

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Bảng xếp hạng</h2>
      <span class="badge bg-info">{{ quizTitle }}</span>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

    <div v-else-if="leaderboard.length === 0" class="text-center py-5">
      <p>Chưa có ai làm bài quiz này.</p>
    </div>

    <div v-else>
      <table class="table table-striped table-hover align-middle">
        <thead class="table-dark">
          <tr>
            <th>Xếp hạng</th>
            <th>Người chơi</th>
            <th>Điểm</th>
            <th>Đúng/Số câu</th>
            <th>Thời gian</th>
            <th>Ngày nộp</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in leaderboard" :key="item.id">
            <td>
              <span :class="item.rank <= 3 ? 'badge bg-warning text-dark fw-bold' : 'text-muted'">
                #{{ item.rank }}
              </span>
            </td>
            <td>{{ item.username }}</td>
            <td class="fw-bold">{{ item.score }} / 10</td>
            <td>{{ item.correct_answers }} / {{ item.total_questions }}</td>
            <td>{{ formatTime(item.time_spent) }}</td>
            <td class="small text-muted">{{ new Date(item.submitted_at).toLocaleString('vi-VN') }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '@/api/axios'

const route = useRoute()
const leaderboard = ref([])
const quizTitle = ref('')
const loading = ref(true)
const error = ref(null)

const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

const loadLeaderboard = async () => {
  try {
    const res = await apiClient.get(`/quizzes/${route.params.id}/leaderboard`)
    leaderboard.value = res.data.leaderboard
    quizTitle.value = res.data.quiz_title
  } catch (e) {
    error.value = e.response?.data?.error || 'Không tải được bảng xếp hạng'
  } finally {
    loading.value = false
  }
}

onMounted(loadLeaderboard)
</script>
