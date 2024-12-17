import os


class File:
    def __init__(self, 文件名路径, _file_: str = None):
        """
        路径可以为相对路径 文件不存在的话会询问是否创建
        @example
            from xx0.os import File
            file = File("test.txt", __file__)  # 创建文件对象
        """
        if _file_:
            self.绝对路径 = os.path.join(os.path.dirname(_file_), 文件名路径)
        else:
            self.绝对路径 = os.path.join(os.getcwd(), 文件名路径)
        if not os.path.exists(self.绝对路径):
            if input(f"文件 '{self.绝对路径}' 不存在,是否创建? (y/n):") == "y":
                with open(self.绝对路径, 'w', encoding='utf-8') as file:
                    file.write("")  # 创建空文件
            else:
                raise FileNotFoundError(f"文件 '{self.绝对路径}' 不存在")



    def read(self):
        """读取文件内容"""
        with open(self.绝对路径, 'r', encoding='utf-8') as file:
            return file.read()

    def write(self, content):
        """写入内容到文件"""
        with open(self.绝对路径, 'w', encoding='utf-8') as file:
            file.write(content)

    def append(self, 内容:str):
        """追加内容到文件"""
        with open(self.绝对路径, 'a', encoding='utf-8') as file:
            file.write(内容)
    add = append
    追加 = add

    def exists(self) -> bool:
        """判断文件是否存在"""
        return os.path.exists(self.绝对路径)
    判断存在 = exists

    def delete(self):
        """删除文件"""
        import os
        if os.path.exists(self.绝对路径):
            os.remove(self.绝对路径)
        else:
            print("文件不存在")

    删除 = delete
