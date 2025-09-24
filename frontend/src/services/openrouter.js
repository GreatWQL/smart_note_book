/**
 * OpenRouter API 服务模块
 * 处理与 OpenRouter API 的交互
 */

class OpenRouterService {
  constructor() {
    this.baseURL = 'https://openrouter.ai/api/v1'
    this.config = this.loadConfig()
    this.modelInfo = this.initModelInfo()
  }

  /**
   * 初始化模型信息映射
   */
  initModelInfo() {
    return {
      // OpenAI 模型
      'openai/gpt-4o': {
        name: 'GPT-4o',
        provider: 'OpenAI',
        description: '最新的多模态模型，支持文本和图像',
        contextLength: 128000,
        pricing: { input: 5, output: 15 },
        features: ['文本', '图像', '代码']
      },
      'openai/gpt-4o-mini': {
        name: 'GPT-4o Mini',
        provider: 'OpenAI',
        description: '轻量级版本，速度更快，成本更低',
        contextLength: 128000,
        pricing: { input: 0.15, output: 0.6 },
        features: ['文本', '图像', '代码']
      },
      'openai/gpt-4-turbo': {
        name: 'GPT-4 Turbo',
        provider: 'OpenAI',
        description: '高性能版本，支持更长上下文',
        contextLength: 128000,
        pricing: { input: 10, output: 30 },
        features: ['文本', '代码', '分析']
      },
      'openai/gpt-4': {
        name: 'GPT-4',
        provider: 'OpenAI',
        description: '强大的推理能力，适合复杂任务',
        contextLength: 8192,
        pricing: { input: 30, output: 60 },
        features: ['文本', '代码', '推理']
      },
      'openai/gpt-3.5-turbo': {
        name: 'GPT-3.5 Turbo',
        provider: 'OpenAI',
        description: '经济实用，响应速度快',
        contextLength: 16385,
        pricing: { input: 0.5, output: 1.5 },
        features: ['文本', '对话']
      },

      // Anthropic Claude 模型
      'anthropic/claude-3.5-sonnet': {
        name: 'Claude 3.5 Sonnet',
        provider: 'Anthropic',
        description: '最新版本，平衡性能与效率',
        contextLength: 200000,
        pricing: { input: 3, output: 15 },
        features: ['文本', '分析', '创作']
      },
      'anthropic/claude-3-opus': {
        name: 'Claude 3 Opus',
        provider: 'Anthropic',
        description: '最强版本，适合复杂推理任务',
        contextLength: 200000,
        pricing: { input: 15, output: 75 },
        features: ['文本', '推理', '分析']
      },
      'anthropic/claude-3-sonnet': {
        name: 'Claude 3 Sonnet',
        provider: 'Anthropic',
        description: '平衡性能与成本的选择',
        contextLength: 200000,
        pricing: { input: 3, output: 15 },
        features: ['文本', '对话', '分析']
      },
      'anthropic/claude-3-haiku': {
        name: 'Claude 3 Haiku',
        provider: 'Anthropic',
        description: '快速响应，适合简单任务',
        contextLength: 200000,
        pricing: { input: 0.25, output: 1.25 },
        features: ['文本', '对话']
      },

      // Google 模型
      'google/gemini-pro-1.5': {
        name: 'Gemini Pro 1.5',
        provider: 'Google',
        description: '增强版本，支持更长上下文',
        contextLength: 1000000,
        pricing: { input: 3.5, output: 10.5 },
        features: ['文本', '代码', '多模态']
      },
      'google/gemini-pro': {
        name: 'Gemini Pro',
        provider: 'Google',
        description: 'Google的旗舰模型',
        contextLength: 30720,
        pricing: { input: 0.5, output: 1.5 },
        features: ['文本', '代码']
      },
      'google/gemini-flash-1.5': {
        name: 'Gemini Flash 1.5',
        provider: 'Google',
        description: '快速版本，优化响应速度',
        contextLength: 1000000,
        pricing: { input: 0.075, output: 0.3 },
        features: ['文本', '快速响应']
      },

      // Meta 模型
      'meta-llama/llama-3.1-405b-instruct': {
        name: 'Llama 3.1 405B',
        provider: 'Meta',
        description: '最大参数模型，顶级性能',
        contextLength: 131072,
        pricing: { input: 3, output: 3 },
        features: ['文本', '推理', '代码']
      },
      'meta-llama/llama-3.1-70b-instruct': {
        name: 'Llama 3.1 70B',
        provider: 'Meta',
        description: '高性能开源模型',
        contextLength: 131072,
        pricing: { input: 0.88, output: 0.88 },
        features: ['文本', '代码']
      },
      'meta-llama/llama-3.1-8b-instruct': {
        name: 'Llama 3.1 8B',
        provider: 'Meta',
        description: '轻量级开源模型',
        contextLength: 131072,
        pricing: { input: 0.055, output: 0.055 },
        features: ['文本', '对话']
      },

      // Mistral 模型
      'mistralai/mistral-large-2407': {
        name: 'Mistral Large 2',
        provider: 'Mistral',
        description: '最新大型模型',
        contextLength: 128000,
        pricing: { input: 3, output: 9 },
        features: ['文本', '代码', '多语言']
      },
      'mistralai/mistral-nemo': {
        name: 'Mistral Nemo',
        provider: 'Mistral',
        description: '中等规模，平衡性能',
        contextLength: 128000,
        pricing: { input: 0.3, output: 0.3 },
        features: ['文本', '对话']
      },
      'mistralai/codestral-mamba': {
        name: 'Codestral',
        provider: 'Mistral',
        description: '专门优化代码生成',
        contextLength: 256000,
        pricing: { input: 0.25, output: 0.25 },
        features: ['代码', '编程']
      },

      // 其他模型
      'perplexity/llama-3.1-sonar-large-128k-online': {
        name: 'Perplexity Sonar',
        provider: 'Perplexity',
        description: '联网搜索增强模型',
        contextLength: 127072,
        pricing: { input: 1, output: 1 },
        features: ['搜索', '实时信息']
      },
      'cohere/command-r-plus': {
        name: 'Command R+',
        provider: 'Cohere',
        description: '企业级对话模型',
        contextLength: 128000,
        pricing: { input: 3, output: 15 },
        features: ['文本', '企业应用']
      },
      'deepseek/deepseek-coder': {
        name: 'DeepSeek Coder V2',
        provider: 'DeepSeek',
        description: '专业代码生成模型',
        contextLength: 163840,
        pricing: { input: 0.14, output: 0.28 },
        features: ['代码', '编程', '调试']
      }
    }
  }

