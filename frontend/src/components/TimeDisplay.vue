<template>
  <div class="time-display">
    <div class="time-container">
      <div class="current-time">{{ currentTime }}</div>
      <div class="current-date">{{ currentDate }}</div>
      <div class="day-of-week">{{ dayOfWeek }}</div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'TimeDisplay',
  setup() {
    const currentTime = ref('')
    const currentDate = ref('')
    const dayOfWeek = ref('')
    let timer = null

    const updateTime = () => {
      const now = new Date()
      
      // 格式化时间 (HH:MM:SS)
      currentTime.value = now.toLocaleTimeString('zh-CN', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
      
      // 格式化日期 (YYYY年MM月DD日)
      currentDate.value = now.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
      
      // 格式化星期
      const days = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
      dayOfWeek.value = days[now.getDay()]
    }

    onMounted(() => {
      updateTime()
      // 每秒更新一次时间
      timer = setInterval(updateTime, 1000)
    })

    onUnmounted(() => {
      if (timer) {
        clearInterval(timer)
      }
    })

    return {
      currentTime,
      currentDate,
      dayOfWeek
    }
  }
}
</script>

<style scoped>
.time-display {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  color: white;
  min-width: 220px;
  height: fit-content;
}

.time-container {
  text-align: center;
}

.current-time {
  font-size: 2.25rem;
  font-weight: 700;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  margin-bottom: 4px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.current-date {
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 2px;
  opacity: 0.9;
}

.day-of-week {
  font-size: 0.875rem;
  font-weight: 400;
  opacity: 0.8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .time-display {
    padding: 12px;
    min-width: 160px;
  }
  
  .current-time {
    font-size: 1.5rem;
  }
  
  .current-date {
    font-size: 0.875rem;
  }
  
  .day-of-week {
    font-size: 0.75rem;
  }
}

/* 暗色主题支持 */
.dark-theme .time-display {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}
</style>