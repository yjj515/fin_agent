#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动Web服务器的便捷脚本
"""
import sys
import os

# 确保项目根目录在Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("Fin-Agent Web 可视化系统")
    print("=" * 60)
    print(f"项目目录: {parent_dir}")
    print(f"输出目录: {os.path.join(parent_dir, 'outputs')}")
    print(f"访问地址: http://127.0.0.1:5000")
    print("=" * 60)
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
