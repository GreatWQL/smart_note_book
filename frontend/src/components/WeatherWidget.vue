<template>
  <div class="weather-widget">
    <el-card>
      <template #header>
        <div class="weather-header">
          <i class="el-icon-sunny"></i>
          <span>天气信息</span>
        </div>
      </template>
      
      <div v-if="loading" class="loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>获取天气信息中...</span>
      </div>
      
      <div v-else-if="weather" class="weather-content">
        <div class="current-weather">
          <div class="weather-icon">
            <i :class="getWeatherIcon(weather.current.condition)"></i>
          </div>
          <div class="weather-info">
            <div class="temperature">{{ weather.current.temperature }}°C</div>
            <div class="condition">{{ weather.current.condition }}</div>
            <div class="location">{{ weather.location.city }}</div>
          </div>
        </div>
        
        <div class="weather-details">
          <div class="detail-item">
            <i class="el-icon-view"></i>
            <span>湿度: {{ weather.current.humidity }}%</span>
          </div>
          <div class="detail-item">
            <i class="el-icon-wind-power"></i>
            <span>风速: {{ weather.current.windSpeed }} km/h</span>
          </div>
          <div class="detail-item">
            <i class="el-icon-thermometer"></i>
            <span>体感: {{ weather.current.feelsLike }}°C</span>
          </div>
        </div>
        
        <div class="forecast">
          <h4>未来3天</h4>
          <div class="forecast-list">
            <div v-for="day in weather.forecast" :key="day.date" class="forecast-item">
              <div class="forecast-date">{{ formatDate(day.date) }}</div>
              <i :class="getWeatherIcon(day.condition)" class="forecast-icon"></i>
              <div class="forecast-temp">
                <span class="high">{{ day.high }}°</span>
                <span class="low">{{ day.low }}°</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="error">
        <el-icon><Warning /></el-icon>
        <span>无法获取天气信息</span>
        <el-button type="text" @click="loadWeather">重试</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { Loading, Warning } from '@element-plus/icons-vue'

export default {
  name: 'WeatherWidget',
  components: {
    Loading,
    Warning
  },
  setup() {
    const loading = ref(false)
    const weather = ref(null)
    
    // 模拟天气数据（实际项目中应该调用真实的天气API）
    const mockWeatherData = {
      location: {
        city: '北京',
        country: '中国'
      },
      current: {
        temperature: 22,
        condition: 'sunny',
        humidity: 65,
        windSpeed: 12,
        feelsLike: 24
      },
      forecast: [
        { date: '2024-01-15', condition: 'sunny', high: 25, low: 15 },
        { date: '2024-01-16', condition: 'cloudy', high: 23, low: 13 },
        { date: '2024-01-17', condition: 'rainy', high: 20, low: 12 }
      ]
    }
    
    const loadWeather = async () => {
      loading.value = true
      try {
        // 获取用户位置
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            async (position) => {
              const { latitude, longitude } = position.coords
              await fetchWeatherData(latitude, longitude)
            },
            () => {
              // 位置获取失败，使用默认数据
              setTimeout(() => {
                weather.value = mockWeatherData
                loading.value = false
              }, 1000)
            }
          )
        } else {
          // 浏览器不支持地理位置，使用默认数据
          setTimeout(() => {
            weather.value = mockWeatherData
            loading.value = false
          }, 1000)
        }
      } catch (error) {
        console.error('获取天气信息失败:', error)
        loading.value = false
      }
    }
    
    const fetchWeatherData = async (lat, lon) => {
      try {
        // 这里应该调用真实的天气API
        // 例如: OpenWeatherMap, 和风天气等
        // const response = await fetch(`/api/weather?lat=${lat}&lon=${lon}`)
        // const data = await response.json()
        
        // 模拟API调用延迟
        setTimeout(() => {
          // 根据位置调整城市名称
          const cities = ['北京', '上海', '广州', '深圳', '杭州', '成都']
          const randomCity = cities[Math.floor(Math.random() * cities.length)]
          
          weather.value = {
            ...mockWeatherData,
            location: { ...mockWeatherData.location, city: randomCity },
            current: {
              ...mockWeatherData.current,
              temperature: Math.floor(Math.random() * 20) + 15 // 15-35度随机温度
            }
          }
          loading.value = false
        }, 1500)
      } catch (error) {
        console.error('获取天气数据失败:', error)
        weather.value = mockWeatherData
        loading.value = false
      }
    }
    
    const getWeatherIcon = (condition) => {
      const iconMap = {
        sunny: 'el-icon-sunny',
        cloudy: 'el-icon-cloudy',
        rainy: 'el-icon-heavy-rain',
        snowy: 'el-icon-light-rain',
        windy: 'el-icon-wind-power'
      }
      return iconMap[condition] || 'el-icon-sunny'
    }
    
    const formatDate = (dateStr) => {
      const date = new Date(dateStr)
      const today = new Date()
      const tomorrow = new Date(today)
      tomorrow.setDate(today.getDate() + 1)
      
      if (date.toDateString() === today.toDateString()) {
        return '今天'
      } else if (date.toDateString() === tomorrow.toDateString()) {
        return '明天'
      } else {
        return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
      }
    }
    
    onMounted(() => {
      loadWeather()
    })
    
    return {
      loading,
      weather,
      loadWeather,
      getWeatherIcon,
      formatDate
    }
  }
}
</script>

<style scoped>
.weather-widget {
  height: 100%;
}

.weather-header {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #409eff;
  font-weight: 500;
}

.loading, .error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #909399;
  gap: 12px;
}

.loading .el-icon {
  font-size: 24px;
}

.current-weather {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.weather-icon {
  font-size: 48px;
  color: #409eff;
}

.weather-info .temperature {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
}

.weather-info .condition {
  font-size: 16px;
  color: #606266;
  margin: 4px 0;
}

.weather-info .location {
  font-size: 14px;
  color: #909399;
}

.weather-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.detail-item i {
  color: #409eff;
  width: 16px;
}

.forecast h4 {
  margin: 0 0 12px 0;
  color: #303133;
  font-size: 16px;
}

.forecast-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.forecast-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.forecast-item:last-child {
  border-bottom: none;
}

.forecast-date {
  font-size: 14px;
  color: #606266;
  width: 40px;
}

.forecast-icon {
  font-size: 20px;
  color: #409eff;
  width: 24px;
  text-align: center;
}

.forecast-temp {
  display: flex;
  gap: 8px;
  font-size: 14px;
}

.forecast-temp .high {
  color: #303133;
  font-weight: 500;
}

.forecast-temp .low {
  color: #909399;
}
</style>