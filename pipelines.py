# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MsdnPipeline(object):
    def __init__(self):
        self.file = open('msdnc.csv', 'a+', encoding='utf8')

    def process_item(self, item, spider):
        title = item['name']
        url = item['url']
        self.file.write(title + '*' + url + '\n')

    def down_item(self, item, spider):
        self.file.close()
