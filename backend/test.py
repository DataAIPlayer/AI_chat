# code: utf-8
  
import requests
import json

headers = {'Content-type': 'application/json'}
data = [{'msg':'hello, who are you?', 'sender':'user'}]
data = json.dumps(data, ensure_ascii=False).encode('utf-8')

link = 'your_domain/chat'

response = requests.post(link,
                        data=data,
                        headers=headers).json()
print(response)