from flask import Flask, request, jsonify
import json
import time
from util import get_score
import asyncio
import sqlite3
from elasticsearch import Elasticsearch


app = Flask(__name__)

@app.route('/')
def hello():
    return 'The service has been successfully started!'

@app.route('/upload', methods=['POST'])
async def upload():

    log_file_path ='upload_log.txt'

    # 获取 URL 参数 tag
    tag = request.args.get('tag')
    # 如果提供了tag参数，将其添加到日志文件名中
    if tag:
        log_file_path = f'upload_log_{tag}.txt'

    data_samples = request.get_json()
    # 校验 data_samples
    if not isinstance(data_samples, dict):
        return jsonify({'error': 'data_samples 必须是一个字典'}), 400
    
    required_keys = ['question', 'answer', 'contexts', 'ground_truth']
    for key in required_keys:
        if key not in data_samples:
            return jsonify({'error': f'data_samples 缺少必要的键: {key}'}), 400
        if not isinstance(data_samples[key], list):
            return jsonify({'error': f'{key} 必须是一个列表'}), 400
    
    # if not all(len(data_samples[key]) == len(data_samples['question']) for key in required_keys):
    #     return jsonify({'error': '所有列表的长度必须相同'}), 400
    
    if len(data_samples['question']) == 0:
        return jsonify({'error': 'data_samples 不能为空'}), 400
    
    for i, context in enumerate(data_samples['contexts']):
        if not isinstance(context, list):
            return jsonify({'error': f'contexts[{i}] 必须是一个列表'}), 400
    
    # 获取当前时间戳
    timestamp = time.time()
    
    # 将时间戳格式化为可读的日期时间字符串
    datetime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

    score = await get_score(data_samples)

    data = {
        'score': score,
        'data_samples': data_samples,
        'datetime': datetime_str,
    }

    try:        
        # 将 JSON 数据写入文件
        with open(log_file_path, "a") as f:
            json.dump(data, f)
            f.write('\n')  # 添加换行符
        print(f"成功写入日志到 {log_file_path}")

        # # 将 JSON 数据存入本地SQLite
        # conn = sqlite3.connect('data.db')
        # c = conn.cursor()
        # c.execute("INSERT INTO logs (data) VALUES (?)", (json.dumps(data),))
        # conn.commit()
        # conn.close()
        # print("成功将数据存入本地SQLite")


        # # 创建 Elasticsearch 客户端
        # es = Elasticsearch()

        # # 将数据存储在 Elasticsearch 中
        # es.index(index='data_samples', body=data)
    except Exception as e:
        print(f"写入日志时发生错误: {str(e)}")
        return jsonify({'error': '无法写入日志文件'}), 500

    
    # 返回响应
    return jsonify(score), 200
    # return jsonify({'message': 'Data samples uploaded successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()