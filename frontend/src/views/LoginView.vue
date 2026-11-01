<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
    <div class="container">
      <router-link class="navbar-brand" to="/">← Về trang chủ</router-link>
    </div>
  </nav>

  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-5">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h4 class="mb-0">{{ isLogin ? 'Đăng nhập' : 'Đăng ký tài khoản' }}</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleSubmit" novalidate>
              <div class="mb-3">
                <label class="form-label">Tên đăng nhập hoặc email</label>
                <input v-model="form.usernameOrEmail" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Mật khẩu</label>
                <input v-model="form.password" type="password" class="form-control" required />
              </div>
              <div v-if="errorMessage" class="alert alert-danger mb-3">{{ errorMessage }}</div>
              <button class="btn btn-primary w-100" type="submit">{{ isLogin ? 'Đăng nhập' : 'Đăng ký' }}</button>
            </form>
          </div>
          <div class="card-footer text-center">
            <p class="mb-0">
              {{ isLogin ? 'Chưa có tài khoản?' : 'Đã có tài khoản?' }}
              <router-link class="text-decoration-none" @click="toggleMode">
                {{ isLogin ? 'Đăng ký ngay' : 'Đăng nhập tại đây' }}
              </router-link>
            </p>
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
const isLogin = ref(true)

const form = ref({
  usernameOrEmail: '',
  password: ''
})

const errorMessage = ref('')

const toggleMode = () => { isLogin.value = !isLogin.value }

const handleSubmit = async () => {
  errorMessage.value = ''
  try {
    if (isLogin.value) {
      await authStore.login({
        username_or_email: form.value.usernameOrEmail,
        password: form.value.password
      })
      router.push('/')
    } else {
      await authStore.register({
        username: form.value.usernameOrEmail,
        email: form.value.usernameOrEmail,
        password: form.value.password
      })
      router.push('/')
    }
  } catch (e) {
    errorMessage.value = e.response?.data?.error || 'Có lỗi xảy ra, vui lòng thử lại'
  }
}
</script>
