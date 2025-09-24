<template>
  <div class="chat-container">
    <SidebarNav />
    <div class="main-content">
      <div class="content-header">
        <h1>AI 对话</h1>
        <div class="header-actions">
          <el-button @click="clearChat" type="danger" plain>
            <el-icon><Delete /></el-icon>
            清空对话
          </el-button>
          <el-button @click="exportChat" type="primary" plain>
            <el-icon><Download /></el-icon>
            导出对话
          </el-button>
        </div>
      </div>

      <div class="chat-content">
        <!-- 聊天区域 -->
        <div class="chat-area">
          <div class="chat-messages" ref="messagesContainer">
            <!-- 欢迎消息 -->
            <div v-if="messages.length === 0" class="welcome-message">
              <div class="ai-avatar">
                <div class="avatar-icon">🤖</div>
              </div>
              <div class="welcome-content">
                <h3>你好！我是你的AI助手</h3>
                
                <!-- API配置状态 -->
                <div v-if="!isApiConfigured" class="api-status-warning">
                  <el-alert
                    title="需要配置API"
                    type="warning"
                    :closable="false"
                    show-icon
                  >
                    <template #default>
                      <p>请先在设置中配置 OpenRouter API Key 以启用AI对话功能。</p>
                      <el-button type="primary" size="small" @click="$router.push('/settings')">
                        前往设置
                      </el-button>
                    </template>
                  </el-alert>
                </div>
                
                <div v-else class="api-status-success">
                  <el-alert
                    title="AI已就绪"
                    type="success"
                    :closable="false"
                    show-icon
                  >
                    <template #default>
                      <div class="model-info">
                        <div class="model-basic">
                          <strong>{{ currentModelInfo.name }}</strong>
                          <el-tag size="small" type="info">{{ currentModelInfo.provider }}</el-tag>
                        </div>
                        <p class="model-description">{{ currentModelInfo.description }}</p>
                        <div class="model-details">
                          <span class="detail-item">
                            <el-icon><Document /></el-icon>
                            上下文: {{ formatContextLength(currentModelInfo.contextLength) }}
                          </span>
                          <span class="detail-item">
                            <el-icon><Money /></el-icon>
                            输入: ${{ currentModelInfo.pricing.input }}/1M tokens
                          </span>
                          <div class="model-features">
                            <el-tag 
                              v-for="feature in currentModelInfo.features" 
                              :key="feature" 
                              size="small" 
                              effect="plain"
                            >
                              {{ feature }}
                            </el-tag>
                          </div>
                        </div>
                      </div>
                    </template>
                  </el-alert>
                </div>

                <p>我可以帮助你：</p>
                <ul>
                  <li>📝 整理和总结笔记内容</li>
                  <li>📋 制定任务计划和提醒</li>
                  <li>💡 提供创意和建议</li>
                  <li>🔍 回答各种问题</li>
                  <li>📊 分析数据和生成报告</li>
                </ul>
                <p>有什么我可以帮助你的吗？</p>
              </div>
            </div>

            <!-- 对话消息 -->
            <div 
              v-for="message in messages" 
              :key="message.id"
              class="message"
              :class="{ 'user-message': message.type === 'user', 'ai-message': message.type === 'ai' }"
            >
              <div class="message-avatar">
                <div v-if="message.type === 'user'" class="user-avatar">
                  <el-icon><User /></el-icon>
                </div>
                <div v-else class="ai-avatar">
                  <div class="avatar-icon">🤖</div>
                </div>
              </div>
              <div class="message-content">
                <div class="message-bubble">
                  <div class="message-text" v-html="formatMessage(message.content)"></div>
                  <div class="message-time">{{ formatTime(message.timestamp) }}</div>
                </div>
                <div v-if="message.type === 'ai'" class="message-actions">
                  <el-button size="small" text @click="copyMessage(message.content)">
                    <el-icon><CopyDocument /></el-icon>
                    复制
                  </el-button>
                  <el-button size="small" text @click="regenerateResponse(message)">
                    <el-icon><Refresh /></el-icon>
                    重新生成
                  </el-button>
                </div>
              </div>
            </div>

            <!-- 正在输入指示器 -->
            <div v-if="isTyping" class="message ai-message typing-indicator">
              <div class="message-avatar">
                <div class="ai-avatar">
                  <div class="avatar-icon">🤖</div>
                </div>
              </div>
              <div class="message-content">
                <div class="message-bubble">
                  <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="chat-input-area">
            <div class="input-container">
              <el-input
                v-model="inputMessage"
                type="textarea"
                :rows="1"
                :autosize="{ minRows: 1, maxRows: 4 }"
                placeholder="输入你的问题..."
                @keydown.enter.exact="handleSend"
                @keydown.enter.shift.exact.prevent="inputMessage += '\n'"
                :disabled="isTyping"
                class="message-input"
              />
              <div class="input-actions">
                <el-button 
                  type="primary" 
                  @click="handleSend"
                  :disabled="!inputMessage.trim() || isTyping"
                  :loading="isTyping"
                  circle
                >
                  <el-icon><Promotion /></el-icon>
                </el-button>
              </div>
            </div>
            <div class="input-tips">
              <span>按 Enter 发送，Shift + Enter 换行</span>
            </div>
          </div>
        </div>

        <!-- 侧边栏 -->
        <div class="chat-sidebar">
          <!-- 快捷操作 -->
          <div class="sidebar-section">
            <h3>快捷操作</h3>
            <div class="quick-actions">
              <el-button 
                v-for="action in quickActions" 
                :key="action.id"
                @click="sendQuickMessage(action.message)"
                size="small"
                class="quick-action-btn"
              >
                {{ action.label }}
              </el-button>
            </div>
          </div>

          <!-- 对话历史 -->
          <div class="sidebar-section">
            <h3>对话历史</h3>
            <div class="chat-history">
              <div 
                v-for="session in chatSessions" 
                :key="session.id"
                class="history-item"
                :class="{ active: session.id === currentSessionId }"
                @click="loadChatSession(session.id)"
              >
                <div class="history-title">{{ session.title }}</div>
                <div class="history-time">{{ formatDate(session.timestamp) }}</div>
              </div>
              <div v-if="chatSessions.length === 0" class="no-history">
                暂无对话历史
              </div>
            </div>
          </div>

          <!-- AI 设置 -->
          <div class="sidebar-section">
            <h3>AI 设置</h3>
            <div class="ai-settings">
              <div class="setting-item">
                <label>回复风格</label>
                <el-select v-model="aiSettings.style" size="small">
                  <el-option label="专业" value="professional" />
                  <el-option label="友好" value="friendly" />
                  <el-option label="简洁" value="concise" />
                  <el-option label="详细" value="detailed" />
                </el-select>
              </div>
              <div class="setting-item">
                <label>创造性</label>
                <el-slider 
                  v-model="aiSettings.creativity" 
                  :min="0" 
                  :max="100" 
                  size="small"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, nextTick, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Delete, 
  Download, 
  User, 
  CopyDocument, 
  Refresh, 
  Promotion,
  Document,
  Money
} from '@element-plus/icons-vue'
import SidebarNav from '@/components/SidebarNav.vue'
import openRouterService from '@/services/openrouter'

