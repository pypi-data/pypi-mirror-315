import os


class Path:
    def __init__(self, 绝对路径: str):
        """初始化路径类

        Args:
            绝对路径: 文件或文件夹的绝对路径
            example:
                Path('C:/Users/Administrator/Desktop/test.txt')
        """
        self.绝对路径 = os.path.abspath(绝对路径)

    @property
    def 文件名(self) -> str:
        """获取路径中的文件名"""
        return os.path.basename(self.绝对路径)

    @property
    def 所在文件夹(self) -> str:
        """获取路径所在的文件夹路径"""
        return os.path.dirname(self.绝对路径)

    def 是否存在(self) -> bool:
        """判断路径是否存在"""
        return os.path.exists(self.绝对路径)

    def 是否是文件(self) -> bool:
        """判断是否为文件"""
        return os.path.isfile(self.绝对路径)

    def 是否是文件夹(self) -> bool:
        """判断是否为文件夹"""
        return os.path.isdir(self.绝对路径)

    def __str__(self) -> str:
        return self.绝对路径

    def __repr__(self) -> str:
        return f"Path('{self.绝对路径}')"



