# coding=utf-8

import urllib2
import re


class QiushibaikeCrawler:

    # 初始化方法
    def __init__(self):
        self.total_page = 35
        self.url_without_page = "http://www.qiushibaike.com/8hr/page/"
        self.headers = {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",  # 伪装成浏览器
            "Referer": "http://www.qiushibaike.com"  # 对付“防盗链”
        }
        self.enable = False
        self.page = 0
        self.stories = [[] for i in range(self.total_page)]

    # 启动
    def start(self):
        print u"欢迎进入糗事百科爬虫系统！\n\n操作指南：\n\tEnter:\t查看新段子\n\tQ:\t退出"

        self.enable = True
        while self.enable:
            self.crawl_one_page()
            self.monitor_input_then_response()

    # 爬取 page 页的段子
    def crawl_one_page(self):
        if self.page == self.total_page:
            print u"已爬完所有段子，即将自动退出，再见！"
            self.enable = False
            return

        request = urllib2.Request(self.url_without_page + str(self.page + 1), headers=self.headers)  # 创建请求
        response = urllib2.urlopen(request)  # 发出请求
        document = response.read().decode("utf-8")  # 获取整个 HTML 文档

        # 编译 Pattern
        pattern = re.compile(r'<div.*?author.*?<h2>(.*?)</h2>.*?<div.*?content.*?<span>(.*?)</span>(.*?)stats.*?<i.*?number">(.*?)</i>.*?<span.*?stats-comments.*?<i.*?number">(.*?)</i>', re.DOTALL)

        # 查找所有满足 Pattern 的子串
        results = re.findall(pattern, document)

        for m in results:
            have_img = re.search(r"img", m[2])  # 过滤掉带图片的段子
            if not have_img:
                text_without_br = self.replace_br(m[1])
                self.stories[self.page].append([m[0], text_without_br, m[3], m[4]])  # [作者, 段子, 赞的数量, 评论数量]

        # 页数加一
        self.page += 1

    # 替换 <br> 为 \n
    @staticmethod
    def replace_br(string_with_br):
        pattern = re.compile(r"<br.*?>")
        return re.sub(pattern, "\n", string_with_br)

    # 监测输入，并做出响应
    def monitor_input_then_response(self):
        for i in range(len(self.stories[self.page - 1])):
            command = raw_input()
            if command == "Q" or command == "q":
                print u"您已选择退出，再见！"
                self.enable = False
                return
            print self.stories[self.page - 1][i][0] + u"（收获 " + self.stories[self.page - 1][i][2] + u" 个赞和 " + self.stories[self.page - 1][i][3] + u" 个评论）："
            print self.stories[self.page - 1][i][1]


if __name__ == '__main__':
    qiushibaike_crawler = QiushibaikeCrawler()
    qiushibaike_crawler.start()
