# 使用Python作为基础映像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制应用代码到容器中
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

# 安装依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用的端口
EXPOSE 8000

# 设置环境变量
ENV OPENAI_API_KEY=YOUR_API_KEY
ENV USERNAME=admin
ENV PASSWORD=password

# 运行应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

