<template>
  <div style="background: linear-gradient(135deg, #f0f9ff 0%, #f0fdf4 100%); min-height: 100vh;">
    <PageHeader 
      title="服务大厅"
      subtitle="浏览需要帮助的服务需求"
    />

    <v-container class="py-6">
      <v-card elevation="4" class="rounded-xl overflow-hidden mb-6">
        <v-card-text class="pa-6">
          <v-row class="mb-4">
            <v-col cols="12" sm="6" lg="3">
              <v-text-field
                v-model="filters.keyword"
                label="搜索关键词"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="comfortable"
                color="primary"
                @keyup.enter="loadNeeds"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" lg="3">
              <v-select
                v-model="filters.serviceType"
                label="服务类型"
                :items="serviceTypes"
                prepend-inner-icon="mdi-tag"
                variant="outlined"
                density="comfortable"
                color="primary"
                clearable
                @update:model-value="loadNeeds"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6" lg="3">
              <v-select
                v-model="filters.region"
                label="地区"
                :items="regions"
                item-title="full_name"
                item-value="id"
                prepend-inner-icon="mdi-map-marker"
                variant="outlined"
                density="comfortable"
                color="primary"
                clearable
                @update:model-value="loadNeeds"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6" lg="3">
              <v-btn 
                variant="flat" 
                block
                color="white"
                class="rounded-lg font-weight-bold py-3"
                style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);"
                @click="loadNeeds"
              >
                <v-icon class="mr-2">mdi-refresh</v-icon>刷新
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <v-row>
        <v-col cols="12" sm="6" lg="4" v-for="need in needs" :key="need.id">
          <v-card elevation="4" class="rounded-xl overflow-hidden h-100 hover-shadow" style="transition: transform 0.2s, box-shadow 0.2s;" @mouseover="$event.currentTarget.style.transform='translateY(-4px)'" @mouseout="$event.currentTarget.style.transform='translateY(0)'">
            <div style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); color: white;" class="pa-4">
              <div class="d-flex justify-space-between align-center">
                <v-chip :color="getTypeColor(need.service_type)" text-color="white" size="small">{{ need.service_type }}</v-chip>
                <v-chip :color="getStatusColor(need.status)" text-color="white" size="small">{{ need.status_text }}</v-chip>
              </div>
            </div>

            <v-card-text class="pa-6">
              <h3 class="mb-4 font-weight-bold text-h6">{{ need.title }}</h3>
              <p class="text-sm mb-4" style="color: #666; height: 60px; overflow: hidden;">{{ need.description }}</p>

              <v-divider class="my-4"></v-divider>

              <div class="text-sm mb-4">
                <div class="mb-2"><v-icon size="small" color="primary">mdi-map-marker</v-icon> <span class="ml-2">{{ need.region }}</span></div>
                <div class="mb-2"><v-icon size="small" color="primary">mdi-calendar</v-icon> <span class="ml-2">{{ formatDate(need.create_time) }}</span></div>
                <div><v-icon size="small" color="primary">mdi-user</v-icon> <span class="ml-2">{{ need.created_by }}</span></div>
              </div>
            </v-card-text>

            <v-card-actions class="pa-4">
              <v-btn 
                variant="outlined" 
                color="primary"
                size="small"
                block
                class="rounded-lg mr-2"
                @click="viewDetail(need)"
              >
                详情
              </v-btn>
              <v-btn 
                v-if="need.status === 'open'"
                variant="flat" 
                color="white"
                size="small"
                block
                class="rounded-lg"
                style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);"
                @click="responseDialog.need = need; responseDialog.show = true"
              >
                响应
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-6">
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

    <!-- 详情对话框 -->
    <v-dialog v-model="detailDialog.show" max-width="600px">
      <v-card v-if="detailDialog.need" class="rounded-xl overflow-hidden">
        <div style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); color: white;" class="pa-6">
          <v-card-title class="text-h5 text-white pa-0">{{ detailDialog.need.title }}</v-card-title>
        </div>

        <v-card-text class="py-6 px-6">
          <div class="mb-6">
            <span class="text-sm font-weight-bold" style="color: #999;">服务类型</span>
            <v-chip :color="getTypeColor(detailDialog.need.service_type)" text-color="white" class="mt-2">{{ detailDialog.need.service_type }}</v-chip>
          </div>

          <div class="mb-6">
            <span class="text-sm font-weight-bold" style="color: #999;">描述</span>
            <p class="mt-2">{{ detailDialog.need.description }}</p>
          </div>

          <div class="mb-6">
            <span class="text-sm font-weight-bold" style="color: #999;">地区</span>
            <p class="mt-2">{{ detailDialog.need.region }}</p>
          </div>

          <div class="mb-6">
            <span class="text-sm font-weight-bold" style="color: #999;">发布者</span>
            <p class="mt-2">{{ detailDialog.need.created_by }}</p>
          </div>

          <div class="mb-6">
            <span class="text-sm font-weight-bold" style="color: #999;">发布时间</span>
            <p class="mt-2">{{ formatDate(detailDialog.need.create_time) }}</p>
          </div>

          <div v-if="detailDialog.need.status === 'closed'">
            <span class="text-sm font-weight-bold" style="color: #999;">完成人</span>
            <p class="mt-2">{{ detailDialog.need.completed_by || '未设置' }}</p>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="py-4 px-6">
          <v-spacer></v-spacer>
          <v-btn variant="outlined" color="primary" class="rounded-lg" @click="detailDialog.show = false">关闭</v-btn>
          <v-btn v-if="detailDialog.need.status === 'open'" variant="flat" color="white" class="rounded-lg ml-2" style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);" @click="responseDialog.need = detailDialog.need; responseDialog.show = true; detailDialog.show = false">响应</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 响应对话框 -->
    <v-dialog v-model="responseDialog.show" max-width="600px">
      <v-card v-if="responseDialog.need" class="rounded-xl overflow-hidden">
        <div style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); color: white;" class="pa-6">
          <v-card-title class="text-h6 text-white pa-0">
            <v-icon class="mr-2">mdi-reply</v-icon>响应服务需求
          </v-card-title>
        </div>

        <v-card-text class="py-6 px-6">
          <div class="mb-4 pa-4 rounded-lg" style="background-color: #f5f5f5;">
            <span class="text-sm font-weight-bold">需求</span>
            <p class="mt-2">{{ responseDialog.need.title }}</p>
          </div>

          <v-form ref="responseForm" v-model="responseDialog.valid">
            <v-textarea
              v-model="responseDialog.content"
              label="响应内容"
              rows="6"
              counter="500"
              maxlength="500"
              required
              :rules="[v => !!v || '必填', v => v.length >= 10 || '至少10个字']"
              variant="outlined"
              color="primary"
              density="comfortable"
            ></v-textarea>
          </v-form>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="py-4 px-6">
          <v-spacer></v-spacer>
          <v-btn variant="outlined" color="primary" class="rounded-lg" @click="responseDialog.show = false">取消</v-btn>
          <v-btn variant="flat" color="white" class="rounded-lg ml-2" style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%);" @click="submitResponse" :loading="responseDialog.submitting">提交</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" rounded="lg">{{ snackbar.message }}</v-snackbar>
  </div>
