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
                  <div class="d-flex gap-2 justify-end">
                    <v-btn
                      variant="flat"
                      color="secondary" 
                      size="x-small"
                      class="rounded-md text-white"
                      @click="openResponseListDialog(item)"
                    >
                      查看响应
                      <v-badge
                        v-if="item.responses && item.responses.length > 0"
                        :content="item.responses.length"
                        color="error"
                        floating
                        offset-x="-2"
                        offset-y="-2"
                      ></v-badge>
                    </v-btn>

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
              density="comfortable"
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
              density="comfortable"
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
              density="comfortable"
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
              density="comfortable"
              placeholder="请详细描述您的服务需求"
            ></v-textarea>

            <v-file-input
              v-model="needData.file"
              label="上传图片或视频（可选）"
              accept="image/*,video/*"
              prepend-inner-icon="mdi-camera"
              variant="outlined"
              show-size
              class="mb-6"
            ></v-file-input>

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

    <v-dialog v-model="responseListDialog.show" max-width="700px" scrollable>
      <v-card class="rounded-xl overflow-hidden">
        <div style="background: linear-gradient(135deg, #1976D2 0%, #64B5F6 100%); color: white;" class="pa-6">
          <v-card-title class="text-h6 text-white pa-0">
            <v-icon class="mr-2">mdi-account-group</v-icon>
            响应管理 - {{ responseListDialog.title }}
          </v-card-title>
        </div>

        <v-card-text class="pa-0" style="max-height: 60vh; overflow-y: auto;">
          <div v-if="!responseListDialog.list || responseListDialog.list.length === 0" class="text-center pa-12">
            <v-icon size="64" color="grey lighten-2">mdi-comment-off-outline</v-icon>
            <p class="text-grey mt-4">暂无响应信息</p>
          </div>

          <v-list v-else lines="three" class="pa-2">
            <template v-for="(resp, index) in responseListDialog.list" :key="resp.id">
              <v-list-item class="mb-2 rounded-lg elevation-1 ma-2 pa-4">
                <template v-slot:prepend>
                  <v-avatar color="primary" class="text-white">
                    {{ resp.responder_name ? resp.responder_name[0] : 'U' }}
                  </v-avatar>
                </template>

                <v-list-item-title class="font-weight-bold mb-1">
                  {{ resp.responder_name || '匿名用户' }}
                  <v-chip :color="getResponseStatusColor(resp.status)" size="x-small" class="ml-2 text-white">
                    {{ getResponseStatusText(resp.status) }}
                  </v-chip>
                </v-list-item-title>

                <v-list-item-subtitle class="text-body-2 text-high-emphasis mb-2">
                  {{ resp.content }}
                </v-list-item-subtitle>
                
                <div v-if="resp.media_url" class="mt-2 mb-2">
                  <video 
                    v-if="resp.media_url.toLowerCase().match(/\.(mp4|avi|mov)$/)" 
                    :src="'http://127.0.0.1:5000' + resp.media_url" 
                    controls 
                    style="max-width: 200px; border-radius: 8px; border: 1px solid #eee;"
                  ></video>
                  <v-img 
                    v-else 
                    :src="'http://127.0.0.1:5000' + resp.media_url" 
                    max-width="200" 
                    max-height="150"
                    class="rounded-lg bg-grey-lighten-4"
                    cover
                  ></v-img>
                </div>

                <template v-slot:append>
                  <div class="d-flex flex-column gap-2" v-if="resp.status === 0">
                    <v-btn
                      color="success"
                      size="small"
                      variant="flat"
                      @click="handleResponse(resp, 1)"
                      :loading="resp.loading"
                    >
                      接受
                    </v-btn>
                    <v-btn
                      color="error"
                      size="small"
                      variant="outlined"
                      @click="handleResponse(resp, 2)"
                      :loading="resp.loading"
                    >
                      拒绝
                    </v-btn>
                  </div>
                  <div v-else class="text-caption text-grey">
                    已处理
                  </div>
                </template>
              </v-list-item>
              <v-divider v-if="index < responseListDialog.list.length - 1"></v-divider>
            </template>
          </v-list>
        </v-card-text>

        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="responseListDialog.show = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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

