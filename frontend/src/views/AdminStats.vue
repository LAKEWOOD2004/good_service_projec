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

    <!-- 概览统计卡片 -->
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

    <!-- 按服务类型统计 -->
    <v-row class="mb-6">
      <v-col cols="12" md="6">
        <v-card class="elevation-4">
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-tag-multiple</v-icon>
            按服务类型统计
          </v-card-title>
          <v-card-text>
            <v-data-table
              dense
              class="elevation-1 rounded-lg"
              :headers="serviceTypeHeaders"
              :items="serviceTypeItems"
              hide-default-footer
            >
              <template v-slot:item.success_count="{ item }">
                <v-chip size="small" color="success" variant="outlined">
                  {{ item.success_count }}
                </v-chip>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- 按地域统计 -->
      <v-col cols="12" md="6">
        <v-card class="elevation-4">
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-map-marker</v-icon>
            按地域统计
          </v-card-title>
          <v-card-text>
            <v-data-table
              dense
              class="elevation-1 rounded-lg"
              :headers="regionHeaders"
              :items="regionItems"
              hide-default-footer
            >
              <template v-slot:item.region="{ item }">
                <span class="text-truncate">{{ item.region }}</span>
              </template>
              <template v-slot:item.success_count="{ item }">
                <v-chip size="small" color="success" variant="outlined">
                  {{ item.success_count }}
                </v-chip>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 响应成功率 -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card class="elevation-4">
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-chart-line</v-icon>
            响应成功率统计
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="3" class="text-center">
                <div class="mb-4">
                  <div class="text-caption text-medium-emphasis">响应率</div>
                  <v-progress-circular
                    :value="stats.responseRate.response_rate"
                    color="info"
                    size="80"
                  >
                    {{ stats.responseRate.response_rate }}%
                  </v-progress-circular>
                </div>
              </v-col>
              <v-col cols="12" sm="6" md="3" class="text-center">
                <div class="mb-4">
                  <div class="text-caption text-medium-emphasis">成功率</div>
                  <v-progress-circular
                    :value="stats.responseRate.success_rate"
                    color="success"
                    size="80"
                  >
                    {{ stats.responseRate.success_rate }}%
                  </v-progress-circular>
                </div>
              </v-col>
              <v-col cols="12" md="6">
                <v-list>
                  <v-list-item>
                    <template #title>总需求数</template>
                    <template #append>
                      <strong>{{ stats.responseRate.total_needs }}</strong>
                    </template>
                  </v-list-item>
                  <v-list-item>
                    <template #title>有响应的需求</template>
                    <template #append>
                      <strong>{{ stats.responseRate.needs_with_response }}</strong>
                    </template>
                  </v-list-item>
                  <v-list-item>
                    <template #title>成功配对的需求</template>
                    <template #append>
                      <strong>{{ stats.responseRate.needs_with_success }}</strong>
                    </template>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 用户活跃度 -->
    <v-row class="mb-6">
      <v-col cols="12" md="6">
        <v-card class="elevation-4">
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-star</v-icon>
            最活跃的需求发布者
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="(user, idx) in stats.userActivity.top_need_publishers" :key="idx">
                <template #prepend>
                  <v-avatar color="primary" class="text-white">
                    {{ idx + 1 }}
                  </v-avatar>
                </template>
                <template #title>{{ user.name }}</template>
                <template #append>
                  <v-chip size="small" color="primary">
                    {{ user.count }} 个
                  </v-chip>
                </template>
              </v-list-item>
              <v-list-item v-if="stats.userActivity.top_need_publishers.length === 0">
                <template #title>暂无数据</template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="elevation-4">
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-heart</v-icon>
            最活跃的服务响应者
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="(user, idx) in stats.userActivity.top_responders" :key="idx">
                <template #prepend>
                  <v-avatar color="success" class="text-white">
                    {{ idx + 1 }}
                  </v-avatar>
                </template>
                <template #title>{{ user.name }}</template>
                <template #append>
                  <v-chip size="small" color="success">
                    {{ user.count }} 个
                  </v-chip>
                </template>
              </v-list-item>
              <v-list-item v-if="stats.userActivity.top_responders.length === 0">
                <template #title>暂无数据</template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 月度统计 -->
    <v-card class="elevation-4 mb-6">
      <v-card-title class="text-h6">
        <v-icon class="mr-2">mdi-calendar-text</v-icon>
        月度服务需求与响应统计
      </v-card-title>
      <v-card-text>
        <!-- 查询表单 -->
        <v-form class="mb-6">
          <v-row>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="monthlyParams.start_month"
                label="起始年月 (YYYYMM)"
                placeholder="如 202301"
                density="compact"
                variant="outlined"
                color="primary"
                prepend-icon="mdi-calendar-start"
                class="bg-white"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="monthlyParams.end_month"
                label="终止年月 (YYYYMM)"
                placeholder="如 202303"
                density="compact"
                variant="outlined"
                color="primary"
                prepend-icon="mdi-calendar-end"
                class="bg-white"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="2">
              <v-select
                v-model="monthlyParams.province"
                label="省份"
                density="compact"
                variant="outlined"
                color="primary"
                prepend-icon="mdi-map-marker-radius"
                class="bg-white"
                :items="availableOptions.provinces"
                clearable
                hide-details="auto"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6" md="2">
              <v-select
                v-model="monthlyParams.city"
                label="城市"
                density="compact"
                variant="outlined"
                color="primary"
                prepend-icon="mdi-city"
                class="bg-white"
                :items="cityOptions"
                clearable
                hide-details="auto"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6" md="2">
              <v-select
                v-model="monthlyParams.service_type"
                label="服务类型"
                density="compact"
                variant="outlined"
                color="primary"
                prepend-icon="mdi-tag"
                class="bg-white"
                :items="availableOptions.serviceTypes"
                clearable
                hide-details="auto"
              ></v-select>
            </v-col>
            <v-col cols="12" class="text-right">
              <v-btn
                prepend-icon="mdi-magnify"
                @click="searchMonthlyStats"
                style="background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);"
                text-color="white"
                class="rounded-lg"
              >
                查询
              </v-btn>
            </v-col>
          </v-row>
        </v-form>

        <!-- 图表展示 -->
        <v-card class="elevation-4 mb-6 rounded-lg bg-white">
          <v-card-text class="pt-4">
            <div style="height: 400px; padding: 20px;">
              <Line :data="chartData" :options="chartOptions" />
            </div>
          </v-card-text>
        </v-card>

        <!-- 数据列表 -->
        <v-data-table
          dense
          class="elevation-3 rounded-lg"
          :headers="monthlyHeaders"
          :items="stats.monthlySummary.data"
          :items-per-page="stats.monthlySummary.pagination.per_page"
          :page="stats.monthlySummary.pagination.page"
          :total-items="stats.monthlySummary.pagination.total"
          @update:page="changePage"
          show-empty
          :loading="false"
        >
          <template v-slot:item.month="{ item }">
            {{ item.month.substring(0, 4) }}年{{ item.month.substring(4, 6) }}月
          </template>
          <template v-slot:item.region="{ item }">
            <span class="text-truncate">{{ item.region }}</span>
          </template>
          <template v-slot:item.need_count="{ item }">
            <v-chip size="small" color="primary" variant="outlined">
              {{ item.need_count }}
            </v-chip>
          </template>
          <template v-slot:item.response_success_count="{ item }">
            <v-chip size="small" color="success" variant="outlined">
              {{ item.response_success_count }}
            </v-chip>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- 消息提示 -->
    <v-snackbar v-model="snackbar" :color="snackbarColor">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
  </div>