export default {
  name: 'ChatPage',
  components: {
    SidebarNav,
    Delete,
    Download,
    User,
    CopyDocument,
    Refresh,
    Promotion,
    Document,
    Money
  },
  setup() {
    const messagesContainer = ref(null)
    const inputMessage = ref('')
    const isTyping = ref(false)
    const currentSessionId = ref(1)
    const isApiConfigured = ref(false)
    const currentModel = ref('')
    const currentModelInfo = ref({})
    
    const messages = ref([])
    
    const chatSessions = ref([
      {
        id: 1,
        title: '新对话',
        timestamp: new Date(),
        messages: []
      }
    ])

    const quickActions = ref([
      { id: 1, label: '总结今日任务', message: '请帮我总结今天的任务完成情况' },
      { id: 2, label: '制定学习计划', message: '请帮我制定一个学习计划' },
      { id: 3, label: '写作建议', message: '请给我一些写作建议' },
      { id: 4, label: '时间管理', message: '请教我一些时间管理的技巧' },
      { id: 5, label: '创意灵感', message: '请给我一些创意灵感' }
    ])

    const aiSettings = reactive({
      style: 'friendly',
      creativity: 70
    })

    // 检查API配置
    const checkApiConfiguration = () => {
      openRouterService.updateConfig()
      isApiConfigured.value = openRouterService.isConfigured()
      
      if (isApiConfigured.value) {
        const config = openRouterService.loadConfig()
        currentModel.value = config.defaultModel || 'openai/gpt-3.5-turbo'
        currentModelInfo.value = openRouterService.getModelInfo(currentModel.value)
      }
    }

    // 模拟AI回复
    const aiResponses = [
      '这是一个很好的问题！让我来帮你分析一下...',
      '根据你的描述，我建议你可以尝试以下几个方法：',
      '我理解你的需求，这里有一些实用的建议：',
      '让我为你整理一下相关信息：',
      '基于我的分析，我认为你可以从这几个角度考虑：'
    ]

    // 格式化消息内容
    const formatMessage = (content) => {
      // 简单的markdown格式化
      return content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>')
    }

    // 格式化时间
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    // 格式化日期
    const formatDate = (timestamp) => {
      return new Date(timestamp).toLocaleDateString('zh-CN', {
        month: 'short',
        day: 'numeric'
      })
    }

    // 格式化上下文长度
    const formatContextLength = (length) => {
      if (length >= 1000000) {
        return `${(length / 1000000).toFixed(1)}M`
      } else if (length >= 1000) {
        return `${(length / 1000).toFixed(0)}K`
      }
      return length.toString()
    }

    // 滚动到底部
    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }

    // 发送消息
    const handleSend = async () => {
      if (!inputMessage.value.trim() || isTyping.value) return

      // 检查API配置
      if (!isApiConfigured.value) {
        ElMessage.warning('请先在设置中配置 OpenRouter API Key')
        return
      }

      const userMessage = {
        id: Date.now(),
        type: 'user',
        content: inputMessage.value.trim(),
        timestamp: new Date()
      }

      messages.value.push(userMessage)
      const userInput = inputMessage.value.trim()
      inputMessage.value = ''
      
      scrollToBottom()

      // 调用真实API
      await sendToAI(userInput)
    }

    // 发送到AI API
    const sendToAI = async (userInput) => {
      isTyping.value = true
      
      try {
        // 构建消息历史
        const messageHistory = messages.value
          .filter(msg => msg.type === 'user' || msg.type === 'ai')
          .map(msg => ({
            role: msg.type === 'user' ? 'user' : 'assistant',
            content: msg.content
          }))

        // 添加当前用户消息
        messageHistory.push({
          role: 'user',
          content: userInput
        })

        // 创建AI消息占位符
        const aiMessage = {
          id: Date.now(),
          type: 'ai',
          content: '',
          timestamp: new Date()
        }
        messages.value.push(aiMessage)
        scrollToBottom()

        // 流式调用API
        await openRouterService.sendMessageStream(
          messageHistory,
          {
            model: currentModel.value,
            temperature: aiSettings.creativity / 100,
            maxTokens: 2000
          },
          (chunk) => {
            // 更新消息内容
            aiMessage.content += chunk
            scrollToBottom()
          }
        )

        // 更新会话标题
        updateSessionTitle()
      } catch (error) {
        console.error('AI API调用失败:', error)
        
        // 移除失败的消息
        const lastMessageIndex = messages.value.length - 1
        if (lastMessageIndex >= 0 && messages.value[lastMessageIndex].type === 'ai') {
          messages.value.splice(lastMessageIndex, 1)
        }

        // 显示错误消息
        const errorMessage = {
          id: Date.now(),
          type: 'ai',
          content: `抱歉，我遇到了一些问题：${error.message}\n\n请检查您的API配置或稍后重试。`,
          timestamp: new Date(),
          isError: true
        }
        messages.value.push(errorMessage)
        
        ElMessage.error('AI回复失败，请检查网络连接和API配置')
      } finally {
        isTyping.value = false
        scrollToBottom()
      }
    }

    // 模拟AI回复（备用方法）
    const simulateAIResponse = (userInput) => {
      isTyping.value = true
      
      setTimeout(() => {
        const aiMessage = {
          id: Date.now(),
          type: 'ai',
          content: generateAIResponse(userInput),
          timestamp: new Date()
        }

        messages.value.push(aiMessage)
        isTyping.value = false
        scrollToBottom()

        // 更新会话标题
        updateSessionTitle()
      }, 1000 + Math.random() * 2000)
    }

    // 生成AI回复
    const generateAIResponse = (userInput) => {
      const responses = [
        `关于"${userInput}"，我来为你详细分析一下：\n\n**主要观点：**\n- 这是一个很有价值的问题\n- 需要从多个角度来考虑\n- 建议采用系统性的方法\n\n**具体建议：**\n1. 首先明确目标和需求\n2. 制定详细的行动计划\n3. 定期评估和调整策略\n\n希望这些建议对你有帮助！`,
        
        `我理解你提到的"${userInput}"。让我为你提供一些实用的建议：\n\n**核心要点：**\n- 保持积极的心态\n- 注重实际行动\n- 持续学习和改进\n\n**推荐方法：**\n• 设定明确的目标\n• 分解复杂任务\n• 建立反馈机制\n\n如果你需要更具体的指导，请告诉我更多细节。`,
        
        `针对你的问题"${userInput}"，我有以下几点思考：\n\n**分析框架：**\n1. **现状评估** - 了解当前情况\n2. **目标设定** - 明确期望结果\n3. **路径规划** - 制定实施步骤\n4. **风险管控** - 识别潜在问题\n\n**实施建议：**\n- 从小处着手，逐步推进\n- 保持灵活性，适时调整\n- 寻求反馈，持续优化\n\n还有什么具体方面需要深入讨论吗？`
      ]
      
      return responses[Math.floor(Math.random() * responses.length)]
    }

    // 更新会话标题
    const updateSessionTitle = () => {
      const currentSession = chatSessions.value.find(s => s.id === currentSessionId.value)
      if (currentSession && messages.value.length > 0) {
        const firstUserMessage = messages.value.find(m => m.type === 'user')
        if (firstUserMessage) {
          currentSession.title = firstUserMessage.content.slice(0, 20) + '...'
        }
      }
    }

    // 快捷消息
    const sendQuickMessage = (message) => {
      inputMessage.value = message
      handleSend()
    }

    // 复制消息
    const copyMessage = async (content) => {
      try {
        await navigator.clipboard.writeText(content)
        ElMessage.success('已复制到剪贴板')
      } catch (err) {
        ElMessage.error('复制失败')
      }
    }

    // 重新生成回复
    const regenerateResponse = async (message) => {
      if (!isApiConfigured.value) {
        ElMessage.warning('请先在设置中配置 OpenRouter API Key')
        return
      }

      const messageIndex = messages.value.findIndex(m => m.id === message.id)
      if (messageIndex > 0) {
        const previousUserMessage = messages.value[messageIndex - 1]
        if (previousUserMessage.type === 'user') {
          // 移除当前AI回复
          messages.value.splice(messageIndex, 1)
          // 重新生成回复
          await sendToAI(previousUserMessage.content)
        }
      }
    }

    // 清空对话
    const clearChat = () => {
      messages.value = []
      ElMessage.success('对话已清空')
    }

    // 导出对话
    const exportChat = () => {
      if (messages.value.length === 0) {
        ElMessage.warning('暂无对话内容可导出')
        return
      }

      const chatContent = messages.value.map(msg => {
        const time = formatTime(msg.timestamp)
        const sender = msg.type === 'user' ? '用户' : 'AI助手'
        return `[${time}] ${sender}: ${msg.content}`
      }).join('\n\n')

      const blob = new Blob([chatContent], { type: 'text/plain;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `AI对话记录_${new Date().toLocaleDateString()}.txt`
      a.click()
      URL.revokeObjectURL(url)
      
      ElMessage.success('对话已导出')
    }

    // 加载对话会话
    const loadChatSession = (sessionId) => {
      currentSessionId.value = sessionId
      const session = chatSessions.value.find(s => s.id === sessionId)
      if (session) {
        messages.value = [...session.messages]
        scrollToBottom()
      }
    }

    onMounted(() => {
      scrollToBottom()
      checkApiConfiguration()
    })

    return {
      messagesContainer,
      inputMessage,
      isTyping,
      currentSessionId,
      isApiConfigured,
      currentModel,
      currentModelInfo,
      messages,
      chatSessions,
      quickActions,
      aiSettings,
      formatMessage,
      formatTime,
      formatDate,
      formatContextLength,
      handleSend,
      sendQuickMessage,
      copyMessage,
      regenerateResponse,
      clearChat,
      exportChat,
      loadChatSession,
      checkApiConfiguration
    }
  }
}
</script>

<style scoped>
.chat-container {
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
  gap: var(--spacing-3);
}

.chat-content {
  flex: 1;
  display: flex;
  gap: var(--spacing-6);
  overflow: hidden;
}

/* 聊天区域 */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--bg-color-card);
  backdrop-filter: blur(20px);
  border-radius: var(--border-radius-2xl);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: var(--box-shadow-card);
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  padding: var(--spacing-6);
  overflow-y: auto;
  scroll-behavior: smooth;
}

