from github import Github as PyGithub, Auth

class GithubUser:
    """Github 用户基类"""

    def __init__(self, token: str):
        """
        初始化 Github 用户

        Args:
            token: Github 个人访问令牌
        """
        self.token = token
        self.github = PyGithub(auth=Auth.Token(token))

    @property
    def 用户名(self) -> str:
        """获取用户名称"""
        return self.github.get_user().name

    @property
    def 邮箱(self) -> str:
        """获取用户邮箱"""
        return self.github.get_user().email

    @property
    def 信息(self) -> dict:
        """获取用户信息字典"""
        return self.github.get_user()._rawData

    @property
    def 主页(self) -> str:
        """获取用户主页地址"""
        return self.github.get_user().html_url

    @property
    def __dict__(self) -> dict:
        """获取用户信息字典

        返回:
            dict: 用户信息字典,包含以下字段:
                - 用户名: 用户名称
                - 邮箱: 用户邮箱
                - 主页: 用户主页地址
                - 信息: 完整的用户信息字典
        """
        return {
            "用户名": self.用户名,
            "邮箱": self.邮箱,
            "主页": self.主页,
            "信息": self.信息
        }
