import scrapy
from urllib.parse import urlparse, urljoin

class SingleSpider(scrapy.Spider):
    name = "single"
    start_urls = [str(input("Url:"))]

    def parse(self, response):
        domain = urlparse(response.url).scheme + "://" + urlparse(response.url).netloc

        for link in response.xpath('//a[contains(@href, ".pdf")]/@href').getall():
            if not link.startswith('http'):
                link = urljoin(domain, link)
            
            yield {
                'file_urls': [link],
                'file_name': link.split("/")[-1]
            }