// 【关键修改点 3】增加操作列宽度，以容纳新按钮 (220)
const headers = ref([
  { title: '标题', key: 'subject' },
  { title: '服务类型', key: 'service_type' },
  { title: '状态', key: 'status' },
  { title: '发布时间', key: 'created_at' },
  { title: '操作', key: 'action', width: 220, align: 'end' } 
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
  description: '',
  file: null
})
const editingNeed = ref(null)
const needError = ref('')
const needSubmitting = ref(false)

// 【关键修改点 4】新增：响应列表对话框状态
const responseListDialog = ref({
  show: false,
  title: '',
  list: [],
  needId: null
})

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
      // 确保 responses 存在
      myNeeds.value = res.data.data.map(item => ({
        ...item,
        responses: item.responses || []
      }))
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
    description: '',
    file: null
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

// 【关键修改点 5】新增：打开响应列表对话框
const openResponseListDialog = (need) => {
  responseListDialog.value.title = need.subject
  responseListDialog.value.needId = need.id
  // 增加 loading 状态字段
  responseListDialog.value.list = need.responses.map(r => ({ ...r, loading: false }))
  responseListDialog.value.show = true
}

// 【关键修改点 6】新增：处理响应（接受/拒绝）
const handleResponse = async (response, status) => {
  // status: 1=接受, 2=拒绝
  response.loading = true
  try {
    // 调用更新接口
    const res = await axios.put(`http://127.0.0.1:5000/api/service-responses/${response.id}`, {
      user_id: user.value.id, // 必须传当前用户ID以校验权限
      status: status
    })

    if (res.data.code === 200) {
      showMessage(status === 1 ? '已接受该响应' : '已拒绝该响应', 'success')
      // 更新本地状态
      response.status = status
      // 重新加载列表以确保同步
      loadMyNeeds()
    } else {
      showMessage(res.data.msg, 'error')
    }
  } catch (error) {
    showMessage(error.response?.data?.msg || '操作失败', 'error')
  } finally {
    response.loading = false
  }
}

// 提交需求
const submitNeed = async () => {
  if (!needFormValid.value) return
  
  needSubmitting.value = true
  needError.value = ''
  
  try {
    let res
    
    // 情况 A: 编辑模式
    if (editingNeed.value) {
      const payload = {
        ...needData.value,
        user_id: user.value.id
      }
      res = await axios.put(
        `http://127.0.0.1:5000/api/service-needs/${editingNeed.value.id}`,
        payload
      )
    } 
    // 情况 B: 发布新需求
    else {
      const formData = new FormData()
      formData.append('user_id', user.value.id)
      formData.append('subject', needData.value.subject)
      formData.append('service_type', needData.value.service_type)
      formData.append('description', needData.value.description)
      if (needData.value.region_id) {
        formData.append('region_id', needData.value.region_id)
      }
      if (needData.value.file) {
        const fileToUpload = Array.isArray(needData.value.file) ? needData.value.file[0] : needData.value.file
        formData.append('file', fileToUpload)
      }

      res = await axios.post('http://127.0.0.1:5000/api/service-needs', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }
    
    if (res.data.code === 200) {
      publishDialog.value = false
      showMessage(editingNeed.value ? '更新成功' : '发布成功', 'success')
      loadMyNeeds()
    } else {
      needError.value = res.data.msg
    }
  } catch (error) {
    console.error(error)
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
    2: '#FFA726', // 橙色 - 已过期
    '-1': '#FF5252' // 红色 - 已取消
  }
  return colors[status] || 'grey'
}

// 【关键修改点 7】新增：获取响应状态颜色
const getResponseStatusColor = (status) => {
  const colors = {
    0: 'info',     // 待处理
    1: 'success',  // 已接受
    2: 'error',    // 已拒绝
    3: 'grey'      // 已取消
  }
  return colors[status] || 'grey'
}

// 【关键修改点 8】新增：获取响应状态文字
const getResponseStatusText = (status) => {
  const texts = {
    0: '待处理',
    1: '已接受',
    2: '已拒绝',
    3: '已取消'
  }
  return texts[status] || '未知'
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