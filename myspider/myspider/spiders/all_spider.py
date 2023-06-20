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
        start_url = input("Url:")  # Replace with your desired starting URL
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


class FaoSpider(CrawlSpider):
    name = 'fao'

    def start_requests(self):
        self.start_url = str(input("Url:"))  # Replace with your desired starting URL
        yield scrapy.Request(url=self.start_url, callback=self.parse)


    def parse(self, response):

        if response.status in [301, 302]:
            redirected_url = response.headers.get('Location').decode('utf-8')

            yield scrapy.Request(url=redirected_url, callback=self.parse, meta={'original_url': response.url})
        else:
            pdf_links = response.xpath('//a[span[text()="Download PDF"]]/@href').getall()
            for link in pdf_links:
                yield response.follow(url=link, callback=self.load_pdf, meta={'original_url': response.url})

    def load_pdf(self, response):
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
            name = rendered_response.xpath("//h2[@class='page-title py-0']/text()").get()
            name = name.replace(":"," ")
            if not link.startswith(('http://', 'https://')):
                link = urljoin(domain, link)
            if link.startswith('http://'):
                link = link.replace('http://', 'https://')
            file_extension = os.path.splitext(link)[1].lower()
            file_name = f"{name}{file_extension}"

            yield {
                'file_urls': [link],
                'file_name': file_name
            }



    
class food_research(scrapy.Spider):
    name = "food"
    allowed_domains = []
    max_pages = 3
    c = 0
    def start_requests(self):
        start_url = input("Url:")  # Replace with your desired starting URL
        self.allowed_domains.append(urlparse(start_url).netloc)
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        # Extract the links within h1 tags
        for link in response.xpath('//h1[@class="field--name-title-field"]/a/@href').getall():
            yield response.follow(link, callback=self.parse_link)

        if self.c < self.max_pages :
            next_page = response.xpath('//*[@id="block-serenity-system-main"]/div/div/nav/ul/li[11]/a').get()
            if next_page is not None:
                self.c += 1
                yield response.follow(next_page, callback=self.parse)


    def parse_link(self, response):
        domain = "https://" + urlparse(response.url).netloc

        name = response.xpath("//h1[@class='field--name-title-field']/text()").get()

        for link in response.xpath('//a[contains(@href, ".pdf")]/@href').getall():
            if not link.startswith(('http', 'https')):
                link = urljoin(domain, link)
                file_extension = os.path.splitext(link)[1].lower()
                name = name.replace(':','_')
                file_name = f"{name}{file_extension}"

            yield {
                'file_urls': [link],
                'file_name': f"{file_name}"
            }
   
class UnidoSpider(scrapy.Spider):
    name = 'unido'
    max_pages = 5
    c = 0
    allowed_domains = []

    def start_requests(self):
        start_url = input("URL:")  # Replace with your desired starting URL
        self.allowed_domains.append(urlparse(start_url).netloc)
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        # Extract the links within <a> tags
        for link in response.xpath("//p[@class='h4 mb-2']/a[@class='unido-link link ' and contains(@href, '.pdf')]"):
            domain = "https://" + urlparse(response.url).netloc
            href = link.xpath("./@href").get()
            if not href.startswith(('http', 'https')):
                href = urljoin(domain, href)
            name = link.xpath("./span/span/text()").get()
            name = name.replace(':', '_')
            file_extension = os.path.splitext(href)[1].lower()
            file_name = f"{name}{file_extension}"

            yield {
                'file_urls': [href],
                'file_name': file_name
            }

        if self.c < self.max_pages:
            self.c += 1
            next_page = response.xpath('//a[@title="Go to next page"]/@href').get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

