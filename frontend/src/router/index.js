import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'
import ServiceNeeds from '../views/ServiceNeeds.vue'
import ServiceHall from '../views/ServiceHall.vue'
import ServiceResponses from '../views/ServiceResponses.vue'
import NeedsManagement from '../views/NeedsManagement.vue'
import AdminStats from '../views/AdminStats.vue'

const routes = [
  { path: '/login', component: Login, name: 'Login' },
  { path: '/register', component: Register, name: 'Register' },
  { path: '/home', component: Home, name: 'Home' },
  { path: '/profile', component: Profile, name: 'Profile' },
  { path: '/my-services', component: ServiceNeeds, name: 'ServiceNeeds' },
  { path: '/service-hall', component: ServiceHall, name: 'ServiceHall' },
  { path: '/my-responses', component: ServiceResponses, name: 'ServiceResponses' },
  { path: '/needs-management', component: NeedsManagement, name: 'NeedsManagement' },
  { path: '/admin-stats', component: AdminStats, name: 'AdminStats' },
  { path: '/', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router