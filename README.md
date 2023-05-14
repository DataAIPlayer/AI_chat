# AI_chat

## 启动服务

- 设置环境变量
    ```
    export OPENAI_API_KEY=你的OpenAI api key
    ```

- 创建容器
    ```
    docker build -t my_chatgpt_app .
    docker run -p 80:80 my_chatgpt_app
    ```

- 准备https的域名，没有SSL证书，可以使用 Let's Encrypt 为域名颁发一个免费的 SSL 证书
    ```
    apt-get install -y certbot python3-certbot-nginx
    certbot --nginx -d yourdomain.com
    ```