</template>

<script setup name="AdminStatsPage">
import { ref, computed, onMounted } from 'vue'
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

// 注册Chart.js组件
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

// 统计数据
const stats = ref({
  overview: {
    total_users: 0,
    total_needs: 0,
    total_responses: 0,
    total_success: 0
  },
  byServiceType: {},
  byRegion: {},
  responseRate: {
    total_needs: 0,
    needs_with_response: 0,
    needs_with_success: 0,
    response_rate: 0,
    success_rate: 0
  },
  userActivity: {
    top_need_publishers: [],
    top_responders: []
  },
  monthlySummary: {
    data: [],
    pagination: {
      page: 1,
      per_page: 10,
      total: 0,
      pages: 0
    }
  }
})

// 服务类型统计表格配置
const serviceTypeHeaders = ref([
  { title: '服务类型', key: 'type' },
  { title: '需求数', key: 'need_count', align: 'right' },
  { title: '成功数', key: 'success_count', align: 'right' }
])

const serviceTypeItems = ref([])

// 地域统计表格配置
const regionHeaders = ref([
  { title: '地域', key: 'region' },
  { title: '需求数', key: 'need_count', align: 'right' },
  { title: '成功数', key: 'success_count', align: 'right' }
])

const regionItems = ref([])

// 月度统计表格配置
const monthlyHeaders = ref([
  { title: '月份', key: 'month' },
  { title: '地域', key: 'region' },
  { title: '服务类型', key: 'service_type' },
  { title: '需求数', key: 'need_count', align: 'right' },
  { title: '成功数', key: 'response_success_count', align: 'right' },
  { title: '更新时间', key: 'updated_at' }
])

