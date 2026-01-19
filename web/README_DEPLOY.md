# 快速部署指南 - 我应该上传什么？

## 🎯 简单回答

**只上传 `web/` 目录到GitHub！**

这是最佳实践，原因：
- ✅ 代码干净，只包含Web应用
- ✅ 上传快，不包含大型数据文件
- ✅ 符合部署平台要求

---

## 📋 具体操作

### 方式1: 创建独立的Web仓库（推荐）⭐

```bash
# 1. 进入web目录
cd web

# 2. 初始化Git仓库
git init

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Initial commit: Fin-Agent Web Frontend"

# 5. 在GitHub创建新仓库（如：fin-agent-web）

# 6. 连接并推送
git remote add origin https://github.com/your-username/fin-agent-web.git
git branch -M main
git push -u origin main
```

### 方式2: 上传整个项目（需要配置）

如果必须上传整个项目：

1. **确保 .gitignore 正确配置**（忽略outputs/、data/等）
2. **在部署平台设置Root Directory为 `web`**
   - Railway: Settings → Root Directory → `web`
   - Render: Root Directory → `web`

---

## ✅ 需要上传的文件（web目录）

```
web/
├── app.py              ✅ 必须
├── requirements.txt    ✅ 必须
├── Procfile           ✅ 必须（部署用）
├── runtime.txt        ✅ 必须（Python版本）
├── Dockerfile         ✅ 可选（Docker部署）
├── fly.toml           ✅ 可选（Fly.io部署）
├── templates/         ✅ 必须
│   ├── base.html
│   ├── index.html
│   └── detail.html
└── static/            ✅ 必须
    └── css/
        └── style.css
```

---

## ❌ 不要上传的

- `outputs/` - 数据文件（可能很大）
- `data/` - 原始数据
- `.env` - 敏感信息
- `__pycache__/` - Python缓存

---

## 🚀 部署平台配置

### Railway.app
1. 连接到GitHub仓库
2. 如果上传了整个项目，设置 Root Directory = `web`
3. 如果只上传了web目录，直接部署即可

### Render.com
1. 连接到GitHub仓库  
2. Root Directory: `web`（如果上传了整个项目）
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

---

## 📝 总结

**推荐：创建新仓库，只上传web目录**

这样：
- ✅ 仓库干净
- ✅ 部署简单
- ✅ 维护方便
- ✅ 不暴露敏感数据

详细说明请查看 `DEPLOY_GUIDE.md`
