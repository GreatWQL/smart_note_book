<template>
  <div class="data-backup">
    <el-card>
      <template #header>
        <div class="backup-header">
          <h3>数据备份与恢复</h3>
          <el-tag type="info">保护您的数据安全</el-tag>
        </div>
      </template>
      
      <div class="backup-content">
        <!-- 备份操作 -->
        <div class="backup-section">
          <h4>数据备份</h4>
          <p class="section-desc">将您的笔记、任务和专注记录导出为JSON文件</p>
          
          <div class="backup-options">
            <el-checkbox-group v-model="backupOptions">
              <el-checkbox label="notes">笔记数据</el-checkbox>
              <el-checkbox label="tasks">任务数据</el-checkbox>
              <el-checkbox label="focus">专注记录</el-checkbox>
              <el-checkbox label="reminders">提醒事项</el-checkbox>
            </el-checkbox-group>
          </div>
          
          <div class="backup-actions">
            <el-button 
              type="primary" 
              @click="exportData"
              :loading="exporting"
              :disabled="backupOptions.length === 0"
            >
              <el-icon><Download /></el-icon>
              导出数据
            </el-button>
            
            <el-button @click="scheduleBackup">
              <el-icon><Timer /></el-icon>
              定时备份
            </el-button>
          </div>
        </div>
        
        <el-divider />
        
        <!-- 恢复操作 -->
        <div class="restore-section">
          <h4>数据恢复</h4>
          <p class="section-desc">从备份文件恢复您的数据</p>
          
          <div class="restore-actions">
            <el-upload
              ref="uploadRef"
              :auto-upload="false"
              :show-file-list="false"
              accept=".json"
              :on-change="handleFileSelect"
            >
              <el-button>
                <el-icon><Upload /></el-icon>
                选择备份文件
              </el-button>
            </el-upload>
            
            <el-button 
              type="success" 
              @click="importData"
              :loading="importing"
              :disabled="!selectedFile"
            >
              <el-icon><Refresh /></el-icon>
              恢复数据
            </el-button>
          </div>
          
          <div v-if="selectedFile" class="file-info">
            <el-alert
              :title="`已选择文件: ${selectedFile.name}`"
              type="info"
              :closable="false"
            />
          </div>
        </div>
        
        <el-divider />
        
        <!-- 备份历史 -->
        <div class="backup-history">
          <h4>备份历史</h4>
          <div v-if="backupHistory.length === 0" class="empty-state">
            暂无备份记录
          </div>
          <div v-else class="history-list">
            <div 
              v-for="backup in backupHistory" 
              :key="backup.id"
              class="history-item"
            >
              <div class="backup-info">
                <div class="backup-name">{{ backup.name }}</div>
                <div class="backup-time">{{ formatTime(backup.created_at) }}</div>
                <div class="backup-size">{{ formatSize(backup.size) }}</div>
              </div>
              <div class="backup-actions">
                <el-button type="text" @click="downloadBackup(backup)">
                  <el-icon><Download /></el-icon>
                </el-button>
                <el-button type="text" @click="deleteBackup(backup)" class="delete-btn">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-card>
    
    <!-- 定时备份设置对话框 -->
    <el-dialog
      v-model="scheduleDialogVisible"
      title="定时备份设置"
      width="500px"
    >
      <el-form :model="scheduleForm" label-width="100px">
        <el-form-item label="备份频率">
          <el-select v-model="scheduleForm.frequency">
            <el-option label="每天" value="daily" />
            <el-option label="每周" value="weekly" />
            <el-option label="每月" value="monthly" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="备份时间">
          <el-time-picker
            v-model="scheduleForm.time"
            format="HH:mm"
            placeholder="选择时间"
          />
        </el-form-item>
        
        <el-form-item label="保留数量">
          <el-input-number
            v-model="scheduleForm.keepCount"
            :min="1"
            :max="30"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="scheduleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveSchedule">保存设置</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Download, Upload, Timer, Refresh, Delete } from '@element-plus/icons-vue'
import request from '@/utils/request'