// 月度统计查询参数
const monthlyParams = ref({
  start_month: '',
  end_month: '',
  province: '',
  city: '',
  service_type: '',
  sort_by: 'need_count',
  sort_order: 'desc'
})

// 图表数据
const chartData = ref({
  labels: ['暂无数据'],
  datasets: [
    {
      label: '月累计发布服务需求数',
      data: [0],
      borderColor: '#1976D2',
      backgroundColor: 'rgba(25, 118, 210, 0.1)',
      fill: true,
      tension: 0.1
    },
    {
      label: '月累计响应成功服务数',
      data: [0],
      borderColor: '#4CAF50',
      backgroundColor: 'rgba(76, 175, 80, 0.1)',
      fill: true,
      tension: 0.1
    }
  ]
})

// 可用选项数据
const availableOptions = ref({
  provinces: [],
  cities: [],
  serviceTypes: []
})

// 城市选项（根据选择的省份动态更新）
const cityOptions = computed(() => {
  if (!monthlyParams.value.province) {
    return availableOptions.value.cities
  }
  return availableOptions.value.cities.filter(city => {
    return city.startsWith(monthlyParams.value.province + '-')
  })
})

// 加载可用选项
const loadAvailableOptions = async () => {
  try {
    // 从by-service-type接口获取可用的服务类型
    const serviceTypeRes = await axios.get('http://127.0.0.1:5000/api/admin/stats/by-service-type')
    if (serviceTypeRes.data.code === 200) {
      availableOptions.value.serviceTypes = Object.keys(serviceTypeRes.data.data)
    }
    
    // 从by-region接口获取可用的省份和城市
    const regionRes = await axios.get('http://127.0.0.1:5000/api/admin/stats/by-region')
    if (regionRes.data.code === 200) {
      const regions = Object.keys(regionRes.data.data)
      const provinces = new Set()
      const cities = new Set()
      
      regions.forEach(region => {
        const parts = region.split('-')
        if (parts.length >= 2) {
          provinces.add(parts[0])
          cities.add(`${parts[0]}-${parts[1]}`)
        }
      })
      
      availableOptions.value.provinces = Array.from(provinces).sort()
      availableOptions.value.cities = Array.from(cities).sort()
    }
  } catch (error) {
    console.error('加载可用选项失败:', error)
  }
}

