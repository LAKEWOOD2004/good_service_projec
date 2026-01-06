<template>
  <div style="background: linear-gradient(135deg, #f0f9ff 0%, #f0fdf4 100%); min-height: 100vh;">
    <PageHeader 
      title="我需要 - 服务需求管理"
      subtitle="发布和管理您的服务需求"
    >
      <template #actions>
        <v-btn
          color="white"
          variant="flat"
          class="rounded-lg font-weight-bold text-subtitle-2"
          @click="openPublishDialog"
          style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);"
        >
          <v-icon class="mr-2">mdi-plus</v-icon>
          发布新需求
        </v-btn>
      </template>
    </PageHeader>

    <v-container class="py-6">
      <v-row>
        <v-col cols="12" md="10" lg="9" class="mx-auto">
          <!-- 我发布的需求列表 -->
          <v-card elevation="4" class="rounded-xl overflow-hidden">
            <v-card-text class="pa-6">
              <h3 class="text-h6 font-weight-bold mb-6 text-primary">我发布的需求</h3>
              
              <v-data-table
                v-if="myNeeds.length > 0"
                :headers="headers"
                :items="myNeeds"
                :items-per-page="10"
                class="elevation-0"
                hide-default-footer
              >
                <template v-slot:item.subject="{ item }">
                  <div class="font-semibold text-primary">{{ item.subject }}</div>
                </template>
                <template v-slot:item.service_type="{ item }">
                  <v-chip size="small" variant="tonal" color="secondary">
                    {{ item.service_type }}
                  </v-chip>
                </template>
                <template v-slot:item.status="{ item }">
                  <v-chip
                    :color="getStatusColor(item.status)"
                    text-color="white"
                    size="small"
                  >
                    {{ item.status_text }}
                  </v-chip>
                </template>
                <template v-slot:item.created_at="{ item }">
                  <div class="text-caption text-secondary">{{ formatDate(item.created_at) }}</div>
                </template>
                <template v-slot:item.action="{ item }">
                  <div class="d-flex gap-2">
                    <v-btn
                      variant="outlined"
                      color="primary"
                      size="x-small"
                      class="rounded-md"
                      @click="openEditDialog(item)"
                      :disabled="item.status !== 0"
                    >
                      编辑
                    </v-btn>
                    <v-btn
                      variant="outlined"
                      color="error"
                      size="x-small"
                      class="rounded-md"
                      @click="deleteNeed(item.id)"
                      :disabled="item.status !== 0"
                    >
                      删除
                    </v-btn>
                  </div>
                </template>
              </v-data-table>

              <v-alert v-else type="info" title="暂无需求" class="rounded-lg" variant="tonal">
                您还没有发布任何服务需求，点击上方"发布新需求"按钮来创建一个。
              </v-alert>

              <!-- 分页 -->
              <v-pagination
                v-if="pagination.pages > 1"
                v-model="currentPage"
                :length="pagination.pages"
                class="mt-8"
                color="primary"
                rounded
                @update:model-value="loadMyNeeds"
              ></v-pagination>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- 发布/编辑需求对话框 -->
    <v-dialog v-model="publishDialog" max-width="600px">
      <v-card class="rounded-xl overflow-hidden">
        <v-card-title class="text-h6 pa-6" style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); color: white;">
          {{ editingNeed ? '编辑需求' : '发布新的服务需求' }}
        </v-card-title>

        <v-card-text class="pa-6">
          <v-form ref="needForm" v-model="needFormValid">
            <v-text-field
              v-model="needData.subject"
              label="需求标题"
              required
              :rules="[v => !!v || '标题必填']"
              class="mb-4"
              variant="outlined"
              color="primary"
              density="default"
              placeholder="请输入需求标题"
            ></v-text-field>

            <v-select
              v-model="needData.service_type"
              label="服务类型"
              :items="serviceTypes"
              required
              :rules="[v => !!v || '服务类型必填']"
              class="mb-4"
              variant="outlined"
              color="primary"
              density="default"
            ></v-select>

            <v-select
              v-model="needData.region_id"
              label="所在地域"
              :items="regions"
              item-title="full_name"
              item-value="id"
              class="mb-4"
              variant="outlined"
              color="primary"
              density="default"
            ></v-select>

            <v-textarea
              v-model="needData.description"
              label="需求描述"
              rows="5"
              counter="500"
              maxlength="500"
              class="mb-4"
              variant="outlined"
              color="primary"
              density="default"
              placeholder="请详细描述您的服务需求"
            ></v-textarea>

            <v-alert v-if="needError" type="error" closable variant="tonal">
              {{ needError }}
            </v-alert>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn variant="outlined" color="primary" class="rounded-lg font-weight-medium" @click="publishDialog = false">
            取消
          </v-btn>
          <v-btn
            color="white"
            variant="flat"
            class="rounded-lg font-weight-medium"
            style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);"
            @click="submitNeed"
            :loading="needSubmitting"
            :disabled="!needFormValid"
          >
            {{ editingNeed ? '更新' : '发布' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 消息提示 -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" rounded="lg">
      {{ snackbarMessage }}
    </v-snackbar>
  </div>
</template>

<script setup name="ServiceNeedPage">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import PageHeader from '@/components/PageHeader.vue'

// 表格表头配置
const headers = ref([
  { title: '标题', key: 'subject' },
  { title: '服务类型', key: 'service_type' },
  { title: '状态', key: 'status' },
  { title: '发布时间', key: 'created_at' },
  { title: '操作', key: 'action', width: 150, align: 'end' }
])

const router = useRouter()

// 数据
const myNeeds = ref([])
const regions = ref([])
const currentPage = ref(1)
const pagination = ref({
  pages: 0,
  total: 0,
  per_page: 10
})

// 服务类型选项
const serviceTypes = ref([
  '管道维修',
  '助老服务',
  '保洁服务',
  '就诊服务',
  '营养餐服务',
  '定期接送服务',
  '其他'
])

// 发布/编辑表单
const publishDialog = ref(false)
const needForm = ref(null)
const needFormValid = ref(false)
const needData = ref({
  subject: '',
  service_type: '',
  region_id: null,
  description: ''
})
const editingNeed = ref(null)
const needError = ref('')
const needSubmitting = ref(false)

// 消息提示
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

// 当前用户信息
const user = ref(null)

// 初始化
onMounted(() => {
  const userData = localStorage.getItem('user')
  if (!userData) {
    router.push('/login')
    return
  }
  
  user.value = JSON.parse(userData)
  loadRegions()
  loadMyNeeds()
})

// 加载地域列表
const loadRegions = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/api/regions')
    if (res.data.code === 200) {
      regions.value = res.data.data
    }
  } catch (error) {
    console.error('加载地域失败', error)
  }
}

