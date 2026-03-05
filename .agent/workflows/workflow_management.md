---
description: Natural Language Workflow Management (Linear + Git)
---

# 项目配置管理

```yaml
project:
  name: "data_assistant_new"
  team: "智能数据分析助手"  # Linear 的 Team Key
  repo: "git@github.com:FatCat08/DAT.git"
```

# 工作流执行规则

当你处理日常开发口语指令（如 "开始做登录系统功能"、"修复主页崩溃"、"测试写完了" 等）时，你必须按照以下步骤自动执行工作流：

## 1. 意图识别与任务查找
1. 解析用户的口语指令，提取核心动作（如：开始做、已完成、修复、测试等）和功能描述。
2. 使用 `linear-mcp-server_list_issues` 工具，在配置的 Linear `team` (如: DAT) 及 `name` (如: 只能数据分析助手) 下查找相关的 Issue。
   - 如果找到了匹配的 Issue，记录其 ID (如: DAT-12) 和标题。
   - 如果没有找到匹配的 Issue，使用 `linear-mcp-server_save_issue` 自动创建一个新 Issue，提取合适的标题，并将状态设置为 "In Progress"（或适合该动作的初始状态）。

## 2. 状态扭转
1. 根据用户的口语动作，更新 Linear Issue 的状态：
   - "开始做 / 认领" -> 将状态更新为 **In Progress**，并将 Assignee 设为 `me`。
   - "做完了 / 提测" -> 将状态更新为 **In Review** 或 **Done**（根据团队实际工作流状态定）。
   - "测试通过" -> 将状态更新为 **Done**。
2. 使用 `linear-mcp-server_save_issue` 提交状态更新。

## 3. 开发分支推荐
1. 当用户指令意为 "开始开发" 或刚创建了新 Issue 时，你需要基于 Linear Issue 的信息生成 Git 分支命令推荐。
2. 分支命名规范：`{功能类型}/{Issue-ID}-{简短的英文标题描述}`。
   - `功能类型` 示例: `feat` (新功能), `fix` (修复), `chore` (构建/工具), `docs` (文档)。
3. 获取配置中的 `repo` 信息，组装完整的 Git 操作建议。
4. **输出格式**：向用户展示类似下方的 Markdown 代码块：
   ```bash
   # 更新代码并创建新分支
   git checkout main
   git pull origin main
   git checkout -b feat/DAT-12-login-system
   ```

## 4. 反馈报告
1. 执行完毕后，向用户简短汇报结果。
2. 汇报内容必须包括：
   - 更新/创建的 Linear 任务链接。
   - 当前的最新状态（如: In Progress）。
   - 推荐的 Git 分支操作命令。