// 图表配置
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        font: {
          size: 14
        }
      }
    },
    title: {
      display: true,
      text: '月度服务需求与响应统计',
      font: {
        size: 16
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        font: {
          size: 12
        }
      }
    },
    x: {
      ticks: {
        font: {
          size: 12,
          color: '#333' // 确保X轴标签颜色可见
        },
        maxRotation: 45,
        minRotation: 45
      },
      grid: {
        display: false // 隐藏X轴网格线，使图表更清晰
      }
    }
  }
})

// 消息提示
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

// 当前用户信息
const user = ref(null)

// 初始化
onMounted(async () => {
  const userData = localStorage.getItem('user')
  if (!userData) {
    router.push('/login')
    return
  }
  
  user.value = JSON.parse(userData)
  
  // 只有管理员可以访问
  if (user.value.user_type !== 'admin') {
    showMessage('只有管理员可以访问此页面', 'error')
    setTimeout(() => {
      router.push('/home')
    }, 1500)
    return
  }
  
  console.log('开始初始化')
  
  // 先加载所有统计数据，再加载可用选项
  try {
    await loadAllStats()
    console.log('统计数据加载完成')
    await loadAvailableOptions()
    console.log('可用选项加载完成')
  } catch (error) {
    console.error('初始化失败:', error)
    showMessage('初始化失败', 'error')
  }
})

// 加载月度统计数据
const loadMonthlyStats = async (page = 1) => {
  try {
    const params = {
      ...monthlyParams.value,
      page: page,
      per_page: stats.value.monthlySummary.pagination.per_page
    }
    
    console.log('请求月度统计数据参数:', params)
    
    const response = await axios.get('http://127.0.0.1:5000/api/admin/stats/monthly-summary', {
      params: params
    })
    
    console.log('月度统计数据响应:', response.data)
    
    if (response.data.code === 200) {
      console.log('月度统计数据:', response.data.data)
      stats.value.monthlySummary.data = response.data.data
      // 确保pagination字段存在，避免访问undefined属性
      if (response.data.pagination) {
        stats.value.monthlySummary.pagination = response.data.pagination
      } else {
        // 如果没有pagination字段，设置默认值
        stats.value.monthlySummary.pagination = {
          page: 1,
          per_page: 10,
          total: response.data.data.length,
          pages: Math.ceil(response.data.data.length / 10)
        }
      }
      console.log('更新前的stats.monthlySummary.data:', stats.value.monthlySummary.data)
      updateChartData()
    }
  } catch (error) {
    console.error('加载月度统计数据失败:', error)
    console.error('错误详情:', error.response)
    showMessage(error.response?.data?.msg || '加载月度统计数据失败', 'error')
  }
}

// 更新图表数据
const updateChartData = () => {
  // 初始化图表数据
  const newChartData = {
    labels: [],
    datasets: [
      {
        label: '月累计发布服务需求数',
        data: [],
        borderColor: '#1976D2',
        backgroundColor: 'rgba(25, 118, 210, 0.1)',
        fill: true,
        tension: 0.1
      },
      {
        label: '月累计响应成功服务数',
        data: [],
        borderColor: '#4CAF50',
        backgroundColor: 'rgba(76, 175, 80, 0.1)',
        fill: true,
        tension: 0.1
      }
    ]
  };
  
  // 确保stats.value.monthlySummary.data是数组
  if (!stats.value.monthlySummary || !Array.isArray(stats.value.monthlySummary.data)) {
    // 如果数据为空或不是数组，显示暂无数据
    newChartData.labels = ['暂无数据'];
    newChartData.datasets[0].data = [0];
    newChartData.datasets[1].data = [0];
    chartData.value = newChartData;
    return;
  }
  
  const monthlyData = stats.value.monthlySummary.data;
  
  // 如果没有数据，显示暂无数据
  if (monthlyData.length === 0) {
    newChartData.labels = ['暂无数据'];
    newChartData.datasets[0].data = [0];
    newChartData.datasets[1].data = [0];
    chartData.value = newChartData;
    return;
  }
  
  // 按月份分组统计数据
  const monthlyStats = {};
  
  // 遍历所有数据，按月份分组
  monthlyData.forEach(item => {
    const month = item.month;
    
    // 如果该月份不存在，初始化
    if (!monthlyStats[month]) {
      monthlyStats[month] = {
        need_count: 0,
        response_success_count: 0
      };
    }
    
    // 累加需求数和成功数
    monthlyStats[month].need_count += item.need_count;
    monthlyStats[month].response_success_count += item.response_success_count;
  });
  
  // 获取月份列表并按月份排序
  const monthList = Object.keys(monthlyStats).sort();
  
  // 填充图表数据
  monthList.forEach(month => {
    // 格式化月份显示：YYYY年MM月
    const formattedMonth = `${month.substring(0, 4)}年${month.substring(4, 6)}月`;
    newChartData.labels.push(formattedMonth);
    
    // 填充需求数和成功数
    newChartData.datasets[0].data.push(monthlyStats[month].need_count);
    newChartData.datasets[1].data.push(monthlyStats[month].response_success_count);
  });
  
  // 更新图表数据
  chartData.value = newChartData;
}

