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
        file_url = request.url
        # Decode the URL and extract the filename
        file_name = unquote(os.path.basename(file_url))
        # Construct the file path
        file_path = os.path.join('doc', file_name)
        return file_path