<template>
  <div style="background: linear-gradient(135deg, #f0f9ff 0%, #f0fdf4 100%); min-height: 100vh;">
    <PageHeader 
      title="需求管理"
      subtitle="管理您发布的服务需求"
    />

    <v-container class="py-6">
      <v-row class="mb-6">
        <v-col cols="12">
          <v-btn 
            variant="flat" 
            color="white"
            size="large"
            class="rounded-lg font-weight-bold"
            style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); min-height: 48px;"
            @click="$router.push('/my-services')"
          >
            <v-icon class="mr-2">mdi-plus</v-icon>发布新需求
          </v-btn>
        </v-col>
      </v-row>

      <div v-if="needs.length > 0">
        <v-expansion-panels>
          <v-expansion-panel v-for="need in needs" :key="need.id">
            <template v-slot:title>
              <div class="d-flex align-center justify-space-between w-100">
                <span class="font-weight-bold">{{ need.title }}</span>
                <v-chip :color="getStatusColor(need.status)" text-color="white" size="small">{{ need.status_text }}</v-chip>
              </div>
            </template>

            <v-card elevation="0" class="mt-4">
              <v-card-text class="pa-6">
                <v-row class="mb-6">
                  <v-col cols="12" md="6">
                    <div class="info-item pa-4 rounded-lg" style="background-color: #f5f5f5;">
                      <span class="label d-block mb-2">服务类型</span>
                      <v-chip :color="getTypeColor(need.service_type)" text-color="white" size="small">{{ need.service_type }}</v-chip>
                    </div>
                  </v-col>
                  <v-col cols="12" md="6">
                    <div class="info-item pa-4 rounded-lg" style="background-color: #f5f5f5;">
                      <span class="label d-block mb-2">地区</span>
                      <p class="mt-2 font-weight-bold">{{ need.region }}</p>
                    </div>
                  </v-col>
                </v-row>

                <div class="mb-6 pa-4 rounded-lg" style="background-color: #f5f5f5;">
                  <span class="label d-block mb-2">描述</span>
                  <p class="mt-2">{{ need.description }}</p>
                </div>

                <div class="mb-6">
                  <span class="label d-block mb-4">响应列表</span>
                  <v-list v-if="need.responses && need.responses.length > 0" class="rounded-lg" style="background-color: #f5f5f5;">
                    <v-list-item v-for="response in need.responses" :key="response.id" class="mb-2">
                      <template v-slot:prepend>
                        <v-avatar color="primary" size="small">
                          <span class="text-white">{{ response.responder_name[0] }}</span>
                        </v-avatar>
                      </template>
                      <v-list-item-title class="font-weight-bold">{{ response.responder_name }}</v-list-item-title>
                      <v-list-item-subtitle>{{ response.content }}</v-list-item-subtitle>
                      <div v-if="response.media_url" class="mt-3">
                        <p class="text-caption text-grey mb-1">附件介绍：</p>
                        
                        <video 
                          v-if="response.media_url.toLowerCase().match(/\.(mp4|avi|mov)$/)" 
                          :src="'http://127.0.0.1:5000' + response.media_url" 
                          controls 
                          style="max-width: 200px; border-radius: 8px; border: 1px solid #eee;"
                        ></video>
                        
                        <v-img 
                          v-else 
                          :src="'http://127.0.0.1:5000' + response.media_url" 
                          max-width="200" 
                          max-height="150"
                          class="rounded-lg bg-grey-lighten-4"
                          style="cursor: pointer;"
                          @click="window.open('http://127.0.0.1:5000' + response.media_url)"
                        ></v-img>
                      </div>
                      <template v-slot:append>
                        <v-chip :color="getResponseStatusColor(response.status)" text-color="white" size="x-small">{{ getResponseStatusText(response.status) }}</v-chip>
                      </template>
                    </v-list-item>
                  </v-list>
                  <p v-else style="color: #999;">暂无响应</p>
                </div>

                <v-row>
                  <v-col cols="12" sm="6">
                    <v-btn 
                      variant="flat" 
                      block
                      color="white"
                      class="rounded-lg font-weight-bold py-3"
                      style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);"
                      @click="editNeed(need)"
                    >
                      <v-icon class="mr-2">mdi-pencil</v-icon>编辑
                    </v-btn>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-btn 
                      variant="outlined" 
                      block
                      color="error" 
                      class="rounded-lg font-weight-bold py-3"
                      @click="deleteNeed(need)"
                    >
                      <v-icon class="mr-2">mdi-delete</v-icon>删除
                    </v-btn>
                  </v-col>
                </v-row>

                <v-row v-if="need.status === 'open' && need.responses && need.responses.length > 0" class="mt-4">
                  <v-col cols="12">
                    <v-divider class="mb-4"></v-divider>
                    <span class="label d-block mb-4">待处理响应</span>
                    <v-row>
                      <v-col v-for="response in need.responses.filter(r => r.status === 'pending')" :key="response.id" cols="12" sm="6">
                        <v-card elevation="2" class="rounded-lg pa-4">
                          <div class="mb-3">
                            <v-icon color="primary" size="small">mdi-account</v-icon>
                            <span class="ml-2 font-weight-bold">{{ response.responder_name }}</span>
                          </div>
                          <p class="text-sm mb-4">{{ response.content }}</p>
                          <v-row>
                            <v-col cols="6">
                              <v-btn variant="outlined" color="success" size="small" block class="rounded-lg" @click="acceptResponse(response)">接受</v-btn>
                            </v-col>
                            <v-col cols="6">
                              <v-btn variant="outlined" color="error" size="small" block class="rounded-lg" @click="rejectResponse(response)">拒绝</v-btn>
                            </v-col>
                          </v-row>
                        </v-card>
                      </v-col>
                    </v-row>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>

      <v-card v-else elevation="4" class="rounded-xl py-12 text-center">
        <v-icon size="64" color="primary" class="mb-4" style="opacity: 0.5;">mdi-file-outline</v-icon>
        <p class="text-h6" style="color: #999;">暂无服务需求</p>
        <v-btn 
          variant="flat" 
          color="white"
          class="rounded-lg font-weight-bold mt-4 px-8"
          style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);"
          @click="$router.push('/service-needs')"
        >
          <v-icon class="mr-2">mdi-plus</v-icon>发布需求
        </v-btn>
      </v-card>

      <v-row class="mt-6" v-if="pagination.totalPages > 1">
        <v-col cols="12">
          <v-pagination
            v-model="pagination.page"
            :length="pagination.totalPages"
            @update:model-value="loadNeeds"
            color="primary"
          ></v-pagination>
        </v-col>
      </v-row>
    </v-container>

    <!-- 删除确认对话框 -->
    <v-dialog v-model="deleteDialog.show" max-width="400px">
      <v-card class="rounded-xl overflow-hidden">
        <div style="background: linear-gradient(135deg, #FF6F00 0%, #F57C00 100%); color: white;" class="pa-6">
          <v-card-title class="text-h6 text-white pa-0">
            <v-icon class="mr-2">mdi-alert</v-icon>确认删除
          </v-card-title>
        </div>

        <v-card-text class="py-6 px-6">
          <p>确定要删除这个服务需求吗？此操作不可恢复。</p>
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

