from playwright.sync_api import Page

class XPage:
    def __init__(self, page: Page):
        self._page = page

    def __getattr__(self, name):
        """代理未实现的方法到原始 page 对象"""
        return getattr(self._page, name)

    def click(self, selector: str, **kwargs) -> None:
        """扩展点击方法"""
        print(f"点击元素: {selector}")
        self._page.click(selector, **kwargs)

    def my_custom_action(self, selector: str):
        """添加新的自定义方法"""
        self._page.hover(selector)
        self._page.click(selector)

