<template>
  <div class="notes-container">
    <SidebarNav />
    <div class="main-content">
      <div class="content-header">
        <h1>笔记管理</h1>
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新建笔记
        </el-button>
      </div>
      
      <div class="notes-content">
        <div class="notes-list">
          <div v-if="notes.length === 0" class="empty-state">
            <el-empty description="暂无笔记，点击新建笔记开始记录" />
          </div>
          <div v-else>
            <el-card
              v-for="note in notes"
              :key="note.id"
              class="note-card"
              @click="selectNote(note)"
            >
              <div class="note-header">
                <h3>{{ note.title }}</h3>
                <div class="note-actions">
                  <el-button
                    type="text"
                    size="small"
                    @click.stop="editNote(note)"
                  >
                    编辑
                  </el-button>
                  <el-button
                    type="text"
                    size="small"
                    @click.stop="deleteNote(note)"
                  >
                    删除
                  </el-button>
                </div>
              </div>
              <div class="note-meta">
                <span class="note-folder">{{ note.folder }}</span>
                <span class="note-time">{{ formatTime(note.updated_at) }}</span>
              </div>
              <div class="note-preview">
                {{ getPreview(note.content) }}
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 新建/编辑笔记对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingNote ? '编辑笔记' : '新建笔记'"
      width="680px"
      :close-on-click-modal="false"
      class="note-dialog"
    >
      <div class="dialog-content">
        <el-form :model="noteForm" label-width="90px" class="dialog-form">
          <div class="form-row">
            <el-form-item label="标题" required class="form-item-title">
              <el-input 
                v-model="noteForm.title" 
                placeholder="请输入笔记标题"
                size="large"
                clearable
              />
            </el-form-item>
            <el-form-item label="文件夹" class="form-item-folder">
              <el-input 
                v-model="noteForm.folder" 
                placeholder="默认文件夹"
                size="large"
                clearable
              />
            </el-form-item>
          </div>
          <el-form-item label="内容" class="content-item">
            <div class="editor-wrapper">
              <MarkdownEditor v-model="noteForm.content" />
            </div>
          </el-form-item>
        </el-form>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showCreateDialog = false" size="large">取消</el-button>
          <el-button type="primary" @click="saveNote" :loading="saving" size="large">
            <el-icon v-if="!saving"><DocumentAdd /></el-icon>
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { DocumentAdd } from '@element-plus/icons-vue'
import SidebarNav from '@/components/SidebarNav.vue'
import MarkdownEditor from '@/components/MarkdownEditor.vue'
import request from '@/utils/request'

export default {
  name: 'NotesPage',
  components: {
    SidebarNav,
    MarkdownEditor
  },
  setup() {
    const notes = ref([])
    const showCreateDialog = ref(false)
    const editingNote = ref(null)
    const saving = ref(false)
    
    const noteForm = reactive({
      title: '',
      folder: '默认文件夹',
      content: ''
    })
    
    const loadNotes = async () => {
      try {
        const response = await request.get('/notes')
        notes.value = response.notes || []
      } catch (error) {
        console.error('加载笔记失败:', error)
      }
    }
    
    const selectNote = (note) => {
      // 这里可以实现笔记详情查看
      console.log('选中笔记:', note)
    }
    
    const editNote = (note) => {
      editingNote.value = note
      noteForm.title = note.title
      noteForm.folder = note.folder
      noteForm.content = note.content
      showCreateDialog.value = true
    }
    
    const deleteNote = async (note) => {
      try {
        await ElMessageBox.confirm(`确定要删除笔记"${note.title}"吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await request.delete(`/notes/${note.id}`)
        ElMessage.success('删除成功')
        loadNotes()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除笔记失败:', error)
        }
      }
    }
    
    const saveNote = async () => {
      if (!noteForm.title.trim()) {
        ElMessage.warning('请输入笔记标题')
        return
      }
      
      try {
        saving.value = true
        
        if (editingNote.value) {
          // 编辑笔记
          await request.put(`/notes/${editingNote.value.id}`, noteForm)
          ElMessage.success('更新成功')
        } else {
          // 新建笔记
          await request.post('/notes', noteForm)
          ElMessage.success('创建成功')
        }
        
        showCreateDialog.value = false
        resetForm()
        loadNotes()
      } catch (error) {
        console.error('保存笔记失败:', error)
      } finally {
        saving.value = false
      }
    }
    
    const resetForm = () => {
      editingNote.value = null
      noteForm.title = ''
      noteForm.folder = '默认文件夹'
      noteForm.content = ''
    }
    
    const formatTime = (timeStr) => {
      const date = new Date(timeStr)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    }
    
    const getPreview = (content) => {
      if (!content) return '暂无内容'
      return content.length > 100 ? content.substring(0, 100) + '...' : content
    }
    
    onMounted(() => {
      loadNotes()
    })
    
    return {
      notes,
      showCreateDialog,
      editingNote,
      saving,
      noteForm,
      selectNote,
      editNote,
      deleteNote,
      saveNote,
      formatTime,
      getPreview
    }
  }
}
</script>

<style scoped>
.notes-container {
  display: flex;
  height: 100vh;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.content-header h1 {
  color: #303133;
  font-size: 24px;
  margin: 0;
}

.notes-content {
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.note-card {
  margin-bottom: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.note-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.note-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.note-header h3 {
  margin: 0;
  color: #303133;
  font-size: 16px;
}

.note-actions {
  display: flex;
  gap: 5px;
}

.note-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-size: 12px;
  color: #909399;
}

.note-folder {
  background: #f0f9ff;
  color: #0369a1;
  padding: 2px 8px;
  border-radius: 4px;
}

.note-preview {
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

/* 对话框样式优化 */
:deep(.note-dialog .el-dialog) {
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

:deep(.note-dialog .el-dialog__header) {
  padding: 24px 24px 16px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.note-dialog .el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.dialog-content {
  padding: 24px;
}

.dialog-form {
  margin: 0;
}

.dialog-form .el-form-item {
  margin-bottom: 20px;
}

.dialog-form .el-form-item__label {
  font-weight: 500;
  color: #606266;
  line-height: 32px;
}

.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.form-item-title {
  flex: 2;
}

.form-item-folder {
  flex: 1;
}

.content-item {
  margin-bottom: 0;
}

.content-item .el-form-item__label {
  align-self: flex-start;
  padding-top: 8px;
}

.editor-wrapper {
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s;
}

.editor-wrapper:hover {
  border-color: #c0c4cc;
}

.editor-wrapper:focus-within {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.dialog-form .el-input__wrapper {
  border-radius: 8px;
  box-shadow: 0 0 0 1px #dcdfe6;
  transition: all 0.3s;
}

.dialog-form .el-input__wrapper:hover {
  box-shadow: 0 0 0 1px #c0c4cc;
}

.dialog-form .el-input__wrapper.is-focus {
  box-shadow: 0 0 0 1px #409eff;
}

.dialog-footer {
  padding: 16px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid #f0f0f0;
}

.dialog-footer .el-button {
  min-width: 80px;
  border-radius: 8px;
  font-weight: 500;
}

.dialog-footer .el-button--primary {
  background: linear-gradient(135deg, #409eff 0%, #3a8ee6 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.dialog-footer .el-button--primary:hover {
  background: linear-gradient(135deg, #3a8ee6 0%, #337ecc 100%);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.4);
}
</style>