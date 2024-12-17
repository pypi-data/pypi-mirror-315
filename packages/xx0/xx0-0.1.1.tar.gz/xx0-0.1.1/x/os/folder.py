import os


class Folder:

    @property
    def folder_name(self) -> str:
        """获取文件夹的名字"""
        return os.path.basename(self.path)

    def __init__(self, path: str):
        """初始化文件夹类，设置文件夹路径"""
        self.path: str = path

    def create(self) -> None:
        """创建文件夹"""
        try:
            os.makedirs(self.path, exist_ok=True)  # 如果文件夹已存在，则不抛出异常
            print(f"文件夹 '{self.path}' 创建成功。")
        except Exception as e:
            print(f"创建文件夹时出错: {e}")

    def delete(self) -> None:
        """删除文件夹"""
        try:
            os.rmdir(self.path)  # 仅删除空文件夹
            print(f"文件夹 '{self.path}' 删除成功。")
        except Exception as e:
            print(f"删除文件夹时出错: {e}")



    def list_files(self) -> list:
        """列出文件夹中的文件"""
        try:
            files: list = os.listdir(self.path)
            print(f"文件夹 '{self.path}' 中的文件: {files}")
            return files
        except Exception as e:
            print(f"列出文件时出错: {e}")
            return []
