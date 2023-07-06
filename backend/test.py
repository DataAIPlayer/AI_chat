# code: utf-8
  
import requests
import json
import asyncio
import websockets
import sys
import openai

your_domain = sys.argv[1]

chat_link = f'https://{your_domain}/chat'

stream_link = f'https://{your_domain}/stream_chat'

ws_link = f"wss://{your_domain}/ws"

# azure openai
def chat(model = "gpt35-16k"):
    openai.api_type = "azure"
    openai.api_key = "..."
    openai.api_base = your_domain
    openai.api_version = "2023-05-15"
    messages = [{"role":"system","content":"You are an AI assistant that helps people find information."}, {'content':'介绍一下你自己', 'role':'user'}]
    completion = openai.ChatCompletion.create(
    deployment_id = model,
    messages = messages,
    stream=True
    )
    for resp in completion:
        role = resp["choices"][0]["delta"].get("role", 'assistant')
        token = resp["choices"][0]["delta"].get("content", "")
        print(token, flush=True)

def test_https():
    headers = {'Content-type': 'application/json'}
    data = [{'msg':'介绍一下你自己？', 'sender':'user'}]
    data = json.dumps(data, ensure_ascii=False).encode('utf-8')

    # response = requests.post(chat_link,
    #                         data=data,
    #                         headers=headers)

    # print(response.json())


    response = requests.post(stream_link,
                            data=data,
                            headers=headers,
                            stream=True)

    response.raise_for_status()

    for line in response.iter_lines():
        print(line.decode('utf-8'), end='', flush=True)

async def test_connect():
    uri = ws_link
    async with websockets.connect(uri) as websocket:
        # 创建你的消息内容
        data = [{'msg':'介绍一下你自己？', 'sender':'user'}]
        
        # 发送消息到WebSocket服务器
        await websocket.send(json.dumps(data))

        # 接收并打印服务器的响应
        while True:
            response = await websocket.recv()
            print(json.loads(response), end='', flush=True)

# 运行测试函数
if __name__ == "__main__":
    # test_https()
    # asyncio.get_event_loop().run_until_complete(test_connect())
    chat()