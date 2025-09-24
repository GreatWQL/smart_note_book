<template>
  <div class="focus-timer">
    <el-card class="timer-card">
      <template #header>
        <div class="timer-header">
          <h3>专注计时器</h3>
          <el-button 
            v-if="!isRunning && !isPaused" 
            type="text" 
            @click="showSettings = !showSettings"
          >
            <el-icon><Setting /></el-icon>
          </el-button>
        </div>
      </template>
      
      <!-- 设置面板 -->
      <div v-if="showSettings && !isRunning && !isPaused" class="timer-settings">
        <el-form label-width="80px">
          <el-form-item label="专注时长">
            <el-input-number
              v-model="settings.focusMinutes"
              :min="1"
              :max="120"
              controls-position="right"
            />
            <span class="unit">分钟</span>
          </el-form-item>
          <el-form-item label="短休息">
            <el-input-number
              v-model="settings.shortBreakMinutes"
              :min="1"
              :max="30"
              controls-position="right"
            />
            <span class="unit">分钟</span>
          </el-form-item>
          <el-form-item label="长休息">
            <el-input-number
              v-model="settings.longBreakMinutes"
              :min="1"
              :max="60"
              controls-position="right"
            />
            <span class="unit">分钟</span>
          </el-form-item>
          <el-form-item label="长休息间隔">
            <el-input-number
              v-model="settings.longBreakInterval"
              :min="2"
              :max="10"
              controls-position="right"
            />
            <span class="unit">个专注周期</span>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 计时器显示 -->
      <div class="timer-display">
        <div class="timer-mode">
          <el-tag :type="getModeTagType()" size="large">
            {{ getModeText() }}
          </el-tag>
        </div>
        
        <div class="timer-circle">
          <el-progress
            type="circle"
            :percentage="progress"
            :width="200"
            :stroke-width="8"
            :color="getProgressColor()"
          >
            <div class="timer-time">
              <div class="time-display">{{ formatTime(timeLeft) }}</div>
              <div class="time-label">{{ getTimeLabel() }}</div>
            </div>
          </el-progress>
        </div>
        
        <div class="timer-controls">
          <el-button
            v-if="!isRunning && !isPaused"
            type="primary"
            size="large"
            @click="startTimer"
          >
            开始专注
          </el-button>
          
          <template v-else>
            <el-button
              v-if="isRunning"
              type="warning"
              size="large"
              @click="pauseTimer"
            >
              暂停
            </el-button>
            
            <el-button
              v-if="isPaused"
              type="primary"
              size="large"
              @click="resumeTimer"
            >
              继续
            </el-button>
            
            <el-button
              size="large"
              @click="stopTimer"
            >
              停止
            </el-button>
          </template>
        </div>
        
        <!-- 统计信息 -->
        <div class="timer-stats">
          <div class="stat-item">
            <span class="stat-label">今日专注</span>
            <span class="stat-value">{{ todayStats.focusCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">专注时长</span>
            <span class="stat-value">{{ formatDuration(todayStats.focusTime) }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">完成率</span>
            <span class="stat-value">{{ getCompletionRate() }}%</span>
          </div>
        </div>
      </div>
    </el-card>
    
    <!-- 完成提示 -->
    <el-dialog
      v-model="showCompletionDialog"
      title="专注完成"
      width="400px"
      :show-close="false"
      :close-on-click-modal="false"
    >
      <div class="completion-content">
        <el-icon class="completion-icon" size="48"><SuccessFilled /></el-icon>
        <h3>{{ getCompletionMessage() }}</h3>
        <p>{{ getCompletionDescription() }}</p>
      </div>
      
      <template #footer>
        <el-button @click="skipBreak" v-if="currentMode !== 'focus'">
          跳过休息
        </el-button>
        <el-button type="primary" @click="startNextSession">
          {{ getNextButtonText() }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElNotification } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'FocusTimer',
  setup() {
    const isRunning = ref(false)
    const isPaused = ref(false)
    const showSettings = ref(false)
    const showCompletionDialog = ref(false)
    const timeLeft = ref(0)
    const totalTime = ref(0)
    const currentMode = ref('focus') // 'focus', 'shortBreak', 'longBreak'
    const sessionCount = ref(0)
    const timer = ref(null)
    
    const settings = reactive({
      focusMinutes: 25,
      shortBreakMinutes: 5,
      longBreakMinutes: 15,
      longBreakInterval: 4
    })
    
    const todayStats = reactive({
      focusCount: 0,
      focusTime: 0,
      totalSessions: 0
    })
    
    const progress = computed(() => {
      if (totalTime.value === 0) return 0
      return Math.round(((totalTime.value - timeLeft.value) / totalTime.value) * 100)
    })
    
    const getModeText = () => {
      switch (currentMode.value) {
        case 'focus': return '专注时间'
        case 'shortBreak': return '短休息'
        case 'longBreak': return '长休息'
        default: return '专注时间'
      }
    }
    
    const getModeTagType = () => {
      switch (currentMode.value) {
        case 'focus': return 'primary'
        case 'shortBreak': return 'success'
        case 'longBreak': return 'warning'
        default: return 'primary'
      }
    }
    
    const getProgressColor = () => {
      switch (currentMode.value) {
        case 'focus': return '#409eff'
        case 'shortBreak': return '#67c23a'
        case 'longBreak': return '#e6a23c'
        default: return '#409eff'
      }
    }
    
    const getTimeLabel = () => {
      return isRunning.value ? '剩余时间' : '总时长'
    }
    
    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    
    const formatDuration = (minutes) => {
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      if (hours > 0) {
        return `${hours}h ${mins}m`
      }
      return `${mins}m`
    }
    
    const getCompletionRate = () => {
      if (todayStats.totalSessions === 0) return 0
      return Math.round((todayStats.focusCount / todayStats.totalSessions) * 100)
    }
    
    const getCompletionMessage = () => {
      switch (currentMode.value) {
        case 'focus': return '专注完成！'
        case 'shortBreak': return '短休息结束'
        case 'longBreak': return '长休息结束'
        default: return '完成！'
      }
    }
    
    const getCompletionDescription = () => {
      switch (currentMode.value) {
        case 'focus': 
          return sessionCount.value % settings.longBreakInterval === 0 
            ? '你已完成一个专注周期，是时候来个长休息了！'
            : '你已完成一个专注周期，来个短休息吧！'
        case 'shortBreak': return '休息结束，准备开始下一个专注周期'
        case 'longBreak': return '长休息结束，你已经充分休息，可以开始新的专注了！'
        default: return ''
      }
    }
    
    const getNextButtonText = () => {
      switch (currentMode.value) {
        case 'focus': 
          return sessionCount.value % settings.longBreakInterval === 0 ? '开始长休息' : '开始短休息'
        case 'shortBreak':
        case 'longBreak': 
          return '开始专注'
        default: return '开始'
      }
    }
    
    const initTimer = (mode) => {
      currentMode.value = mode
      switch (mode) {
        case 'focus':
          timeLeft.value = settings.focusMinutes * 60
          break
        case 'shortBreak':
          timeLeft.value = settings.shortBreakMinutes * 60
          break
        case 'longBreak':
          timeLeft.value = settings.longBreakMinutes * 60
          break
      }
      totalTime.value = timeLeft.value
    }
    
    const startTimer = () => {
      if (!isRunning.value && !isPaused.value) {
        initTimer('focus')
      }
      
      isRunning.value = true
      isPaused.value = false
      showSettings.value = false
      
      timer.value = setInterval(() => {
        if (timeLeft.value > 0) {
          timeLeft.value--
        } else {
          completeSession()
        }
      }, 1000)
    }
    
    const pauseTimer = () => {
      isRunning.value = false
      isPaused.value = true
      if (timer.value) {
        clearInterval(timer.value)
        timer.value = null
      }
    }
    
    const resumeTimer = () => {
      startTimer()
    }
    
    const stopTimer = () => {
      isRunning.value = false
      isPaused.value = false
      if (timer.value) {
        clearInterval(timer.value)
        timer.value = null
      }
      initTimer('focus')
    }
    
    const completeSession = () => {
      isRunning.value = false
      if (timer.value) {
        clearInterval(timer.value)
        timer.value = null
      }
      
      // 更新统计
      if (currentMode.value === 'focus') {
        sessionCount.value++
        todayStats.focusCount++
        todayStats.focusTime += settings.focusMinutes
      }
      todayStats.totalSessions++
      
      // 保存专注记录
      saveFocusSession()
      
      // 显示完成对话框
      showCompletionDialog.value = true
      
      // 发送通知
      sendNotification()
    }
    
    const startNextSession = () => {
      showCompletionDialog.value = false
      
      if (currentMode.value === 'focus') {
        // 专注完成，开始休息
        const isLongBreak = sessionCount.value % settings.longBreakInterval === 0
        initTimer(isLongBreak ? 'longBreak' : 'shortBreak')
      } else {
        // 休息完成，开始专注
        initTimer('focus')
      }
      
      startTimer()
    }
    
    const skipBreak = () => {
      showCompletionDialog.value = false
      initTimer('focus')
    }
    
    const sendNotification = () => {
      if (Notification.permission === 'granted') {
        new Notification(getCompletionMessage(), {
          body: getCompletionDescription(),
          icon: '/favicon.ico'
        })
      }
      
      ElNotification({
        title: getCompletionMessage(),
        message: getCompletionDescription(),
        type: 'success',
        duration: 5000
      })
    }
    
    const saveFocusSession = async () => {
      if (currentMode.value === 'focus') {
        try {
          await request.post('/focus-sessions', {
            duration: settings.focusMinutes,
            completed: true,
            date: new Date().toISOString().split('T')[0]
          })
        } catch (error) {
          console.error('保存专注记录失败:', error)
        }
      }
    }
    
    const loadTodayStats = async () => {
      try {
        const today = new Date().toISOString().split('T')[0]
        const response = await request.get(`/focus-sessions?date=${today}`)
        const sessions = response.sessions || []
        
        todayStats.focusCount = sessions.filter(s => s.completed).length
        todayStats.focusTime = sessions.reduce((total, s) => total + (s.completed ? s.duration : 0), 0)
        todayStats.totalSessions = sessions.length
      } catch (error) {
        console.error('加载今日统计失败:', error)
      }
    }
    
    const requestNotificationPermission = () => {
      if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission()
      }
    }
    
    onMounted(() => {
      initTimer('focus')
      loadTodayStats()
      requestNotificationPermission()
    })
    
    onUnmounted(() => {
      if (timer.value) {
        clearInterval(timer.value)
      }
    })
    
    return {
      isRunning,
      isPaused,
      showSettings,
      showCompletionDialog,
      timeLeft,
      currentMode,
      settings,
      todayStats,
      progress,
      getModeText,
      getModeTagType,
      getProgressColor,
      getTimeLabel,
      formatTime,
      formatDuration,
      getCompletionRate,
      getCompletionMessage,
      getCompletionDescription,
      getNextButtonText,
      startTimer,
      pauseTimer,
      resumeTimer,
      stopTimer,
      startNextSession,
      skipBreak
    }
  }
}
</script>

<style scoped>
.focus-timer {
  max-width: 400px;
  margin: 0 auto;
}

.timer-card {
  text-align: center;
}

.timer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.timer-header h3 {
  margin: 0;
  color: #303133;
}

.timer-settings {
  margin-bottom: 20px;
  text-align: left;
}

.timer-settings .unit {
  margin-left: 8px;
  color: #909399;
  font-size: 14px;
}

.timer-display {
  padding: 20px 0;
}

.timer-mode {
  margin-bottom: 20px;
}

.timer-circle {
  margin-bottom: 30px;
}

.timer-time {
  text-align: center;
}

.time-display {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
}

.time-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.timer-controls {
  margin-bottom: 30px;
}

.timer-controls .el-button {
  margin: 0 8px;
}

.timer-stats {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
  border-top: 1px solid #ebeef5;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.stat-value {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.completion-content {
  text-align: center;
  padding: 20px 0;
}

.completion-icon {
  color: #67c23a;
  margin-bottom: 16px;
}

.completion-content h3 {
  margin: 0 0 12px 0;
  color: #303133;
}

.completion-content p {
  margin: 0;
  color: #606266;
  line-height: 1.6;
}
</style>