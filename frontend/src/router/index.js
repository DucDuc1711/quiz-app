import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import QuizListView from '../views/QuizListView.vue'
import QuizTakeView from '../views/QuizTakeView.vue'
import QuizResultView from '../views/QuizResultView.vue'
import LeaderboardView from '../views/LeaderboardView.vue'
import HistoryView from '../views/HistoryView.vue'
import AdminDashboardView from '../views/admin/AdminDashboardView.vue'
import AdminQuizManageView from '../views/admin/AdminQuizManageView.vue'
import AdminQuestionManageView from '../views/admin/AdminQuestionManageView.vue'

const routes = [
  { path: '/', name: 'QuizList', component: QuizListView, meta: { requiresAuth: true } },
  { path: '/login', name: 'Login', component: LoginView, meta: { guestOnly: true } },
  { path: '/register', name: 'Register', component: RegisterView, meta: { guestOnly: true } },
  { path: '/quizzes/:id/take', name: 'QuizTake', component: QuizTakeView, meta: { requiresAuth: true } },
  { path: '/attempts/:id', name: 'QuizResult', component: QuizResultView, meta: { requiresAuth: true } },
  { path: '/quizzes/:id/leaderboard', name: 'Leaderboard', component: LeaderboardView, meta: { requiresAuth: true } },
  { path: '/me/history', name: 'History', component: HistoryView, meta: { requiresAuth: true } },
  
  // Admin routes
  { path: '/admin', name: 'AdminDashboard', component: AdminDashboardView, meta: { requiresAdmin: true } },
  { path: '/admin/quizzes', name: 'AdminQuizManage', component: AdminQuizManageView, meta: { requiresAdmin: true } },
  { path: '/admin/quizzes/:id/questions', name: 'AdminQuestionManage', component: AdminQuestionManageView, meta: { requiresAdmin: true } },
  
  { path: '/:catchAll(.*)', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login' })
  } else if (to.meta.guestOnly && authStore.isAuthenticated) {
    next({ name: 'QuizList' })
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    alert('Bạn không có quyền truy cập trang quản trị!')
    next({ name: 'QuizList' })
  } else {
    next()
  }
})

export default router
