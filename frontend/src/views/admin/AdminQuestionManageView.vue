<template>
  <div class="container">
    <nav class="navbar navbar-light bg-light mb-4">
      <div class="container">
        <router-link class="navbar-brand" to="/admin/quizzes">← Quay lại Quản lý Quiz</router-link>
      </div>
    </nav>

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Quản lý câu hỏi</h2>
      <button class="btn btn-success" @click="showQuestionModal = true">
        <i class="bi bi-plus-lg"></i> Thêm câu hỏi
      </button>
    </div>

    <div v-if="loadingQuiz" class="text-center py-4">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else-if="quiz">
      <div class="card mb-4">
        <div class="card-body">
          <h5 class="card-title">{{ quiz.title }}</h5>
          <p class="text-muted">{{ quiz.description }}</p>
          <span class="badge bg-secondary">{{ quiz.question_count }} câu hỏi</span>
        </div>
      </div>

      <div v-if="quiz.questions.length === 0" class="text-center py-4 text-muted">
        Chưa có câu hỏi nào trong bộ quiz này.
      </div>

      <div v-else>
        <div class="table-responsive">
          <table class="table table-striped table-hover align-middle">
            <thead class="table-dark">
              <tr>
                <th>STT</th>
                <th>Nội dung câu hỏi</th>
                <th>Đáp án đúng</th>
                <th>Hành động</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(q, idx) in quiz.questions" :key="q.id">
                <td>{{ idx + 1 }}</td>
                <td class="fw-bold">{{ q.content }}</td>
                <td><span class="badge bg-success">{{ getCorrectChoice(q.choices) }}</span></td>
                <td>
                  <button class="btn btn-sm btn-outline-primary" @click="editQuestion(q)">Sửa</button>
                  <button class="btn btn-sm btn-outline-danger" @click="deleteQuestion(q.id)">Xóa</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
      <!-- Modal tạo / sửa câu hỏi -->
      <div v-if="showQuestionModal" class="modal fade show d-block" style="display: block;" role="dialog">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header bg-{{ isEditQuestion ? 'warning' : 'success' }} text-white">
              <h5 class="modal-title">{{ isEditQuestion ? 'Cập nhật' : 'Tạo mới' }} câu hỏi</h5>
              <button class="btn-close btn-close-white" @click="showQuestionModal = false"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveQuestion">
                <div class="mb-3">
                  <label class="form-label">Nội dung câu hỏi</label>
                  <input v-model="questionForm.content" class="form-control" required />
                </div>
                <div class="mb-3">
                  <label class="form-label">Giải thích đáp án đúng</label>
                  <textarea v-model="questionForm.explanation" class="form-control" rows="2"></textarea>
                </div>
                <div class="mb-3 border rounded p-3 bg-light">
                  <label class="form-label fw-bold">4 đáp án</label>
                  <div v-for="(c, idx) in questionForm.choices" :key="idx" class="mb-2 row align-items-center">
                    <div class="col-2 fw-bold">Đáp án {{ idx + 1 }}</div>
                    <div class="col-8">
                      <input v-model="c.content" class="form-control" required />
                    </div>
                    <div class="col-2 text-end">
                      <input type="radio" v-model="questionForm.correctIndex" :value="idx" class="form-check-input mt-1" required />
                    </div>
                  </div>
                  <div class="text-danger small" v-if="choiceError">{{ choiceError }}</div>
                </div>
                <button class="btn btn-{{ isEditQuestion ? 'warning' : 'success' }} w-100" type="submit">{{ isEditQuestion ? 'Cập nhật' : 'Tạo mới' }}</button>
              </form>
            </div>
          </div>
        </div>
        <div class="modal-backdrop fade show"></div>
      </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '@/api/axios'

const route = useRoute()
const router = useRouter()

const quiz = ref(null)
const loadingQuiz = ref(true)
const error = ref(null)
const showQuestionModal = ref(false)
const isEditQuestion = ref(false)
const editQuestionId = ref(null)
const questionForm = ref({
  content: '',
  explanation: '',
  choices: [{ content: '', is_correct: false }, { content: '', is_correct: false }, { content: '', is_correct: false }, { content: '', is_correct: false }],
  correctIndex: 0
})
const choiceError = ref(null)

const loadQuiz = async () => {
  try {
    const res = await apiClient.get(`/admin/quizzes/${route.params.id}`)
    quiz.value = res.data.quiz
  } catch (e) {
    error.value = e.response?.data?.error || 'Không tải được thông tin quiz'
  } finally {
    loadingQuiz.value = false
  }
}

const getCorrectChoice = (choices) => {
  const c = choices.find(x => x.is_correct)
  return c ? c.content : ''
}

const saveQuestion = async () => {
  choiceError.value = null
  const correctCount = questionForm.value.choices.filter(c => c.is_correct).length
  if (correctCount !== 1) { choiceError.value = 'Phải đánh dấu chính xác 1 đáp án đúng'; return }
  if (questionForm.value.choices.some(c => !c.content.trim())) { choiceError.value = 'Vui lòng điền đầy đủ nội dung 4 đáp án'; return }

  const payload = {
    content: questionForm.value.content,
    explanation: questionForm.value.explanation,
    choices: questionForm.value.choices.map((c, idx) => ({ content: c.content, is_correct: idx === questionForm.value.correctIndex }))
  }

  try {
    if (isEditQuestion.value && editQuestionId.value) {
      await apiClient.put(`/admin/questions/${editQuestionId.value}`, payload)
    } else {
      await apiClient.post(`/admin/quizzes/${route.params.id}/questions`, payload)
    }
    showQuestionModal.value = false
    loadQuiz()
    resetForm()
  } catch (e) {
    alert(e.response?.data?.error || 'Lưu câu hỏi thất bại')
  }
}

const editQuestion = (q) => {
  isEditQuestion.value = true
  editQuestionId.value = q.id
  questionForm.value = { content: q.content, explanation: q.explanation || '', choices: q.choices.map(c => ({ content: c.content, is_correct: c.is_correct })), correctIndex: q.choices.findIndex(c => c.is_correct) }
  showQuestionModal.value = true
}

const deleteQuestion = async (id) => {
  if (!confirm('Xóa câu hỏi này?')) return
  try {
    await apiClient.delete(`/admin/questions/${id}`)
    loadQuiz()
  } catch (e) {
    alert(e.response?.data?.error || 'Xóa thất bại')
  }
}

const resetForm = () => {
  questionForm.value = { content: '', explanation: '', choices: [{ content: '', is_correct: false }, { content: '', is_correct: false }, { content: '', is_correct: false }, { content: '', is_correct: false }], correctIndex: 0 }
  isEditQuestion.value = false
  editQuestionId.value = null
}

onMounted(loadQuiz)
</script>
