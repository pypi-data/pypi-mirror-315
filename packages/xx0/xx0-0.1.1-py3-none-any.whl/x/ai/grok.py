from openai import OpenAI
import os
import x.os.shell as s
import json

def grok(prompt: str):
    json_data = {
        "messages": [
            {
                "role": "system",
                "content": "你是一个专业的新闻助手,擅长总结和分析新闻。请用简洁专业的语言回答问题。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "grok-beta",
        "stream": False,
        "temperature": 0
    }

    # 使用 json.dumps 序列化数据，并使用单引号包裹
    curl_command = f"""curl https://api.x.ai/v1/chat/completions \
                   -H "Content-Type: application/json" \
                   -H "Authorization: Bearer xai-AI5OkvGd9qLINnMiKveqxR8O4T5B9IDSigqrpPXNX3zvlma0U58nxxri3dHtiziuhKqued0TQz9an8Jy" \
                   -d '{json.dumps(json_data)}'"""

    return s.cmd(curl_command)

if __name__ == "__main__":
    grok("grok 的收费标准?")

'''
XAI_API_KEY = os.getenv("XAI_API_KEY")
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

completion = client.chat.completions.create(
    model="grok-beta",
    messages=[
        {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."},
        {"role": "user", "content": "What is the meaning of life, the universe, and everything?"},
    ],
)

print(completion.choices[0].message)
'''