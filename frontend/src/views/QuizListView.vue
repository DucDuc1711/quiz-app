<template>
  <div class="container mt-4">
    <h2 class="mb-4 text-center">Danh sách bộ Quiz</h2>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

    <div v-else-if="quizzes.length === 0" class="empty-state text-center">
      <p>Hiện tại chưa có bộ quiz nào.</p>
    </div>

    <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div class="col" v-for="quiz in quizzes" :key="quiz.id">
        <div class="card quiz-card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">{{ quiz.title }}</h5>
            <p class="card-text text-muted small">{{ quiz.description }}</p>
            <div class="d-flex justify-content-between text-muted small mb-3">
              <span><i class="bi bi-question-circle"></i> {{ quiz.question_count }} câu hỏi</span>
              <span><i class="bi bi-clock"></i> {{ quiz.time_limit }} phút</span>
            </div>
            <router-link :to="{ name: 'QuizTake', params: { id: quiz.id } }" class="btn btn-primary w-100">
              Làm bài ngay
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/axios'

const quizzes = ref([])
const loading = ref(true)
const error = ref(null)

const loadQuizzes = async () => {
  try {
    const res = await apiClient.get('/quizzes')
    quizzes.value = res.data.quizzes
  } catch (e) {
    error.value = e.response?.data?.error || 'Không tải được danh sách quiz'
  } finally {
    loading.value = false
  }
}

onMounted(loadQuizzes)
</script>
