"""
Flask Web应用 - 金融观点挖掘与回测系统可视化前端
"""
import os
import json
import pandas as pd
from flask import Flask, render_template, jsonify, send_from_directory
from datetime import datetime
import glob

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 支持中文JSON

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, 'outputs')
DATA_DIR = os.path.join(BASE_DIR, 'data')


def get_all_runs():
    """获取所有运行记录"""
    runs = []
    if not os.path.exists(OUTPUTS_DIR):
        return runs
    
    for run_dir in os.listdir(OUTPUTS_DIR):
        run_path = os.path.join(OUTPUTS_DIR, run_dir)
        if not os.path.isdir(run_path):
            continue
        
        # 解析目录名：用户名_年份_run_时间戳 或 用户名_run_时间戳
        parts = run_dir.split('_run_')
        if len(parts) != 2:
            continue
        
        username_part = parts[0]
        timestamp = parts[1]
        
        # 尝试提取用户名（去掉可能的年份后缀，如_2025）
        # 如果最后部分是4位数字，则去掉
        if '_' in username_part:
            name_parts = username_part.rsplit('_', 1)
            if name_parts[1].isdigit() and len(name_parts[1]) == 4:
                username = name_parts[0]
            else:
                username = username_part
        else:
            username = username_part
        
        # 获取运行信息
        run_info = {
            'id': run_dir,
            'username': username,
            'timestamp': timestamp,
            'path': run_path,
            'created_at': timestamp
        }
        
        # 尝试读取performance_report.csv获取统计信息
        perf_csv = os.path.join(run_path, 'performance_report.csv')
        if os.path.exists(perf_csv):
            try:
                df = pd.read_csv(perf_csv, header=None)
                # 查找Total All行
                total_rows = df[df.iloc[:, 0].astype(str).str.contains('Total', na=False) & 
                               df.iloc[:, 1].astype(str).str.contains('All', na=False)]
                if not total_rows.empty:
                    row = total_rows.iloc[0]
                    try:
                        run_info['total_trades'] = int(float(row.iloc[2])) if pd.notna(row.iloc[2]) else 0
                    except (ValueError, TypeError):
                        run_info['total_trades'] = 0
                    win_rate_str = str(row.iloc[3]) if pd.notna(row.iloc[3]) else '0%'
                    run_info['win_rate'] = win_rate_str
                    # 计算胜率数值用于判断颜色
                    try:
                        win_rate_num = float(win_rate_str.replace('%', ''))
                        run_info['win_rate_class'] = 'success' if win_rate_num >= 50 else 'danger'
                    except (ValueError, TypeError):
                        run_info['win_rate_class'] = 'danger'
                    
                    avg_return_str = str(row.iloc[4]) if pd.notna(row.iloc[4]) else '0%'
                    run_info['avg_return'] = avg_return_str
                    # 计算收益数值用于判断颜色
                    try:
                        return_num = float(avg_return_str.replace('%', ''))
                        run_info['avg_return_class'] = 'success' if return_num >= 0 else 'danger'
                    except (ValueError, TypeError):
                        run_info['avg_return_class'] = 'danger'
            except Exception as e:
                pass  # 静默失败，使用默认值
        
        runs.append(run_info)
    
    # 按时间戳倒序排列
    runs.sort(key=lambda x: x['timestamp'], reverse=True)
    return runs


@app.route('/')
def index():
    """主页 - 显示所有运行记录"""
    runs = get_all_runs()
    return render_template('index.html', runs=runs)


@app.route('/run/<run_id>')
def run_detail(run_id):
    """运行详情页"""
    run_path = os.path.join(OUTPUTS_DIR, run_id)
    if not os.path.exists(run_path):
        return "运行记录不存在", 404
    
    return render_template('detail.html', run_id=run_id)


@app.route('/api/runs')
def api_runs():
    """API: 获取所有运行列表"""
    runs = get_all_runs()
    return jsonify(runs)


@app.route('/api/search/<path:username>')
def api_search_user(username):
    """API: 根据用户名搜索运行记录
    
    支持中文用户名，使用path转换器来处理URL编码
    """
    from urllib.parse import unquote
    
    # 解码URL编码的用户名
    username = unquote(username)
    all_runs = get_all_runs()
    
    # 搜索匹配的用户名（不区分大小写，支持部分匹配）
    username_lower = username.lower().strip()
    matched_runs = [
        run for run in all_runs 
        if username_lower in run.get('username', '').lower()
    ]
    
    if not matched_runs:
        return jsonify({
            'error': f'未找到用户名 "{username}" 的运行记录',
            'username': username,
            'runs': [],
            'count': 0
        }), 404
    
    return jsonify({
        'username': username,
        'runs': matched_runs,
        'count': len(matched_runs)
    })


