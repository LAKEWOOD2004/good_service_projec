<template>
  <v-app id="inspire">
    <v-navigation-drawer 
      v-model="drawer" 
      :rail="!drawer"
      permanent
      color="white" 
      elevation="4"
    >
      <v-list-item 
        prepend-avatar="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='%232E7D32' d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z'/></svg>"
        title="好服务"
        subtitle="社区服务平台"
        class="mb-6 mt-3"
      ></v-list-item>

      <v-divider class="my-2 mx-2"></v-divider>
      
      <v-list nav density="compact">
        <v-list-item 
          title="服务大厅" 
          to="/service-hall" 
          prepend-icon="mdi-shopping-search"
          class="mb-2 rounded-lg mx-2"
          active-color="primary"
          @click="drawer = false"
        ></v-list-item>

        <template v-if="userType !== 'admin'">
          <v-list-item 
            title="发布需求" 
            to="/my-services" 
            prepend-icon="mdi-plus-circle"
            class="mb-2 rounded-lg mx-2"
            active-color="primary"
            @click="drawer = false"
          ></v-list-item>

          <v-list-item 
            title="需求管理" 
            to="/needs-management" 
            prepend-icon="mdi-inbox"
            class="mb-2 rounded-lg mx-2"
            active-color="primary"
            @click="drawer = false"
          ></v-list-item>

          <v-list-item 
            title="我的服务" 
            to="/my-responses" 
            prepend-icon="mdi-hand-heart"
            class="mb-2 rounded-lg mx-2"
            active-color="primary"
            @click="drawer = false"
          ></v-list-item>
        </template>

        <template v-if="userType === 'admin'">
          <v-divider class="my-3 mx-2"></v-divider>
          <v-list-item 
            title="统计仪表板" 
            to="/admin-stats" 
            prepend-icon="mdi-chart-box"
            class="mb-2 rounded-lg mx-2"
            active-color="primary"
            @click="drawer = false"
          ></v-list-item>
        </template>

        <v-list-item 
          title="个人信息" 
          to="/profile" 
          prepend-icon="mdi-account"
          class="mb-2 rounded-lg mx-2"
          active-color="primary"
          @click="drawer = false"
        ></v-list-item>
      </v-list>

      <v-spacer></v-spacer>

      <v-divider class="my-2 mx-2"></v-divider>
      <v-list density="compact">
        <v-list-item 
          :title="username" 
          :subtitle="userType === 'admin' ? '系统管理员' : '普通用户'"
          prepend-icon="mdi-account-circle"
          class="mb-2 rounded-lg mx-2"
        ></v-list-item>
        <v-list-item 
          title="退出登录" 
          prepend-icon="mdi-logout"
          class="rounded-lg mx-2"
          @click="handleLogout"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar color="white" elevation="4" density="comfortable">
      <v-app-bar-nav-icon @click="drawer = !drawer" color="primary"></v-app-bar-nav-icon>
      
      <v-app-bar-title class="font-weight-bold text-primary">
        <v-icon class="mr-2" color="primary">mdi-handshake</v-icon>
        好服务社区平台
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <v-chip color="primary-light" text-color="primary" variant="flat" class="mr-4">
        <v-icon start>mdi-account-circle</v-icon>
        {{ username }}
      </v-chip>

      <v-btn icon @click="handleLogout" color="primary">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main class="bg-surface-variant" style="background: linear-gradient(135deg, #f0f9ff 0%, #f0fdf4 100%);">
      <v-container class="py-8" fluid>
        <div v-if="$route.path === '/home'">
          <v-card 
            elevation="0"
            class="rounded-2xl overflow-hidden mb-8 gradient-card"
            style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); color: white;"
          >
            <v-card-text class="pa-8 py-12">
              <v-row align="center" justify="space-between">
                <v-col cols="12" md="8">
                  <h1 class="text-h3 font-weight-bold mb-4 text-white">
                    👋 欢迎回来，{{ username }}！
                  </h1>
                  <p class="text-subtitle-1 mb-6 text-white opacity-95 leading-relaxed">
                    {{ userType === 'admin' ? '您正在以管理员身份登录，请查看系统统计数据。' : '在这里，你可以发布服务需求、浏览社区帮助、或者提供自己的服务。' }}
                  </p>
                </v-col>
                <v-col cols="12" md="4" class="text-center">
                  <v-icon size="120" class="opacity-20">mdi-handshake</v-icon>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <v-row class="mb-8">
            <v-col cols="12" sm="6" md="3">
              <v-card elevation="4" class="rounded-xl h-100 hover:elevation-12 transition-all cursor-pointer" @click="$router.push('/service-hall')">
                <v-card-text class="text-center py-8 d-flex flex-column align-center">
                  <v-icon size="56" color="primary" class="mb-4">mdi-shopping-search</v-icon>
                  <h3 class="text-h6 font-weight-bold">服务大厅</h3>
                  <p class="text-caption text-secondary">浏览所有需求</p>
                </v-card-text>
              </v-card>
            </v-col>

            <template v-if="userType !== 'admin'">
              <v-col cols="12" sm="6" md="3">
                <v-card elevation="4" class="rounded-xl h-100 hover:elevation-12 transition-all cursor-pointer" @click="$router.push('/my-services')">
                  <v-card-text class="text-center py-8 d-flex flex-column align-center">
                    <v-icon size="56" color="primary" class="mb-4">mdi-plus-circle</v-icon>
                    <h3 class="text-h6 font-weight-bold">发布需求</h3>
                    <p class="text-caption text-secondary">寻求帮助</p>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-card elevation="4" class="rounded-xl h-100 hover:elevation-12 transition-all cursor-pointer" @click="$router.push('/my-responses')">
                  <v-card-text class="text-center py-8 d-flex flex-column align-center">
                    <v-icon size="56" color="primary" class="mb-4">mdi-hand-heart</v-icon>
                    <h3 class="text-h6 font-weight-bold">我的服务</h3>
                    <p class="text-caption text-secondary">管理我的响应</p>
                  </v-card-text>
                </v-card>
              </v-col>
            </template>

            <template v-if="userType === 'admin'">
              <v-col cols="12" sm="6" md="3">
                <v-card elevation="4" class="rounded-xl h-100 hover:elevation-12 transition-all cursor-pointer" @click="$router.push('/admin-stats')">
                  <v-card-text class="text-center py-8 d-flex flex-column align-center">
                    <v-icon size="56" color="error" class="mb-4">mdi-chart-box</v-icon>
                    <h3 class="text-h6 font-weight-bold">统计仪表板</h3>
                    <p class="text-caption text-secondary">查看系统数据</p>
                  </v-card-text>
                </v-card>
              </v-col>
            </template>

            <v-col cols="12" sm="6" md="3">
              <v-card elevation="4" class="rounded-xl h-100 hover:elevation-12 transition-all cursor-pointer" @click="$router.push('/profile')">
                <v-card-text class="text-center py-8 d-flex flex-column align-center">
                  <v-icon size="56" color="primary" class="mb-4">mdi-account-circle</v-icon>
                  <h3 class="text-h6 font-weight-bold">个人中心</h3>
                  <p class="text-caption text-secondary">管理账号信息</p>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </div>

        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup name="HomePage">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const drawer = ref(true)
const username = ref('用户')
const userType = ref('normal')
const router = useRouter()

onMounted(() => {
  const userData = localStorage.getItem('user')
  if (userData) {
    const user = JSON.parse(userData)
    username.value = user.real_name || user.username
    userType.value = user.user_type
  } else {
    router.push('/login')
  }
})

const handleLogout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.gradient-card {
  position: relative;
}
.h-100 { height: 100%; }
.cursor-pointer { cursor: pointer; }
</style>