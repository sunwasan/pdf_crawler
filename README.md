## Scrapy PDF Spider Readme

This repository contains Scrapy spiders designed to scrape PDF files from websites. The spiders utilize different techniques and approaches to extract PDF links and download the files. This readme will guide you on how to use the `SingleSpider` and `AllSpider` included in this repository.

### Purpose

The purpose of these spiders is to provide a convenient way to crawl websites and extract PDF files. The spiders are built using Scrapy, a powerful and flexible web scraping framework. By using these spiders, you can automate the process of finding and downloading PDF files from websites, saving you time and effort.

### Installation

Before using the spiders, make sure you have the following dependencies installed:

- Python 3.x
- Scrapy
- Selenium
- ChromeDriver

To install the dependencies, you can use pip:

```
pip install scrapy selenium
```

You also need to download the ChromeDriver executable compatible with your Chrome browser version. You can download it from the official ChromeDriver website: [ChromeDriver Downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)

Make sure to place the ChromeDriver executable in a location accessible by your system's PATH.

### SingleSpider

The `SingleSpider` is designed to extract PDF links from a single webpage. It uses Selenium to render the page with JavaScript, ensuring that the dynamically generated content is accessible. Here's how you can use the `SingleSpider`:

1. Open a terminal or command prompt.
2. Navigate to the directory where you have cloned or downloaded this repository.
3. Run the following command:

```
scrapy crawl single
```

4. Enter the URL of the webpage from which you want to extract PDF files when prompted.
5. The spider will start crawling the webpage and extract PDF links.
6. Once the process is complete, the PDF files will be saved in the `results` folder within the same directory.

### AllSpider

The `AllSpider` is designed to crawl a website and extract PDF links from multiple webpages. It follows internal links within the allowed domain and recursively extracts PDF links. Here's how you can use the `AllSpider`:

1. Open a terminal or command prompt.
2. Navigate to the directory where you have cloned or downloaded this repository.
3. Run the following command:

```
scrapy crawl all
```

4. Enter the URL of the website from which you want to extract PDF files when prompted.
5. The spider will start crawling the website and extract PDF links from each page.
6. Once the process is complete, the PDF files will be saved in the `results` folder within the same directory.

### Customization

Both the `SingleSpider` and `AllSpider` can be customized to suit your specific requirements. You can modify the spider code to extract different types of files or scrape additional information from the webpages. Refer to the Scrapy documentation for more information on customizing spiders: [Scrapy Documentation](https://docs.scrapy.org/)

Feel free to explore and modify the spiders according to your needs.

### Conclusion

The Scrapy PDF spiders provided in this repository offer a convenient solution for extracting PDF files from websites. By using these spiders, you can automate the process of finding and downloading PDFs, saving valuable time and effort. Customize the spiders according to your requirements and explore the capabilities of Scrapy for web scraping tasks.

Please note that web scraping should be done responsibly and in compliance with the website's terms of service. Make sure to respect the website's policies and use these spiders for legal and ethical purposes.

The downloaded PDF files will be saved in the `results` folder within the same directory as the spiders. Make sure to check the `results` folder for the extracted PDF files after running
