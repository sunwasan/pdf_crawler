import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import unquote,urlparse


class MetroSpiderSpider(CrawlSpider):
    name = "metro_spider"
    allowed_domains = ["thai-inter-org.mfa.go.th"]
    start_urls = ["https://thai-inter-org.mfa.go.th"]

    rules = (
        Rule(LinkExtractor(allow_domains=allowed_domains), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for link in response.xpath('//a[contains(@href, ".pdf")]/@href').getall():
            yield {
                'file_urls': [link],
                'file_name': link.split("/")[-1]
            }