# 智能笔记本 - Smart Notebook

一个功能丰富的个人生产力平台，集成了笔记管理、任务管理、专注计时、数据可视化等多种功能。

## 🌟 主要功能

### 📝 笔记管理
- **Markdown编辑器**: 支持实时预览的Markdown编辑器
- **分类管理**: 按分类组织笔记
- **搜索功能**: 快速查找笔记内容
- **导入导出**: 支持笔记的批量导入导出

### ✅ 任务管理
- **项目分组**: 按项目组织任务
- **优先级设置**: 高、中、低三级优先级
- **状态跟踪**: 待办、进行中、已完成状态管理
- **截止日期**: 任务截止时间提醒

### ⏰ 专注计时
- **番茄工作法**: 25分钟专注时间 + 5分钟休息
- **自定义时长**: 可自定义专注和休息时间
- **统计记录**: 专注时长统计和历史记录
- **音效提醒**: 时间到达时的音效通知

### 📊 数据可视化
- **统计图表**: 使用Chart.js展示数据趋势
- **多维度分析**: 专注时长、任务完成、笔记创建统计
- **时间范围**: 支持7天、30天、90天数据查看
- **实时更新**: 数据实时更新显示

### 🌤️ 天气信息
- **实时天气**: 显示当前天气状况
- **三天预报**: 未来三天天气预报
- **地理定位**: 自动获取用户位置信息
- **图标显示**: 直观的天气图标展示

### 🔔 提醒管理
- **任务提醒**: 重要任务到期提醒
- **重复提醒**: 支持每日、每周、每月重复
- **浏览器通知**: 系统级通知提醒
- **过期标记**: 自动标记过期提醒

### 💾 数据备份
- **选择性导出**: 可选择导出特定类型数据
- **批量导入**: 支持从备份文件恢复数据
- **定时备份**: 自动定时备份功能
- **历史管理**: 备份历史记录管理

### 🎨 主题切换
- **多主题支持**: 浅色、深色、自动主题
- **系统跟随**: 自动跟随系统主题设置
- **实时切换**: 无需刷新即时切换主题
- **个性化**: 保存用户主题偏好

## 🛠️ 技术栈

### 前端
- **Vue 3**: 现代化的前端框架
- **Element Plus**: 企业级UI组件库
- **Chart.js**: 数据可视化图表库
- **Vite**: 快速的构建工具
- **Vue Router**: 单页应用路由管理

### 后端
- **Flask**: 轻量级Python Web框架
- **SQLite**: 嵌入式数据库
- **Flask-CORS**: 跨域资源共享支持
- **RESTful API**: 标准化API接口设计

## 📁 项目结构

```
智能笔记本/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── __init__.py     # Flask应用初始化
│   │   ├── models.py       # 数据模型定义
│   │   └── routes/         # API路由
│   │       ├── __init__.py
│   │       ├── auth.py     # 认证相关API
│   │       ├── notes.py    # 笔记管理API
│   │       ├── tasks.py    # 任务管理API
│   │       ├── focus.py    # 专注计时API
│   │       └── reminders.py # 提醒管理API
│   ├── instance/
│   │   └── smart_notebook.db # SQLite数据库
│   ├── requirements.txt    # Python依赖
│   └── run.py             # 应用启动文件
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   │   ├── DataBackup.vue      # 数据备份组件
│   │   │   ├── FocusTimer.vue      # 专注计时器组件
│   │   │   ├── MarkdownEditor.vue  # Markdown编辑器组件
│   │   │   ├── ReminderManager.vue # 提醒管理组件
│   │   │   ├── SidebarNav.vue      # 侧边栏导航组件
│   │   │   ├── StatsChart.vue      # 统计图表组件
│   │   │   ├── ThemeToggle.vue     # 主题切换组件
│   │   │   └── WeatherWidget.vue   # 天气小组件
│   │   ├── views/          # 页面组件
│   │   │   ├── DashboardPage.vue   # 仪表盘页面
│   │   │   ├── NotesPage.vue       # 笔记管理页面
│   │   │   ├── TasksPage.vue       # 任务管理页面
│   │   │   ├── FocusPage.vue       # 专注计时页面
│   │   │   ├── SettingsPage.vue    # 设置页面
│   │   │   ├── LoginPage.vue       # 登录页面
│   │   │   └── RegisterPage.vue    # 注册页面
│   │   ├── styles/         # 样式文件
│   │   │   └── global.css  # 全局样式
│   │   ├── utils/          # 工具函数
│   │   │   ├── auth.js     # 认证工具
│   │   │   └── request.js  # HTTP请求工具
│   │   ├── router/         # 路由配置
│   │   │   └── index.js
│   │   ├── App.vue         # 根组件
│   │   └── main.js         # 应用入口
│   ├── package.json        # 前端依赖配置
│   └── vite.config.js      # Vite配置
└── README.md              # 项目说明文档
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd 智能笔记本
   ```