/* 欢迎消息 */
.welcome-message {
  display: flex;
  gap: var(--spacing-4);
  margin-bottom: var(--spacing-6);
}

.welcome-content {
  flex: 1;
  padding: var(--spacing-6);
  background: var(--bg-color-card-solid);
  border-radius: var(--border-radius-xl);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: var(--box-shadow-light);
}

.welcome-content h3 {
  margin: 0 0 var(--spacing-4) 0;
  color: var(--text-color-primary);
  font-size: var(--font-size-lg);
}

.welcome-content p {
  margin: var(--spacing-3) 0;
  color: var(--text-color-secondary);
}

.welcome-content ul {
  margin: var(--spacing-4) 0;
  padding-left: var(--spacing-6);
  color: var(--text-color-secondary);
}

.welcome-content li {
  margin: var(--spacing-2) 0;
}

/* API状态样式 */
.api-status-warning,
.api-status-success {
  margin: var(--spacing-4) 0;
}

.api-status-warning .el-alert,
.api-status-success .el-alert {
  border-radius: var(--border-radius-lg);
}

.api-status-warning .el-button {
  margin-top: var(--spacing-2);
}

/* 模型信息样式 */
.model-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-3);
}

.model-basic {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.model-basic strong {
  font-size: var(--font-size-lg);
  color: var(--text-color-primary);
}

.model-description {
  margin: 0;
  color: var(--text-color-secondary);
  font-size: var(--font-size-sm);
  line-height: 1.5;
}

.model-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.detail-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-1);
  font-size: var(--font-size-sm);
  color: var(--text-color-secondary);
}

