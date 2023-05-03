# 使用官方 Python 基础镜像
FROM python:3.9 AS builder

# 设置工作目录
WORKDIR /app

# 将 requirements.txt 文件复制到工作目录
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 将应用代码复制到工作目录
COPY . .

# 使用多阶段构建减小镜像大小
FROM python:3.9-slim

# 安装 Nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# 将工作目录设置为 /app
WORKDIR /app

# 复制依赖和代码到新的镜像中
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app .

# 复制 Nginx 配置文件
COPY nginx.conf /etc/nginx/sites-available/default

# 暴露端口
EXPOSE 80

# 启动 Nginx 和 Uvicorn
CMD ["bash", "-c", "nginx && uvicorn main:app --host 0.0.0.0 --port 9140"]