</template>

<script setup name="ServiceHall">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import PageHeader from '@/components/PageHeader.vue'

const router = useRouter()

const needs = ref([])
const filters = ref({ keyword: '', serviceType: '', region: null })
const pagination = ref({ page: 1, pageSize: 9, totalPages: 1 })
const serviceTypes = ref(['管道维修', '助老服务', '保洁服务', '就诊服务', '营养餐服务', '定期接送服务', '其他'])
const regions = ref([])
const detailDialog = ref({ show: false, need: null })
const responseDialog = ref({ show: false, need: null, content: '', valid: false, submitting: false })
const responseForm = ref(null)
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

const getTypeColor = (type) => {
  const colors = {
    '管道维修': '#FF6F00',
    '助老服务': '#1976D2',
    '保洁服务': '#2E7D32',
    '就诊服务': '#7B1FA2',
    '营养餐服务': '#F57C00',
    '定期接送服务': '#0097A7',
    '其他': '#616161'
  }
  return colors[type] || '#616161'
}

const getStatusColor = (status) => {
  const colors = { 'open': '#4CAF50', 'closed': '#FF9800', 'pending': '#2196F3' }
  return colors[status] || '#616161'
}

const loadNeeds = async () => {
  try {
    const params = {
      page: pagination.value.page,
      per_page: pagination.value.pageSize,
      service_type: filters.value.serviceType,
      region_id: filters.value.region
    }
    const res = await axios.get('http://127.0.0.1:5000/api/service-needs', { params })
    if (res.data.code === 200) {
      needs.value = res.data.data.map(n => ({
        id: n.id,
        title: n.subject,
        service_type: n.service_type,
        description: n.description,
        region: n.region,
        created_by: n.publisher,
        create_time: n.created_at,
        status: 'open',
        status_text: '开放'
      }))
      pagination.value.totalPages = res.data.pagination.pages
    }
  } catch (error) {
    console.error('加载失败:', error)
    snackbar.value = { show: true, message: error.response?.data?.msg || '加载失败', color: 'error' }
  }
}

const viewDetail = (need) => {
  detailDialog.value.need = need
  detailDialog.value.show = true
}

const submitResponse = async () => {
  const userData = localStorage.getItem('user')
  if (!userData) {
    router.push('/login')
    return
  }
  const user = JSON.parse(userData)
  
  responseDialog.value.submitting = true
  try {
    const res = await axios.post(`http://127.0.0.1:5000/api/service-needs/${responseDialog.value.need.id}/respond`, {
      responder_id: user.id,
      content: responseDialog.value.content
    })
    if (res.data.code === 200 || res.data.code === 201) {
      snackbar.value = { show: true, message: '响应成功', color: 'success' }
      responseDialog.value.show = false
      responseDialog.value.content = ''
      loadNeeds()
    }
  } catch (error) {
    snackbar.value = { show: true, message: error.response?.data?.msg || '提交失败', color: 'error' }
  } finally {
    responseDialog.value.submitting = false
  }
}

onMounted(() => {
  loadRegions()
  loadNeeds()
})

const loadRegions = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/api/regions')
    if (res.data.code === 200) {
      regions.value = res.data.data
    }
  } catch (error) {
    console.error('加载地区失败:', error)
  }
}
</script>

<style scoped>
.hover-shadow {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}
</style>
