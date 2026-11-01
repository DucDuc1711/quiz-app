<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
    <div class="container">
      <router-link class="navbar-brand" to="/">Quiz App</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.name === 'QuizList' }" to="/">Danh sách Quiz</router-link>
          </li>
          <li class="nav-item" v-if="isAuthenticated">
            <router-link class="nav-link" :class="{ active: $route.name === 'History' }" to="/me/history">Lịch sử làm bài</router-link>
          </li>
          <li class="nav-item" v-if="isAdmin">
            <router-link class="nav-link" :class="{ active: $route.name === 'AdminDashboard' }" to="/admin">Quản trị</router-link>
          </li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item" v-if="!isAuthenticated">
            <router-link class="btn btn-light btn-sm text-dark" to="/login">Đăng nhập</router-link>
          </li>
          <li class="nav-item" v-if="!isAuthenticated">
            <router-link class="btn btn-outline-light btn-sm" to="/register">Đăng ký</router-link>
          </li>
          <li class="nav-item" v-if="isAuthenticated">
            <span class="nav-link text-white">{{ user.username }} ({{ user.role }})</span>
            <button class="btn btn-danger btn-sm ms-2" @click="handleLogout">Đăng xuất</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <main class="container mt-5 pt-4">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </main>

  <footer class="text-center text-muted py-4">
    <div class="container">
      <p class="mb-0 small">© 2026 Hệ thống Quiz Trực Tuyến</p>
    </div>
  </footer>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const { user, isAuthenticated, isAdmin } = storeToRefs(authStore)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
