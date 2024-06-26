import scrapy
from scrapy.pipelines.images import ImagesPipeline


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        requests = []
        name = item.get('name')
        for image_url in item.get('image_urls', []):
                requests.append(scrapy.Request(image_url, meta={'name': name}))
        return requests

    def file_path(self, request, response=None, info=None, *, item=None):
        name = request.meta['name']
        image_guid = request.url.split('/')[-1]  # 提取图片 URL 中的文件名作为保存的文件名
        return f'{name}/{image_guid}'  # 指定保存的文件路径和文件名
