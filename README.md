# AI_chat
基于大模型API（代码中使用的是ChatGPT 3.5），构建的多种后端服务

## 启动服务
- 创建容器
    ```
    cd backend
    docker build -t my_chatgpt_app .
    docker run -d -p 80:80 -p 443:443 -e certbot_email=YOUR_EMAIL -e your_domain=YOUR_DOMAIN -e OPENAI_API_KEY=sk-xxxxxxx my_chatgpt_app
    ```

## 功能
- 支持http请求
- 支持http流式请求
- 支持websocket请求
- 异步多线程
- 数据库存储问答记录