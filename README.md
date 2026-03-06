# Data Assistant (DAT)

Data Assistant 是一个基于大语言模型 (LLM) 和大前端技术的智能数据问答与图表可视化助手。它能够通过自然语言对话，自动理解用户意图，生成 SQL 查询本地数据库，并动态推荐和渲染合适的 ECharts 数据图表。

## 🎯 核心功能
* **自然语言转 SQL (NL2SQL)**: 基于大模型自动将用户的自然语言问题转化为 SQL 并安全执行查询。
* **智能图表推荐与渲染**: 自动分析查询结果的数据结构，推荐最合适的图表类型（折线图、柱状图、饼图等）并实时动态渲染。
* **流式对话交互 (SSE)**: 采用 Server-Sent Events 支持大模型的流式字级输出。
* **会话管理**: 支持多历史会话保存与无缝切换。

---

## 🛠️ 技术栈
* **前 端**: React 18, Vite, ECharts, Lucide React, Vanilla CSS (自定义全套精美 UI)
* **后 端**: FastAPI, Python 3.11+, LangChain, SQLAlchemy, aiosqlite (异步数据库)
* **大模型引擎**: 阿里云通义千问 (Qwen-Max)

---

## 🚀 快速启动指南

### 1. 准备工作
确保你的本地开发环境已经安装了以下依赖：
- **Node.js** (推荐 v18+ 版本)
- **Python** (推荐 v3.11+ 版本)

### 2. 后端服务 (Backend) 启动
后端负责处理大语言模型的对话分析与数据库操作。

```bash
# 进入后端目录
cd backend

# 创建并激活虚拟环境 (Windows)
python -m venv venv
.\venv\Scripts\activate
# 或者 (macOS / Linux)
# python3 -m venv venv
# source venv/bin/activate

# 安装 Python 依赖包
pip install -r requirements.txt

# 配置环境变量
# 复制一份 .env.example 并重命名为 .env
cp .env.example .env
# 打开 .env 文件，填入你的阿里通义千问 API KEY (DASHSCOPE_API_KEY)

# 【重要】初始化模拟业务数据库
# 这一步会生成 data/business.db 并写入几百条模拟的 Q3/Q4 销售数据，供大模型查询展示
python init_business_db.py

# 启动 FastAPI 服务 (运行在 http://localhost:8000)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 前端应用 (Frontend) 启动
前端是与用户进行对话和展示精美数据看板的界面。

请**新开一个终端窗口**：

```bash
# 进入前端目录
cd frontend

# 安装 Node 依赖包
npm install

# 启动 Vite 本地开发服务器 (通常运行在 http://localhost:5173 或 5174)
npm run dev
```

---

## 💡 使用说明

1. 浏览器打开前端提供的本地地址（如 `http://localhost:5173`）。
2. 在左侧边栏点击 **"New Chat"** 发起一个新会话。
3. 在底部输入框输入与业务数据相关的问题，例如：
   * *"帮我看一下 Q4 的销售额情况，画个图表"*
   * *"对比一下昨天和今天的各个大区销售额"*
   * *"排名前三的产品是哪些？画个饼图"*
4. 助手会流式输出推理过程，查询数据，并在右侧的数据面板（Data Visualization）**自动为您渲染对应的图表**。

## ⚠️ 注意事项
- 由于系统具备执行大语言模型生成的 SQL 行为，所有通过大模型进行的查询都被加上了**严格的只读 (SELECT Only) 校验与数据行数 (LIMIT) 限制**，避免改变或拖垮数据库。
- 需要使用具有函数调用 (Tool calling) 能力的强大 LLM，本项目已经默认深度兼容 `qwen-max` 模型。
