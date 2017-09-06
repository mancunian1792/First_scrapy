# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FirstScrapyPipeline(object):
    def process_item(self, item, spider):
        if(item['author']):
            for i in range(0, len(item['author'])):
                item['author'][i] = item['author'][i].upper()
        return item
