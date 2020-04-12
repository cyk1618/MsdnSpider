# -*- coding: utf-8 -*-
import json

import scrapy


class MsdnzySpider(scrapy.Spider):
    name = 'msdnzy'
    allowed_domains = ['msdn.itellyou.cn']
    start_urls = ['http://msdn.itellyou.cn/']

    def parse(self, response):
        self.index = [i for i in response.xpath('//h4[@class="panel-title"]/a/@data-menuid').extract()]
        self.index_title = [i for i in response.xpath('//h4[@class="panel-title"]/a/text()').extract()]
        url = 'https://msdn.itellyou.cn/Category/Index'
        yield scrapy.FormRequest(url=url, formdata={'id': self.index[0]}, dont_filter=True,
                                 callback=self.Get_Lang)
        # for i in self.index:
        #     url = 'https://msdn.itellyou.cn/Category/Index'
        #     yield scrapy.FormRequest(url=url, formdata={'id': i}, dont_filter=True,
        #                              callback=self.Get_Lang)

    def Get_Lang(self, response):
        result = json.loads(response.text)
        self.lang = []
        url = 'https://msdn.itellyou.cn/Category/GetLang'
        for i in result:
            self.lang.append(i['id'])
            self.id = i['id']
            yield scrapy.FormRequest(url=url, formdata={'id': self.id}, dont_filter=True, callback=self.Get_List)

    def Get_List(self, response):
        res_json = json.loads(response.text)
        self.list = []
        for i in res_json['result']:
            self.list.append(i['id'])
            self.lang = i['id']
        print(self.lang)
        print(self.list)
            # yield scrapy.FormRequest(url='https://msdn.itellyou.cn/Category/GetList',
            #                          formdata={'self.id': self.id, 'lang': self.lang, 'filter': 'true'},
            #                          dont_filter=True, callback=self.Get_Result)

    def Get_Result(self, response):
        print(response.text)
