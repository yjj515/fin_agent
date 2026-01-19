# 部署指南 - Fin-Agent Web应用

本指南提供了多种方式将Flask应用部署到公网。

## 📦 部署前准备

### 1. 检查依赖

确保 `requirements.txt` 包含所有依赖：
```bash
cd web
pip install -r requirements.txt
```

### 2. 准备数据文件

确保 `outputs/` 目录包含分析结果数据（如果需要在服务器上使用）。

---

## 🚀 部署方案

### 方案1: Railway.app（推荐，最简单）

**优点**：
- ✅ 免费额度：每月$5（500小时运行时间）
- ✅ 自动部署（GitHub集成）
- ✅ 无需信用卡
- ✅ 简单易用

**步骤**：

1. **注册账户**
   - 访问 https://railway.app
   - 使用GitHub账户登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库

3. **配置项目**
   - Railway会自动检测到 `Procfile`
   - 设置环境变量（如果需要）：
     ```
     FLASK_ENV=production
     PORT=5000
     ```

4. **部署**
   - Railway会自动构建和部署
   - 等待部署完成，会获得一个 `.railway.app` 域名

5. **查看日志**
   - 在项目页面点击 "View Logs" 查看运行日志

**注意事项**：
- 免费版可能会在无活动15分钟后休眠
- 首次访问唤醒可能需要几秒钟

---

### 方案2: Render.com

**优点**：
- ✅ 永久免费（但有休眠限制）
- ✅ 自动HTTPS
- ✅ GitHub集成

**步骤**：

1. **注册账户**
   - 访问 https://render.com
   - 使用GitHub账户登录

2. **创建Web服务**
   - 点击 "New" → "Web Service"
   - 连接你的GitHub仓库

3. **配置服务**
   - **Name**: fin-agent-web
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Free

4. **环境变量**
   ```
   PYTHON_VERSION=3.11.7
   FLASK_ENV=production
   ```

5. **部署**
   - 点击 "Create Web Service"
   - 等待部署完成

**注意事项**：
- 免费版会在15分钟无活动后休眠
- 首次访问需要等待几秒钟唤醒

---

### 方案3: Fly.io

**优点**：
- ✅ 免费额度（需要信用卡验证）
- ✅ 全球边缘网络
- ✅ 快速响应

**步骤**：

1. **安装Fly CLI**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Mac/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **登录**
   ```bash
   fly auth login
   ```

3. **初始化项目**
   ```bash
   cd web
   fly launch
   ```

4. **配置**
   - 选择应用名称
   - 选择区域（推荐选择离你最近的）
   - 选择 "No" 不复制配置文件（我们手动创建）

5. **部署**
   ```bash
   fly deploy
   ```

6. **查看URL**
   ```bash
   fly open
   ```

---

### 方案4: 云服务器部署（阿里云/腾讯云/AWS等）

**优点**：
- ✅ 完全控制
- ✅ 无休眠限制
- ✅ 可以配置域名

**步骤**：

1. **购买服务器**
   - 选择Ubuntu 20.04或更高版本
   - 至少1GB内存

2. **SSH连接服务器**
   ```bash
   ssh root@your-server-ip
   ```

3. **安装依赖**
   ```bash
   # 更新系统
   apt update && apt upgrade -y
   
   # 安装Python和pip
   apt install -y python3.11 python3-pip python3-venv nginx
   
   # 安装Git
   apt install -y git
   ```

4. **上传代码**
   ```bash
   # 方式1: 使用Git
   cd /var/www
   git clone your-repo-url fin-agent-web
   cd fin-agent-web/web
   
   # 方式2: 使用scp从本地上传
   # 在本地执行：
   # scp -r web root@your-server-ip:/var/www/fin-agent-web/
   ```

5. **创建虚拟环境**
   ```bash
   cd /var/www/fin-agent-web/web
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **配置Gunicorn服务**
   ```bash
   # 创建systemd服务文件
   sudo nano /etc/systemd/system/fin-agent-web.service
   ```
   
   添加以下内容：
   ```ini
   [Unit]
   Description=Fin-Agent Web Application
   After=network.target
   
   [Service]
   User=root
   Group=root
   WorkingDirectory=/var/www/fin-agent-web/web
   Environment="PATH=/var/www/fin-agent-web/web/venv/bin"
   ExecStart=/var/www/fin-agent-web/web/venv/bin/gunicorn app:app --bind 0.0.0.0:5000 --workers 2 --timeout 120
   
   [Install]
   WantedBy=multi-user.target
   ```

7. **启动服务**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start fin-agent-web
   sudo systemctl enable fin-agent-web
   sudo systemctl status fin-agent-web
   ```

8. **配置Nginx反向代理**
   ```bash
   sudo nano /etc/nginx/sites-available/fin-agent-web
   ```
   
   添加以下内容：
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;  # 替换为你的域名或IP
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   
   启用配置：
   ```bash
   sudo ln -s /etc/nginx/sites-available/fin-agent-web /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

9. **配置防火墙**
   ```bash
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw allow 22
   sudo ufw enable
   ```

10. **配置SSL（可选，使用Let's Encrypt）**
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

---

### 方案5: Docker部署（通用方案）

**步骤**：

1. **构建镜像**
   ```bash
   cd web
   docker build -t fin-agent-web .
   ```

2. **运行容器**
   ```bash
   docker run -d \
     --name fin-agent-web \
     -p 5000:5000 \
     -v /path/to/outputs:/app/outputs \
     fin-agent-web
   ```

3. **使用Docker Compose（推荐）**
   
   创建 `docker-compose.yml`：
   ```yaml
   version: '3.8'
   
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       volumes:
         - ../outputs:/app/outputs
       environment:
         - FLASK_ENV=production
       restart: always
   ```
   
   运行：
   ```bash
   docker-compose up -d
   ```

---

## 🔧 常见问题

### Q1: 部署后无法访问？

**检查清单**：
- ✅ 端口是否正确开放（5000或环境变量PORT）
- ✅ 防火墙是否允许访问
- ✅ 应用日志是否有错误
- ✅ 环境变量是否正确设置

### Q2: 静态文件404错误？

确保 `static/` 和 `templates/` 目录都在 `web/` 目录下。

### Q3: 中文显示乱码？

确保：
- 文件使用UTF-8编码
- Flask配置 `app.config['JSON_AS_ASCII'] = False`

### Q4: 如何查看日志？

**Railway**: 项目页面 → View Logs  
**Render**: Dashboard → 服务 → Logs  
**云服务器**: `sudo journalctl -u fin-agent-web -f`

### Q5: 如何更新部署？

**Railway/Render**: 推送到GitHub会自动重新部署  
**云服务器**: 
```bash
cd /var/www/fin-agent-web/web
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart fin-agent-web
```

---

## 📝 推荐方案

- **快速测试/演示**: Railway.app
- **长期使用/生产环境**: 云服务器 + Nginx
- **需要全球加速**: Fly.io
- **容器化部署**: Docker + 云服务器

---

## 🔐 安全建议

1. **不要提交敏感信息**
   - 确保 `.env` 在 `.gitignore` 中
   - 使用环境变量存储敏感配置

2. **启用HTTPS**
   - 使用Let's Encrypt免费SSL证书
   - 或使用Cloudflare等CDN服务

3. **限制访问**
   - 配置防火墙规则
   - 使用Nginx限制IP访问（如需要）

4. **定期更新**
   - 保持依赖包最新
   - 定期更新系统补丁

---

## 📞 需要帮助？

如果遇到部署问题，请检查：
1. 应用日志
2. 服务器日志
3. 网络连接
4. 端口配置
