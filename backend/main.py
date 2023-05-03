# coding: utf-8

from fastapi import FastAPI
import json
import random
import openai
import os
from pydantic import BaseModel
from typing import List

app = FastAPI()

openai_api_key=os.environ['OPENAI_API_KEY']

class message(BaseModel):
    msg:str
    sender:str

@app.post("/chat")
def gpt_chat(mess: List[message]):
    openai.api_key = openai_api_key
    system_msg = [
        {"role": "system", "content": "你是一位非常有帮助的人类助理"},
    ]
    completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = system_msg + mess
    )
    res = {
            "res":completion,
            "code":200
            }
    return res