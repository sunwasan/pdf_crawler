import scrapy
from urllib.parse import urlparse, urljoin
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
import os


class SingleSpider(scrapy.Spider):
    name = "single"

    def start_requests(self):
        start_url = str(input("Url:"))  # Replace with your desired starting URL
        yield scrapy.Request(url=start_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # Use Selenium to render the page with JavaScript
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode
        driver = webdriver.Chrome(options=options)  # Replace with the path to your ChromeDriver executable

        # Set the maximum wait time in seconds
        wait_time = 5
        driver.implicitly_wait(wait_time)

        driver.get(response.request.url)

        # Wait for the desired element to be clickable
        wait = WebDriverWait(driver, wait_time)
        wait.until(lambda driver: driver.find_element(By.XPATH, '//a[contains(@href, ".pdf")]'))

        body = driver.page_source
        driver.quit()

        # Create a new Scrapy response with the rendered HTML
        rendered_response = HtmlResponse(url=response.request.url, body=body, encoding='utf-8')

        # Continue parsing the rendered response
        domain = "https://" + urlparse(response.url).netloc

        for link in rendered_response.xpath('//a[contains(@href, ".pdf")]/@href').getall():
            if not link.startswith(('http://', 'https://')):
                link = urljoin(domain, link)
                if link.startswith('http://'):
                    link = link.replace('http://', 'https://')

            yield {
                'file_urls': [link],
                'file_name': link.split("/")[-1]
            }

class AllSpider(CrawlSpider):
    name = "all"
    allowed_domains = []

    def start_requests(self):
        start_url = input("Url:") 
        self.allowed_domains.append(urlparse(start_url).netloc)
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        domain = urlparse(response.url).scheme + "://" + urlparse(response.url).netloc

        # Extract PDF links and yield them as items
        pdf_links = response.xpath('//a[contains(@href, ".pdf")]/@href').getall()
        for link in pdf_links:
            if not link.startswith(('http', 'https')):
                link = urljoin(domain, link)

            yield {
                'file_urls': [link],
                'file_name': link.split("/")[-1]
            }

        # Follow internal links within the allowed domain
        internal_links = response.css('a::attr(href)').getall()
        for link in internal_links:
            if not link.startswith(('http', 'https')):
                link = urljoin(domain, link)
            
            if urlparse(link).netloc == self.allowed_domains[0]:
                yield scrapy.Request(url=link, callback=self.parse)

    rules = (
        Rule(LinkExtractor(allow=()), callback='parse', follow=False),
    )



