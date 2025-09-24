<template>
  <div class="calendar-container">
    <SidebarNav />
    <div class="main-content">
      <div class="content-header">
        <h1>日历</h1>
        <div class="header-actions">
          <el-button type="primary" @click="showAddEventDialog = true">
            <el-icon><Plus /></el-icon>
            添加事件
          </el-button>
          <div class="view-controls">
            <el-button-group>
              <el-button 
                :type="currentView === 'month' ? 'primary' : 'default'"
                @click="currentView = 'month'"
              >
                月视图
              </el-button>
              <el-button 
                :type="currentView === 'week' ? 'primary' : 'default'"
                @click="currentView = 'week'"
              >
                周视图
              </el-button>
            </el-button-group>
          </div>
        </div>
      </div>

      <div class="calendar-layout">
        <div class="calendar-content">
          <!-- 日历导航 -->
          <div class="calendar-nav">
            <div class="nav-controls">
              <el-button @click="previousPeriod" circle>
                <el-icon><ArrowLeft /></el-icon>
              </el-button>
              <h2 class="current-period">{{ currentPeriodText }}</h2>
              <el-button @click="nextPeriod" circle>
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
            <el-button @click="goToToday" type="primary" plain>今天</el-button>
          </div>

          <!-- 月视图 -->
          <div v-if="currentView === 'month'" class="calendar-month">
            <div class="weekdays">
              <div v-for="day in weekdays" :key="day" class="weekday">
                {{ day }}
              </div>
            </div>
            <div class="calendar-grid">
              <div 
                v-for="date in monthDates" 
                :key="date.key"
                class="calendar-cell"
                :class="{
                  'other-month': !date.isCurrentMonth,
                  'today': date.isToday,
                  'selected': date.isSelected
                }"
                @click="selectDate(date)"
              >
                <div class="date-number">{{ date.day }}</div>
                <div class="events">
                  <div 
                    v-for="event in getEventsForDate(date.date)" 
                    :key="event.id"
                    class="event-item"
                    :class="`event-${event.type}`"
                    @click.stop="viewEvent(event)"
                  >
                    {{ event.title }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 周视图 -->
          <div v-if="currentView === 'week'" class="calendar-week">
            <div class="week-header">
              <div class="time-column"></div>
              <div 
                v-for="date in weekDates" 
                :key="date.key"
                class="week-day-header"
                :class="{ 'today': date.isToday }"
              >
                <div class="day-name">{{ date.dayName }}</div>
                <div class="day-number">{{ date.day }}</div>
              </div>
            </div>
            <div class="week-body">
              <div class="time-slots">
                <div 
                  v-for="hour in hours" 
                  :key="hour"
                  class="time-slot"
                >
                  {{ hour }}:00
                </div>
              </div>
              <div class="week-grid">
                <div 
                  v-for="date in weekDates" 
                  :key="date.key"
                  class="week-day-column"
                >
                  <div 
                    v-for="hour in hours" 
                    :key="hour"
                    class="hour-slot"
                    @click="addEventAtTime(date.date, hour)"
                  >
                    <div 
                      v-for="event in getEventsForDateTime(date.date, hour)" 
                      :key="event.id"
                      class="week-event"
                      :class="`event-${event.type}`"
                      @click.stop="viewEvent(event)"
                    >
                      {{ event.title }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 今日事件侧边栏 -->
        <div class="today-events">
          <h3>今日事件</h3>
          <div class="event-list">
            <div 
              v-for="event in todayEvents" 
              :key="event.id"
              class="today-event-item"
              :class="`event-${event.type}`"
            >
              <div class="event-time">{{ formatTime(event.start_time) }}</div>
              <div class="event-details">
                <div class="event-title">{{ event.title }}</div>
                <div class="event-description">{{ event.description }}</div>
              </div>
            </div>
            <div v-if="todayEvents.length === 0" class="no-events">
              今日暂无事件
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加事件对话框 -->
    <el-dialog 
      v-model="showAddEventDialog" 
      title="添加事件" 
      width="500px"
    >
      <el-form :model="newEvent" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="newEvent.title" placeholder="请输入事件标题" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input 
            v-model="newEvent.description" 
            type="textarea" 
            placeholder="请输入事件描述"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker
            v-model="newEvent.date"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="时间">
          <el-time-picker
            v-model="newEvent.time"
            placeholder="选择时间"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="newEvent.type" placeholder="选择事件类型" style="width: 100%">
            <el-option label="工作" value="work" />
            <el-option label="个人" value="personal" />
            <el-option label="重要" value="important" />
            <el-option label="会议" value="meeting" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddEventDialog = false">取消</el-button>
        <el-button type="primary" @click="addEvent">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import SidebarNav from '@/components/SidebarNav.vue'

export default {
  name: 'CalendarPage',
  components: {
    SidebarNav,
    Plus,
    ArrowLeft,
    ArrowRight
  },
  setup() {
    const currentDate = ref(new Date())
    const currentView = ref('month')
    const selectedDate = ref(new Date())
    const showAddEventDialog = ref(false)
    
    const events = ref([
      {
        id: 1,
        title: '团队会议',
        description: '讨论项目进度',
        date: new Date(),
        start_time: '09:00',
        type: 'meeting'
      },
      {
        id: 2,
        title: '完成报告',
        description: '月度工作总结',
        date: new Date(),
        start_time: '14:00',
        type: 'work'
      }
    ])

    const newEvent = reactive({
      title: '',
      description: '',
      date: new Date(),
      time: '',
      type: 'work'
    })

    const weekdays = ['日', '一', '二', '三', '四', '五', '六']
    const hours = Array.from({ length: 24 }, (_, i) => i)

    // 计算当前期间文本
    const currentPeriodText = computed(() => {
      const year = currentDate.value.getFullYear()
      const month = currentDate.value.getMonth() + 1
      
      if (currentView.value === 'month') {
        return `${year}年${month}月`
      } else {
        // 周视图显示周的开始和结束日期
        const startOfWeek = getStartOfWeek(currentDate.value)
        const endOfWeek = new Date(startOfWeek)
        endOfWeek.setDate(startOfWeek.getDate() + 6)
        
        return `${startOfWeek.getMonth() + 1}月${startOfWeek.getDate()}日 - ${endOfWeek.getMonth() + 1}月${endOfWeek.getDate()}日`
      }
    })

    // 计算月视图日期
    const monthDates = computed(() => {
      const year = currentDate.value.getFullYear()
      const month = currentDate.value.getMonth()
      const firstDay = new Date(year, month, 1)
      const lastDay = new Date(year, month + 1, 0)
      const startDate = getStartOfWeek(firstDay)
      
      const dates = []
      const current = new Date(startDate)
      
      for (let i = 0; i < 42; i++) {
        const isCurrentMonth = current.getMonth() === month
        const isToday = isSameDay(current, new Date())
        const isSelected = isSameDay(current, selectedDate.value)
        
        dates.push({
          date: new Date(current),
          day: current.getDate(),
          isCurrentMonth,
          isToday,
          isSelected,
          key: current.toISOString()
        })
        
        current.setDate(current.getDate() + 1)
      }
      
      return dates
    })

    // 计算周视图日期
    const weekDates = computed(() => {
      const startOfWeek = getStartOfWeek(currentDate.value)
      const dates = []
      
      for (let i = 0; i < 7; i++) {
        const date = new Date(startOfWeek)
        date.setDate(startOfWeek.getDate() + i)
        
        dates.push({
          date: new Date(date),
          day: date.getDate(),
          dayName: weekdays[date.getDay()],
          isToday: isSameDay(date, new Date()),
          key: date.toISOString()
        })
      }
      
      return dates
    })

    // 今日事件
    const todayEvents = computed(() => {
      const today = new Date()
      return events.value.filter(event => isSameDay(event.date, today))
        .sort((a, b) => a.start_time.localeCompare(b.start_time))
    })

    // 工具函数
    const getStartOfWeek = (date) => {
      const start = new Date(date)
      const day = start.getDay()
      start.setDate(start.getDate() - day)
      return start
    }

    const isSameDay = (date1, date2) => {
      return date1.getFullYear() === date2.getFullYear() &&
             date1.getMonth() === date2.getMonth() &&
             date1.getDate() === date2.getDate()
    }

    const formatTime = (time) => {
      return time
    }

    // 获取指定日期的事件
    const getEventsForDate = (date) => {
      return events.value.filter(event => isSameDay(event.date, date))
    }

    // 获取指定日期时间的事件
    const getEventsForDateTime = (date, hour) => {
      return events.value.filter(event => {
        if (!isSameDay(event.date, date)) return false
        const eventHour = parseInt(event.start_time.split(':')[0])
        return eventHour === hour
      })
    }

    // 导航方法
    const previousPeriod = () => {
      if (currentView.value === 'month') {
        currentDate.value.setMonth(currentDate.value.getMonth() - 1)
      } else {
        currentDate.value.setDate(currentDate.value.getDate() - 7)
      }
      currentDate.value = new Date(currentDate.value)
    }

    const nextPeriod = () => {
      if (currentView.value === 'month') {
        currentDate.value.setMonth(currentDate.value.getMonth() + 1)
      } else {
        currentDate.value.setDate(currentDate.value.getDate() + 7)
      }
      currentDate.value = new Date(currentDate.value)
    }

    const goToToday = () => {
      currentDate.value = new Date()
      selectedDate.value = new Date()
    }

    const selectDate = (date) => {
      selectedDate.value = new Date(date.date)
    }

    const addEventAtTime = (date, hour) => {
      newEvent.date = new Date(date)
      newEvent.time = `${hour.toString().padStart(2, '0')}:00`
      showAddEventDialog.value = true
    }

    const addEvent = () => {
      if (!newEvent.title.trim()) {
        ElMessage.warning('请输入事件标题')
        return
      }

      const event = {
        id: Date.now(),
        title: newEvent.title,
        description: newEvent.description,
        date: new Date(newEvent.date),
        start_time: newEvent.time || '09:00',
        type: newEvent.type
      }

      events.value.push(event)
      
      // 重置表单
      Object.assign(newEvent, {
        title: '',
        description: '',
        date: new Date(),
        time: '',
        type: 'work'
      })
      
      showAddEventDialog.value = false
      ElMessage.success('事件添加成功')
    }

    const viewEvent = (event) => {
      ElMessage.info(`查看事件: ${event.title}`)
    }

    return {
      currentDate,
      currentView,
      selectedDate,
      showAddEventDialog,
      events,
      newEvent,
      weekdays,
      hours,
      currentPeriodText,
      monthDates,
      weekDates,
      todayEvents,
      getEventsForDate,
      getEventsForDateTime,
      previousPeriod,
      nextPeriod,
      goToToday,
      selectDate,
      addEventAtTime,
      addEvent,
      viewEvent,
      formatTime
    }
  }
}
</script>

<style scoped>
.calendar-container {
  display: flex;
  height: 100vh;
  background: transparent;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: var(--spacing-6);
  overflow: hidden;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-6);
  padding: var(--spacing-6);
  background: var(--bg-color-card);
  backdrop-filter: blur(20px);
  border-radius: var(--border-radius-2xl);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: var(--box-shadow-card);
}

.calendar-layout {
  flex: 1;
  display: flex;
  gap: var(--spacing-6);
  overflow: hidden;
}

.content-header h1 {
  font-size: var(--font-size-3xl);
  font-weight: 800;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: var(--spacing-4);
  align-items: center;
}

.calendar-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--bg-color-card);
  backdrop-filter: blur(20px);
  border-radius: var(--border-radius-2xl);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: var(--box-shadow-card);
  padding: var(--spacing-6);
  overflow: hidden;
  min-width: 0;
}

