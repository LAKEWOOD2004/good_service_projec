<template>
  <div style="background: linear-gradient(135deg, #f0f9ff 0%, #f0fdf4 100%); min-height: 100vh;">
    <PageHeader 
      title="我的服务响应"
      subtitle="管理您对服务需求的响应"
    />

    <v-container class="py-6">
      <v-card elevation="4" class="rounded-xl overflow-hidden">
        <v-table v-if="responses.length > 0" class="rounded-xl">
          <thead>
            <tr style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); color: white;">
              <th class="font-weight-bold">需求</th>
              <th class="font-weight-bold">响应内容</th>
              <th class="font-weight-bold">状态</th>
              <th class="font-weight-bold">提交时间</th>
              <th class="font-weight-bold">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="response in responses" :key="response.id">
              <td class="font-weight-bold">{{ response.need_title }}</td>
              <td class="text-sm" style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ response.content }}</td>
              <td>
                <v-chip :color="getStatusColor(response.status)" text-color="white" size="small">{{ response.status_text }}</v-chip>
              </td>
              <td class="text-sm">{{ formatDate(response.create_time) }}</td>
              <td>
                <v-btn variant="outlined" color="primary" size="x-small" class="mr-2" @click="viewDetail(response)">详情</v-btn>
                <v-btn v-if="response.status === 0" variant="outlined" color="error" size="x-small" @click="deleteResponse(response)">删除</v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>

        <v-card-text v-else class="text-center py-12">
          <v-icon size="64" color="primary" class="mb-4" style="opacity: 0.5;">mdi-inbox-outline</v-icon>
          <p class="text-h6" style="color: #999;">暂无响应</p>
        </v-card-text>
      </v-card>

      <v-row class="mt-6" v-if="pagination.totalPages > 1">
        <v-col cols="12">
          <v-pagination
            v-model="pagination.page"
            :length="pagination.totalPages"
            @update:model-value="loadResponses"
            color="primary"
          ></v-pagination>
        </v-col>
      </v-row>
    </v-container>

    <!-- 详情对话框 -->
    <v-dialog v-model="detailDialog.show" max-width="600px">
      <v-card v-if="detailDialog.response" class="rounded-xl overflow-hidden">
        <div style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); color: white;" class="pa-6">
          <v-card-title class="text-h6 text-white pa-0">
            <v-icon class="mr-2">mdi-file-document</v-icon>响应详情
          </v-card-title>
        </div>

        <v-card-text class="py-6 px-6" style="max-height: 60vh; overflow-y: auto;">
          <div class="mb-6">
            <span class="text-sm font-weight-bold" style="color: #999;">需求</span>
            <p class="mt-2 text-h6 font-weight-bold">{{ detailDialog.response.need_title }}</p>
          </div>

          <div class="mb-6">
            <span class="text-sm font-weight-bold" style="color: #999;">响应内容</span>
            <div class="mt-2 pa-4 rounded-lg" style="background-color: #f5f5f5; line-height: 1.6;">{{ detailDialog.response.content }}</div>
          </div>

          <div v-if="detailDialog.response.media_url" class="mb-6">
            <span class="text-sm font-weight-bold" style="color: #999;">响应附件</span>
            <div class="mt-2">
              <video 
                v-if="detailDialog.response.media_url.toLowerCase().match(/\.(mp4|avi|mov)$/)" 
                :src="'http://127.0.0.1:5000' + detailDialog.response.media_url" 
                controls 
                style="max-width: 100%; border-radius: 12px; border: 1px solid #e0e0e0;"
              ></video>
              
              <v-img 
                v-else 
                :src="'http://127.0.0.1:5000' + detailDialog.response.media_url" 
                max-height="300" 
                class="rounded-xl bg-grey-lighten-4"
              >
                <template v-slot:placeholder>
                  <v-row class="fill-height ma-0" align="center" justify="center">
                    <v-progress-circular indeterminate color="grey-lighten-5"></v-progress-circular>
                  </v-row>
                </template>
              </v-img>
            </div>
          </div>

          <div class="mb-6">
            <span class="text-sm font-weight-bold" style="color: #999;">状态</span>
            <v-chip :color="getStatusColor(detailDialog.response.status)" text-color="white" class="mt-2">{{ detailDialog.response.status_text }}</v-chip>
          </div>

          <div class="mb-6">
            <span class="text-sm font-weight-bold" style="color: #999;">提交时间</span>
            <p class="mt-2">{{ formatDate(detailDialog.response.create_time) }}</p>
          </div>

          <div v-if="detailDialog.response.review_time">
            <span class="text-sm font-weight-bold" style="color: #999;">审核时间</span>
            <p class="mt-2">{{ formatDate(detailDialog.response.review_time) }}</p>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="py-4 px-6">
          <v-spacer></v-spacer>
          <v-btn variant="outlined" color="primary" class="rounded-lg" @click="detailDialog.show = false">关闭</v-btn>
          <v-btn v-if="detailDialog.response.status === 0" variant="flat" color="white" class="rounded-lg ml-2" style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);" @click="deleteResponse(detailDialog.response); detailDialog.show = false">删除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 删除确认对话框 -->
    <v-dialog v-model="deleteDialog.show" max-width="400px">
      <v-card class="rounded-xl overflow-hidden">
        <div style="background: linear-gradient(135deg, #FF6F00 0%, #F57C00 100%); color: white;" class="pa-6">
          <v-card-title class="text-h6 text-white pa-0">
            <v-icon class="mr-2">mdi-alert</v-icon>确认删除
          </v-card-title>
        </div>

        <v-card-text class="py-6 px-6">
          <p>确定要删除这条响应吗？此操作不可恢复。</p>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="py-4 px-6">
          <v-spacer></v-spacer>
          <v-btn variant="outlined" color="primary" class="rounded-lg" @click="deleteDialog.show = false">取消</v-btn>
          <v-btn variant="flat" color="white" class="rounded-lg ml-2" style="background: linear-gradient(135deg, #FF6F00 0%, #F57C00 100%);" @click="confirmDelete" :loading="deleteDialog.loading">删除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" rounded="lg">{{ snackbar.message }}</v-snackbar>
  </div>
