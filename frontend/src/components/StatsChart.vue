<template>
  <div class="stats-chart">
    <el-card>
      <template #header>
        <div class="chart-header">
          <h3>数据统计</h3>
          <el-select v-model="selectedPeriod" @change="loadChartData">
            <el-option label="最近7天" value="7days" />
            <el-option label="最近30天" value="30days" />
            <el-option label="最近90天" value="90days" />
          </el-select>
        </div>
      </template>
      
      <div class="chart-tabs">
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="专注时长" name="focus">
            <div class="chart-container">
              <canvas ref="focusChartRef"></canvas>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="任务完成" name="tasks">
            <div class="chart-container">
              <canvas ref="tasksChartRef"></canvas>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="笔记创建" name="notes">
            <div class="chart-container">
              <canvas ref="notesChartRef"></canvas>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  BarElement,
  BarController,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js'
import request from '@/utils/request'

// 注册Chart.js组件
Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  BarElement,
  BarController,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

export default {
  name: 'StatsChart',
  setup() {
    const selectedPeriod = ref('7days')
    const activeTab = ref('focus')
    const focusChartRef = ref(null)
    const tasksChartRef = ref(null)
    const notesChartRef = ref(null)
    
    let focusChart = null
    let tasksChart = null
    let notesChart = null
    
    const chartData = ref({
      focus: { labels: [], data: [] },
      tasks: { labels: [], data: [] },
      notes: { labels: [], data: [] }
    })
    
    const loadChartData = async () => {
      try {
        const days = parseInt(selectedPeriod.value.replace('days', ''))
        const endDate = new Date()
        const startDate = new Date()
        startDate.setDate(endDate.getDate() - days)
        
        // 生成日期标签
        const labels = []
        const currentDate = new Date(startDate)
        while (currentDate <= endDate) {
          labels.push(currentDate.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }))
          currentDate.setDate(currentDate.getDate() + 1)
        }
        
        // 加载专注数据
        const focusResponse = await request.get(`/focus-sessions?start_date=${startDate.toISOString().split('T')[0]}&end_date=${endDate.toISOString().split('T')[0]}`)
        const focusSessions = focusResponse.sessions || []
        
        const focusData = labels.map(label => {
          const date = label
          const dayData = focusSessions.filter(session => {
            const sessionDate = new Date(session.created_at).toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
            return sessionDate === date && session.completed
          })
          return dayData.reduce((total, session) => total + session.duration, 0)
        })
        
        // 加载任务数据
        const tasksResponse = await request.get(`/tasks?start_date=${startDate.toISOString().split('T')[0]}&end_date=${endDate.toISOString().split('T')[0]}`)
        const tasks = tasksResponse.tasks || []
        
        const tasksData = labels.map(label => {
          const date = label
          return tasks.filter(task => {
            const taskDate = new Date(task.completed_at || task.created_at).toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
            return taskDate === date && task.status === 'completed'
          }).length
        })
        
        // 加载笔记数据
        const notesResponse = await request.get(`/notes?start_date=${startDate.toISOString().split('T')[0]}&end_date=${endDate.toISOString().split('T')[0]}`)
        const notes = notesResponse.notes || []
        
        const notesData = labels.map(label => {
          const date = label
          return notes.filter(note => {
            const noteDate = new Date(note.created_at).toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
            return noteDate === date
          }).length
        })
        
        chartData.value = {
          focus: { labels, data: focusData },
          tasks: { labels, data: tasksData },
          notes: { labels, data: notesData }
        }
        
        updateCharts()
      } catch (error) {
        console.error('加载图表数据失败:', error)
      }
    }
    
    const createFocusChart = () => {
      if (focusChart) {
        focusChart.destroy()
      }
      
      const ctx = focusChartRef.value?.getContext('2d')
      if (!ctx) return
      
      focusChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: chartData.value.focus.labels,
          datasets: [{
            label: '专注时长(分钟)',
            data: chartData.value.focus.data,
            borderColor: '#409eff',
            backgroundColor: 'rgba(64, 158, 255, 0.1)',
            tension: 0.4,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 30
              }
            }
          }
        }
      })
    }
    
    const createTasksChart = () => {
      if (tasksChart) {
        tasksChart.destroy()
      }
      
      const ctx = tasksChartRef.value?.getContext('2d')
      if (!ctx) return
      
      tasksChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: chartData.value.tasks.labels,
          datasets: [{
            label: '完成任务数',
            data: chartData.value.tasks.data,
            backgroundColor: '#67c23a',
            borderColor: '#67c23a',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      })
    }
    
    const createNotesChart = () => {
      if (notesChart) {
        notesChart.destroy()
      }
      
      const ctx = notesChartRef.value?.getContext('2d')
      if (!ctx) return
      
      notesChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: chartData.value.notes.labels,
          datasets: [{
            label: '创建笔记数',
            data: chartData.value.notes.data,
            backgroundColor: '#e6a23c',
            borderColor: '#e6a23c',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      })
    }
    
    const updateCharts = async () => {
      await nextTick()
      
      if (activeTab.value === 'focus') {
        createFocusChart()
      } else if (activeTab.value === 'tasks') {
        createTasksChart()
      } else if (activeTab.value === 'notes') {
        createNotesChart()
      }
    }
    
    const handleTabChange = (tabName) => {
      activeTab.value = tabName
      updateCharts()
    }
    
    onMounted(() => {
      loadChartData()
    })
    
    onUnmounted(() => {
      if (focusChart) focusChart.destroy()
      if (tasksChart) tasksChart.destroy()
      if (notesChart) notesChart.destroy()
    })
    
    return {
      selectedPeriod,
      activeTab,
      focusChartRef,
      tasksChartRef,
      notesChartRef,
      loadChartData,
      handleTabChange
    }
  }
}
</script>

<style scoped>
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-header h3 {
  margin: 0;
  color: #303133;
}

.chart-container {
  height: 300px;
  position: relative;
}

.chart-tabs {
  margin-top: 16px;
}

.chart-tabs :deep(.el-tabs__content) {
  padding-top: 16px;
}
</style>