  /**
   * 加载配置
   */
  loadConfig() {
    const savedConfig = localStorage.getItem('openrouter_config')
    if (savedConfig) {
      return JSON.parse(savedConfig)
    }
    return null
  }

  /**
   * 检查是否已配置
   */
  isConfigured() {
    return this.config && this.config.apiKey
  }

  /**
   * 保存配置
   */
  saveConfig(config) {
    localStorage.setItem('openrouter_config', JSON.stringify(config))
    this.config = config
  }

  /**
   * 清除配置
   */
  clearConfig() {
    localStorage.removeItem('openrouter_config')
    this.config = null
  }

  /**
   * 更新配置
   */
  updateConfig() {
    this.config = this.loadConfig()
  }

  /**
   * 获取请求头
   */
  getHeaders() {
    if (!this.config || !this.config.apiKey) {
      throw new Error('OpenRouter API Key 未配置')
    }

    return {
      'Authorization': `Bearer ${this.config.apiKey}`,
      'Content-Type': 'application/json',
      'HTTP-Referer': window.location.origin,
      'X-Title': '智能笔记本'
    }
  }

  /**
   * 获取可用模型列表
   */
  async getModels() {
    try {
      const response = await fetch(`${this.baseURL}/models`, {
        headers: this.getHeaders()
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      return data.data || []
    } catch (error) {
      console.error('获取模型列表失败:', error)
      throw error
    }
  }

  /**
   * 获取模型详细信息
   */
  getModelInfo(modelId) {
    return this.modelInfo[modelId] || {
      name: modelId,
      provider: '未知',
      description: '暂无描述',
      contextLength: 0,
      pricing: { input: 0, output: 0 },
      features: ['文本']
    }
  }

  /**
   * 获取所有模型信息
   */
  getAllModelInfo() {
    return this.modelInfo
  }

  /**
   * 根据提供商筛选模型
   */
  getModelsByProvider(provider) {
    return Object.entries(this.modelInfo)
      .filter(([_, info]) => info.provider === provider)
      .reduce((acc, [id, info]) => {
        acc[id] = info
        return acc
      }, {})
  }

  /**
   * 获取推荐模型（按用途分类）
   */
  getRecommendedModels() {
    return {
      general: ['openai/gpt-4o', 'anthropic/claude-3.5-sonnet', 'google/gemini-pro-1.5'],
      coding: ['deepseek/deepseek-coder', 'mistralai/codestral-mamba', 'openai/gpt-4o'],
      fast: ['openai/gpt-4o-mini', 'anthropic/claude-3-haiku', 'google/gemini-flash-1.5'],
      economical: ['meta-llama/llama-3.1-8b-instruct', 'openai/gpt-3.5-turbo', 'mistralai/mistral-nemo'],
      powerful: ['anthropic/claude-3-opus', 'meta-llama/llama-3.1-405b-instruct', 'openai/gpt-4']
    }
  }

  /**
   * 测试 API 连接
   */
  async testConnection() {
    try {
      await this.getModels()
      return true
    } catch (error) {
      console.error('API 连接测试失败:', error)
      return false
    }
  }

  /**
   * 发送聊天消息
   */
  async sendMessage(messages, options = {}) {
    if (!this.isConfigured()) {
      throw new Error('请先在设置中配置 OpenRouter API Key')
    }

    const model = options.model || this.config.defaultModel || 'openai/gpt-3.5-turbo'
    
    const requestBody = {
      model: model,
      messages: messages,
      temperature: options.temperature || 0.7,
      max_tokens: options.maxTokens || 2000,
      stream: options.stream || false
    }

    try {
      const response = await fetch(`${this.baseURL}/chat/completions`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(requestBody)
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error?.message || `HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('发送消息失败:', error)
      throw error
    }
  }

  /**
   * 流式发送聊天消息
   */
  async sendMessageStream(messages, options = {}, onChunk) {
    if (!this.isConfigured()) {
      throw new Error('请先在设置中配置 OpenRouter API Key')
    }

    const model = options.model || this.config.defaultModel || 'openai/gpt-3.5-turbo'
    
    const requestBody = {
      model: model,
      messages: messages,
      temperature: options.temperature || 0.7,
      max_tokens: options.maxTokens || 2000,
      stream: true
    }

    try {
      const response = await fetch(`${this.baseURL}/chat/completions`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(requestBody)
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error?.message || `HTTP ${response.status}: ${response.statusText}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            
            if (data === '[DONE]') {
              return
            }

            try {
              const parsed = JSON.parse(data)
              const content = parsed.choices?.[0]?.delta?.content
              
              if (content && onChunk) {
                onChunk(content)
              }
            } catch (e) {
              // 忽略解析错误
            }
          }
        }
      }
    } catch (error) {
      console.error('流式发送消息失败:', error)
      throw error
    }
  }

  /**
   * 获取账户信息
   */
  async getAccountInfo() {
    try {
      const response = await fetch(`${this.baseURL}/auth/key`, {
        headers: this.getHeaders()
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      return data.data
    } catch (error) {
      console.error('获取账户信息失败:', error)
      throw error
    }
  }
}

// 创建单例实例
const openRouterService = new OpenRouterService()

export default openRouterService