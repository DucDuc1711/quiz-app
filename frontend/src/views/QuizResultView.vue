<template>
  <div class="container">
    <nav class="navbar navbar-light bg-light mb-4">
      <div class="container">
        <router-link class="navbar-brand" to="/">← Quay lại danh sách</router-link>
      </div>
    </nav>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

    <div v-else-if="attempt" class="row">
      <div class="col-md-8">
        <div class="card shadow mb-4">
          <div class="card-header bg-success text-white">
            <h5 class="mb-0">Kết quả làm bài</h5>
          </div>
          <div class="card-body text-center">
            <h2 class="display-4 text-primary">{{ attempt.score }} / 10</h2>
            <p class="mb-0">{{ attempt.correct_answers }}/{{ attempt.total_questions }} câu trả lời đúng</p>
          </div>
          <div class="card-body">
            <div class="d-flex justify-content-between text-muted small mb-3">
              <span>Thời gian: {{ formatTime(attempt.time_spent) }}</span>
              <span>Nộp lúc: {{ new Date(attempt.submitted_at).toLocaleString('vi-VN') }}</span>
            </div>
          </div>
        </div>

        <h5 class="mb-3">Chi tiết từng câu hỏi</h5>
        <div class="accordion" id="reviewAccordion">
          <div v-for="(q, idx) in questionReviews" :key="q.question_id" class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" :data-bs-target="'#collapse' + idx">
                Câu {{ q.order_num }}: {{ q.content }}
                <span class="float-end" :class="q.is_correct ? 'text-success' : 'text-danger'">
                  {{ q.is_correct ? '✓ Đúng' : '✗ Sai' }}
                </span>
              </button>
            </h2>
            <div :id="'collapse' + idx" class="accordion-collapse collapse" data-bs-parent="#reviewAccordion">
              <div class="accordion-body">
                <div class="mb-2">
                  <span class="fw-bold">Đáp án bạn chọn: </span>
                  <span :class="q.selected_choice_id === q.correct_choice_id ? 'text-success' : 'text-danger'">
                    {{ getChoiceText(q.selected_choice_id) || 'Chưa chọn' }}
                  </span>
                </div>
                <div class="mb-2">
                  <span class="fw-bold">Đáp án đúng: </span>
                  <span class="text-success">{{ getChoiceText(q.correct_choice_id) }}</span>
                </div>
                <div v-if="q.explanation" class="mt-2 p-2 bg-light rounded">
                  <small class="text-muted"><i class="bi bi-chat-quote"></i> {{ q.explanation }}</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card shadow">
          <div class="card-header">Thông tin</div>
          <div class="card-body">
            <p><strong>Bộ quiz:</strong> {{ attempt.quiz_title }}</p>
            <p><strong>Người làm:</strong> {{ attempt.username }}</p>
            <p><strong>Điểm:</strong> {{ attempt.score }} / 10</p>
          </div>
        </div>
        <div class="mt-3">
          <router-link to="/" class="btn btn-outline-primary w-100">Làm quiz khác</router-link>
          <router-link :to="{ name: 'Leaderboard', params: { id: attempt.quiz_id } }" class="btn btn-primary w-100 mt-2">Bảng xếp hạng</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '@/api/axios'

const route = useRoute()
const router = useRouter()
const attempt = ref(null)
const questionReviews = ref([])
const loading = ref(true)
const error = ref(null)

const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

const getChoiceText = (choiceId) => {
  for (const q of questionReviews.value) {
    const c = q.choices.find(x => x.id === choiceId)
    if (c) return c.content
  }
  return ''
}

const loadResult = async () => {
  try {
    const res = await apiClient.get(`/attempts/${route.params.id}`)
    attempt.value = res.data.attempt
    questionReviews.value = res.data.question_reviews
  } catch (e) {
    error.value = e.response?.data?.error || 'Không tải được kết quả'
  } finally {
    loading.value = false
  }
}

onMounted(loadResult)
</script>
