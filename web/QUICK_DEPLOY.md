# 快速部署指南

## 🚀 最快部署方式（Railway.app - 推荐）

### 步骤1: 准备代码
确保你的代码已经推送到GitHub仓库。

### 步骤2: 部署到Railway
1. 访问 https://railway.app
2. 使用GitHub登录
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择你的仓库
5. Railway会自动检测到 `Procfile` 并开始部署
6. 等待部署完成，获得 `.railway.app` 域名

### 步骤3: 访问应用
部署完成后，点击提供的URL即可访问！

**就这么简单！** 🎉

---

## 📋 其他快速部署选项

### Render.com（免费）
1. 访问 https://render.com
2. 注册并连接GitHub
3. 创建 "Web Service"
4. 选择仓库
5. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Fly.io（需要CLI）
```bash
# 安装CLI后
cd web
fly launch
fly deploy
```

---

## ⚠️ 注意事项

1. **数据文件**: 如果应用需要 `outputs/` 目录的数据，需要确保：
   - 数据文件包含在代码仓库中，或
   - 在部署平台上配置持久化存储

2. **环境变量**: 某些平台可能需要设置环境变量，参考 `DEPLOY.md`

3. **免费限制**: 
   - Railway: 每月$5免费额度
   - Render: 15分钟无活动后休眠
   - Fly.io: 需要信用卡验证

---

详细部署说明请查看 `DEPLOY.md`