// 加载我的需求
const loadMyNeeds = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:5000/api/my-service-needs/${user.value.id}`, {
      params: {
        page: currentPage.value,
        per_page: 10
      }
    })
    
    if (res.data.code === 200) {
      myNeeds.value = res.data.data
      pagination.value = res.data.pagination
    }
  } catch (error) {
    showMessage(error.response?.data?.msg || '加载失败', 'error')
  }
}

// 打开发布对话框
const openPublishDialog = () => {
  editingNeed.value = null
  needData.value = {
    subject: '',
    service_type: '',
    region_id: null,
    description: ''
  }
  needError.value = ''
  publishDialog.value = true
}

// 打开编辑对话框
const openEditDialog = (need) => {
  editingNeed.value = need
  needData.value = {
    subject: need.subject,
    service_type: need.service_type,
    region_id: need.region_id || null,
    description: need.description
  }
  needError.value = ''
  publishDialog.value = true
}

// 提交需求
const submitNeed = async () => {
  if (!needFormValid.value) return
  
  needSubmitting.value = true
  needError.value = ''
  
  try {
    const payload = {
      ...needData.value,
      user_id: user.value.id
    }
    
    let res
    if (editingNeed.value) {
      res = await axios.put(
        `http://127.0.0.1:5000/api/service-needs/${editingNeed.value.id}`,
        payload
      )
    } else {
      res = await axios.post('http://127.0.0.1:5000/api/service-needs', payload)
    }
    
    if (res.data.code === 200) {
      publishDialog.value = false
      showMessage(editingNeed.value ? '更新成功' : '发布成功', 'success')
      loadMyNeeds()
    } else {
      needError.value = res.data.msg
    }
  } catch (error) {
    needError.value = error.response?.data?.msg || '操作失败'
  } finally {
    needSubmitting.value = false
  }
}

// 删除需求
const deleteNeed = async (needId) => {
  if (!confirm('确认删除此需求吗？')) return
  
  try {
    const res = await axios.delete(`http://127.0.0.1:5000/api/service-needs/${needId}`, {
      data: {
        user_id: user.value.id
      }
    })
    
    if (res.data.code === 200) {
      showMessage('删除成功', 'success')
      loadMyNeeds()
    } else {
      showMessage(res.data.msg, 'error')
    }
  } catch (error) {
    showMessage(error.response?.data?.msg || '删除失败', 'error')
  }
}

// 获取状态颜色
const getStatusColor = (status) => {
  const colors = {
    0: '#4CAF50', // 绿色 - 进行中
    1: '#757575', // 灰色 - 已完成
    2: '#FFA726'  // 橙色 - 已过期
  }
  return colors[status] || 'grey'
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

// 显示消息
const showMessage = (message, color = 'success') => {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
