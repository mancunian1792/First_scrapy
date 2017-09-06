# -*- coding: utf-8 -*-
# To have an argument when you are crawling, 
# define an __int__function and have an argument
# To invoke the spider with an argument,
# scrapy crawl 'spider-name' -a 'arg-name'='arg-value'
from scrapy import Spider
from scrapy.http import Request
import re
import os
import csv
import glob

class BooksScrapySpider(Spider):
    name = 'books_scrapy'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']
    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)
        # Process next page
#        next_page_url = response.xpath('//*[@class = "next"]/a/@href').extract_first()
#        absoulte_next_page = response.urljoin(next_page_url)
#        yield Request(absoulte_next_page)
    def parse_book(self, response):
        title = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'books.toscrape.com')
        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')
        stock_available = stock_available = response.xpath('//*[@class="instock availability"]/text()').extract()
        available_count = 0
        regex = r"(\d+)"
        for stock in stock_available:
            match =  re.search(regex, stock)
            if match:
                available_count = match.group(0)
        yield {
               'title':title,
               'price':price,
               'image_url':image_url,
               'rating':rating,
               'available_count':available_count      
               }
    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        print(csv_file)