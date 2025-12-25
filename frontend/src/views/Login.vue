<template>
  <div class="login-container" style="background: linear-gradient(135deg, #C8E6C9 0%, #BBDEFB 100%); min-height: 100vh; width: 100%; display: flex; align-items: center; justify-content: center;">
    <v-container class="py-8">
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="5" lg="4">
        <!-- 主卡片 -->
        <v-card class="elevation-12 overflow-hidden" style="border-radius: 20px; box-shadow: 0 20px 60px rgba(46, 125, 50, 0.2);">
          <!-- 卡片头部 - 渐变背景 -->
          <div class="page-header text-center py-8 px-6" style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); border-radius: 20px 20px 0 0;">
            <v-icon size="56" class="mb-3" style="color: white;">mdi-handshake</v-icon>
            <h1 class="text-h4 font-weight-bold mb-2" style="color: white; letter-spacing: -1px;">好服务平台</h1>
            <p class="text-subtitle-2 mb-0" style="color: rgba(255,255,255,0.9);">用心服务 · 让生活更美好</p>
          </div>
          
          <!-- 卡片内容 -->
          <v-card-text class="pa-8">
            <!-- 标签页 -->
            <v-tabs 
              v-model="tab" 
              class="mb-8"
              color="primary"
              slider-color="primary"
              density="comfortable"
              show-arrows
            >
              <v-tab 
                value="login" 
                class="font-weight-bold text-subtitle-2"
              >
                <v-icon class="mr-2">mdi-account-circle</v-icon>
                登录
              </v-tab>
              <v-tab 
                value="register" 
                class="font-weight-bold text-subtitle-2"
              >
                <v-icon class="mr-2">mdi-account-plus</v-icon>
                注册
              </v-tab>
            </v-tabs>

            <!-- 标签页内容 -->
            <v-window v-model="tab" transition="fade-transition">
              <!-- 登录表单 -->
              <v-window-item value="login">
                <v-form ref="loginForm" v-model="loginValid">
                  <div class="form-group">
                    <v-text-field
                      v-model="loginData.username"
                      label="用户名"
                      prepend-inner-icon="mdi-account"
                      required
                      :rules="[v => !!v || '用户名必填']"
                      class="mb-5"
                      variant="outlined"
                      density="comfortable"
                      hide-details="auto"
                      color="primary"
                      placeholder="输入用户名或邮箱"
                      autocomplete="username"
                    ></v-text-field>
                  </div>

                  <div class="form-group">
                    <v-text-field
                      v-model="loginData.password"
                      label="密码"
                      type="password"
                      prepend-inner-icon="mdi-lock"
                      required
                      :rules="[v => !!v || '密码必填']"
                      class="mb-6"
                      variant="outlined"
                      density="comfortable"
                      hide-details="auto"
                      color="primary"
                      placeholder="输入密码"
                      autocomplete="current-password"
                    ></v-text-field>
                  </div>

                  <!-- 登录按钮 -->
                  <v-btn
                    color="white"
                    block
                    size="large"
                    @click="handleLogin"
                    :loading="loginLoading"
                    class="mb-4 font-weight-bold text-subtitle-1 rounded-lg"
                    style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); color: white; min-height: 48px; text-transform: none; letter-spacing: 0.5px;"
                  >
                    <v-icon class="mr-2">mdi-login</v-icon>
                    登录
                  </v-btn>

                  <!-- 演示账户提示 -->
                  <v-alert
                    type="info"
                    class="mb-4 rounded-lg"
                    density="compact"
                    variant="tonal"
                    icon="mdi-information"
                  >
                    <div class="text-caption font-weight-bold mb-1">演示账户</div>
                    <div class="text-caption">admin / admin (管理员)</div>
                    <div class="text-caption">user1 / Pass1234 (普通用户)</div>
                  </v-alert>

                  <!-- 错误提示 -->
                  <v-alert
                    v-if="loginError"
                    type="error"
                    closable
                    class="rounded-lg"
                    variant="tonal"
                    icon="mdi-alert-circle"
                  >
                    {{ loginError }}
                  </v-alert>
                </v-form>
              </v-window-item>

              <!-- 注册表单 -->
              <v-window-item value="register">
                <v-form ref="registerForm" v-model="registerValid">
                  <div class="form-group">
                    <v-text-field
                      v-model="registerData.username"
                      label="用户名"
                      prepend-inner-icon="mdi-account"
                      required
                      :rules="[v => !!v || '用户名必填', v => v.length >= 3 || '用户名至少3个字符']"
                      class="mb-5"
                      variant="outlined"
                      density="comfortable"
                      hide-details="auto"
                      color="primary"
                      placeholder="输入用户名"
                    ></v-text-field>
                  </div>

                  <div class="form-group">
                    <v-text-field
                      v-model="registerData.password"
                      label="密码"
                      type="password"
                      prepend-inner-icon="mdi-lock"
                      :rules="passwordRules"
                      class="mb-5"
                      variant="outlined"
                      density="comfortable"
                      color="primary"
                      placeholder="至少6位，含2个数字，不能全大写或小写"
                      hide-details="auto"
                    ></v-text-field>
                    <!-- 密码强度指示器 -->
                    <div class="mt-2 mb-5">
                      <v-progress-linear
                        :value="getPasswordStrength(registerData.password)"
                        :color="getPasswordColor(registerData.password)"
                        height="6"
                        class="rounded-lg"
                      ></v-progress-linear>
                      <p class="text-caption mt-1" :style="{ color: getPasswordColor(registerData.password) }">
                        密码强度: {{ getPasswordStrengthText(registerData.password) }}
                      </p>
                    </div>
                  </div>

                  <div class="form-group">
                    <v-text-field
                      v-model="registerData.phone"
                      label="手机号码"
                      prepend-inner-icon="mdi-phone"
                      :rules="[v => !!v || '手机号必填', v => /^\d{11}$/.test(v) || '必须是11位数字']"
                      class="mb-6"
                      variant="outlined"
                      density="comfortable"
                      hide-details="auto"
                      color="primary"
                      placeholder="输入11位手机号码"
                    ></v-text-field>
                  </div>

                  <!-- 注册按钮 -->
                  <v-btn
                    color="white"
                    block
                    size="large"
                    @click="handleRegister"
                    :disabled="!registerValid"
                    :loading="registerLoading"
                    class="mb-4 font-weight-bold text-subtitle-1 rounded-lg"
                    style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); color: white; min-height: 48px; text-transform: none; letter-spacing: 0.5px;"
                  >
                    <v-icon class="mr-2">mdi-account-plus</v-icon>
                    注册
                  </v-btn>

                  <!-- 错误提示 -->
                  <v-alert
                    v-if="registerError"
                    type="error"
                    closable
                    class="mb-4 rounded-lg"
                    variant="tonal"
                    icon="mdi-alert-circle"
                  >
                    {{ registerError }}
                  </v-alert>

                  <!-- 成功提示 -->
                  <v-alert
                    v-if="registerSuccess"
                    type="success"
                    closable
                    class="rounded-lg"
                    variant="tonal"
                    icon="mdi-check-circle"
                  >
                    {{ registerSuccess }}
                  </v-alert>
                </v-form>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>

        <!-- 页脚 -->
        <div class="text-center mt-6">
          <p class="text-subtitle-2 font-weight-500" style="color: rgba(255,255,255,0.9);">
            © 2025 好服务平台
          </p>
          <p class="text-caption" style="color: rgba(255,255,255,0.7);">用心服务，让生活更美好</p>
        </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup name="LoginPage">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const tab = ref('login')

