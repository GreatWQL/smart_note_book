<template>
  <div class="simple-weather">
    <div class="weather-icon">
      <svg v-if="isDaytime" class="sun-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="2"/>
        <path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke="currentColor" stroke-width="2"/>
      </svg>
      <svg v-else class="moon-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2"/>
      </svg>
    </div>
    <div class="weather-info">
      <div class="location">{{ location }}</div>
      <div class="temperature">{{ temperature }}°C</div>
      <div class="condition">{{ condition }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const location = ref('北京')
const temperature = ref(15)
const condition = ref('晴朗')
const currentHour = ref(new Date().getHours())

// 判断是否为白天（6:00-18:00为白天）
const isDaytime = computed(() => {
  return currentHour.value >= 6 && currentHour.value < 18
})

// 模拟获取天气数据
const fetchWeatherData = async () => {
  try {
    // 这里可以调用真实的天气API
    // 目前使用模拟数据
    location.value = '北京'
    temperature.value = Math.floor(Math.random() * 20) + 10 // 10-30度随机温度
    const conditions = ['晴朗', '多云', '阴天', '小雨']
    condition.value = conditions[Math.floor(Math.random() * conditions.length)]
  } catch (error) {
    console.error('获取天气数据失败:', error)
  }
}

onMounted(() => {
  fetchWeatherData()
  // 每小时更新一次时间
  setInterval(() => {
    currentHour.value = new Date().getHours()
  }, 3600000)
})
</script>

<style scoped>
.simple-weather {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.simple-weather:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.weather-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sun-icon {
  width: 32px;
  height: 32px;
  color: #FFD700;
}

.moon-icon {
  width: 28px;
  height: 28px;
  color: #E6E6FA;
  animation: glow 3s ease-in-out infinite alternate;
}

.weather-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.location {
  font-size: 14px;
  font-weight: 500;
  opacity: 0.9;
}

.temperature {
  font-size: 24px;
  font-weight: 700;
  line-height: 1;
}

.condition {
  font-size: 12px;
  opacity: 0.8;
  font-weight: 400;
}



@keyframes glow {
  from {
    opacity: 0.7;
  }
  to {
    opacity: 1;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .simple-weather {
    padding: 12px 16px;
    gap: 10px;
  }
  
  .weather-icon {
    width: 36px;
    height: 36px;
  }
  
  .sun-icon {
    width: 28px;
    height: 28px;
  }
  
  .moon-icon {
    width: 24px;
    height: 24px;
  }
  
  .temperature {
    font-size: 20px;
  }
  
  .location {
    font-size: 13px;
  }
  
  .condition {
    font-size: 11px;
  }
}
</style>