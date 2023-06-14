# coding: utf-8

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
import json
import random
import openai
import os
from pydantic import BaseModel
from typing import List
from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiomysql

app = FastAPI()

openai_api_key=os.environ['OPENAI_API_KEY']

class message(BaseModel):
    msg:str
    sender:str

executor = ThreadPoolExecutor(max_workers=4)

# 创建数据库连接池
async def create_db_pool():
    loop = asyncio.get_event_loop()
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='root', password='pass',
                                      db='chat', loop=loop)
    return pool

def chat(mess, model = "gpt-3.5-turbo-0301", stream=False):
    openai.api_key = openai_api_key
    messages = [{"role": m.sender, "content": m.msg} for m in mess]
    completion = openai.ChatCompletion.create(
    model = model,
    messages = messages,
    stream=stream
    )
    return completion

# http模式
@app.post("/chat")
def gpt_chat(mess: List[message]):
    completion = chat(mess)
    res = {
            "res":completion,
            "code":200
            }
    return res

async def chat_stream(mess, model="gpt-3.5-turbo-0301"):

    # 获取一个事件循环
    loop = asyncio.get_event_loop()

    # 在另一个线程中运行 openai.ChatCompletion.create() 方法
    resp_future = loop.run_in_executor(executor, chat, mess, model, True)

    resp_gen = await resp_future

    # 从响应生成器中获取值并生成
    for resp in resp_gen:
        role = resp["choices"][0]["delta"].get("role", 'assistant')
        token = resp["choices"][0]["delta"].get("content", "")
        yield token.encode('utf-8') + b'\n'

# http流模式
@app.post("/stream_chat")
async def gpt_stream_chat(mess: List[message]):
    return StreamingResponse(chat_stream(mess), media_type="text/plain")

# websocket模式
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pool = await create_db_pool()
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)

            mess = [message(**d) for d in data]

            # 获取一个事件循环
            loop = asyncio.get_event_loop()
            # 在另一个线程中运行 openai.ChatCompletion.create() 方法
            resp_future = loop.run_in_executor(executor, chat, mess, "gpt-3.5-turbo-0301", True)

            resp_gen = await resp_future

            ret = ''

            # 从响应生成器中获取值并生成
            for resp in resp_gen:
                role = resp["choices"][0]["delta"].get("role", 'assistant')
                token = resp["choices"][0]["delta"].get("content", "")
                ret += token
                await websocket.send_text(json.dumps(token))

            data += [{'msg': ret, 'sender': 'assistant'}]
            data = json.dumps(data)
            try:
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("INSERT INTO user_qa (qa) VALUES (%s)", data)
                        await conn.commit()
            except Exception as e:
                print(f"Database error: {e}")
    except WebSocketDisconnect:
        await websocket.close()