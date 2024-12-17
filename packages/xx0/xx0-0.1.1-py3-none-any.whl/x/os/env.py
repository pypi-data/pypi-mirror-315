import os
import dotenv

class Env:
    def __init__(self, env_key: str):
        """初始化环境变量类

        Args:
            env_file: 环境变量文件路径,如果不传则使用系统环境变量
        """
        dotenv.load_dotenv()
        self.env_key = env_key
    def get(self) -> str:
        """获取环境变量"""
        return os.getenv(self.env_key)

    def set(self, value: str):
        """设置系统级环境变量"""
        os.environ[self.env_key] = value
