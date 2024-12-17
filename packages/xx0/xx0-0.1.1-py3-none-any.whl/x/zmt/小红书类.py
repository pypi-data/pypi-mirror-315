from playwright.sync_api import Page,sync_playwright
from x.browser.xpage import XPage


class 小红书类:
    def __init__(self,page:Page):
        self.page = XPage(page)

    def 打开小红书(self):

        self.page = self.browser.new_page()
        self.page.goto("https://www.xiaohongshu.com/")

if __name__ == "__main__":

    小红书 = 小红书类()
    小红书.打开小红书()