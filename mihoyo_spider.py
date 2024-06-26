import json

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from items import Image
import re

import static


class mihomoSpider(scrapy.Spider):
    name = "mihomo"
    allowed_domains = []
    m_url = static.mihomo_urls.get("wallpaper")
    start_urls = []
    for i in range(1, 30):
        start_urls.append(m_url.replace("iPage=1", "iPage=" + str(i)))

    def parse(self, response):
        # 豆瓣页面的标题通常在<h1>标签内，但可能需要根据实际页面结构调整选择器)
        # resList = response.css("script::text").getall()
        res = json.loads(response.body)
        resList = res.get("data").get("list")
        items = []
        for child in resList:
            line = child.get("sExt")
            img_url = re.findall(r'(https:[^ ]*.[png|jpg|png|jpeg])', line)
            img_url = img_url[0]
            item = Image()
            item['image_urls'] = [img_url,]
            item['name'] = str(static.cnt) + ".png"
            items.append(item)
        static.cnt += 1
        return items


def setting():
    settings = get_project_settings()
    settings.update({
        'ITEM_PIPELINES': {"pipelines.MyImagesPipeline": 1},
        'IMAGES_STORE': './images',
        'USER_AGENT': 'Mozilla/5.0 (compatible; DoubanBookSpider/1.0)',
        'DOWNLOAD_DELAY ': '2',
        'CLOSESPIDER_PAGECOUNT ': '999'
    })
    return settings


def main():
    process = CrawlerProcess(setting())
    process.crawl(mihomoSpider)
    process.start()  # the script will block here until all crawling jobs are finished


if __name__ == "__main__":
    main()
