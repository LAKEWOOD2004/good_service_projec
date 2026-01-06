<template>
  <div style="background: linear-gradient(135deg, #f0f9ff 0%, #f0fdf4 100%); min-height: 100vh;">
    <PageHeader 
      title="个人信息管理"
      subtitle="查看和编辑您的个人资料"
    />

    <v-container class="py-6">
      <v-row>
        <v-col cols="12" md="8" lg="6" class="mx-auto">
          <v-card elevation="4" class="rounded-xl overflow-hidden">
            <v-card-text class="pa-8">
              <div v-if="!editing">
                <v-row class="mb-6">
                  <v-col cols="12" md="6">
                    <div class="info-item pa-4 rounded-lg" style="background-color: #f5f5f5;">
                      <span class="label d-block mb-2">用户名</span>
                      <span class="value text-h6 font-weight-bold">{{ user.username }}</span>
                    </div>
                  </v-col>
                  <v-col cols="12" md="6">
                    <div class="info-item pa-4 rounded-lg" style="background-color: #f5f5f5;">
                      <span class="label d-block mb-2">真实姓名</span>
                      <span class="value text-h6 font-weight-bold">{{ user.real_name || '未设置' }}</span>
                    </div>
                  </v-col>
                </v-row>

                <v-row class="mb-6">
                  <v-col cols="12" md="6">
                    <div class="info-item pa-4 rounded-lg" style="background-color: #f5f5f5;">
                      <span class="label d-block mb-2">手机号码</span>
                      <span class="value text-h6 font-weight-bold">{{ user.phone || '未设置' }}</span>
                    </div>
                  </v-col>
                  <v-col cols="12" md="6">
                    <div class="info-item pa-4 rounded-lg" style="background-color: #f5f5f5;">
                      <span class="label d-block mb-2">用户类型</span>
                      <v-chip :color="user.user_type === 'admin' ? 'error' : 'primary'" text-color="white" class="mt-2">
                        {{ user.user_type === 'admin' ? '管理员' : '普通用户' }}
                      </v-chip>
                    </div>
                  </v-col>
                </v-row>

                <v-divider class="my-6"></v-divider>

                <v-row>
                  <v-col cols="12" sm="6">
                    <v-btn 
                      variant="flat" 
                      block
                      color="white"
                      class="rounded-lg font-weight-bold py-3"
                      style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);"
                      @click="editing = true"
                    >
                      <v-icon class="mr-2">mdi-pencil</v-icon>编辑信息
                    </v-btn>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-btn 
                      variant="outlined" 
                      block
                      color="primary" 
                      class="rounded-lg font-weight-bold py-3"
                      @click="passwordDialog = true"
                    >
                      <v-icon class="mr-2">mdi-lock-reset</v-icon>修改密码
                    </v-btn>
                  </v-col>
                </v-row>
              </div>

              <div v-else>
                <v-form ref="editForm" v-model="editValid">
                  <v-text-field
                    v-model="editData.phone"
                    label="手机号码"
                    prepend-inner-icon="mdi-phone"
                    :rules="[v => !v || /^\d{11}$/.test(v) || '必须是11位数字']"
                    class="mb-6"
                    variant="outlined"
                    color="primary"
                    density="default"
                  ></v-text-field>

                  <v-textarea
                    v-model="editData.bio"
                    label="个人简介"
                    rows="4"
                    counter="200"
                    maxlength="200"
                    class="mb-6"
                    variant="outlined"
                    color="primary"
                    density="default"
                  ></v-textarea>

                  <v-row>
                    <v-col cols="12" sm="6">
                      <v-btn 
                        variant="flat" 
                        block
                        color="white"
                        class="rounded-lg font-weight-bold py-3"
                        style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);"
                        @click="saveChanges" 
                        :loading="saving"
                      >
                        <v-icon class="mr-2">mdi-content-save</v-icon>保存
                      </v-btn>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-btn 
                        variant="outlined" 
                        block
                        color="primary" 
                        class="rounded-lg font-weight-bold py-3"
                        @click="editing = false"
                      >
                        <v-icon class="mr-2">mdi-cancel</v-icon>取消
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-form>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <v-dialog v-model="passwordDialog" max-width="500px">
      <v-card class="rounded-xl overflow-hidden">
        <div style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); color: white;" class="pa-6">
          <v-card-title class="text-h6 text-white pa-0">
            <v-icon class="mr-2">mdi-lock-reset</v-icon>修改密码
          </v-card-title>
        </div>

        <v-card-text class="py-6 px-6">
          <v-form ref="passwordForm" v-model="passwordFormValid">
            <v-text-field
              v-model="passwordData.oldPassword"
              label="原密码"
              type="password"
              required
              :rules="[v => !!v || '必填']"
              class="mb-6"
              variant="outlined"
              color="primary"
              density="default"
            ></v-text-field>

            <v-text-field
              v-model="passwordData.newPassword"
              label="新密码"
              type="password"
              :rules="passwordRules"
              class="mb-6"
              variant="outlined"
              color="primary"
              density="default"
            ></v-text-field>

            <v-text-field
              v-model="passwordData.confirmPassword"
              label="确认新密码"
              type="password"
              required
              :rules="[v => !!v || '必填', v => v === passwordData.newPassword || '两次输入不一致']"
              class="mb-6"
              variant="outlined"
              color="primary"
              density="default"
            ></v-text-field>

            <v-alert v-if="passwordError" type="error" closable variant="tonal">
              {{ passwordError }}
            </v-alert>
          </v-form>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="py-4 px-6">
          <v-spacer></v-spacer>
          <v-btn variant="outlined" color="primary" class="rounded-lg mr-3" @click="passwordDialog = false">取消</v-btn>
          <v-btn variant="flat" color="white" class="rounded-lg" style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);" @click="changePassword" :loading="passwordSubmitting">确认</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar" :color="snackbarColor" rounded="lg">{{ snackbarMessage }}</v-snackbar>
  </div>
