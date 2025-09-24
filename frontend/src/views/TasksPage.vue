<template>
  <div class="tasks-container">
    <SidebarNav />
    <div class="main-content">
      <div class="content-header">
        <h1>任务管理</h1>
        <div class="header-actions">
          <el-button @click="showProjectDialog = true">
            <el-icon><FolderAdd /></el-icon>
            新建项目
          </el-button>
          <el-button type="primary" @click="showTaskDialog = true">
            <el-icon><Plus /></el-icon>
            新建任务
          </el-button>
        </div>
      </div>
      
      <div class="tasks-content">
        <!-- 项目列表 -->
        <div class="projects-section">
          <h2>项目</h2>
          <div class="projects-grid">
            <el-card
              v-for="project in projects"
              :key="project.id"
              class="project-card"
              @click="selectProject(project)"
            >
              <div class="project-header">
                <h3>{{ project.name }}</h3>
                <el-dropdown @command="handleProjectAction">
                  <el-button type="text" size="small">
                    <el-icon><MoreFilled /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item :command="{action: 'edit', project}">编辑</el-dropdown-item>
                      <el-dropdown-item :command="{action: 'delete', project}">删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
              <p class="project-description">{{ project.description || '暂无描述' }}</p>
              <div class="project-stats">
                <span>任务: {{ getProjectTaskCount(project.id) }}</span>
                <span>完成: {{ getProjectCompletedCount(project.id) }}</span>
              </div>
            </el-card>
          </div>
        </div>
        
        <!-- 任务列表 -->
        <div class="tasks-section">
          <div class="tasks-header">
            <h2>任务</h2>
            <el-select v-model="selectedProjectId" placeholder="筛选项目" clearable>
              <el-option label="全部项目" value="" />
              <el-option
                v-for="project in projects"
                :key="project.id"
                :label="project.name"
                :value="project.id"
              />
            </el-select>
          </div>
          
          <div v-if="filteredTasks.length === 0" class="empty-state">
            <el-empty description="暂无任务，点击新建任务开始管理" />
          </div>
          
          <div v-else class="tasks-list">
            <el-card
              v-for="task in filteredTasks"
              :key="task.id"
              class="task-card"
              :class="{ completed: task.status === 'completed' }"
            >
              <div class="task-content">
                <div class="task-main">
                  <el-checkbox
                    :model-value="task.status === 'completed'"
                    @change="toggleTaskStatus(task)"
                  />
                  <div class="task-info">
                    <h3 :class="{ 'task-completed': task.status === 'completed' }">
                      {{ task.title }}
                    </h3>
                    <p class="task-description">{{ task.description || '暂无描述' }}</p>
                    <div class="task-meta">
                      <el-tag
                        :type="getPriorityType(task.priority)"
                        size="small"
                      >
                        {{ getPriorityText(task.priority) }}
                      </el-tag>
                      <span v-if="task.due_date" class="due-date">
                        截止: {{ formatDate(task.due_date) }}
                      </span>
                      <span v-if="task.project_name" class="project-name">
                        项目: {{ task.project_name }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="task-actions">
                  <el-button type="text" size="small" @click="editTask(task)">
                    编辑
                  </el-button>
                  <el-button type="text" size="small" @click="deleteTask(task)">
                    删除
                  </el-button>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 新建/编辑项目对话框 -->
    <el-dialog
      v-model="showProjectDialog"
      :title="editingProject ? '编辑项目' : '新建项目'"
      width="480px"
      :close-on-click-modal="false"
      class="project-dialog"
    >
      <div class="dialog-content">
        <el-form :model="projectForm" label-width="90px" class="dialog-form">
          <el-form-item label="项目名称" required>
            <el-input 
              v-model="projectForm.name" 
              placeholder="请输入项目名称"
              size="large"
              clearable
            />
          </el-form-item>
          <el-form-item label="项目描述">
            <el-input
              v-model="projectForm.description"
              type="textarea"
              :rows="4"
              placeholder="请输入项目描述"
              resize="none"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>
        </el-form>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showProjectDialog = false" size="large">取消</el-button>
          <el-button type="primary" @click="saveProject" :loading="saving" size="large">
            <el-icon v-if="!saving"><Check /></el-icon>
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 新建/编辑任务对话框 -->
    <el-dialog
      v-model="showTaskDialog"
      :title="editingTask ? '编辑任务' : '新建任务'"
      width="520px"
      :close-on-click-modal="false"
      class="task-dialog"
    >
      <div class="dialog-content">
        <el-form :model="taskForm" label-width="90px" class="dialog-form">
          <el-form-item label="任务标题" required>
            <el-input 
              v-model="taskForm.title" 
              placeholder="请输入任务标题"
              size="large"
              clearable
            />
          </el-form-item>
          <el-form-item label="任务描述">
            <el-input
              v-model="taskForm.description"
              type="textarea"
              :rows="3"
              placeholder="请输入任务描述"
              resize="none"
              maxlength="300"
              show-word-limit
            />
          </el-form-item>
          <div class="form-row">
            <el-form-item label="所属项目" class="form-item-half">
              <el-select v-model="taskForm.project_id" placeholder="选择项目" clearable size="large">
                <el-option label="无项目" :value="null" />
                <el-option
                  v-for="project in projects"
                  :key="project.id"
                  :label="project.name"
                  :value="project.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="优先级" class="form-item-half">
              <el-select v-model="taskForm.priority" placeholder="选择优先级" size="large">
                <el-option label="低" value="low">
                  <span style="color: #67c23a;">🟢 低</span>
                </el-option>
                <el-option label="中" value="medium">
                  <span style="color: #e6a23c;">🟡 中</span>
                </el-option>
                <el-option label="高" value="high">
                  <span style="color: #f56c6c;">🔴 高</span>
                </el-option>
              </el-select>
            </el-form-item>
          </div>
          <el-form-item label="截止日期">
            <el-date-picker
              v-model="taskForm.due_date"
              type="date"
              placeholder="选择截止日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              size="large"
              style="width: 100%;"
            />
          </el-form-item>
        </el-form>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showTaskDialog = false" size="large">取消</el-button>
          <el-button type="primary" @click="saveTask" :loading="saving" size="large">
            <el-icon v-if="!saving"><Check /></el-icon>
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Check } from '@element-plus/icons-vue'
import SidebarNav from '@/components/SidebarNav.vue'
import request from '@/utils/request'

