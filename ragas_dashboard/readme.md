# Ragas Dashboard

Ragas Dashboard 是一个基于 Flask 的 Web 应用，用于评估问答系统的性能。它使用 Ragas 库来计算各种评估指标，如忠实度、答案正确性、上下文召回率和上下文精确度。

## 目录

1. [系统要求](#系统要求)
2. [安装步骤](#安装步骤)
3. [运行应用](#运行应用)
4. [使用方法](#使用方法)
5. [部署到服务器](#部署到服务器)


## 系统要求

- Python 3.12
- pip（Python 包管理器）
- 虚拟环境工具（推荐使用conda）

## 安装步骤

1. 创建并激活虚拟环境：
   ```
   conda create -n flask python=3.12 -y
   conda activate flask
   ```

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

## 运行应用

在开发环境中，使用以下命令启动应用：
```
flask run --debug
```


打开浏览器，访问 `http://127.0.0.1:5000` 来确定服务已经成功启动。

## 使用方法

1. 准备数据：
   准备包含问题、答案、上下文和真实答案的 JSON 数据。数据格式应如下：
   ```json
   {
     "question": ["问题1", "问题2", ...],
     "answer": ["答案1", "答案2", ...],
     "contexts": [["上下文1-1", "上下文1-2"], ["上下文2-1", "上下文2-2"], ...],
     "ground_truth": ["真实答案1", "真实答案2", ...]
   }
   ```

2. 发送数据：
   使用 POST 请求将准备好的 JSON 数据发送到 `/upload` 端点。可以使用 curl、Postman 或其他 API 测试工具。
   建议使用tag，请求`/upload?tag=test` 会生成相应tag的日志`upload_log_test.txt`。

3. 查看结果：
   服务器将处理数据并返回评估结果。结果将包含各项评估指标的分数。

4. 日志查看：
   评估结果会被记录在 `upload_log.txt` 文件中，您可以查看此文件以获取历史评估记录。

## 部署到服务器

使用 Gunicorn（推荐）

1.安装 Gunicorn：

```
pip install gunicorn
```

2. 运行 Gunicorn：

```
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```