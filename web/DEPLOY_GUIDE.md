# GitHub上传指南

## 📦 应该上传什么？

### ✅ 推荐方案：只上传 `web/` 目录

**为什么？**
- ✅ 代码简洁，只包含必要文件
- ✅ 上传速度快
- ✅ 不会上传大型数据文件（outputs/）
- ✅ 符合最佳实践

### ❌ 不推荐：上传整个项目

**为什么不？**
- ❌ `outputs/` 目录可能很大（几百MB或GB）
- ❌ `data/` 目录包含用户数据，不应该上传
- ❌ 上传慢，占用仓库空间大
- ❌ 可能包含敏感信息

---

## 🚀 推荐步骤

### 方案1: 创建独立的Web仓库（推荐）

1. **创建新的GitHub仓库**
   - 仓库名：`fin-agent-web` 或 `fin-agent-frontend`
   
2. **只上传web目录**
   ```bash
   # 在项目根目录执行
   cd web
   git init
   git add .
   git commit -m "Initial commit: Fin-Agent Web Frontend"
   git branch -M main
   git remote add origin https://github.com/your-username/fin-agent-web.git
   git push -u origin main
   ```

3. **优势**
   - ✅ 仓库干净，只包含Web应用代码
   - ✅ 容易部署和维护
   - ✅ 不包含敏感数据

---

### 方案2: 上传整个项目，但忽略大文件

如果必须上传整个项目：

1. **检查 .gitignore 文件**

2. **确保忽略以下目录/文件**
   ```
   # 数据目录（不应上传）
   outputs/
   data/
   user_data/
   
   # Python缓存
   __pycache__/
   *.pyc
   *.pyo
   
   # 环境文件
   .env
   venv/
   env/
   
   # 大型模型文件
   *.bin
   *.safetensors
   *.pt
   *.pth
   ```

3. **只部署web目录**
   - Railway/Render可以指定子目录部署
   - 设置根目录为 `web/`

---

## 📝 部署平台配置

### Railway.app
1. 如果上传整个项目：
   - 在项目设置中找到 "Root Directory"
   - 设置为 `web`

2. 如果只上传web目录：
   - 直接部署，无需配置

### Render.com
1. 如果上传整个项目：
   - 在 "Root Directory" 中设置：`web`

2. 如果只上传web目录：
   - 无需配置

---

## 🔍 如何检查上传了什么

在GitHub仓库页面：
1. 查看文件列表
2. 确认没有 `outputs/`、`data/` 等大目录
3. 确认有 `web/` 目录下的所有文件：
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - `templates/`
   - `static/`

---

## ⚠️ 关于数据文件

### 问题：部署后没有数据怎么办？

**解决方案**：

1. **方案A: 数据文件单独处理**（推荐）
   - 数据文件不上传GitHub
   - 在部署平台配置持久化存储
   - 通过环境变量指定数据路径

2. **方案B: 数据文件打包上传**（小数据量时）
   - 将 `outputs/` 目录压缩
   - 上传到对象存储（如阿里云OSS、AWS S3）
   - 部署时下载解压

3. **方案C: 部署后生成数据**
   - 应用部署后，通过后端API生成数据
   - 数据存储在部署平台的持久化卷中

---

## 📋 完整上传清单

### 必须上传（web目录）：
- ✅ `app.py` - Flask应用
- ✅ `requirements.txt` - 依赖列表
- ✅ `Procfile` - 部署配置
- ✅ `runtime.txt` - Python版本
- ✅ `templates/` - HTML模板
- ✅ `static/` - CSS/JS文件
- ✅ `Dockerfile` - Docker配置（如果使用）
- ✅ `fly.toml` - Fly.io配置（如果使用）

### 可选上传：
- ✅ `README.md` - 说明文档
- ✅ `DEPLOY.md` - 部署文档

### 不应上传：
- ❌ `outputs/` - 数据文件
- ❌ `data/` - 原始数据
- ❌ `.env` - 环境变量（包含敏感信息）
- ❌ `__pycache__/` - Python缓存
- ❌ `*.log` - 日志文件

---

## 🎯 推荐操作流程

1. **创建新的GitHub仓库**（专门用于Web应用）
   ```
   仓库名: fin-agent-web
   描述: Fin-Agent Web可视化前端
   公开/私有: 根据需求选择
   ```

2. **初始化并上传web目录**
   ```bash
   cd web
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-username/fin-agent-web.git
   git push -u origin main
   ```

3. **在部署平台连接仓库**
   - Railway/Render连接到新创建的仓库
   - 自动部署

4. **配置数据存储**（如果需要）
   - 使用部署平台的持久化存储
   - 或通过API动态生成数据

---

## ❓ 常见问题

**Q: 如果我已经上传了整个项目怎么办？**

A: 
1. 在仓库设置中添加 `.gitignore`
2. 使用 `git rm --cached` 移除已跟踪的大文件
3. 或者创建新的仓库只上传web目录

**Q: 部署后如何访问数据？**

A: 需要将数据文件上传到部署平台或配置持久化存储。如果只是演示，可以先不上传数据，应用仍能运行（只是显示"暂无数据"）。

**Q: 可以同时维护两个仓库吗？**

A: 可以！
- 主项目仓库：包含完整代码和数据（私有）
- Web应用仓库：只包含web目录（可以公开）
