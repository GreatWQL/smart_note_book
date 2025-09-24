<template>
  <div class="reminder-manager">
    <el-card>
      <template #header>
        <div class="reminder-header">
          <h3>提醒管理</h3>
          <el-button type="primary" size="small" @click="showCreateDialog = true">
            <el-icon><Plus /></el-icon>
            新建提醒
          </el-button>
        </div>
      </template>
      
      <div class="reminder-list">
        <div v-if="reminders.length === 0" class="empty-state">
          <el-empty description="暂无提醒" />
        </div>
        <div v-else>
          <div
            v-for="reminder in reminders"
            :key="reminder.id"
            class="reminder-item"
            :class="{ 'reminder-overdue': isOverdue(reminder) }"
          >
            <div class="reminder-content">
              <div class="reminder-title">{{ reminder.title }}</div>
              <div class="reminder-time">
                <el-icon><Clock /></el-icon>
                {{ formatDateTime(reminder.remind_at) }}
              </div>
              <div v-if="reminder.content" class="reminder-description">
                {{ reminder.content }}
              </div>
            </div>
            <div class="reminder-actions">
              <el-tag :type="getStatusTagType(reminder)" size="small">
                {{ getStatusText(reminder) }}
              </el-tag>
              <el-button
                v-if="!reminder.is_completed"
                type="text"
                size="small"
                @click="completeReminder(reminder)"
              >
                完成
              </el-button>
              <el-button
                type="text"
                size="small"
                @click="editReminder(reminder)"
              >
                编辑
              </el-button>
              <el-button
                type="text"
                size="small"
                @click="deleteReminder(reminder)"
              >
                删除
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-card>
    
    <!-- 新建/编辑提醒对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingReminder ? '编辑提醒' : '新建提醒'"
      width="500px"
    >
      <el-form :model="reminderForm" label-width="80px">
        <el-form-item label="标题" required>
          <el-input v-model="reminderForm.title" placeholder="请输入提醒标题" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="reminderForm.content"
            type="textarea"
            :rows="3"
            placeholder="请输入提醒描述（可选）"
          />
        </el-form-item>
        <el-form-item label="提醒时间" required>
          <el-date-picker
            v-model="reminderForm.remind_at"
            type="datetime"
            placeholder="选择提醒时间"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="重复">
          <el-select v-model="reminderForm.recurring_type" placeholder="选择重复类型">
            <el-option label="不重复" value="none" />
            <el-option label="每天" value="daily" />
            <el-option label="每周" value="weekly" />
            <el-option label="每月" value="monthly" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="saveReminder" :loading="saving">
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'ReminderManager',
  setup() {
    const reminders = ref([])
    const showCreateDialog = ref(false)
    const editingReminder = ref(null)
    const saving = ref(false)
    const checkInterval = ref(null)
    
    const reminderForm = reactive({
      title: '',
      content: '',
      remind_at: '',
      is_recurring: false,
      recurring_type: null
    })
    
    const loadReminders = async () => {
      try {
        const response = await request.get('/reminders')
        reminders.value = response.reminders || []
      } catch (error) {
        console.error('加载提醒失败:', error)
      }
    }
    
    const saveReminder = async () => {
      if (!reminderForm.title.trim()) {
        ElMessage.warning('请输入提醒标题')
        return
      }
      
      if (!reminderForm.remind_at) {
        ElMessage.warning('请选择提醒时间')
        return
      }
      
      try {
        saving.value = true
        
        // 根据recurring_type设置is_recurring
        const formData = {
          ...reminderForm,
          is_recurring: reminderForm.recurring_type && reminderForm.recurring_type !== 'none',
          recurring_type: reminderForm.recurring_type === 'none' ? null : reminderForm.recurring_type
        }
        
        if (editingReminder.value) {
          await request.put(`/reminders/${editingReminder.value.id}`, formData)
          ElMessage.success('更新成功')
        } else {
          await request.post('/reminders', formData)
          ElMessage.success('创建成功')
        }
        
        showCreateDialog.value = false
        resetForm()
        loadReminders()
      } catch (error) {
        console.error('保存提醒失败:', error)
      } finally {
        saving.value = false
      }
    }
    
    const editReminder = (reminder) => {
      editingReminder.value = reminder
      reminderForm.title = reminder.title
      reminderForm.content = reminder.content || ''
      reminderForm.remind_at = reminder.remind_at
      reminderForm.is_recurring = reminder.is_recurring || false
      reminderForm.recurring_type = reminder.recurring_type || 'none'
      showCreateDialog.value = true
    }
    
    const completeReminder = async (reminder) => {
      try {
        await request.put(`/reminders/${reminder.id}`, {
          ...reminder,
          is_completed: true
        })
        ElMessage.success('提醒已完成')
        loadReminders()
      } catch (error) {
        console.error('完成提醒失败:', error)
      }
    }
    
    const deleteReminder = async (reminder) => {
      try {
        await ElMessageBox.confirm(`确定要删除提醒"${reminder.title}"吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await request.delete(`/reminders/${reminder.id}`)
        ElMessage.success('删除成功')
        loadReminders()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除提醒失败:', error)
        }
      }
    }
    
    const resetForm = () => {
      editingReminder.value = null
      reminderForm.title = ''
      reminderForm.content = ''
      reminderForm.remind_at = ''
      reminderForm.is_recurring = false
      reminderForm.recurring_type = 'none'
    }
    
    const formatDateTime = (dateTimeStr) => {
      const date = new Date(dateTimeStr)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const isOverdue = (reminder) => {
      if (reminder.is_completed) return false
      const now = new Date()
      const remindTime = new Date(reminder.remind_at)
      return remindTime < now
    }
    
    const getStatusText = (reminder) => {
      if (reminder.is_completed) return '已完成'
      if (isOverdue(reminder)) return '已过期'
      return '待提醒'
    }
    
    const getStatusTagType = (reminder) => {
      if (reminder.is_completed) return 'success'
      if (isOverdue(reminder)) return 'danger'
      return 'warning'
    }
    
    const checkReminders = () => {
      const now = new Date()
      
      reminders.value.forEach(reminder => {
        if (reminder.is_completed) return
        
        const remindTime = new Date(reminder.remind_at)
        const timeDiff = remindTime.getTime() - now.getTime()
        
        // 如果提醒时间在1分钟内，显示通知
        if (timeDiff > 0 && timeDiff <= 60000) {
          showReminderNotification(reminder)
        }
      })
    }
    
    const showReminderNotification = (reminder) => {
      // 浏览器通知
      if (Notification.permission === 'granted') {
        new Notification(`提醒：${reminder.title}`, {
          body: reminder.content || '您有一个提醒',
          icon: '/favicon.ico'
        })
      }
      
      // Element Plus 通知
      ElNotification({
        title: '提醒',
        message: `${reminder.title}${reminder.content ? '\n' + reminder.content : ''}`,
        type: 'warning',
        duration: 0, // 不自动关闭
        onClick: () => {
          completeReminder(reminder)
        }
      })
    }
    
    const requestNotificationPermission = () => {
      if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission()
      }
    }
    
    onMounted(() => {
      loadReminders()
      requestNotificationPermission()
      
      // 每分钟检查一次提醒
      checkInterval.value = setInterval(checkReminders, 60000)
    })
    
    onUnmounted(() => {
      if (checkInterval.value) {
        clearInterval(checkInterval.value)
      }
    })
    
    return {
      reminders,
      showCreateDialog,
      editingReminder,
      saving,
      reminderForm,
      saveReminder,
      editReminder,
      completeReminder,
      deleteReminder,
      formatDateTime,
      isOverdue,
      getStatusText,
      getStatusTagType
    }
  }
}
</script>

<style scoped>
.reminder-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reminder-header h3 {
  margin: 0;
  color: #303133;
}

.reminder-list {
  max-height: 400px;
  overflow-y: auto;
}

.reminder-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 16px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 12px;
  transition: all 0.3s;
}

.reminder-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.reminder-item.reminder-overdue {
  border-color: #f56c6c;
  background-color: #fef0f0;
}

.reminder-content {
  flex: 1;
}

.reminder-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.reminder-time {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.reminder-time .el-icon {
  margin-right: 4px;
}

.reminder-description {
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}

.reminder-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}

.reminder-actions .el-button {
  padding: 4px 8px;
  min-width: auto;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}
</style>