<script setup name="NeedsManagement">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import PageHeader from '@/components/PageHeader.vue'

const router = useRouter()

const needs = ref([])
const pagination = ref({ page: 1, pageSize: 10, totalPages: 1 })
const deleteDialog = ref({ show: false, need: null, loading: false })
const snackbar = ref({ show: false, message: '', color: 'success' })

const getTypeColor = (type) => {
  const colors = { '家政服务': '#FF6F00', '维修服务': '#1976D2', '教育培训': '#2E7D32', '运输搬家': '#7B1FA2', '其他': '#616161' }
  return colors[type] || '#616161'
}

const getStatusColor = (status) => {
  const colors = { 'open': '#4CAF50', 'closed': '#FF9800', 'pending': '#2196F3' }
  return colors[status] || '#616161'
}

const getResponseStatusText = (status) => {
  // 必须对应数据库存的数字
  const texts = { 0: '待处理', 1: '已接受', 2: '已拒绝', 3: '已取消' }
  return texts[status] || '未知'
}

const getResponseStatusColor = (status) => {
  const colors = { 0: '#2196F3', 1: '#4CAF50', 2: '#F44336', 3: '#9E9E9E' }
  return colors[status] || '#616161'
}
const loadNeeds = async () => {
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
    const res = await axios.get(`http://127.0.0.1:5000/api/user/${user.id}/service-needs`, { params })
    if (res.data.code === 200) {
      needs.value = res.data.data.map(n => ({
        id: n.id,
        title: n.subject,
        service_type: n.service_type,
        description: n.description,
        region: n.region,
        status: n.status,
        media_url: n.media_url, // 【新增】保存发布者上传的媒体路径 
        // 【关键修正】将后端返回的 responses 映射到前端 [cite: 12]
        responses: n.responses ? n.responses.map(r => ({
          id: r.id,
          responder_name: r.responder_name || '匿名用户',
          content: r.content,
          status: r.status,
          media_url: r.media_url // 【新增】保存响应者上传的媒体路径 
        })) : [],
        status_text: n.status === 0 ? '开放' : n.status === 1 ? '已完成' : '已取消'
      }))
      pagination.value.totalPages = res.data.pagination?.pages || 1
    }
  } catch (error) {
    console.error('加载失败:', error)
    snackbar.value = { show: true, message: error.response?.data?.msg || '加载失败', color: 'error' }
  }
}

const editNeed = (need) => {
  router.push({ name: 'ServiceNeeds', params: { editId: need.id } })
}

const deleteNeed = (need) => {
  deleteDialog.value.need = need
  deleteDialog.value.show = true
}

const confirmDelete = async () => {
  if (!deleteDialog.value.need) return
  deleteDialog.value.loading = true
  try {
    const res = await axios.delete(`http://127.0.0.1:5000/api/service-needs/${deleteDialog.value.need.id}`)
    if (res.data.code === 200) {
      snackbar.value = { show: true, message: '删除成功', color: 'success' }
      deleteDialog.value.show = false
      loadNeeds()
    }
  } catch (error) {
    snackbar.value = { show: true, message: error.response?.data?.msg || '删除失败', color: 'error' }
  } finally {
    deleteDialog.value.loading = false
  }
}

const acceptResponse = async (response) => {
  try {
    const res = await axios.put(`http://127.0.0.1:5000/api/service_responses/${response.id}`, {
      status: 'accepted'
    })
    if (res.data.code === 200) {
      snackbar.value = { show: true, message: '已接受', color: 'success' }
      loadNeeds()
    }
  } catch (error) {
    snackbar.value = { show: true, message: error.response?.data?.msg || '操作失败', color: 'error' }
  }
}

const rejectResponse = async (response) => {
  try {
    const res = await axios.put(`http://127.0.0.1:5000/api/service_responses/${response.id}`, {
      status: 'rejected'
    })
    if (res.data.code === 200) {
      snackbar.value = { show: true, message: '已拒绝', color: 'success' }
      loadNeeds()
    }
  } catch (error) {
    snackbar.value = { show: true, message: error.response?.data?.msg || '操作失败', color: 'error' }
  }
}

onMounted(() => {
  loadNeeds()
})
</script>

<style scoped>
.label { font-weight: 600; color: #666; font-size: 12px; text-transform: uppercase; }
</style>