// 登录数据
const loginForm = ref(null)
const loginData = ref({
  username: '',
  password: ''
})
const loginValid = ref(false)
const loginLoading = ref(false)
const loginError = ref('')

// 注册数据
const registerForm = ref(null)
const registerData = ref({
  username: '',
  password: '',
  phone: ''
})
const registerValid = ref(false)
const registerLoading = ref(false)
const registerError = ref('')
const registerSuccess = ref('')

const passwordRules = [
  v => !!v || '密码必填',
  v => v.length >= 6 || '长度至少6位',
  v => (v.match(/\d/g) || []).length >= 2 || '必须含有至少两个数字',
  v => !(/^[a-z]+$/.test(v) || /^[A-Z]+$/.test(v)) || '不能全是大写或小写'
]

// 密码强度计算
const getPasswordStrength = (password) => {
  if (!password) return 0
  let strength = 0
  if (password.length >= 6) strength += 20
  if (password.length >= 8) strength += 10
  if (password.length >= 12) strength += 10
  if (/[a-z]/.test(password)) strength += 15
  if (/[A-Z]/.test(password)) strength += 15
  if (/\d/.test(password)) strength += 15
  if (/[!@#$%^&*()_+=\-{};':"\\|,.<>/?]/.test(password)) strength += 15
  return Math.min(strength, 100)
}

const getPasswordColor = (password) => {
  const strength = getPasswordStrength(password)
  if (strength < 40) return '#EF5350'
  if (strength < 70) return '#FFA726'
  return '#4CAF50'
}

const getPasswordStrengthText = (password) => {
  const strength = getPasswordStrength(password)
  if (strength < 40) return '弱'
  if (strength < 70) return '中'
  return '强'
}

// 登录处理
const handleLogin = async () => {
  if (!loginValid.value) return
  
  loginLoading.value = true
  loginError.value = ''
  
  try {
    const res = await axios.post('http://127.0.0.1:5000/api/login', {
      username: loginData.value.username,
      password: loginData.value.password
    })
    
    if (res.data.code === 200) {
      // 保存用户信息到 localStorage
      localStorage.setItem('user', JSON.stringify(res.data.data))
      // 跳转到首页
      router.push('/home')
    } else {
      loginError.value = res.data.msg
    }
  } catch (error) {
    loginError.value = error.response?.data?.msg || '登录失败'
  } finally {
    loginLoading.value = false
  }
}

// 注册处理
const handleRegister = async () => {
  if (!registerValid.value) return
  
  registerLoading.value = true
  registerError.value = ''
  registerSuccess.value = ''
  
  try {
    const res = await axios.post('http://127.0.0.1:5000/api/register', {
      username: registerData.value.username,
      password: registerData.value.password,
      phone: registerData.value.phone
    })
    
    if (res.data.code === 200) {
      registerSuccess.value = '注册成功！请切换到登录标签进行登录'
      registerData.value = {
        username: '',
        password: '',
        phone: ''
      }
    } else {
      registerError.value = res.data.msg
    }
  } catch (error) {
    registerError.value = error.response?.data?.msg || '注册失败'
  } finally {
    registerLoading.value = false
  }
}
</script>

<style scoped>
.h-100 {
  height: 100%;
}

.form-group {
  margin-bottom: 20px;
}
</style>

