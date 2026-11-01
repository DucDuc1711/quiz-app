<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
      <div class="container">
        <router-link class="navbar-brand" to="/">← Về trang chủ</router-link>
      </div>
    </nav>

    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card shadow">
            <div class="card-header bg-success text-white">
              <h4 class="mb-0">Đăng ký tài khoản</h4>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleRegister" novalidate>
                <div class="mb-3">
                  <label class="form-label">Tên đăng nhập</label>
                  <input v-model="form.username" type="text" class="form-control" required minlength="3" />
                </div>
                <div class="mb-3">
                  <label class="form-label">Email</label>
                  <input v-model="form.email" type="email" class="form-control" required />
                </div>
                <div class="mb-3">
                  <label class="form-label">Mật khẩu</label>
                  <input v-model="form.password" type="password" class="form-control" required minlength="6" />
                </div>
                <div class="mb-3">
                  <label class="form-label">Nhập lại mật khẩu</label>
                  <input v-model="form.confirmPassword" type="password" class="form-control" required />
                </div>
                <div v-if="errorMessage" class="alert alert-danger mb-3">{{ errorMessage }}</div>
                <button class="btn btn-success w-100" type="submit">Đăng ký</button>
              </form>
            </div>
            <div class="card-footer text-center">
              <p class="mb-0">
                Đã có tài khoản?
                <router-link class="text-decoration-none fw-bold" to="/login">Đăng nhập ngay</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const errorMessage = ref('')

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const handleRegister = async () => {
  errorMessage.value = ''

  // Validate tên đăng nhập
  if (!form.value.username || form.value.username.trim().length < 6) {
    errorMessage.value = 'Tên đăng nhập phải có ít nhất 6 ký tự'
    return
  }

  // Validate email định dạng
  if (!EMAIL_REGEX.test(form.value.email)) {
    errorMessage.value = 'Email không hợp lệ'
    return
  }

  // Validate mật khẩu
  if (!form.value.password || form.value.password.length < 6) {
    errorMessage.value = 'Mật khẩu phải có ít nhất 6 ký tự'
    return
  }

  // Validate nhập lại mật khẩu
  if (form.value.password !== form.value.confirmPassword) {
    errorMessage.value = 'Mật khẩu nhập lại không khớp'
    return
  }

  try {
    await authStore.register({
      username: form.value.username.trim(),
      email: form.value.email.trim().toLowerCase(),
      password: form.value.password
    })
    router.push('/')
  } catch (e) {
    errorMessage.value = e.response?.data?.error || 'Có lỗi xảy ra, vui lòng thử lại'
  }
}
</script>
