<template>
  <div class="settings-container">
    <SidebarNav />
    <div class="main-content">
      <div class="content-header">
        <h1>{{ t('settings.title') }}</h1>
        <div class="header-actions">
          <ThemeToggle />
        </div>
      </div>
      
      <div class="settings-content">
        <el-tabs v-model="activeTab" class="settings-tabs">
          <!-- 个人信息 -->
          <el-tab-pane :label="t('settings.profile')" name="profile">
            <div class="settings-section">
              <h3>{{ t('settings.profile') }}</h3>
              <el-form :model="userForm" label-width="100px">
                <el-form-item :label="t('settings.username')">
                  <el-input v-model="userForm.username" disabled />
                </el-form-item>
                <el-form-item :label="t('settings.email')">
                  <el-input v-model="userForm.email" disabled />
                </el-form-item>
                <el-form-item :label="t('settings.registerTime')">
                  <el-input :value="formatTime(userForm.created_at)" disabled />
                </el-form-item>
              </el-form>
            </div>
          </el-tab-pane>
          
          <!-- 主题设置 -->
          <el-tab-pane :label="t('settings.theme')" name="theme">
            <div class="settings-section">
              <h3>{{ t('settings.theme') }}</h3>
              <div class="theme-options">
                <div class="theme-option" @click="setTheme('light')">
                  <div class="theme-preview light-theme" :class="{ active: currentTheme === 'light' }">
                    <div class="theme-header"></div>
                    <div class="theme-content">
                      <div class="theme-sidebar"></div>
                      <div class="theme-main"></div>
                    </div>
                  </div>
                  <p>{{ t('settings.lightTheme') }}</p>
                </div>
                
                <div class="theme-option" @click="setTheme('dark')">
                  <div class="theme-preview dark-theme" :class="{ active: currentTheme === 'dark' }">
                    <div class="theme-header"></div>
                    <div class="theme-content">
                      <div class="theme-sidebar"></div>
                      <div class="theme-main"></div>
                    </div>
                  </div>
                  <p>{{ t('settings.darkTheme') }}</p>
                </div>
              </div>
            </div>
          </el-tab-pane>
          
          <!-- 语言设置 -->
          <el-tab-pane :label="t('settings.language')" name="language">
            <div class="settings-section">
              <h3>{{ t('settings.language') }}</h3>
              <div class="language-options">
                <div 
                  class="language-option" 
                  v-for="lang in languages" 
                  :key="lang.code"
                  @click="setLanguage(lang.code)"
                  :class="{ active: currentLanguage === lang.code }"
                >
                  <div class="language-flag">{{ lang.flag }}</div>
                  <div class="language-info">
                    <h4>{{ lang.name }}</h4>
                    <p>{{ lang.nativeName }}</p>
                  </div>
                  <div class="language-check" v-if="currentLanguage === lang.code">
                    <el-icon><Check /></el-icon>
                  </div>
                </div>
              </div>
              <div class="language-note">
                <el-alert
                  :title="t('settings.languageSwitch')"
                  :description="t('settings.languageSwitchDesc')"
                  type="info"
                  :closable="false"
                  show-icon>
                </el-alert>
              </div>
            </div>
          </el-tab-pane>
          
          <!-- API 配置 -->
          <el-tab-pane :label="t('settings.api')" name="api">
            <div class="settings-section">
              <h3>AI 服务配置</h3>
              <div class="api-config">
                <el-form :model="apiForm" label-width="120px" class="api-form">
                  <el-form-item label="OpenRouter API">
                    <div class="api-input-group">
                      <el-input 
                        v-model="apiForm.openrouterKey" 
                        :type="showApiKey ? 'text' : 'password'"
                        placeholder="请输入 OpenRouter API Key"
                        class="api-key-input"
                      >
                        <template #append>
                          <el-button 
                            @click="showApiKey = !showApiKey"
                            :icon="showApiKey ? 'Hide' : 'View'"
                          >
                            {{ showApiKey ? '隐藏' : '显示' }}
                          </el-button>
                        </template>
                      </el-input>
                    </div>
                    <div class="api-help">
                      <p>
                        <el-icon><InfoFilled /></el-icon>
                        获取 API Key: 
                        <el-link href="https://openrouter.ai/keys" target="_blank" type="primary">
                          访问 OpenRouter 官网
                        </el-link>
                      </p>
                    </div>
                  </el-form-item>
                  
                  <el-form-item label="默认模型">
                    <el-select v-model="apiForm.defaultModel" placeholder="选择默认AI模型" filterable>
                      <!-- OpenAI 模型 -->
                      <el-option-group label="OpenAI">
                        <el-option label="GPT-4o (最新)" value="openai/gpt-4o" />
                        <el-option label="GPT-4o Mini (快速)" value="openai/gpt-4o-mini" />
                        <el-option label="GPT-4 Turbo" value="openai/gpt-4-turbo" />
                        <el-option label="GPT-4" value="openai/gpt-4" />
                        <el-option label="GPT-3.5 Turbo" value="openai/gpt-3.5-turbo" />
                      </el-option-group>
                      
                      <!-- Anthropic Claude 模型 -->
                      <el-option-group label="Anthropic Claude">
                        <el-option label="Claude 3.5 Sonnet (最新)" value="anthropic/claude-3.5-sonnet" />
                        <el-option label="Claude 3 Opus (最强)" value="anthropic/claude-3-opus" />
                        <el-option label="Claude 3 Sonnet" value="anthropic/claude-3-sonnet" />
                        <el-option label="Claude 3 Haiku (快速)" value="anthropic/claude-3-haiku" />
                      </el-option-group>
                      
                      <!-- Google 模型 -->
                      <el-option-group label="Google">
                        <el-option label="Gemini Pro 1.5" value="google/gemini-pro-1.5" />
                        <el-option label="Gemini Pro" value="google/gemini-pro" />
                        <el-option label="Gemini Flash" value="google/gemini-flash-1.5" />
                      </el-option-group>
                      
                      <!-- Meta 模型 -->
                      <el-option-group label="Meta">
                        <el-option label="Llama 3.1 405B (最大)" value="meta-llama/llama-3.1-405b-instruct" />
                        <el-option label="Llama 3.1 70B" value="meta-llama/llama-3.1-70b-instruct" />
                        <el-option label="Llama 3.1 8B (快速)" value="meta-llama/llama-3.1-8b-instruct" />
                      </el-option-group>
                      
                      <!-- Mistral 模型 -->
                      <el-option-group label="Mistral">
                        <el-option label="Mistral Large 2" value="mistralai/mistral-large-2407" />
                        <el-option label="Mistral Nemo" value="mistralai/mistral-nemo" />
                        <el-option label="Codestral (代码)" value="mistralai/codestral-mamba" />
                      </el-option-group>
                      
                      <!-- 其他模型 -->
                      <el-option-group label="其他">
                        <el-option label="Perplexity Sonar" value="perplexity/llama-3.1-sonar-large-128k-online" />
                        <el-option label="Cohere Command R+" value="cohere/command-r-plus" />
                        <el-option label="DeepSeek Coder V2" value="deepseek/deepseek-coder" />
                      </el-option-group>
                    </el-select>
                  </el-form-item>
                  
                  <el-form-item label="API 状态">
                    <div class="api-status">
                      <el-tag :type="apiStatus.type" size="large">
                        <el-icon>
                          <component :is="apiStatus.icon" />
                        </el-icon>
                        {{ apiStatus.text }}
                      </el-tag>
                      <el-button 
                        @click="testApiConnection" 
                        :loading="testing"
                        type="primary"
                        size="small"
                        style="margin-left: 12px;"
                      >
                        测试连接
                      </el-button>
                    </div>
                  </el-form-item>
                  
                  <el-form-item>
                    <el-button type="primary" @click="saveApiConfig" :loading="saving">
                      保存配置
                    </el-button>
                    <el-button @click="resetApiConfig">重置</el-button>
                  </el-form-item>
                </el-form>
                
                <div class="api-usage">
                  <h4>使用说明</h4>
                  <ul>
                    <li>OpenRouter 提供多种 AI 模型的统一接口</li>
                    <li>配置 API Key 后即可在 AI 对话页面使用真实的 AI 服务</li>
                    <li>支持 GPT-4、Claude、Gemini 等主流模型</li>
                    <li>API Key 将安全存储在本地，不会上传到服务器</li>
                  </ul>
                </div>
              </div>
            </div>
          </el-tab-pane>
          
          <!-- 数据管理 -->
          <el-tab-pane label="数据管理" name="data">
            <DataBackup />
          </el-tab-pane>
          
          <!-- 关于 -->
          <el-tab-pane label="关于" name="about">
            <div class="settings-section">
              <h3>关于智能笔记本</h3>
              <div class="about-content">
                <div class="app-info">
                  <h4>智能笔记本</h4>
                  <p>版本: 1.0.0</p>
                  <p>一个集成笔记管理、任务管理、专注计时等功能的个人生产力平台。</p>
                </div>
                
                <div class="features-list">
                  <h4>主要功能</h4>
                  <ul>
                    <li>📝 笔记管理 - 支持Markdown语法</li>
                    <li>✅ 任务管理 - 项目分组、优先级设置</li>
                    <li>⏰ 专注计时 - 番茄工作法</li>
                    <li>📊 数据分析 - 可视化图表</li>
                    <li>🌤️ 天气信息 - 实时天气显示</li>
                    <li>💾 数据备份 - 导入导出功能</li>
                    <li>🎨 主题切换 - 浅色/深色主题</li>
                  </ul>
                </div>
                
                <div class="tech-stack">
                  <h4>技术栈</h4>
                  <p><strong>前端:</strong> Vue.js 3, Element Plus, ECharts</p>
                  <p><strong>后端:</strong> Python Flask, SQLAlchemy, SQLite</p>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { InfoFilled, SuccessFilled, WarningFilled, CircleCloseFilled, Check } from '@element-plus/icons-vue'