// 加载所有统计数据
const loadAllStats = async () => {
  try {
    console.log('开始加载所有统计数据')
    
    // 先加载月度统计数据，这是图表的主要数据
    await loadMonthlyStats()
    console.log('月度统计数据加载完成')
    
    // 然后加载其他统计数据
    const [
      overviewRes,
      serviceTypeRes,
      regionRes,
      responseRateRes,
      userActivityRes
    ] = await Promise.all([
      axios.get('http://127.0.0.1:5000/api/admin/stats/overview'),
      axios.get('http://127.0.0.1:5000/api/admin/stats/by-service-type'),
      axios.get('http://127.0.0.1:5000/api/admin/stats/by-region'),
      axios.get('http://127.0.0.1:5000/api/admin/stats/response-rate'),
      axios.get('http://127.0.0.1:5000/api/admin/stats/user-activity')
    ])
    
    console.log('其他统计数据加载完成')
    
    // 更新统计数据
    if (overviewRes.data.code === 200) {
      stats.value.overview = overviewRes.data.data
    }
    if (serviceTypeRes.data.code === 200) {
      stats.value.byServiceType = serviceTypeRes.data.data
      // 转换为v-data-table格式
      serviceTypeItems.value = Object.entries(stats.value.byServiceType).map(([type, data]) => ({
        type,
        ...data
      }))
    }
    if (regionRes.data.code === 200) {
      stats.value.byRegion = regionRes.data.data
      // 转换为v-data-table格式
      regionItems.value = Object.entries(stats.value.byRegion).map(([region, data]) => ({
        region,
        ...data
      }))
    }
    if (responseRateRes.data.code === 200) {
      stats.value.responseRate = responseRateRes.data.data
    }
    if (userActivityRes.data.code === 200) {
      stats.value.userActivity = userActivityRes.data.data
    }
    
    console.log('所有统计数据加载完成')
  } catch (error) {
    console.error('加载统计数据失败:', error)
    console.error('错误详情:', error.response)
    showMessage(error.response?.data?.msg || '加载统计数据失败', 'error')
  }
}

// 搜索月度统计
const searchMonthlyStats = () => {
  loadMonthlyStats(1) // 搜索时重置到第一页
}

// 切换页码
const changePage = (newPage) => {
  if (newPage >= 1 && newPage <= stats.value.monthlySummary.pagination.pages) {
    loadMonthlyStats(newPage)
  }
}

// 显示消息
const showMessage = (message, color = 'success') => {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}
</script>

<style scoped>
/* 卡片加载动画 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 为所有卡片添加动画 */
.v-card {
  animation: fadeInUp 0.6s ease-out;
  transition: all 0.3s ease;
}

/* 按钮悬停效果 */
.v-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

/* 数据表格行悬停效果 */
.v-data-table tbody tr:hover {
  background-color: rgba(76, 175, 80, 0.1);
}
</style>
