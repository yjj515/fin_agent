#!/bin/bash
# Fin-Agent Web 可视化系统启动脚本

echo "========================================"
echo "Fin-Agent Web 可视化系统"
echo "========================================"
echo ""

cd "$(dirname "$0")"
python3 run.py