import SidebarNav from '@/components/SidebarNav.vue'
import ThemeToggle from '@/components/ThemeToggle.vue'
import DataBackup from '@/components/DataBackup.vue'
import request from '@/utils/request'
import { getUser } from '@/utils/auth'
import openRouterService from '@/services/openrouter'

export default {
  name: 'SettingsPage',
  components: {
    SidebarNav,
    ThemeToggle,
    DataBackup,
    InfoFilled,
    SuccessFilled,
    WarningFilled,
    CircleCloseFilled,
    Check
  },
  setup() {
    const { t, locale } = useI18n()
    const activeTab = ref('profile')
    const currentTheme = ref('light')
    const currentLanguage = ref(locale.value)
    
    const userForm = reactive({
      username: '',
      email: '',
      created_at: ''
    })
    
    // 支持的语言列表
    const languages = ref([
      {
        code: 'zh-CN',
        name: t('languages.zh-CN'),
        nativeName: 'Simplified Chinese',
        flag: '🇨🇳'
      },
      {
        code: 'en-US',
        name: t('languages.en-US'),
        nativeName: 'English',
        flag: '🇺🇸'
      },
      {
        code: 'ko-KR',
        name: t('languages.ko-KR'),
        nativeName: 'Korean',
        flag: '🇰🇷'
      },
      {
        code: 'ja-JP',
        name: t('languages.ja-JP'),
        nativeName: 'Japanese',
        flag: '🇯🇵'
      },
      {
        code: 'fr-FR',
        name: t('languages.fr-FR'),
        nativeName: 'French',
        flag: '🇫🇷'
      }
    ])
    
    // API 配置相关
    const showApiKey = ref(false)
    const testing = ref(false)
    const saving = ref(false)
    
    const apiForm = reactive({
      openrouterKey: '',
      defaultModel: 'openai/gpt-3.5-turbo'
    })
    
    const apiStatus = ref({
      type: 'info',
      icon: 'InfoFilled',
      text: '未配置'
    })
    
    const loadUserInfo = () => {
      const user = getUser()
      if (user) {
        userForm.username = user.username
        userForm.email = user.email
        userForm.created_at = user.created_at
      }
    }
    
    const setTheme = (theme) => {
      currentTheme.value = theme
      localStorage.setItem('theme', theme)
      
      // 这里可以实现主题切换逻辑
      if (theme === 'dark') {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
      
      const themeText = theme === 'light' ? t('settings.lightTheme') : t('settings.darkTheme')
      ElMessage.success(t('settings.themeChanged', { theme: themeText }))
    }
    
    const setLanguage = (langCode) => {
      currentLanguage.value = langCode
      locale.value = langCode
      localStorage.setItem('locale', langCode)
      
      const selectedLang = languages.value.find(lang => lang.code === langCode)
      ElMessage.success(t('settings.languageChanged', { language: selectedLang?.name }))
    }
    
    const formatTime = (timeStr) => {
      if (!timeStr) return ''
      const date = new Date(timeStr)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    }
    
    // API 配置方法
    const loadApiConfig = () => {
      const config = openRouterService.loadConfig()
      if (config) {
        apiForm.openrouterKey = config.apiKey || ''
        apiForm.defaultModel = config.defaultModel || 'openai/gpt-3.5-turbo'
        
        if (apiForm.openrouterKey) {
          apiStatus.value = {
            type: 'success',
            icon: 'SuccessFilled',
            text: '已配置'
          }
        }
      }
    }
    
    const saveApiConfig = () => {
      if (!apiForm.openrouterKey.trim()) {
        ElMessage.warning('请输入 OpenRouter API Key')
        return
      }
      
      saving.value = true
      
      const config = {
        apiKey: apiForm.openrouterKey.trim(),
        defaultModel: apiForm.defaultModel
      }
      
      // 使用 OpenRouter 服务保存配置
      openRouterService.saveConfig(config)
      
      setTimeout(() => {
        saving.value = false
        apiStatus.value = {
          type: 'success',
          icon: 'SuccessFilled',
          text: '已配置'
        }
        ElMessage.success('API 配置已保存')
      }, 1000)
    }
    
    const resetApiConfig = () => {
      apiForm.openrouterKey = ''
      apiForm.defaultModel = 'openai/gpt-3.5-turbo'
      openRouterService.clearConfig()
      apiStatus.value = {
        type: 'info',
        icon: 'InfoFilled',
        text: '未配置'
      }
      ElMessage.success('配置已重置')
    }
    
    const testApiConnection = async () => {
      if (!apiForm.openrouterKey.trim()) {
        ElMessage.warning('请先输入 API Key')
        return
      }
      
      testing.value = true
      
      try {
        // 临时保存配置用于测试
        const tempConfig = {
          apiKey: apiForm.openrouterKey.trim(),
          defaultModel: apiForm.defaultModel
        }
        openRouterService.saveConfig(tempConfig)
        
        // 使用 OpenRouter 服务测试连接
        const success = await openRouterService.testConnection()
        
        if (success) {
          apiStatus.value = {
            type: 'success',
            icon: 'SuccessFilled',
            text: '连接正常'
          }
          ElMessage.success('API 连接测试成功')
        } else {
          throw new Error('API 连接失败')
        }
      } catch (error) {
        apiStatus.value = {
          type: 'danger',
          icon: 'CircleCloseFilled',
          text: '连接失败'
        }
        ElMessage.error('API 连接测试失败，请检查 API Key 是否正确')
      } finally {
        testing.value = false
      }
    }
    
    onMounted(() => {
      loadUserInfo()
      loadApiConfig()
      
      // 加载保存的主题设置
      const savedTheme = localStorage.getItem('theme') || 'light'
      setTheme(savedTheme)
      
      // 加载保存的语言设置
      const savedLanguage = localStorage.getItem('locale') || 'zh-CN'
      currentLanguage.value = savedLanguage
      locale.value = savedLanguage
    })
    
    return {
      t,
      activeTab,
      currentTheme,
      currentLanguage,
      languages,
      userForm,
      setTheme,
      setLanguage,
      formatTime,
      // API 配置相关
      showApiKey,
      testing,
      saving,
      apiForm,
      apiStatus,
      saveApiConfig,
      resetApiConfig,
      testApiConnection
    }
  }
}
</script>

<style scoped>
.settings-container {
  display: flex;
  height: 100vh;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.content-header {
  margin-bottom: 20px;
}

.content-header h1 {
  color: #303133;
  font-size: 24px;
  margin: 0;
}

.settings-content {
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.settings-tabs {
  min-height: 500px;
}

.settings-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.settings-section:last-child {
  border-bottom: none;
}

.settings-section h3 {
  color: #303133;
  font-size: 18px;
  margin-bottom: 15px;
}

.section-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 15px;
  line-height: 1.5;
}

.theme-options {
  display: flex;
  gap: 20px;
}

.theme-option {
  cursor: pointer;
  text-align: center;
}

.theme-preview {
  width: 120px;
  height: 80px;
  border: 2px solid #dcdfe6;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s;
  margin-bottom: 10px;
}

.theme-preview.active {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.light-theme {
  background: #ffffff;
}

.light-theme .theme-header {
  height: 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

.light-theme .theme-content {
  display: flex;
  height: 59px;
}

.light-theme .theme-sidebar {
  width: 30px;
  background: #f0f2f5;
  border-right: 1px solid #ebeef5;
}

.light-theme .theme-main {
  flex: 1;
  background: #ffffff;
}

.dark-theme {
  background: #2c3e50;
}

.dark-theme .theme-header {
  height: 20px;
  background: #34495e;
  border-bottom: 1px solid #4a5568;
}

.dark-theme .theme-content {
  display: flex;
  height: 59px;
}

.dark-theme .theme-sidebar {
  width: 30px;
  background: #34495e;
  border-right: 1px solid #4a5568;
}

.dark-theme .theme-main {
  flex: 1;
  background: #2c3e50;
}

.file-info {
  margin-top: 10px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 4px;
}

.file-info p {
  margin: 0 0 10px 0;
  color: #606266;
  font-size: 14px;
}

.about-content {
  max-width: 600px;
}

.app-info h4,
.features-list h4,
.tech-stack h4 {
  color: #303133;
  font-size: 16px;
  margin-bottom: 10px;
}

.app-info p,
.tech-stack p {
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
  margin: 5px 0;
}

.features-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.features-list li {
  color: #606266;
  font-size: 14px;
  line-height: 1.8;
  padding: 2px 0;
}

.app-info,
.features-list,
.tech-stack {
  margin-bottom: 25px;
}

/* 语言设置样式 */
.language-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.language-option {
  display: flex;
  align-items: center;
  padding: 16px;
  border: 2px solid #ebeef5;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #ffffff;
}

.language-option:hover {
  border-color: #409eff;
  background: #f0f9ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.15);
}

.language-option.active {
  border-color: #409eff;
  background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.2);
}

.language-flag {
  font-size: 32px;
  margin-right: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #f5f7fa;
}

.language-option.active .language-flag {
  background: rgba(64, 158, 255, 0.1);
}

.language-info {
  flex: 1;
}

.language-info h4 {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.language-info p {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.language-check {
  color: #409eff;
  font-size: 20px;
  margin-left: 12px;
}

.language-note {
  margin-top: 20px;
}

.language-note .el-alert {
  border-radius: 8px;
}
</style>