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