@app.route('/api/run/<run_id>/summary')
def api_run_summary(run_id):
    """API: 获取运行摘要信息"""
    run_path = os.path.join(OUTPUTS_DIR, run_id)
    if not os.path.exists(run_path):
        return jsonify({'error': 'Run not found'}), 404
    
    summary = {
        'id': run_id,
        'path': run_path
    }
    
    # 读取performance_report.csv
    perf_csv = os.path.join(run_path, 'performance_report.csv')
    if os.path.exists(perf_csv):
        try:
            df = pd.read_csv(perf_csv, header=None)
            summary['performance_report'] = df.to_dict('records')
        except Exception as e:
            summary['performance_error'] = str(e)
    
    # 读取full_report.md的前几行获取基本信息
    report_md = os.path.join(run_path, 'full_report.md')
    if os.path.exists(report_md):
        try:
            with open(report_md, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]
                for line in lines:
                    if '**用户**:' in line:
                        summary['username'] = line.split('**用户**:')[1].strip()
                    elif '**运行时间**:' in line:
                        summary['run_time'] = line.split('**运行时间**:')[1].strip()
                    elif '**总耗时**:' in line:
                        summary['duration'] = line.split('**总耗时**:')[1].strip()
                    elif '**总信号数**:' in line:
                        summary['total_signals'] = line.split('**总信号数**:')[1].strip()
        except Exception as e:
            pass
    
    return jsonify(summary)


@app.route('/api/run/<run_id>/performance')
def api_run_performance(run_id):
    """API: 获取绩效数据"""
    run_path = os.path.join(OUTPUTS_DIR, run_id)
    perf_csv = os.path.join(run_path, 'performance_report.csv')
    
    if not os.path.exists(perf_csv):
        return jsonify({'error': 'Performance report not found'}), 404
    
    try:
        df = pd.read_csv(perf_csv, header=None)
        # 转换为字典格式（跳过第一行，如果是表头）
        data = []
        start_idx = 0
        
        # 检查第一行是否为表头（第一列为空或包含'Total_Trades'）
        if len(df) > 0:
            first_col = str(df.iloc[0, 0]) if pd.notna(df.iloc[0, 0]) else ''
            second_col = str(df.iloc[0, 1]) if len(df.columns) > 1 and pd.notna(df.iloc[0, 1]) else ''
            # 如果第一列是空且第二列是'Total_Trades'，或者第二列包含'Total_Trades'，则跳过第一行
            if first_col == '' or 'Total_Trades' in second_col:
                start_idx = 1
        
        for idx in range(start_idx, len(df)):
            row = df.iloc[idx]
            if len(row) < 6:
                continue
            
            # 安全地转换数据
            try:
                category = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ''
                window = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ''
                
                # 尝试转换total_trades为数字
                try:
                    total_trades = int(float(row.iloc[2])) if pd.notna(row.iloc[2]) else 0
                except (ValueError, TypeError):
                    # 如果不是数字，跳过这一行
                    continue
                
                win_rate = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else '0%'
                avg_return = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else '0%'
                avg_alpha = str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else '0%'
                
                data.append({
                    'category': category,
                    'window': window,
                    'total_trades': total_trades,
                    'win_rate': win_rate,
                    'avg_return': avg_return,
                    'avg_alpha': avg_alpha
                })
            except (IndexError, ValueError, TypeError) as e:
                # 跳过有问题的行
                continue
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/run/<run_id>/trades')
def api_run_trades(run_id):
    """API: 获取交易明细"""
    run_path = os.path.join(OUTPUTS_DIR, run_id)
    trades_csv = os.path.join(run_path, 'backtest_results.csv')
    
    if not os.path.exists(trades_csv):
        return jsonify({'error': 'Trades file not found'}), 404
    
    try:
        df = pd.read_csv(trades_csv)
        # 限制返回数量，避免数据过大
        df = df.head(1000)
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/run/<run_id>/signals')
def api_run_signals(run_id):
    """API: 获取提取的信号"""
    run_path = os.path.join(OUTPUTS_DIR, run_id)
    signals_json = os.path.join(run_path, 'extracted_signals.json')
    
    if not os.path.exists(signals_json):
        return jsonify({'error': 'Signals file not found'}), 404
    
    try:
        with open(signals_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/run/<run_id>/ticker_stats')
def api_run_ticker_stats(run_id):
    """API: 获取标的统计"""
    run_path = os.path.join(OUTPUTS_DIR, run_id)
    stats_json = os.path.join(run_path, 'ticker_statistics.json')
    
    if not os.path.exists(stats_json):
        return jsonify({'error': 'Ticker statistics not found'}), 404
    
    try:
        with open(stats_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/run/<run_id>/images/<filename>')
def api_run_image(run_id, filename):
    """API: 获取图片资源"""
    run_path = os.path.join(OUTPUTS_DIR, run_id)
    # 尝试多个可能的图片目录
    image_dirs = [
        os.path.join(run_path, 'cross_validation', 'plots'),
        os.path.join(run_path, 'plots'),
        run_path
    ]
    
    for img_dir in image_dirs:
        if os.path.exists(os.path.join(img_dir, filename)):
            return send_from_directory(img_dir, filename)
    
    return jsonify({'error': 'Image not found'}), 404


if __name__ == '__main__':
    # 从环境变量获取端口，如果没有则使用5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"启动Web服务器...")
    print(f"输出目录: {OUTPUTS_DIR}")
    print(f"访问地址: http://0.0.0.0:{port}")
    print(f"调试模式: {debug}")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
