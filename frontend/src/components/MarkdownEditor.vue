<template>
  <div class="markdown-editor">
    <div class="editor-toolbar">
      <el-button-group>
        <el-button 
          :type="mode === 'edit' ? 'primary' : ''" 
          size="small" 
          @click="mode = 'edit'"
        >
          <el-icon><Edit /></el-icon>
          编辑
        </el-button>
        <el-button 
          :type="mode === 'preview' ? 'primary' : ''" 
          size="small" 
          @click="mode = 'preview'"
        >
          <el-icon><View /></el-icon>
          预览
        </el-button>
        <el-button 
          :type="mode === 'split' ? 'primary' : ''" 
          size="small" 
          @click="mode = 'split'"
        >
          <el-icon><Grid /></el-icon>
          分屏
        </el-button>
      </el-button-group>
      
      <div class="toolbar-actions">
        <el-button size="small" @click="insertMarkdown('**', '**')">
          <strong>B</strong>
        </el-button>
        <el-button size="small" @click="insertMarkdown('*', '*')">
          <em>I</em>
        </el-button>
        <el-button size="small" @click="insertMarkdown('`', '`')">
          Code
        </el-button>
        <el-button size="small" @click="insertMarkdown('## ', '')">
          H2
        </el-button>
        <el-button size="small" @click="insertMarkdown('- ', '')">
          List
        </el-button>
        <el-button size="small" @click="insertMarkdown('[', '](url)')">
          Link
        </el-button>
      </div>
    </div>
    
    <div class="editor-content" :class="{ 'split-mode': mode === 'split' }">
      <!-- 编辑区域 -->
      <div v-show="mode === 'edit' || mode === 'split'" class="edit-area">
        <el-input
          ref="textareaRef"
          v-model="content"
          type="textarea"
          :rows="20"
          placeholder="请输入Markdown内容..."
          @input="handleInput"
          @keydown="handleKeydown"
        />
      </div>
      
      <!-- 预览区域 -->
      <div v-show="mode === 'preview' || mode === 'split'" class="preview-area">
        <div class="markdown-preview" v-html="renderedMarkdown"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, nextTick } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

export default {
  name: 'MarkdownEditor',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    height: {
      type: String,
      default: '400px'
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const mode = ref('edit')
    const content = ref(props.modelValue)
    const textareaRef = ref(null)
    
    // 配置marked
    marked.setOptions({
      highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
          try {
            return hljs.highlight(code, { language: lang }).value
          } catch (err) {}
        }
        return hljs.highlightAuto(code).value
      },
      breaks: true,
      gfm: true
    })
    
    const renderedMarkdown = computed(() => {
      return marked(content.value || '')
    })
    
    const handleInput = () => {
      emit('update:modelValue', content.value)
    }
    
    const handleKeydown = (event) => {
      // Tab键插入缩进
      if (event.key === 'Tab') {
        event.preventDefault()
        insertAtCursor('  ')
      }
    }
    
    const insertMarkdown = (before, after) => {
      const textarea = textareaRef.value?.textarea
      if (!textarea) return
      
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const selectedText = content.value.substring(start, end)
      
      const newText = before + selectedText + after
      content.value = content.value.substring(0, start) + newText + content.value.substring(end)
      
      nextTick(() => {
        textarea.focus()
        textarea.setSelectionRange(start + before.length, start + before.length + selectedText.length)
      })
      
      handleInput()
    }
    
    const insertAtCursor = (text) => {
      const textarea = textareaRef.value?.textarea
      if (!textarea) return
      
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      
      content.value = content.value.substring(0, start) + text + content.value.substring(end)
      
      nextTick(() => {
        textarea.focus()
        textarea.setSelectionRange(start + text.length, start + text.length)
      })
      
      handleInput()
    }
    
    // 监听props变化
    watch(() => props.modelValue, (newValue) => {
      content.value = newValue
    })
    
    return {
      mode,
      content,
      textareaRef,
      renderedMarkdown,
      handleInput,
      handleKeydown,
      insertMarkdown
    }
  }
}
</script>

<style scoped>
.markdown-editor {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f5f7fa;
  border-bottom: 1px solid #dcdfe6;
}

.toolbar-actions {
  display: flex;
  gap: 4px;
}

.toolbar-actions .el-button {
  padding: 4px 8px;
  min-width: auto;
}

.editor-content {
  display: flex;
  height: 400px;
}

.editor-content.split-mode .edit-area,
.editor-content.split-mode .preview-area {
  width: 50%;
}

.edit-area {
  width: 100%;
  border-right: 1px solid #dcdfe6;
}

.edit-area :deep(.el-textarea) {
  height: 100%;
}

.edit-area :deep(.el-textarea__inner) {
  height: 100% !important;
  border: none;
  border-radius: 0;
  resize: none;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.6;
}

.preview-area {
  width: 100%;
  overflow-y: auto;
  background: #fff;
}

.markdown-preview {
  padding: 16px;
  line-height: 1.6;
  color: #333;
}

.markdown-preview :deep(h1),
.markdown-preview :deep(h2),
.markdown-preview :deep(h3),
.markdown-preview :deep(h4),
.markdown-preview :deep(h5),
.markdown-preview :deep(h6) {
  margin: 16px 0 8px 0;
  font-weight: 600;
  color: #2c3e50;
}

.markdown-preview :deep(h1) { font-size: 24px; }
.markdown-preview :deep(h2) { font-size: 20px; }
.markdown-preview :deep(h3) { font-size: 18px; }
.markdown-preview :deep(h4) { font-size: 16px; }
.markdown-preview :deep(h5) { font-size: 14px; }
.markdown-preview :deep(h6) { font-size: 12px; }

.markdown-preview :deep(p) {
  margin: 8px 0;
}

.markdown-preview :deep(ul),
.markdown-preview :deep(ol) {
  margin: 8px 0;
  padding-left: 24px;
}

.markdown-preview :deep(li) {
  margin: 4px 0;
}

.markdown-preview :deep(blockquote) {
  margin: 16px 0;
  padding: 8px 16px;
  background: #f8f9fa;
  border-left: 4px solid #409eff;
  color: #666;
}

.markdown-preview :deep(code) {
  padding: 2px 4px;
  background: #f1f2f3;
  border-radius: 3px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  color: #e83e8c;
}

.markdown-preview :deep(pre) {
  margin: 16px 0;
  padding: 16px;
  background: #f8f8f8;
  border-radius: 4px;
  overflow-x: auto;
}

.markdown-preview :deep(pre code) {
  padding: 0;
  background: none;
  color: inherit;
}

.markdown-preview :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
}

.markdown-preview :deep(th),
.markdown-preview :deep(td) {
  padding: 8px 12px;
  border: 1px solid #ddd;
  text-align: left;
}

.markdown-preview :deep(th) {
  background: #f5f7fa;
  font-weight: 600;
}

.markdown-preview :deep(a) {
  color: #409eff;
  text-decoration: none;
}

.markdown-preview :deep(a:hover) {
  text-decoration: underline;
}

.markdown-preview :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  margin: 8px 0;
}

.markdown-preview :deep(hr) {
  margin: 24px 0;
  border: none;
  border-top: 1px solid #eee;
}
</style>