2. **启动后端服务**
   ```bash
   cd backend
   pip install -r requirements.txt
   python3 run.py
   ```
   后端服务将在 `http://localhost:5000` 启动

3. **启动前端服务**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   前端服务将在 `http://localhost:3000` 启动

4. **访问应用**
   打开浏览器访问 `http://localhost:3000`

## 📱 功能截图

### 仪表盘
- 统计卡片展示笔记、任务、专注时长
- 最近笔记和待办任务快速访问
- 数据可视化图表
- 天气信息显示
- 提醒管理

### 笔记管理
- Markdown编辑器，支持实时预览
- 笔记分类和搜索
- 笔记列表和详情查看

### 任务管理
- 项目分组的任务列表
- 任务创建、编辑、删除
- 优先级和状态管理
- 截止日期设置

### 专注计时
- 番茄工作法计时器
- 专注历史记录
- 统计数据展示

### 设置页面
- 个人信息管理
- 主题切换设置
- 数据备份和恢复

## 🎯 核心特性

### 响应式设计
- 适配桌面和移动设备
- 流畅的用户交互体验
- 现代化的UI设计

### 数据持久化
- SQLite数据库存储
- 本地数据备份
- 数据导入导出功能

### 实时更新
- 数据实时同步
- 热模块替换(HMR)
- 即时反馈

### 安全性
- 用户认证系统
- 数据加密存储
- CORS安全配置

## 🔧 开发说明

### API接口
所有API接口都遵循RESTful设计规范：

- `GET /api/notes` - 获取笔记列表
- `POST /api/notes` - 创建新笔记
- `PUT /api/notes/:id` - 更新笔记
- `DELETE /api/notes/:id` - 删除笔记
- `GET /api/tasks` - 获取任务列表
- `POST /api/tasks` - 创建新任务
- `GET /api/focus-sessions` - 获取专注记录
- `POST /api/focus-sessions` - 创建专注记录
- `GET /api/reminders` - 获取提醒列表
- `POST /api/reminders` - 创建新提醒

### 数据库模型
- **User**: 用户信息
- **Note**: 笔记数据
- **Task**: 任务数据
- **Project**: 项目数据
- **FocusSession**: 专注记录
- **Reminder**: 提醒数据

### 组件设计
- 模块化组件设计
- 可复用的UI组件
- 统一的样式规范
- 响应式布局

## 📈 未来规划

- [ ] 移动端APP开发
- [ ] 云端数据同步
- [ ] 团队协作功能
- [ ] 插件系统
- [ ] AI智能助手
- [ ] 更多主题选择
- [ ] 国际化支持
- [ ] 离线模式支持

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License

## 👨‍💻 作者

开发者：AI Assistant
项目版本：1.0.0
最后更新：2025年9月23日

---

**智能笔记本** - 让生产力更上一层楼！ 🚀