</template>

<script setup name="ServiceResponses">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import PageHeader from '@/components/PageHeader.vue'

const router = useRouter()

const responses = ref([])
const pagination = ref({ page: 1, pageSize: 10, totalPages: 1 })
const detailDialog = ref({ show: false, response: null })
const deleteDialog = ref({ show: false, response: null, loading: false })
const snackbar = ref({ show: false, message: '', color: 'success' })

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = (now - date) / 1000
  if (diff < 60) return '刚刚'
  if (diff < 3600) return Math.floor(diff / 60) + '分钟前'
  if (diff < 86400) return Math.floor(diff / 3600) + '小时前'
  return date.toLocaleDateString('zh-CN')
}

const getStatusColor = (status) => {
  const colors = { 
    0: '#2196F3', // 0: 待处理 (蓝色)
    1: '#4CAF50', // 1: 已同意 (绿色)
    2: '#F44336', // 2: 已拒绝 (红色)
    3: '#9E9E9E'  // 3: 已取消 (灰色)
  }
  return colors[status] || '#616161'
}

// 修改加载数据逻辑：正确映射 status_text
const loadResponses = async () => {
  try {
    const userData = localStorage.getItem('user')
    if (!userData) {
      router.push('/login')
      return
    }
    const user = JSON.parse(userData)

    const params = {
      page: pagination.value.page,
      per_page: pagination.value.pageSize
    }
    const res = await axios.get(`http://127.0.0.1:5000/api/user/${user.id}/responses`, { params })
    if (res.data.code === 200) {
      responses.value = res.data.data.map(r => ({
        id: r.id,
        need_title: r.need_subject || r.subject || '未知需求',
        content: r.content,
        media_url: r.media_url, // <--- 【新增】这里接收后端传来的图片地址
        status: r.status, 
        create_time: r.created_at,
        review_time: r.review_time,
        status_text: r.status === 0 ? '待处理' : 
                     r.status === 1 ? '已同意' : 
                     r.status === 2 ? '已拒绝' : 
                     r.status === 3 ? '已取消' : '未知状态'
      }))
      pagination.value.totalPages = res.data.pagination?.pages || 1
    }
  } catch (error) {
    console.error('加载失败:', error)
    snackbar.value = { show: true, message: error.response?.data?.msg || '加载失败', color: 'error' }
  }
}

const viewDetail = (response) => {
  detailDialog.value.response = response
  detailDialog.value.show = true
}

const deleteResponse = (response) => {
  deleteDialog.value.response = response
  deleteDialog.value.show = true
}

const confirmDelete = async () => {
  if (!deleteDialog.value.response) return
  deleteDialog.value.loading = true
  
  try {
    // 1. 先获取当前用户ID (为了传给后端做权限验证)
    const userData = localStorage.getItem('user')
    const user = JSON.parse(userData)

    // 2. 【关键修改】axios.delete 传参需要包在 { data: ... } 里
    const res = await axios.delete(
      `http://127.0.0.1:5000/api/service-responses/${deleteDialog.value.response.id}`,
      {
        data: {
          user_id: user.id
        }
      }
    )

    if (res.data.code === 200) {
      snackbar.value = { show: true, message: '删除成功', color: 'success' }
      deleteDialog.value.show = false
      loadResponses()
    }
  } catch (error) {
    console.error(error) // 方便调试
    snackbar.value = { show: true, message: error.response?.data?.msg || '删除失败', color: 'error' }
  } finally {
    deleteDialog.value.loading = false
  }
}

onMounted(() => {
  loadResponses()
})
</script>

<style scoped>
table {
  border-collapse: collapse;
}
thead tr {
  border-bottom: 2px solid #e0e0e0;
}
tbody tr {
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s;
}
tbody tr:hover {
  background-color: #f5f5f5;
}
</style>

