# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from urllib.parse import unquote,urlparse
from scrapy.pipelines.files import FilesPipeline
import os 

class CustomFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        spider_name = info.spider.name
        domain = urlparse(request.url).netloc
        folder_name = f'{spider_name}_crawl_{domain}'

        file_name = item.get('file_name')
        file_path = os.path.join(folder_name, file_name)
        
        return file_path