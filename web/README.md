# Fin-Agent Web 可视化前端

这是一个基于Flask的Web前端系统，用于可视化展示金融观点挖掘与回测系统的分析结果。

## 功能特性

- 📊 **运行记录列表**: 查看所有分析运行的记录
- 📈 **性能可视化**: 多种图表展示胜率、收益等指标
- 📋 **详细报告**: 查看完整的交易明细和绩效分析
- 🎨 **现代化UI**: 基于Bootstrap 5的美观界面
- 📱 **响应式设计**: 支持桌面和移动设备

## 安装依赖

```bash
pip install -r web/requirements.txt
```

## 运行服务器

```bash
cd web
python app.py
```

然后在浏览器中访问: http://127.0.0.1:5000

## 使用说明

1. **查看运行记录**: 主页显示所有分析运行的列表，包括用户、时间、交易次数、胜率等关键信息

2. **查看详情**: 点击"查看详情"按钮进入详细分析页面，包括：
   - 关键统计指标卡片
   - 绩效分析图表
   - 胜率分布饼图
   - 收益率分布直方图
   - 绩效报告表格
   - 交易明细表格

## API接口

系统提供以下REST API接口：

- `GET /api/runs` - 获取所有运行记录列表
- `GET /api/run/<run_id>/summary` - 获取运行摘要信息
- `GET /api/run/<run_id>/performance` - 获取绩效数据
- `GET /api/run/<run_id>/trades` - 获取交易明细（最多1000条）
- `GET /api/run/<run_id>/signals` - 获取提取的信号
- `GET /api/run/<run_id>/ticker_stats` - 获取标的统计
- `GET /api/run/<run_id>/images/<filename>` - 获取图片资源

## 技术栈

- **后端**: Flask (Python)
- **前端**: HTML5, CSS3, JavaScript
- **UI框架**: Bootstrap 5
- **图表库**: Chart.js
- **图标**: Bootstrap Icons

## 项目结构

```
web/
├── app.py              # Flask应用主文件
├── requirements.txt    # Python依赖
├── README.md          # 说明文档
├── templates/         # HTML模板
│   ├── base.html      # 基础模板
│   ├── index.html     # 主页
│   └── detail.html    # 详情页
└── static/           # 静态资源
    ├── css/
    │   └── style.css  # 自定义样式
    └── js/            # JavaScript文件（如需要）
```

## 注意事项

1. 确保 `outputs/` 目录下有分析结果文件
2. 系统会自动读取 `outputs/` 目录下的所有运行记录
3. 大文件（如超过1000条交易记录）会被限制显示数量以提升性能