export default {
  name: 'DataBackup',
  components: {
    Download,
    Upload,
    Timer,
    Refresh,
    Delete
  },
  setup() {
    const exporting = ref(false)
    const importing = ref(false)
    const selectedFile = ref(null)
    const uploadRef = ref(null)
    const scheduleDialogVisible = ref(false)
    
    const backupOptions = ref(['notes', 'tasks', 'focus', 'reminders'])
    const backupHistory = ref([])
    
    const scheduleForm = reactive({
      frequency: 'weekly',
      time: null,
      keepCount: 5
    })
    
    const exportData = async () => {
      if (backupOptions.value.length === 0) {
        ElMessage.warning('请选择要备份的数据类型')
        return
      }
      
      exporting.value = true
      try {
        const backupData = {
          timestamp: new Date().toISOString(),
          version: '1.0',
          data: {}
        }
        
        // 根据选择的选项获取数据
        for (const option of backupOptions.value) {
          let endpoint = ''
          switch (option) {
            case 'notes':
              endpoint = '/notes'
              break
            case 'tasks':
              endpoint = '/tasks'
              break
            case 'focus':
              endpoint = '/focus-sessions'
              break
            case 'reminders':
              endpoint = '/reminders'
              break
          }
          
          if (endpoint) {
            const response = await request.get(endpoint)
            backupData.data[option] = response[option] || response.data || []
          }
        }
        
        // 创建下载链接
        const blob = new Blob([JSON.stringify(backupData, null, 2)], {
          type: 'application/json'
        })
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `智能笔记本备份_${new Date().toISOString().split('T')[0]}.json`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(url)
        
        // 记录备份历史
        const historyItem = {
          id: Date.now(),
          name: link.download,
          created_at: new Date().toISOString(),
          size: blob.size,
          types: [...backupOptions.value]
        }
        backupHistory.value.unshift(historyItem)
        saveBackupHistory()
        
        ElMessage.success('数据导出成功')
      } catch (error) {
        console.error('导出数据失败:', error)
        ElMessage.error('导出数据失败')
      } finally {
        exporting.value = false
      }
    }
    
    const handleFileSelect = (file) => {
      selectedFile.value = file
    }
    
    const importData = async () => {
      if (!selectedFile.value) {
        ElMessage.warning('请先选择备份文件')
        return
      }
      
      try {
        const result = await ElMessageBox.confirm(
          '恢复数据将覆盖现有数据，是否继续？',
          '确认恢复',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        if (result === 'confirm') {
          importing.value = true
          
          const fileContent = await readFileAsText(selectedFile.value.raw)
          const backupData = JSON.parse(fileContent)
          
          // 验证备份文件格式
          if (!backupData.data || !backupData.timestamp) {
            throw new Error('无效的备份文件格式')
          }
          
          // 恢复数据
          for (const [dataType, data] of Object.entries(backupData.data)) {
            if (Array.isArray(data) && data.length > 0) {
              let endpoint = ''
              switch (dataType) {
                case 'notes':
                  endpoint = '/notes/import'
                  break
                case 'tasks':
                  endpoint = '/tasks/import'
                  break
                case 'focus':
                  endpoint = '/focus-sessions/import'
                  break
                case 'reminders':
                  endpoint = '/reminders/import'
                  break
              }
              
              if (endpoint) {
                await request.post(endpoint, { data })
              }
            }
          }
          
          ElMessage.success('数据恢复成功')
          selectedFile.value = null
        }
      } catch (error) {
        console.error('恢复数据失败:', error)
        ElMessage.error('恢复数据失败: ' + error.message)
      } finally {
        importing.value = false
      }
    }
    
    const readFileAsText = (file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = (e) => resolve(e.target.result)
        reader.onerror = reject
        reader.readAsText(file)
      })
    }
    
    const scheduleBackup = () => {
      scheduleDialogVisible.value = true
    }
    
    const saveSchedule = () => {
      // 保存定时备份设置到本地存储
      localStorage.setItem('backupSchedule', JSON.stringify(scheduleForm))
      ElMessage.success('定时备份设置已保存')
      scheduleDialogVisible.value = false
    }
    
    const downloadBackup = (backup) => {
      ElMessage.info('备份文件下载功能需要服务器支持')
    }
    
    const deleteBackup = async (backup) => {
      try {
        await ElMessageBox.confirm('确定要删除这个备份记录吗？', '确认删除')
        const index = backupHistory.value.findIndex(item => item.id === backup.id)
        if (index > -1) {
          backupHistory.value.splice(index, 1)
          saveBackupHistory()
          ElMessage.success('备份记录已删除')
        }
      } catch (error) {
        // 用户取消删除
      }
    }
    
    const saveBackupHistory = () => {
      localStorage.setItem('backupHistory', JSON.stringify(backupHistory.value))
    }
    
    const loadBackupHistory = () => {
      const saved = localStorage.getItem('backupHistory')
      if (saved) {
        backupHistory.value = JSON.parse(saved)
      }
    }
    
    const formatTime = (timeStr) => {
      return new Date(timeStr).toLocaleString('zh-CN')
    }
    
    const formatSize = (bytes) => {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    onMounted(() => {
      loadBackupHistory()
      
      // 加载定时备份设置
      const savedSchedule = localStorage.getItem('backupSchedule')
      if (savedSchedule) {
        Object.assign(scheduleForm, JSON.parse(savedSchedule))
      }
    })
    
    return {
      exporting,
      importing,
      selectedFile,
      uploadRef,
      scheduleDialogVisible,
      backupOptions,
      backupHistory,
      scheduleForm,
      exportData,
      handleFileSelect,
      importData,
      scheduleBackup,
      saveSchedule,
      downloadBackup,
      deleteBackup,
      formatTime,
      formatSize
    }
  }
}
</script>

<style scoped>
.backup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.backup-header h3 {
  margin: 0;
  color: #303133;
}

.backup-section, .restore-section, .backup-history {
  margin-bottom: 24px;
}

.backup-section h4, .restore-section h4, .backup-history h4 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 16px;
}

.section-desc {
  margin: 0 0 16px 0;
  color: #606266;
  font-size: 14px;
}

.backup-options {
  margin-bottom: 16px;
}

.backup-actions, .restore-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.file-info {
  margin-top: 12px;
}

.empty-state {
  text-align: center;
  color: #909399;
  padding: 40px 0;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background: #fafafa;
}

.backup-info {
  flex: 1;
}

.backup-name {
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.backup-time, .backup-size {
  font-size: 12px;
  color: #909399;
}

.backup-actions {
  display: flex;
  gap: 8px;
}

.delete-btn {
  color: #f56c6c;
}

.delete-btn:hover {
  color: #f56c6c;
  background: rgba(245, 108, 108, 0.1);
}
</style>