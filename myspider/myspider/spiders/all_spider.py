from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse, urljoin


class AllSpider(CrawlSpider):
    name = "all"
    
    start_urls =  [str(input("Start Url:"))]
    allowed_domains = [str(urlparse(start_urls[0]).netloc)]

    rules = (
        Rule(LinkExtractor(allow_domains=allowed_domains), callback='parse_item', follow=True),
    )

    def parse(self, response):
        domain = urlparse(response.url).scheme + "://" + urlparse(response.url).netloc

        for link in response.xpath('//a[contains(@href, ".pdf")]/@href').getall():
            if not link.startswith('http'):
                link = urljoin(domain, link)
            
            yield {
                'file_urls': [link],
                'file_name': link.split("/")[-1]
            }


