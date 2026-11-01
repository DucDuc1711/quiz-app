<template>
  <div class="container">
    <nav class="navbar navbar-light bg-light mb-4">
      <div class="container">
        <router-link class="navbar-brand" to="/admin">← Quay lại Dashboard</router-link>
      </div>
    </nav>

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Quản lý bộ Quiz</h2>
      <button class="btn btn-success" @click="showCreateModal = true">
        <i class="bi bi-plus-lg"></i> Thêm mới
      </button>
    </div>

    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div class="table-responsive">
        <table class="table table-striped table-hover align-middle">
          <thead class="table-dark">
            <tr>
              <th>STT</th>
              <th>Tên bộ quiz</th>
              <th>Mô tả</th>
              <th>Thời gian</th>
              <th>Số câu</th>
              <th>Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(q, idx) in quizzes" :key="q.id">
              <td>{{ idx + 1 }}</td>
              <td class="fw-bold">{{ q.title }}</td>
              <td class="text-truncate" style="max-width: 300px">{{ q.description }}</td>
              <td>{{ q.time_limit }} phút</td>
              <td>{{ q.question_count }}</td>
              <td>
                <router-link :to="{ name: 'AdminQuestionManage', params: { id: q.id } }" class="btn btn-sm btn-primary">Quản lý câu hỏi</router-link>
                <button class="btn btn-sm btn-outline-warning" @click="editQuiz(q)">Sửa</button>
                <button class="btn btn-sm btn-outline-danger" @click="deleteQuiz(q.id)">Xóa</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal tạo / sửa quiz -->
    <div v-if="showCreateModal" class="modal fade show d-block" style="display: block;" role="dialog">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-{{ isEdit ? 'warning' : 'success' }} text-white">
            <h5 class="modal-title">{{ isEdit ? 'Cập nhật' : 'Tạo mới' }} bộ quiz</h5>
            <button class="btn-close btn-close-white" @click="showCreateModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveQuiz">
              <div class="mb-3">
                <label class="form-label">Tên bộ quiz</label>
                <input v-model="quizForm.title" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Mô tả</label>
                <textarea v-model="quizForm.description" class="form-control" rows="2"></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Thời gian (phút)</label>
                <input v-model.number="quizForm.time_limit" type="number" class="form-control" required min="1" />
              </div>
              <button class="btn btn-{{ isEdit ? 'warning' : 'success' }} w-100" type="submit">{{ isEdit ? 'Cập nhật' : 'Tạo mới' }}</button>
            </form>
          </div>
        </div>
      </div>
      <div class="modal-backdrop fade show"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '@/api/axios'

const quizzes = ref([])
const loading = ref(true)
const error = ref(null)
const showCreateModal = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const quizForm = ref({ title: '', description: '', time_limit: 10 })

const loadQuizzes = async () => {
  try {
    const res = await apiClient.get('/admin/quizzes')
    quizzes.value = res.data.quizzes
  } catch (e) {
    error.value = e.response?.data?.error || 'Không tải được danh sách quiz'
  } finally {
    loading.value = false
  }
}

const saveQuiz = async () => {
  try {
    if (isEdit.value && editId.value) {
      await apiClient.put(`/admin/quizzes/${editId.value}`, quizForm.value)
    } else {
      await apiClient.post('/admin/quizzes', quizForm.value)
    }
    showCreateModal.value = false
    quizForm.value = { title: '', description: '', time_limit: 10 }
    isEdit.value = false
    editId.value = null
    loadQuizzes()
  } catch (e) {
    alert(e.response?.data?.error || 'Lưu thất bại')
  }
}

const editQuiz = (q) => {
  isEdit.value = true
  editId.value = q.id
  quizForm.value = { title: q.title, description: q.description, time_limit: q.time_limit }
  showCreateModal.value = true
}

const deleteQuiz = async (id) => {
  if (!confirm('Bạn chắc chắn muốn xóa bộ quiz này?')) return
  try {
    await apiClient.delete(`/admin/quizzes/${id}`)
    loadQuizzes()
  } catch (e) {
    alert(e.response?.data?.error || 'Xóa thất bại')
  }
}

onMounted(loadQuizzes)
</script>