.detail-item .el-icon {
  font-size: var(--font-size-base);
  color: var(--color-primary);
}

.model-features {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-1);
  margin-top: var(--spacing-1);
}

.model-features .el-tag {
  font-size: var(--font-size-xs);
}

/* 消息样式 */
.message {
  display: flex;
  gap: var(--spacing-3);
  margin-bottom: var(--spacing-6);
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: var(--gradient-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.ai-avatar {
  width: 40px;
  height: 40px;
  background: var(--gradient-secondary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-icon {
  font-size: var(--font-size-lg);
}

.message-content {
  flex: 1;
  max-width: 70%;
}

.user-message .message-content {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.message-bubble {
  padding: var(--spacing-4);
  border-radius: var(--border-radius-xl);
  position: relative;
}

.user-message .message-bubble {
  background: var(--gradient-primary);
  color: white;
  border-bottom-right-radius: var(--border-radius-sm);
}

.ai-message .message-bubble {
  background: var(--bg-color-card-solid);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--text-color-primary);
  border-bottom-left-radius: var(--border-radius-sm);
  box-shadow: var(--box-shadow-light);
}

.message-text {
  line-height: 1.6;
  word-wrap: break-word;
}

.message-time {
  font-size: var(--font-size-xs);
  opacity: 0.7;
  margin-top: var(--spacing-2);
}

.user-message .message-time {
  text-align: right;
}

.message-actions {
  display: flex;
  gap: var(--spacing-2);
  margin-top: var(--spacing-2);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.message:hover .message-actions {
  opacity: 1;
}

/* 正在输入指示器 */
.typing-indicator .message-bubble {
  padding: var(--spacing-4);
}

.typing-dots {
  display: flex;
  gap: 4px;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  background: var(--text-color-secondary);
  border-radius: 50%;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }



/* 输入区域 */
.chat-input-area {
  padding: var(--spacing-6);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.input-container {
  display: flex;
  gap: var(--spacing-3);
  align-items: flex-end;
}

.message-input {
  flex: 1;
}

.input-tips {
  margin-top: var(--spacing-2);
  font-size: var(--font-size-xs);
  color: var(--text-color-secondary);
  text-align: center;
}

/* 侧边栏 */
.chat-sidebar {
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-6);
}

.sidebar-section {
  background: var(--bg-color-card);
  backdrop-filter: blur(20px);
  border-radius: var(--border-radius-2xl);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: var(--box-shadow-card);
  padding: var(--spacing-6);
}

.sidebar-section h3 {
  margin: 0 0 var(--spacing-4) 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-color-primary);
}

/* 快捷操作 */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.quick-action-btn {
  width: 100%;
  justify-content: flex-start;
  text-align: left;
}

/* 对话历史 */
.chat-history {
  max-height: 300px;
  overflow-y: auto;
}

.history-item {
  padding: var(--spacing-3);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: var(--spacing-2);
}

.history-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.history-item.active {
  background: var(--gradient-primary);
  color: white;
}

.history-title {
  font-weight: 500;
  margin-bottom: var(--spacing-1);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-time {
  font-size: var(--font-size-xs);
  opacity: 0.7;
}

.no-history {
  text-align: center;
  color: var(--text-color-secondary);
  font-style: italic;
  padding: var(--spacing-4);
}

/* AI设置 */
.ai-settings {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.setting-item label {
  font-size: var(--font-size-sm);
  color: var(--text-color-secondary);
  font-weight: 500;
}
</style>