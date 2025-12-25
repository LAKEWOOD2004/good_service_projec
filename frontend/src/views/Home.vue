<template>
  <v-app id="inspire">
    <!-- 侧边栏导航 -->
    <v-navigation-drawer 
      v-model="drawer" 
      :rail="!drawer"
      permanent
      color="white" 
      elevation="4"
    >
      <!-- 应用标题 -->
      <v-list-item 
        prepend-avatar="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='%232E7D32' d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z'/></svg>"
        title="好服务"
        subtitle="社区服务平台"
        class="mb-6 mt-3"
      ></v-list-item>

      <!-- 菜单项 -->
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

        <v-list-item 
          title="个人信息" 
          to="/profile" 
          prepend-icon="mdi-account"
          class="mb-2 rounded-lg mx-2"
          active-color="primary"
          @click="drawer = false"
        ></v-list-item>

        <!-- 管理员菜单 -->
        <v-divider class="my-3 mx-2" v-if="userType === 'admin'"></v-divider>
        <v-list-item 
          v-if="userType === 'admin'"
          title="统计仪表板" 
          to="/admin-stats" 
          prepend-icon="mdi-chart-box"
          class="mb-2 rounded-lg mx-2"
          active-color="primary"
          @click="drawer = false"
        ></v-list-item>
      </v-list>

      <v-spacer></v-spacer>

      <!-- 底部用户信息 -->
      <v-divider class="my-2 mx-2"></v-divider>
      <v-list density="compact">
        <v-list-item 
          :title="username" 
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

    <!-- 顶部应用栏 -->
    <v-app-bar color="white" elevation="4" density="comfortable">
      <v-app-bar-nav-icon @click="drawer = !drawer" color="primary"></v-app-bar-nav-icon>
      
      <v-app-bar-title class="font-weight-bold text-primary">
        <v-icon class="mr-2" color="primary">mdi-handshake</v-icon>
        好服务社区平台
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <!-- 用户芯片 -->
      <v-chip color="primary-light" text-color="primary" variant="flat" class="mr-4">
        <v-icon start>mdi-account-circle</v-icon>
        {{ username }}
      </v-chip>

      <!-- 退出按钮 -->
      <v-btn 
        icon 
        @click="handleLogout"
        color="primary"
        class="hover:bg-error-lighten"
      >
        <v-icon>mdi-logout</v-icon>
        <v-tooltip activator="parent">退出登录</v-tooltip>
      </v-btn>
    </v-app-bar>

    <!-- 主内容区域 -->
    <v-main class="bg-surface-variant" style="background: linear-gradient(135deg, #f0f9ff 0%, #f0fdf4 100%);">
      <v-container class="py-8" fluid>
        <!-- 欢迎横幅 -->
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
                  在这里，你可以发布服务需求、浏览社区帮助、或者提供自己的服务。
                  让我们一起构建一个温暖、互助的社区。
                </p>
                <div class="d-flex flex-wrap gap-3">
                  <v-chip 
                    variant="outlined"
                    text-color="white"
                    class="border-white hover:bg-white hover:text-primary transition-all duration-300"
                  >
                    <v-icon start>mdi-star</v-icon>
                    优质服务
                  </v-chip>
                  <v-chip 
                    variant="outlined"
                    text-color="white"
                    class="border-white hover:bg-white hover:text-primary transition-all duration-300"
                  >
                    <v-icon start>mdi-heart</v-icon>
                    热心帮助
                  </v-chip>
                  <v-chip 
                    variant="outlined"
                    text-color="white"
                    class="border-white hover:bg-white hover:text-primary transition-all duration-300"
                  >
                    <v-icon start>mdi-handshake</v-icon>
                    互帮互助
                  </v-chip>
                </div>
              </v-col>
              <v-col cols="12" md="4" class="text-center">
                <v-icon size="120" class="opacity-20">mdi-handshake</v-icon>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- 快捷操作卡片 -->
        <v-row class="mb-8">
          <v-col cols="12" sm="6" md="3">
            <v-card 
              elevation="4"
              class="rounded-xl h-100 hover:elevation-12 transition-all duration-300 cursor-pointer group"
              @click="$router.push('/service-hall')"
            >
              <v-card-text class="text-center py-8 px-4 d-flex flex-column align-center">
                <v-icon size="56" color="primary" class="mb-4 group-hover:scale-110 transition-all duration-300">mdi-shopping-search</v-icon>
                <h3 class="text-h6 font-weight-bold mb-2">服务大厅</h3>
                <p class="text-caption text-secondary">浏览社区最新<br>服务需求</p>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-card 
              elevation="4"
              class="rounded-xl h-100 hover:elevation-12 transition-all duration-300 cursor-pointer group"
              @click="$router.push('/my-services')"
            >
              <v-card-text class="text-center py-8 px-4 d-flex flex-column align-center">
                <v-icon size="56" color="primary" class="mb-4 group-hover:scale-110 transition-all duration-300">mdi-plus-circle</v-icon>
                <h3 class="text-h6 font-weight-bold mb-2">发布需求</h3>
                <p class="text-caption text-secondary">发布你的服务<br>需求</p>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-card 
              elevation="4"
              class="rounded-xl h-100 hover:elevation-12 transition-all duration-300 cursor-pointer group"
              @click="$router.push('/my-responses')"
            >
              <v-card-text class="text-center py-8 px-4 d-flex flex-column align-center">
                <v-icon size="56" color="primary" class="mb-4 group-hover:scale-110 transition-all duration-300">mdi-hand-heart</v-icon>
                <h3 class="text-h6 font-weight-bold mb-2">我的服务</h3>
                <p class="text-caption text-secondary">管理你提供<br>的服务</p>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-card 
              elevation="4"
              class="rounded-xl h-100 hover:elevation-12 transition-all duration-300 cursor-pointer group"
              @click="$router.push('/profile')"
            >
              <v-card-text class="text-center py-8 px-4 d-flex flex-column align-center">
                <v-icon size="56" color="primary" class="mb-4 group-hover:scale-110 transition-all duration-300">mdi-account-circle</v-icon>
                <h3 class="text-h6 font-weight-bold mb-2">个人中心</h3>
                <p class="text-caption text-secondary">管理你的个人<br>信息</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- 平台特色 -->
        <v-card elevation="4" class="rounded-xl mb-8">
          <v-card-title class="text-h5 font-weight-bold d-flex align-center pa-6">
            <v-icon color="primary" class="mr-3">mdi-lightbulb-outline</v-icon>
            平台特色
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pa-6">
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <div class="d-flex mb-4">
                  <v-avatar size="50" color="primary-lighter" class="mr-4">
                    <v-icon color="primary">mdi-shield-check</v-icon>
                  </v-avatar>
                  <div>
                    <h4 class="font-weight-bold mb-1">安全可信</h4>
                    <p class="text-caption text-secondary">实名认证、信息保护，让你安心</p>
                  </div>
                </div>
              </v-col>

              <v-col cols="12" sm="6" md="4">
                <div class="d-flex mb-4">
                  <v-avatar size="50" color="primary-lighter" class="mr-4">
                    <v-icon color="primary">mdi-account-multiple</v-icon>
                  </v-avatar>
                  <div>
                    <h4 class="font-weight-bold mb-1">互帮互助</h4>
                    <p class="text-caption text-secondary">社区用户相互帮助，共同进步</p>
                  </div>
                </div>
              </v-col>

              <v-col cols="12" sm="6" md="4">
                <div class="d-flex mb-4">
                  <v-avatar size="50" color="primary-lighter" class="mr-4">
                    <v-icon color="primary">mdi-chart-line</v-icon>
                  </v-avatar>
                  <div>
                    <h4 class="font-weight-bold mb-1">数据透明</h4>
                    <p class="text-caption text-secondary">所有数据实时更新，透明可查</p>
                  </div>
                </div>
              </v-col>

              <v-col cols="12" sm="6" md="4">
                <div class="d-flex">
                  <v-avatar size="50" color="primary-lighter" class="mr-4">
                    <v-icon color="primary">mdi-lightning-bolt</v-icon>
                  </v-avatar>
                  <div>
                    <h4 class="font-weight-bold mb-1">快速响应</h4>
                    <p class="text-caption text-secondary">需求发布后快速获得响应</p>
                  </div>
                </div>
              </v-col>

              <v-col cols="12" sm="6" md="4">
                <div class="d-flex">
                  <v-avatar size="50" color="primary-lighter" class="mr-4">
                    <v-icon color="primary">mdi-map-marker</v-icon>
                  </v-avatar>
                  <div>
                    <h4 class="font-weight-bold mb-1">位置服务</h4>
                    <p class="text-caption text-secondary">基于地区的精准匹配</p>
                  </div>
                </div>
              </v-col>

              <v-col cols="12" sm="6" md="4">
                <div class="d-flex">
                  <v-avatar size="50" color="primary-lighter" class="mr-4">
                    <v-icon color="primary">mdi-headset</v-icon>
                  </v-avatar>
                  <div>
                    <h4 class="font-weight-bold mb-1">客户支持</h4>
                    <p class="text-caption text-secondary">专业团队为你服务</p>
                  </div>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
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
  box-shadow: 0 10px 40px rgba(46, 125, 50, 0.15);
  position: relative;
  overflow: hidden;
}

.gradient-card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  animation: pulse 8s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.3;
  }
}

.group:hover {
  transform: translateY(-4px);
}

.border-white {
  border-color: rgba(255, 255, 255, 0.5) !important;
}

.border-white:hover {
  border-color: rgba(255, 255, 255, 1) !important;
}

.h-100 {
  height: 100%;
}

.cursor-pointer {
  cursor: pointer;
}
</style>