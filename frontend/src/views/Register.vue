<template>
  <v-container class="fill-height bg-gradient" style="background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="5" lg="4">
        <v-card class="elevation-16 rounded-xl overflow-hidden">
          <!-- 卡片头部 -->
          <v-card-title class="text-h4 text-center white--text pa-6" style="background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);">
            <v-icon size="40" class="mb-2">mdi-heart</v-icon>
            <br>
            用户注册
          </v-card-title>
          
          <!-- 卡片内容 -->
          <v-card-text class="pa-6">
            <v-form ref="form" v-model="valid">
              <v-text-field
                v-model="user.username"
                label="用户名"
                prepend-icon="mdi-account"
                required
                :rules="[v => !!v || '用户名必填', v => v.length >= 3 || '用户名至少3个字符']"
                class="mb-4"
                variant="outlined"
                density="comfortable"
                hide-details="auto"
                color="primary"
              ></v-text-field>

              <v-text-field
                v-model="user.password"
                label="密码"
                type="password"
                prepend-icon="mdi-lock"
                append-icon="mdi-eye-off"
                :rules="passwordRules"
                required
                hint="至少6位，含2个数字，不能全大写或全小写"
                persistent-hint
                class="mb-4"
                variant="outlined"
                density="comfortable"
                hide-details="auto"
                color="primary"
              ></v-text-field>

              <v-text-field
                v-model="user.phone"
                label="手机号码"
                prepend-icon="mdi-phone"
                :rules="[v => !!v || '手机号必填', v => /^\d{11}$/.test(v) || '必须是11位数字']"
                class="mb-6"
                variant="outlined"
                density="comfortable"
                hide-details="auto"
                color="primary"
              ></v-text-field>
            </v-form>
          </v-card-text>
          
          <!-- 卡片底部 -->
          <v-card-actions class="pa-6">
            <v-spacer></v-spacer>
            <v-btn 
              color="primary"
              :disabled="!valid"
              @click="handleRegister"
              :loading="registerLoading"
              variant="flat"
              class="text-white rounded-lg font-weight-medium px-8 py-3"
              style="background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);"
            >
              <v-icon class="mr-2">mdi-account-plus</v-icon>
              提交注册
            </v-btn>
          </v-card-actions>
        </v-card>

        <!-- 页脚信息 -->
        <div class="text-center mt-4">
          <span class="text-white text-caption">© 2025 好服务平台 | 用心服务，让生活更美好</span>
        </div>
      </v-col>
    </v-row>
    
    <!-- 消息提示 -->
    <v-snackbar 
      v-model="snackbar" 
      :color="sbColor"
      class="elevation-4"
      rounded
      timeout="3000"
    >
      <v-icon class="mr-2">{{ sbColor === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle' }}</v-icon>
      {{ sbText }}
    </v-snackbar>
  </v-container>
</template>

<script setup name="RegisterPage">
import { ref, reactive } from 'vue'
import axios from 'axios'

const valid = ref(false)
const snackbar = ref(false)
const sbText = ref('')
const sbColor = ref('success')
const registerLoading = ref(false)

const user = reactive({
  username: '',
  password: '',
  phone: ''
})

// 对应你的需求：密码不少于6位，必含有两个数字，不能都为大写或小写
const passwordRules = [
  v => !!v || '密码必填',
  v => v.length >= 6 || '长度至少6位',
  v => (v.match(/\d/g) || []).length >= 2 || '必须含有至少两个数字',
  v => !(/^[a-z]+$/.test(v) || /^[A-Z]+$/.test(v)) || '不能全是大写或小写'
]

const handleRegister = async () => {
  registerLoading.value = true
  
  try {
    await axios.post('http://127.0.0.1:5000/api/register', user)
    sbText.value = "注册成功！"
    sbColor.value = "success"
    snackbar.value = true
    
    // 重置表单
    user.username = ''
    user.password = ''
    user.phone = ''
    valid.value = false
  } catch (error) {
    sbText.value = error.response?.data?.msg || "注册失败"
    sbColor.value = "error"
    snackbar.value = true
  } finally {
    registerLoading.value = false
  }
}
</script>