<template>
  <div class="container">
    <nav class="navbar navbar-light bg-light mb-4">
      <div class="container">
        <router-link class="navbar-brand" to="/">← Quay lại danh sách</router-link>
      </div>
    </nav>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2">Đang tải câu hỏi...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

    <div v-else-if="quiz && quiz.questions.length === 0" class="text-center py-5">
      <p>Bộ quiz này chưa có câu hỏi nào.</p>
      <router-link to="/" class="btn btn-primary">Quay lại</router-link>
    </div>

    <div v-else-if="!submitted" class="row justify-content-center">
      <div class="col-md-8 col-lg-7">
        <div class="card shadow mb-3">
          <div class="card-header d-flex justify-content-between align-items-center">
            <span><strong>{{ quiz.title }}</strong></span>
            <span class="badge bg-danger timer-display">{{ formatTime(timeLeft) }}</span>
          </div>
          <div class="card-body">
            <p class="fw-bold mb-3">{{ currentQuestion.order_num }}. {{ currentQuestion.content }}</p>

            <div class="list-group list-group-flush">
              <button
                v-for="choice in currentQuestion.choices"
                :key="choice.id"
                type="button"
                class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                :class="{ 'active bg-primary text-white': selectedChoiceId === choice.id }"
                @click="selectChoice(choice.id)"
              >
                <span>{{ choice.content }}</span>
                <i v-if="selectedChoiceId === choice.id" class="bi bi-check-lg"></i>
              </button>
            </div>

            <div class="d-flex justify-content-between mt-4">
              <button
                v-if="currentQuestionIndex > 0"
                class="btn btn-outline-secondary"
                @click="prevQuestion"
              >
                ← Trước
              </button>
              <span class="text-muted">{{ currentQuestionIndex + 1 }} / {{ quiz.questions.length }}</span>
              <button
                v-if="currentQuestionIndex < quiz.questions.length - 1"
                class="btn btn-primary"
                @click="nextQuestion"
              >
                Tiếp →
              </button>
              <button
                v-if="currentQuestionIndex === quiz.questions.length - 1"
                class="btn btn-success"
                @click="submitQuiz"
              >
                Nộp bài
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-5">
      <h3>Hết giờ hoặc đã nộp bài!</h3>
      <router-link to="/" class="btn btn-primary">Quay lại danh sách</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '@/api/axios'

const router = useRouter()
const route = useRoute()

const quiz = ref(null)
const questions = ref([])
const currentQuestionIndex = ref(0)
const selectedChoiceId = ref(null)
const userAnswers = ref({})
const timeLeft = ref(0)
const timerInterval = ref(null)
const loading = ref(true)
const error = ref(null)
const submitted = ref(false)

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value])

const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

const loadQuiz = async () => {
  try {
    const res = await apiClient.get(`/quizzes/${route.params.id}`)
    quiz.value = res.data.quiz
    questions.value = quiz.value.questions
    timeLeft.value = quiz.value.time_limit * 60
    startTimer()
  } catch (e) {
    error.value = e.response?.data?.error || 'Không tải được bài quiz'
  } finally {
    loading.value = false
  }
}

const startTimer = () => {
  timerInterval.value = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      clearInterval(timerInterval.value)
      autoSubmit()
    }
  }, 1000)
}

const selectChoice = (choiceId) => {
  selectedChoiceId.value = choiceId
  userAnswers.value[currentQuestion.value.id] = choiceId
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
    selectedChoiceId.value = userAnswers.value[questions.value[currentQuestionIndex.value].id] || null
  }
}

const prevQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    selectedChoiceId.value = userAnswers.value[questions.value[currentQuestionIndex.value].id] || null
  }
}

const autoSubmit = async () => {
  submitted.value = true
  await submitQuiz()
}

const submitQuiz = async () => {
  const answers = Object.entries(userAnswers.value).map(([question_id, choice_id]) => ({
    question_id: parseInt(question_id),
    choice_id: parseInt(choice_id)
  }))

  try {
    const timeSpent = quiz.value.time_limit * 60 - timeLeft.value
    const res = await apiClient.post(`/quizzes/${route.params.id}/submit`, {
      answers,
      time_spent: timeSpent
    })
    router.push({ name: 'QuizResult', params: { id: res.data.attempt.id } })
  } catch (e) {
    alert(e.response?.data?.error || 'Không nộp được bài')
  }
}

onMounted(loadQuiz)
onUnmounted(() => clearInterval(timerInterval.value))
</script>
