<template>
  <div class="min-h-screen" style="background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);">
    <v-container class="py-8 max-w-7xl mx-auto">
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4 mb-6 text-white font-bold">
            <v-icon class="mr-3">mdi-chart-box</v-icon>
            管理员统计仪表板
          </h1>
        </v-col>
      </v-row>

    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="3">
        <v-card class="elevation-8 rounded-xl" color="primary">
          <v-card-text class="text-white">
            <div class="text-h6 text-opacity-90">总用户数</div>
            <div class="text-h3 font-bold">{{ stats.overview.total_users }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="elevation-8 rounded-xl" color="success">
          <v-card-text class="text-white">
            <div class="text-h6 text-opacity-90">活跃需求</div>
            <div class="text-h3 font-bold">{{ stats.overview.total_needs }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="elevation-8 rounded-xl" color="info">
          <v-card-text class="text-white">
            <div class="text-h6 text-opacity-90">总响应数</div>
            <div class="text-h3 font-bold">{{ stats.overview.total_responses }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="elevation-8 rounded-xl" color="warning">
          <v-card-text class="text-white">
            <div class="text-h6 text-opacity-90">成功配对</div>
            <div class="text-h3 font-bold">{{ stats.overview.total_success }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-card class="elevation-4 mb-6">
      <v-card-title class="text-h6 pa-4">
        <v-icon class="mr-2" color="primary">mdi-calendar-text</v-icon>
        月度服务需求与响应统计
      </v-card-title>
      <v-card-text>
        <v-form class="mb-6 pa-4" style="background-color: #f5f5f5; border-radius: 12px;">
          <v-row align="center">
            <v-col cols="12" sm="6" md="2">
              <v-text-field
                v-model="monthlyParams.start_month"
                label="起始年月"
                placeholder="如 202301"
                density="compact"
                variant="outlined"
                color="primary"
                hide-details
                bg-color="white"
                clearable
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="2">
              <v-text-field
                v-model="monthlyParams.end_month"
                label="终止年月"
                placeholder="如 202303"
                density="compact"
                variant="outlined"
                color="primary"
                hide-details
                bg-color="white"
                clearable
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="2">
              <v-text-field
                v-model="monthlyParams.province"
                label="省份"
                density="compact"
                variant="outlined"
                color="primary"
                hide-details
                bg-color="white"
                clearable
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="2">
              <v-text-field
                v-model="monthlyParams.city"
                label="城市"
                density="compact"
                variant="outlined"
                color="primary"
                hide-details
                bg-color="white"
                clearable
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="2">
              <v-text-field
                v-model="monthlyParams.service_type"
                label="服务类型"
                density="compact"
                variant="outlined"
                color="primary"
                hide-details
                bg-color="white"
                clearable
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="12" md="2" class="d-flex gap-2">
              <v-btn
                color="primary"
                prepend-icon="mdi-magnify"
                @click="searchMonthlyStats"
                class="flex-grow-1 text-white"
                height="40"
              >
                查询
              </v-btn>
              <v-btn
                variant="outlined"
                color="grey"
                icon="mdi-refresh"
                @click="resetSearch"
                height="40"
                width="40"
                title="重置"
              >
              </v-btn>
            </v-col>
          </v-row>
        </v-form>

        <v-card class="elevation-2 mb-6 rounded-lg bg-white border">
          <v-card-text class="pt-4">
            <div style="height: 400px; padding: 20px;">
              <Line v-if="loaded" :data="chartData" :options="chartOptions" />
            </div>
          </v-card-text>
        </v-card>

        <v-data-table
          :headers="monthlyHeaders"
          :items="stats.monthlySummary.data"
          class="elevation-1 rounded-lg"
          hover
        >
          <template v-slot:item.month="{ item }">
            <v-chip size="small" color="primary" variant="flat">
              {{ item.month }}
            </v-chip>
          </template>
          <template v-slot:item.need_count="{ item }">
            <span class="font-weight-bold text-primary">{{ item.need_count }}</span>
          </template>
          <template v-slot:item.response_success_count="{ item }">
            <span class="font-weight-bold text-success">{{ item.response_success_count }}</span>
          </template>
          
          <template #bottom>
            <div class="d-flex align-center justify-center pa-4" v-if="stats.monthlySummary.pagination.pages > 1">
              <v-btn
                variant="text"
                :disabled="stats.monthlySummary.pagination.page <= 1"
                @click="changePage(stats.monthlySummary.pagination.page - 1)"
              >上一页</v-btn>
              <span class="mx-4 text-body-2">
                第 {{ stats.monthlySummary.pagination.page }} / {{ stats.monthlySummary.pagination.pages }} 页
              </span>
              <v-btn
                variant="text"
                :disabled="stats.monthlySummary.pagination.page >= stats.monthlySummary.pagination.pages"
                @click="changePage(stats.monthlySummary.pagination.page + 1)"
              >下一页</v-btn>
            </div>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <v-row class="mb-6">
      <v-col cols="12" md="6">
        <v-card class="elevation-4 h-100">
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-tag-multiple</v-icon>
            按服务类型统计
          </v-card-title>
          <v-card-text>
            <v-table density="comfortable">
              <thead>
                <tr>
                  <th class="text-left">类型</th>
                  <th class="text-right">需求数</th>
                  <th class="text-right">成功数</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in serviceTypeItems" :key="item.type">
                  <td>{{ item.type }}</td>
                  <td class="text-right">{{ item.need_count }}</td>
                  <td class="text-right">
                    <v-chip size="small" color="success" variant="outlined">{{ item.success_count }}</v-chip>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="elevation-4 h-100">
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-map-marker</v-icon>
            按地域统计
          </v-card-title>
          <v-card-text>
            <v-table density="comfortable">
              <thead>
                <tr>
                  <th class="text-left">地域</th>
                  <th class="text-right">需求数</th>
                  <th class="text-right">成功数</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in regionItems" :key="item.region">
                  <td>{{ item.region }}</td>
                  <td class="text-right">{{ item.need_count }}</td>
                  <td class="text-right">
                    <v-chip size="small" color="success" variant="outlined">{{ item.success_count }}</v-chip>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar" :color="snackbarColor">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
  </div>
</template>

<script setup name="AdminStatsPage">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const router = useRouter()
const loaded = ref(false) // 标记图表数据是否准备好

// 统计数据结构
const stats = ref({
  overview: { total_users: 0, total_needs: 0, total_responses: 0, total_success: 0 },
  monthlySummary: {
    data: [],
    pagination: { page: 1, per_page: 10, total: 0, pages: 0 }
  }
})

// 表格数据
const serviceTypeItems = ref([])
const regionItems = ref([])

const monthlyHeaders = [
  { title: '月份', key: 'month' },
  { title: '地域', key: 'region' },
  { title: '服务类型', key: 'service_type' },
  { title: '需求数', key: 'need_count', align: 'end' },
  { title: '成功数', key: 'response_success_count', align: 'end' }
]

// 查询参数
const monthlyParams = ref({
  start_month: '',
  end_month: '',
  province: '',
  city: '',
  service_type: ''
})

// 图表数据
const chartData = ref({
  labels: [],
  datasets: []
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: '月度趋势' }
  }
}

const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

onMounted(() => {
  const userData = localStorage.getItem('user')
  if (!userData) {
    router.push('/login')
    return
  }
  loadAllStats()
})


const updateChartData = (rawChartData) => {
  // rawChartData 格式: [{month: '202301', need_count: 50, success_count: 20}, ...]
  
  // 如果没有数据，图表置空
  if (!rawChartData || rawChartData.length === 0) {
    chartData.value = { labels: [], datasets: [] }
    return
  }

  // 直接映射数据，无需再做聚合（后端已经聚合好了）
  chartData.value = {
    labels: rawChartData.map(item => `${item.month.substring(0,4)}/${item.month.substring(4,6)}`),
    datasets: [
      {
        label: '发布需求数',
        data: rawChartData.map(item => item.need_count),
        borderColor: '#1976D2',
        backgroundColor: 'rgba(25, 118, 210, 0.2)',
        tension: 0.3,
        fill: true
      },
      {
        label: '响应成功数',
        data: rawChartData.map(item => item.success_count),
        borderColor: '#4CAF50',
        backgroundColor: 'rgba(76, 175, 80, 0.2)',
        tension: 0.3,
        fill: true
      }
    ]
  }
  
  loaded.value = true
}

const loadMonthlyStats = async (page = 1) => {
  try {
    const params = {
      ...monthlyParams.value,
      page,
      per_page: 10
    }
    
    // 清理空参数
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null) delete params[key]
    })

    const res = await axios.get('http://127.0.0.1:5000/api/admin/stats/monthly-summary', { params })
    
    if (res.data.code === 200) {
      stats.value.monthlySummary.data = res.data.data // 表格数据（分页）
      stats.value.monthlySummary.pagination = res.data.pagination
      
      //关键修改:直接使用后端返回的 chart_data 传给图表函数
      // 如果后端没返回(旧缓存等原因)，这就为空数组
      const chartDataFromBackend = res.data.chart_data || []
      updateChartData(chartDataFromBackend)
    }
  } catch (error) {
    console.error(error)
  }
}