.calendar-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-6);
  padding-bottom: var(--spacing-4);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-controls {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
}

.current-period {
  font-size: var(--font-size-xl);
  font-weight: 600;
  margin: 0;
  color: var(--text-color-primary);
}

/* 月视图样式 */
.calendar-month {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  margin-bottom: var(--spacing-2);
}

.weekday {
  padding: var(--spacing-3);
  text-align: center;
  font-weight: 600;
  color: var(--text-color-secondary);
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--border-radius-lg);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-template-rows: repeat(6, 1fr);
  gap: 1px;
  flex: 1;
  min-height: 400px;
}

.calendar-cell {
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-2);
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 80px;
  display: flex;
  flex-direction: column;
}

.calendar-cell:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.calendar-cell.other-month {
  opacity: 0.3;
}

.calendar-cell.today {
  background: var(--gradient-primary);
  color: white;
}

.calendar-cell.selected {
  border: 2px solid var(--color-primary);
}

.date-number {
  font-weight: 600;
  margin-bottom: var(--spacing-1);
}

.events {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.event-item {
  font-size: var(--font-size-xs);
  padding: 2px 4px;
  border-radius: 4px;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.event-work { background: #3b82f6; color: white; }
.event-personal { background: #10b981; color: white; }
.event-important { background: #ef4444; color: white; }
.event-meeting { background: #8b5cf6; color: white; }

/* 周视图样式 */
.calendar-week {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.week-header {
  display: grid;
  grid-template-columns: 60px repeat(7, 1fr);
  gap: 1px;
  margin-bottom: var(--spacing-2);
}

.week-day-header {
  padding: var(--spacing-3);
  text-align: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--border-radius-lg);
}

.week-day-header.today {
  background: var(--gradient-primary);
  color: white;
}

.day-name {
  font-size: var(--font-size-sm);
  color: var(--text-color-secondary);
}

.day-number {
  font-size: var(--font-size-lg);
  font-weight: 600;
  margin-top: 4px;
}

.week-body {
  flex: 1;
  display: grid;
  grid-template-columns: 60px repeat(7, 1fr);
  gap: 1px;
  overflow-y: auto;
}

.time-slots {
  display: flex;
  flex-direction: column;
}

.time-slot {
  height: 60px;
  padding: var(--spacing-2);
  font-size: var(--font-size-xs);
  color: var(--text-color-secondary);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
}

.week-day-column {
  display: flex;
  flex-direction: column;
}

.hour-slot {
  height: 60px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  position: relative;
  transition: background-color 0.2s ease;
}

.hour-slot:hover {
  background: rgba(255, 255, 255, 0.05);
}

.week-event {
  position: absolute;
  left: 2px;
  right: 2px;
  top: 2px;
  padding: 4px;
  border-radius: 4px;
  font-size: var(--font-size-xs);
  cursor: pointer;
  z-index: 1;
}

/* 今日事件侧边栏 */
.today-events {
  width: 320px;
  min-width: 320px;
  background: var(--bg-color-card);
  backdrop-filter: blur(20px);
  border-radius: var(--border-radius-2xl);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: var(--box-shadow-card);
  padding: var(--spacing-6);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.today-events h3 {
  margin: 0 0 var(--spacing-4) 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-color-primary);
}

.event-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-3);
}

.today-event-item {
  padding: var(--spacing-4);
  border-radius: var(--border-radius-lg);
  border-left: 4px solid;
  background: rgba(255, 255, 255, 0.05);
}

.today-event-item.event-work { border-left-color: #3b82f6; }
.today-event-item.event-personal { border-left-color: #10b981; }
.today-event-item.event-important { border-left-color: #ef4444; }
.today-event-item.event-meeting { border-left-color: #8b5cf6; }

.event-time {
  font-size: var(--font-size-sm);
  color: var(--text-color-secondary);
  margin-bottom: var(--spacing-1);
}

.event-title {
  font-weight: 600;
  color: var(--text-color-primary);
  margin-bottom: var(--spacing-1);
}

.event-description {
  font-size: var(--font-size-sm);
  color: var(--text-color-secondary);
}

.no-events {
  text-align: center;
  color: var(--text-color-secondary);
  font-style: italic;
  padding: var(--spacing-8);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .today-events {
    width: 280px;
    min-width: 280px;
  }
}

@media (max-width: 768px) {
  .calendar-layout {
    flex-direction: column;
  }
  
  .today-events {
    width: 100%;
    min-width: auto;
    max-height: 300px;
  }
  
  .calendar-grid {
    min-height: 300px;
  }
}
</style>