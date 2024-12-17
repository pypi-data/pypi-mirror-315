import os
import json
from openai import OpenAI
from x import *

XAI_API_KEY = Env("XAI_API_KEY").get()

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

completion = client.chat.completions.create(
    model="grok-beta",
    messages=[
        # 系统提示,定义AI角色和写作要求
        {"role": "system", "content":
         """
         你是一个世界上最顶级的专业的小说家。这个世界上每个人都敬佩你的小说创作能力 . 请写一个简短的爆款小说，要求：
         0. 开头几句话就要非常吸引读下去
        1. 故事要有吸引力和戏剧性
        2. 字数在200字以内
        3. 要有意想不到的结局
        4. 语言要简洁有力
        5. 最好带有一些悬疑或超自然元素
        6. 反转反转再反转
        7. 高潮迭起
        8. 不要写废话
        9. 不要写重复的文字
        10. 不要写重复的情节
        11. 不要写烂大街的情节
        12. 不要写俗套的情节
        13. 不要写俗套的人物
        14. 不要写俗套的对白
        15. 不要写俗套的结局


       严格按照以下JSON格式返回：
        {
            "title": "小说标题",
            "author": "AI作家",
            "word_count": 500,
            "tags": ["悬疑", "科幻"],
            "content": "小说正文",
            "summary": "故事梗概"
        }

        重要：必须返回有效的JSON格式！不要包含任何其他文字！
        """},
        # 用户提示,请求开始创作
        {"role": "user", "content": "请开始创作"},
    ],
    temperature=0.9,  # 控制输出的随机性  值越大创作性越强 , 0 的话  几乎每次输出都一样
    max_tokens=2000   # 限制生成文本的最大长度
)

# 获取返回的内容
response = completion.choices[0].message.content

# 解析JSON
try:
    # 尝试找到JSON的开始和结束位置
    json_start = response.find('{')
    json_end = response.rfind('}') + 1
    if json_start >= 0 and json_end > json_start:
        json_str = response[json_start:json_end]
        novel = json.loads(json_str)
        # 格式化输出JSON
        print(json.dumps(novel, ensure_ascii=False, indent=2))
    else:
        print("未找到有效的JSON格式")
        print("原始响应:", response)
except json.JSONDecodeError as e:
    print("JSON解析错误:", e)
    print("原始响应:", response)
