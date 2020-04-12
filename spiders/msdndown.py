# -*- coding: utf-8 -*-
import json
import scrapy
from msdn.items import MsdnItem


class MsdndownSpider(scrapy.Spider):
    name = 'msdndown'
    allowed_domains = ['msdn.itellyou.cn']
    start_urls = ['http://msdn.itellyou.cn/']

    def parse(self, response):
        self.index = [i for i in response.xpath('//h4[@class="panel-title"]/a/@data-menuid').extract()]
        # self.index_title = [i for i in response.xpath('//h4[@class="panel-title"]/a/text()').extract()]
        url = 'https://msdn.itellyou.cn/Category/Index'
        for i in self.index:
            yield scrapy.FormRequest(url=url, formdata={'id': i}, dont_filter=True,
                                     callback=self.Get_Lang, meta={'id': i})

    def Get_Lang(self, response):
        id_info = json.loads(response.text)
        url = 'https://msdn.itellyou.cn/Category/GetLang'
        for i in id_info:  # 遍历软件列表（测试时取前9个）
            lang = i['id']  # 软件ID
            title = i['name']  # 软件名
            # 进行下一次爬取，根据lang(语言)id获取软件语言ID列表
            yield scrapy.FormRequest(url=url, formdata={'id': lang}, dont_filter=True, callback=self.Get_List,
                                     meta={'id': lang, 'title': title})

    def Get_List(self, response):
        lang = json.loads(response.text)['result']
        id = response.meta['id']
        title = response.meta['title']
        url = 'https://msdn.itellyou.cn/Category/GetList'
        # 如果语言为空则跳过，否则进行下次爬取下载地址
        if len(lang) != 0:
            # 遍历语言列表ID
            for i in lang:
                data = {
                    'id': id,
                    'lang': i['id'],
                    'filter': 'true'
                }
                yield scrapy.FormRequest(url=url, formdata=data, dont_filter=True, callback=self.Get_Down,
                                         meta={'name': title, 'lang': i['lang']})
        else:
            pass

    def Get_Down(self, response):
        response_json = json.loads(response.text)['result']
        item = MsdnItem()
        for i in response_json:
            item['name'] = i['name']
            item['url'] = i['url']
            print(i['name'] + "--------------" + i['url'])
        return item
