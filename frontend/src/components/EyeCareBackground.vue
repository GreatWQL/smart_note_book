<template>
  <div class="eye-care-background">
    <!-- 背景颜色指示器 -->
    <div class="color-indicator" v-if="showIndicator">
      <div class="indicator-dot" :style="{ background: currentGradient }"></div>
      <span class="indicator-text">{{ colorSchemes[currentSchemeIndex].name }}</span>
      <div class="timer-progress">
        <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'EyeCareBackground',
  setup() {
    const currentSchemeIndex = ref(0)
    const showIndicator = ref(true)
    const progressPercentage = ref(0)
    const currentGradient = ref('')
    
    // 护眼浅色系配色方案
    const colorSchemes = ref([
      {
        name: '薄荷清新',
        gradient: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0fdf4 100%)',
        description: '清新薄荷色，舒缓眼部疲劳'
      },
      {
        name: '樱花粉嫩',
        gradient: 'linear-gradient(135deg, #fef7f0 0%, #fdf2f8 50%, #f9fafb 100%)',
        description: '温柔粉色调，温暖护眼'
      },
      {
        name: '天空蔚蓝',
        gradient: 'linear-gradient(135deg, #f0f9ff 0%, #e6f3ff 50%, #f8fafc 100%)',
        description: '天空蓝色，清澈明亮'
      },
      {
        name: '柠檬微黄',
        gradient: 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 50%, #f9fafb 100%)',
        description: '温暖黄色调，减少蓝光刺激'
      },
      {
        name: '薰衣草紫',
        gradient: 'linear-gradient(135deg, #faf5ff 0%, #f3e8ff 50%, #f8fafc 100%)',
        description: '淡雅紫色，舒缓神经'
      },
      {
        name: '抹茶绿意',
        gradient: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #f9fafb 100%)',
        description: '自然绿色，保护视力'
      },
      {
        name: '珊瑚橙暖',
        gradient: 'linear-gradient(135deg, #fff7ed 0%, #fed7aa 50%, #f9fafb 100%)',
        description: '温暖橙色，活力护眼'
      },
      {
        name: '云朵白净',
        gradient: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%)',
        description: '纯净白色，最大程度保护视力'
      }
    ])
    
    let rotationTimer = null
    let progressTimer = null
    const rotationInterval = 60000 // 1分钟 = 60000毫秒
    const progressUpdateInterval = 100 // 100毫秒更新一次进度
    
    // 应用背景颜色
    const applyBackgroundColor = (gradient) => {
      // 更新CSS变量
      document.documentElement.style.setProperty('--gradient-page-bg', gradient)
      document.documentElement.style.setProperty('--gradient-sidebar-bg', gradient)
      currentGradient.value = gradient
      
      // 添加平滑过渡效果
      document.body.style.transition = 'background 2s ease-in-out'
    }
    
    // 切换到下一个配色方案
    const switchToNextScheme = () => {
      currentSchemeIndex.value = (currentSchemeIndex.value + 1) % colorSchemes.value.length
      const currentScheme = colorSchemes.value[currentSchemeIndex.value]
      applyBackgroundColor(currentScheme.gradient)
      
      // 重置进度
      progressPercentage.value = 0
      
      console.log(`🎨 切换到护眼配色: ${currentScheme.name} - ${currentScheme.description}`)
    }
    
    // 更新进度条
    const updateProgress = () => {
      progressPercentage.value += (progressUpdateInterval / rotationInterval) * 100
      if (progressPercentage.value >= 100) {
        progressPercentage.value = 100
      }
    }
    
    // 开始定时轮转
    const startRotation = () => {
      // 立即应用第一个配色方案
      const currentScheme = colorSchemes.value[currentSchemeIndex.value]
      applyBackgroundColor(currentScheme.gradient)
      
      // 设置轮转定时器
      rotationTimer = setInterval(() => {
        switchToNextScheme()
      }, rotationInterval)
      
      // 设置进度更新定时器
      progressTimer = setInterval(() => {
        updateProgress()
      }, progressUpdateInterval)
    }
    
    // 停止定时轮转
    const stopRotation = () => {
      if (rotationTimer) {
        clearInterval(rotationTimer)
        rotationTimer = null
      }
      if (progressTimer) {
        clearInterval(progressTimer)
        progressTimer = null
      }
    }
    
    // 手动切换配色方案
    const manualSwitch = () => {
      stopRotation()
      switchToNextScheme()
      startRotation()
    }
    
    // 切换指示器显示状态
    const toggleIndicator = () => {
      showIndicator.value = !showIndicator.value
    }
    
    // 获取当前配色方案信息
    const getCurrentScheme = () => {
      return colorSchemes.value[currentSchemeIndex.value]
    }
    
    onMounted(() => {
      console.log('🌈 护眼背景系统启动')
      console.log('💡 配色方案:', colorSchemes.value.map(s => s.name).join(', '))
      startRotation()
      
      // 3秒后隐藏指示器
      setTimeout(() => {
        showIndicator.value = false
      }, 5000)
    })
    
    onUnmounted(() => {
      stopRotation()
      console.log('🌈 护眼背景系统关闭')
    })
    
    return {
      currentSchemeIndex,
      showIndicator,
      progressPercentage,
      currentGradient,
      colorSchemes,
      manualSwitch,
      toggleIndicator,
      getCurrentScheme
    }
  }
}
</script>

<style scoped>
.eye-care-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
}

.color-indicator {
  position: fixed;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  pointer-events: auto;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 1000;
}

.color-indicator:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.indicator-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.indicator-text {
  font-size: 12px;
  color: #374151;
  font-weight: 500;
  white-space: nowrap;
}

.timer-progress {
  width: 40px;
  height: 4px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 2px;
  overflow: hidden;
  position: relative;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #3b82f6);
  border-radius: 2px;
  transition: width 0.1s linear;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .color-indicator {
    top: 10px;
    right: 10px;
    padding: 8px 12px;
    font-size: 11px;
  }
  
  .indicator-dot {
    width: 10px;
    height: 10px;
  }
  
  .timer-progress {
    width: 30px;
    height: 3px;
  }
}

/* 深色主题适配 */
.dark-theme .color-indicator {
  background: rgba(31, 41, 55, 0.95);
  border: 1px solid rgba(75, 85, 99, 0.3);
}

.dark-theme .indicator-text {
  color: #e5e7eb;
}

.dark-theme .timer-progress {
  background: rgba(255, 255, 255, 0.1);
}
</style>