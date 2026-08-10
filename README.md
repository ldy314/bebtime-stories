# 睡前故事 - GitHub 云端备份

这是睡前故事 H5 应用的 GitHub 云端版本。与本地 WorkBuddy 自动化配合使用，形成三重保障：

| 优先级 | 方式 | 触发条件 | 说明 |
|--------|------|----------|------|
| 1 (主) | WorkBuddy 本地 | 电脑开机，每2小时自动检查 | 生成故事 → 更新 CloudStudio 链接 |
| 2 (备) | 手机点一下 | 手机手动触发 | 调用 GitHub Action → 更新 GitHub Pages |
| 3 (兜底) | GitHub Actions 定时 | 每天 23:00 北京时间自动 | 无需任何操作，纯云端运行 |

## 目录结构

```
github-bedtime-stories/
├── .github/workflows/
│   └── generate-stories.yml    # GitHub Action (定时 + 手动触发)
├── scripts/
│   ├── generate-story.js       # 故事生成脚本 (调用智谱 GLM-4V-Flash API)
│   ├── prompt-builder.js       # 提示词构建 (含风格描述)
│   └── generate-collection-html.js  # 合集HTML生成
├── index.html                  # H5 阅读器 (含 EMBEDDED_STORIES)
├── stories.json                # 故事数据
├── collection.html             # 合集页面 (自动生成)
├── .nojekyll                   # 禁用 Jekyll (GitHub Pages 用)
└── .gitignore
```

## 搭建步骤

### 第一步：创建 GitHub 仓库

1. 打开 https://github.com 注册/登录
2. 点击右上角 `+` → `New repository`
3. 仓库名称填 `bedtime-stories`
4. 选择 **Public**（免费仓库才能用 GitHub Actions 和 Pages）
5. 勾选 `Add a README file`
6. 点击 `Create repository`

### 第二步：上传项目文件

#### 方法 A：用命令行推送（推荐）

在本地项目目录执行：

```bash
cd C:\Users\Administrator\WorkBuddy\Claw\github-bedtime-stories

# 初始化 git
git init
git add -A
git commit -m "Initial commit: bedtime story app"

# 关联远程仓库（把 YOUR_USERNAME 换成你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/bedtime-stories.git
git branch -M main
git push -u origin main
```

#### 方法 B：网页上传

1. 在 GitHub 仓库页面点击 `uploading an existing file`
2. 把 `github-bedtime-stories` 目录下所有文件拖进去
3. 注意：`.github`、`.nojekyll`、`.gitignore` 是隐藏文件，需要勾选显示
4. 点击 `Commit changes`

### 第三步：获取智谱 API Key

1. 打开 https://open.bigmodel.cn 注册（支持手机号/邮箱）
2. 登录后进入 API Keys 页面
3. 点击 `Create API Key`
4. 复制生成的 key（格式：`xxxxxxxx.xxxxxxxxxxxxx`）
5. 新用户注册送免费 tokens，GLM-4V-Flash 模型免费

### 第四步：添加 API Key 到 GitHub Secrets

1. 在 GitHub 仓库页面点击 `Settings` → `Secrets and variables` → `Actions`
2. 点击 `New repository secret`
3. Name 填 `ZHIPU_API_KEY`
4. Secret 粘贴你的 API Key
5. 点击 `Add secret`

### 第五步：启用 GitHub Pages

1. 在仓库页面点击 `Settings` → `Pages`
2. Source 选择 `Deploy from a branch`
3. Branch 选择 `main`，文件夹选 `/ (root)`
4. 点击 `Save`
5. 等待 1-2 分钟，页面顶部会显示你的网址：
   `https://YOUR_USERNAME.github.io/bedtime-stories/`

这就是你的**云端备份链接**，永远在线。

### 第六步：测试 GitHub Action

1. 在仓库页面点击 `Actions` 标签
2. 左侧选择 `Generate Bedtime Stories`
3. 点击右侧 `Run workflow` → `Run workflow`
4. 等待执行完成（约 1-2 分钟）
5. 刷新仓库主页，应该能看到新的提交（故事已生成）
6. 打开 Pages 链接，确认故事正常显示

### 第七步：设置手机快捷指令（方案二：手机点一下）

#### iPhone (iOS 快捷指令)

1. 打开「快捷指令」App → 新建快捷指令
2. 搜索并添加「获取 URL 内容」操作
3. 设置：
   - URL: `https://api.github.com/repos/YOUR_USERNAME/bedtime-stories/actions/workflows/generate-stories.yml/dispatches`
   - 方法: `POST`
   - 请求头:
     - `Authorization`: `Bearer YOUR_GITHUB_PAT`（见下方获取 PAT）
     - `Accept`: `application/vnd.github+json`
   - 请求正文: `{"ref":"main"}`
4. 点击右上角 `...` → 「添加到主屏幕」
5. 命名为「故事生成」

#### 获取 GitHub PAT (Personal Access Token)

1. 打开 https://github.com/settings/tokens?type=beta （Fine-grained tokens）
2. 点击 `Generate new token`
3. 设置：
   - Token name: `bedtime-stories-trigger`
   - Expiration: 选 1 年或更长
   - Repository access: `Only select repositories` → 选 `bedtime-stories`
   - Permissions → Repository permissions:
     - `Actions`: `Read and write`
4. 点击 `Generate token`
5. 复制 token（格式：`github_pat_xxxxxxxx`）
6. 这个 token 只能触发该仓库的 Action，没有其他权限

#### Android 手机

1. 安装 `HTTP Shortcuts` App（Google Play 商店免费）
2. 新建快捷方式：
   - Method: `POST`
   - URL: 同上
   - Headers: 同上
   - Body: `{"ref":"main"}`
3. 保存后添加到桌面

## 使用方式

### 日常使用（电脑开着）

什么都不用做。WorkBuddy 每 2 小时自动检查，生成当天故事。
- 主链接（CloudStudio H5 阅读器）：由 WorkBuddy 自动更新
- 主链接（CloudStudio 合集页面）：由 WorkBuddy 自动更新

### 电脑没开时

**方式一：手机点一下**
- 点手机桌面上的「故事生成」图标
- 等 1-2 分钟
- 打开 GitHub Pages 链接看故事

**方式二：什么都不做**
- 每天 23:00 GitHub Action 会自动运行
- 第二天打开 GitHub Pages 链接就有新故事

## 链接汇总

| 链接 | 来源 | 更新方式 |
|------|------|----------|
| CloudStudio H5 阅读器 | WorkBuddy 本地 | 电脑开机时自动 |
| CloudStudio 合集页面 | WorkBuddy 本地 | 电脑开机时自动 |
| GitHub Pages H5 阅读器 | GitHub 云端 | Actions / 手机触发 |
| GitHub Pages 合集页面 | GitHub 云端 | Actions / 手机触发 |

## 技术细节

- **AI 模型**: 智谱 GLM-4V-Flash，OpenAI 兼容 API
- **费用**: GitHub Actions/Pages 免费（public 仓库），GLM-4V-Flash 模型免费
- **补跑机制**: 每次运行检查当天 + 最近 7 天，自动补生成遗漏的故事
- **年龄段**: 根据孩子生日（2026-09-22）自动计算并调整故事风格
- **风格**: 中文融合孙敬修/郑渊洁/冰波/张秋生/金波/汤素兰六位大师风格；英文融合 Dr. Seuss/芝麻街/Roald Dahl/Mark Twain/Robert McCloskey 五位大师风格
