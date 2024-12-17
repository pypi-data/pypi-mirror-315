from github import Github as PyGithub, Auth
from github.Repository import Repository
from typing import List

class Github:
    """Github API 的中文封装类"""
    def __init__(self, token: str):
        """
        初始化 Github 实例

        参数:
            token: Github 访问令牌
        """
        self.github = PyGithub(auth=Auth.Token(token))
        self.user = self.github.get_user()

    def get_repos(self) -> List[Repository]:
        """获取当前用户的所有仓库列表

        返回:
            List[Repository]: 仓库对象列表
        """
        return list(self.user.get_repos())

    def get_repo(self, repo_name: str) -> Repository:
        """获取指定的仓库

        参数:
            repo_name: 要获取的仓库名称

        返回:
            Repository: 仓库对象
        """
        return self.user.get_repo(repo_name)

    def create(self, name: str, description: str = None, private: bool = False,
              auto_init: bool = True, gitignore_template: str = None,
              license: str = f"mit") -> Repository:
        """创建一个新的仓库"""
        return self.user.create_repo(
            name=name,
            description=description,
            private=private,
            auto_init=auto_init,
            gitignore_template=gitignore_template,
            license_template=license
        )
    create_repo = create
