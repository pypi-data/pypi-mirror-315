import google.generativeai as genai

class Gemini:
    """Gemini AI 助手类"""

    def __init__(self, api_key: str):
        """初始化 Gemini

        Args:
            api_key: Google AI API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("文本嵌入 004")

    async def chat(self, prompt: str) -> str:
        """与 Gemini 进行对话

        Args:
            prompt: 用户输入的提示词

        Returns:
            str: Gemini 的回复
        """
        response = await self.model.generate_content_async(prompt)
        return response.text

    async def stream_chat(self, prompt: str):
        """与 Gemini 进行流式对话

        Args:
            prompt: 用户输入的提示词

        Yields:
            str: Gemini 的实时回复片段
        """
        response = await self.model.generate_content_async(
            prompt,
            stream=True
        )
        async for chunk in response:
            if chunk.text:
                yield chunk.text


if __name__ == "__main__":
    import asyncio
    import os

    async def main():
        # 从环境变量获取 API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("请先设置环境变量 GOOGLE_API_KEY")
            return

        # 创建 Gemini 实例
        gemini = Gemini(api_key)

        # # 测试普通对话
        # response = await gemini.chat("你好,请介绍一下自己")
        # print("\n=== 普通对话测试 ===")
        # print(f"AI: {response}")

        # 测试流式对话
        print("\n=== 开始对话 ===")

        while True:
            # 获取用户输入
            user_input = input("\n你: ")

            # 检查是否退出
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("再见!")
                break

            print("AI: ", end="", flush=True)
            async for chunk in gemini.stream_chat(user_input):
                print(chunk, end="", flush=True)

    # 运行测试
    asyncio.run(main())