export default {
  name: 'TasksPage',
  components: {
    SidebarNav
  },
  setup() {
    const projects = ref([])
    const tasks = ref([])
    const selectedProjectId = ref('')
    const showProjectDialog = ref(false)
    const showTaskDialog = ref(false)
    const editingProject = ref(null)
    const editingTask = ref(null)
    const saving = ref(false)
    
    const projectForm = reactive({
      name: '',
      description: ''
    })
    
    const taskForm = reactive({
      title: '',
      description: '',
      project_id: null,
      priority: 'medium',
      due_date: null
    })
    
    const filteredTasks = computed(() => {
      if (!selectedProjectId.value) return tasks.value
      return tasks.value.filter(task => task.project_id === selectedProjectId.value)
    })
    
    const loadProjects = async () => {
      try {
        const response = await request.get('/projects')
        projects.value = response.projects || []
      } catch (error) {
        console.error('加载项目失败:', error)
      }
    }
    
    const loadTasks = async () => {
      try {
        const response = await request.get('/tasks')
        tasks.value = response.tasks || []
      } catch (error) {
        console.error('加载任务失败:', error)
      }
    }
    
    const selectProject = (project) => {
      selectedProjectId.value = project.id
    }
    
    const handleProjectAction = async ({ action, project }) => {
      if (action === 'edit') {
        editProject(project)
      } else if (action === 'delete') {
        await deleteProject(project)
      }
    }
    
    const editProject = (project) => {
      editingProject.value = project
      projectForm.name = project.name
      projectForm.description = project.description
      showProjectDialog.value = true
    }
    
    const deleteProject = async (project) => {
      try {
        await ElMessageBox.confirm(`确定要删除项目"${project.name}"吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await request.delete(`/projects/${project.id}`)
        ElMessage.success('删除成功')
        loadProjects()
        loadTasks()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除项目失败:', error)
        }
      }
    }
    
    const saveProject = async () => {
      if (!projectForm.name.trim()) {
        ElMessage.warning('请输入项目名称')
        return
      }
      
      try {
        saving.value = true
        
        if (editingProject.value) {
          await request.put(`/projects/${editingProject.value.id}`, projectForm)
          ElMessage.success('更新成功')
        } else {
          await request.post('/projects', projectForm)
          ElMessage.success('创建成功')
        }
        
        showProjectDialog.value = false
        resetProjectForm()
        loadProjects()
      } catch (error) {
        console.error('保存项目失败:', error)
      } finally {
        saving.value = false
      }
    }
    
    const editTask = (task) => {
      editingTask.value = task
      taskForm.title = task.title
      taskForm.description = task.description
      taskForm.project_id = task.project_id
      taskForm.priority = task.priority
      taskForm.due_date = task.due_date
      showTaskDialog.value = true
    }
    
    const deleteTask = async (task) => {
      try {
        await ElMessageBox.confirm(`确定要删除任务"${task.title}"吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await request.delete(`/tasks/${task.id}`)
        ElMessage.success('删除成功')
        loadTasks()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除任务失败:', error)
        }
      }
    }
    
    const saveTask = async () => {
      if (!taskForm.title.trim()) {
        ElMessage.warning('请输入任务标题')
        return
      }
      
      try {
        saving.value = true
        
        if (editingTask.value) {
          await request.put(`/tasks/${editingTask.value.id}`, taskForm)
          ElMessage.success('更新成功')
        } else {
          await request.post('/tasks', taskForm)
          ElMessage.success('创建成功')
        }
        
        showTaskDialog.value = false
        resetTaskForm()
        loadTasks()
      } catch (error) {
        console.error('保存任务失败:', error)
      } finally {
        saving.value = false
      }
    }
    
    const toggleTaskStatus = async (task) => {
      try {
        const newStatus = task.status === 'completed' ? 'pending' : 'completed'
        await request.put(`/tasks/${task.id}`, { status: newStatus })
        task.status = newStatus
        ElMessage.success(newStatus === 'completed' ? '任务已完成' : '任务已重新开启')
      } catch (error) {
        console.error('更新任务状态失败:', error)
      }
    }
    
    const resetProjectForm = () => {
      editingProject.value = null
      projectForm.name = ''
      projectForm.description = ''
    }
    
    const resetTaskForm = () => {
      editingTask.value = null
      taskForm.title = ''
      taskForm.description = ''
      taskForm.project_id = null
      taskForm.priority = 'medium'
      taskForm.due_date = null
    }
    
    const getProjectTaskCount = (projectId) => {
      return tasks.value.filter(task => task.project_id === projectId).length
    }
    
    const getProjectCompletedCount = (projectId) => {
      return tasks.value.filter(task => 
        task.project_id === projectId && task.status === 'completed'
      ).length
    }
    
    const getPriorityType = (priority) => {
      const types = {
        low: '',
        medium: 'warning',
        high: 'danger'
      }
      return types[priority] || ''
    }
    
    const getPriorityText = (priority) => {
      const texts = {
        low: '低',
        medium: '中',
        high: '高'
      }
      return texts[priority] || priority
    }
    
    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString()
    }
    
    onMounted(() => {
      loadProjects()
      loadTasks()
    })
    
    return {
      projects,
      tasks,
      selectedProjectId,
      filteredTasks,
      showProjectDialog,
      showTaskDialog,
      editingProject,
      editingTask,
      saving,
      projectForm,
      taskForm,
      selectProject,
      handleProjectAction,
      editProject,
      deleteProject,
      saveProject,
      editTask,
      deleteTask,
      saveTask,
      toggleTaskStatus,
      getProjectTaskCount,
      getProjectCompletedCount,
      getPriorityType,
      getPriorityText,
      formatDate
    }
  }
}
</script>