const loadAllStats = async () => {
  try {
    // 概览
    const overviewRes = await axios.get('http://127.0.0.1:5000/api/admin/stats/overview')
    if (overviewRes.data.code === 200) stats.value.overview = overviewRes.data.data
    
    // 类型统计
    const typeRes = await axios.get('http://127.0.0.1:5000/api/admin/stats/by-service-type')
    if (typeRes.data.code === 200) {
      serviceTypeItems.value = Object.entries(typeRes.data.data).map(([k,v]) => ({ type: k, ...v }))
    }

    // 地域统计
    const regionRes = await axios.get('http://127.0.0.1:5000/api/admin/stats/by-region')
    if (regionRes.data.code === 200) {
      regionItems.value = Object.entries(regionRes.data.data).map(([k,v]) => ({ region: k, ...v }))
    }

    // 月度统计
    await loadMonthlyStats(1)
  } catch (e) {
    showMessage('加载数据失败', 'error')
  }
}

const searchMonthlyStats = () => {
  loadMonthlyStats(1)
}

const resetSearch = () => {
  monthlyParams.value = {
    start_month: '',
    end_month: '',
    province: '',
    city: '',
    service_type: ''
  }
  loadMonthlyStats(1)
}

const changePage = (p) => {
  loadMonthlyStats(p)
}

const showMessage = (msg, color) => {
  snackbarMessage.value = msg
  snackbarColor.value = color
  snackbar.value = true
}
</script>