</template>

<script setup name="ProfilePage">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import PageHeader from '@/components/PageHeader.vue'

const router = useRouter()

const user = ref({ id: null, username: '', real_name: '', phone: '', bio: '', user_type: 'normal' })
const editing = ref(false)
const editForm = ref(null)
const editValid = ref(false)
const editData = ref({ phone: '', bio: '' })
const saving = ref(false)
const passwordDialog = ref(false)
const passwordForm = ref(null)
const passwordFormValid = ref(false)
const passwordData = ref({ oldPassword: '', newPassword: '', confirmPassword: '' })
const passwordError = ref('')
const passwordSubmitting = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const passwordRules = [
  v => !!v || '必填',
  v => v.length >= 6 || '至少6位',
  v => (v.match(/\d/g) || []).length >= 2 || '至少2个数字'
]

onMounted(async () => {
  const userData = localStorage.getItem('user')
  if (!userData) {
    router.push('/login')
    return
  }
  try {
    const localUser = JSON.parse(userData)
    const res = await axios.get(`http://127.0.0.1:5000/api/user/${localUser.id}`)
    if (res.data.code === 200) {
      user.value = res.data.data
      editData.value.phone = res.data.data.phone || ''
      editData.value.bio = res.data.data.bio || ''
    }
  } catch (error) {
    console.error('加载用户信息失败:', error)
    snackbar.value = true
    snackbarMessage.value = '加载用户信息失败'
    snackbarColor.value = 'error'
  }
})

const saveChanges = async () => {
  if (!editValid.value) return
  saving.value = true
  try {
    const res = await axios.put(`http://127.0.0.1:5000/api/user/${user.value.id}`, {
      phone: editData.value.phone,
      bio: editData.value.bio
    })
    if (res.data.code === 200) {
      user.value.phone = editData.value.phone
      user.value.bio = editData.value.bio
      localStorage.setItem('user', JSON.stringify(user.value))
      editing.value = false
      snackbar.value = true
      snackbarMessage.value = '保存成功'
      snackbarColor.value = 'success'
    }
  } catch (error) {
    snackbarColor.value = 'error'
    snackbarMessage.value = error.response?.data?.msg || '失败'
    snackbar.value = true
  } finally {
    saving.value = false
  }
}

const changePassword = async () => {
  if (!passwordFormValid.value) return
  passwordSubmitting.value = true
  passwordError.value = ''
  try {
    const res = await axios.put(`http://127.0.0.1:5000/api/user/${user.value.id}/password`, {
      old_password: passwordData.value.oldPassword,
      new_password: passwordData.value.newPassword
    })
    if (res.data.code === 200) {
      passwordDialog.value = false
      snackbar.value = true
      snackbarMessage.value = '修改成功'
      snackbarColor.value = 'success'
      passwordData.value = { oldPassword: '', newPassword: '', confirmPassword: '' }
    } else {
      passwordError.value = res.data.msg
    }
  } catch (error) {
    passwordError.value = error.response?.data?.msg || '修改失败'
  } finally {
    passwordSubmitting.value = false
  }
}
</script>

<style scoped>
.label { font-weight: 600; color: #666; font-size: 12px; text-transform: uppercase; }
</style>