<style scoped>
.tasks-container {
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

.header-actions {
  display: flex;
  gap: 10px;
}

.tasks-content {
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.projects-section {
  margin-bottom: 30px;
}

.projects-section h2 {
  color: #303133;
  font-size: 18px;
  margin-bottom: 15px;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.project-card {
  cursor: pointer;
  transition: all 0.3s;
}

.project-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.project-header h3 {
  margin: 0;
  color: #303133;
  font-size: 16px;
}

.project-description {
  color: #606266;
  font-size: 14px;
  margin: 10px 0;
  line-height: 1.5;
}

.project-stats {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #909399;
}

.tasks-section h2 {
  color: #303133;
  font-size: 18px;
  margin-bottom: 15px;
}

.tasks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.task-card {
  margin-bottom: 15px;
  transition: all 0.3s;
}

.task-card.completed {
  opacity: 0.7;
}

.task-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.task-main {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  flex: 1;
}

.task-info {
  flex: 1;
}

.task-info h3 {
  margin: 0 0 5px 0;
  color: #303133;
  font-size: 16px;
}

.task-completed {
  text-decoration: line-through;
  color: #909399 !important;
}

.task-description {
  color: #606266;
  font-size: 14px;
  margin: 5px 0 10px 0;
  line-height: 1.5;
}

.task-meta {
  display: flex;
  gap: 10px;
  align-items: center;
  font-size: 12px;
}

.due-date, .project-name {
  color: #909399;
}

.task-actions {
  display: flex;
  gap: 5px;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

/* 对话框样式优化 */
:deep(.project-dialog .el-dialog),
:deep(.task-dialog .el-dialog) {
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

:deep(.project-dialog .el-dialog__header),
:deep(.task-dialog .el-dialog__header) {
  padding: 24px 24px 16px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.project-dialog .el-dialog__title),
:deep(.task-dialog .el-dialog__title) {
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

.dialog-form .el-textarea__inner {
  border-radius: 8px;
  border: 1px solid #dcdfe6;
  transition: all 0.3s;
}

.dialog-form .el-textarea__inner:hover {
  border-color: #c0c4cc;
}

.dialog-form .el-textarea__inner:focus {
  border-color: #409eff;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-item-half {
  flex: 1;
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

:deep(.el-select-dropdown__item) {
  padding: 8px 12px;
  border-radius: 6px;
  margin: 2px 8px;
}

:deep(.el-select-dropdown__item:hover) {
  background-color: #f5f7fa;
}
</style>