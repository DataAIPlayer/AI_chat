# AI_chat

## 启动服务
- 创建容器
    ```
    cd backend
    docker build -t my_chatgpt_app .
    docker run -d -p 80:80 -p 443:443 -e certbot_email=YOUR_EMAIL -e your_domain=YOUR_DOMAIN -e OPENAI_API_KEY=sk-xxxxxxx my_chatgpt_app
    ```