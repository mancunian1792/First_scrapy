# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy import Spider
from scrapy.loader import ItemLoader
from first_scrapy.items import FirstScrapyItem
from scrapy.utils.response import open_in_browser
class QuotesSpider(Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']
    
    def parse(self, response):
        token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        return FormRequest.from_response(response,
                                         formdata={'csrf_token':token,
                                                   'username':"sample",
                                                   'password':"pass"},
                                         callback=self.scrape_home_page)

    def scrape_home_page(self, response):
        open_in_browser(response)
        l = ItemLoader(item=FirstScrapyItem(),  response=response)
        text = response.xpath('//*[@class="text"]/text()').extract()
        author = response.xpath('//*[@class="author"]/text()').extract()
        tags = response.xpath('//*[@class="tag"]/text()').extract()
        l.add_value('text', text)
        l.add_value('author', author)
        l.add_value('tags', tags)
        return l.load_item()
#        quotes = response.xpath('//*[@class="quote"]')
#        for quote in quotes:
#            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
#            author = quote.xpath('.//*[@class="author"]/text()').extract_first()
#            tags = quote.xpath('.//*[@class="tag"]/text()').extract()
#            yield {"Text": text, "Author": author, "Tags":tags}
#            
#            
#        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
#        absolute_next_page_url = response.urljoin(next_page_url)
#        yield Request(absolute_next_page_url)