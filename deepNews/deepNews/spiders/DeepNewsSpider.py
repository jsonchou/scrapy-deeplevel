# -*- coding: utf-8 -*-
import scrapy
import os
from deepNews.items import DeepnewsItem


class DeepNewsSpider(scrapy.Spider):
    name = 'DeepNewsSpider'
    allowed_domains = ['sina.com.cn']
    start_urls = ['https://news.sina.com.cn/guide/']

    def parse(self, response):
        items = []

        # 大类
        parentUrls = response.xpath(
            '//div[@id="tab01"]/div/h3/a/@href').extract()
        parentTitle = response.xpath(
            '//div[@id="tab01"]/div/h3/a/text()').extract()

        # 小类
        subUrls = response.xpath(
            '//div[@id="tab01"]/div/ul/li/a/@href').extract()
        subTitle = response.xpath(
            '//div[@id="tab01"]/div/ul/li/a/text()').extract()

        # 爬取所有大类
        for i in range(0, len(parentTitle)):
            parentFilename = './tmp/Data/' + parentTitle[i]

            if(not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)

            # 爬取所有小类
            for j in range(0, len(subUrls)):
                item = DeepnewsItem()

                item["parentTitle"] = parentTitle[i]
                item["parentUrls"] = parentUrls[i]

                if_belong = subUrls[j].startswith(item['parentUrls'])

                if(if_belong):
                    subFilename = parentFilename+'/'+subTitle[j]

                    if(not os.path.exists(subFilename)):
                        os.makedirs(subFilename)

                    item["subUrls"] = subUrls[j]
                    item['subTitle'] = subTitle[j]
                    item['subFilename'] = subFilename

                    items.append(item)

        for item in items:
            yield scrapy.Request(url=item['subUrls'], meta={'meta_1': item}, callback=self.second_parse)

    def second_parse(self, response):
        meta_1 = response.meta['meta_1']

        sonUrls = response.xpath('//a/@href').extract()

        items = []
        for i in range(0, len(sonUrls)):
            if_belong = sonUrls[i].endswith(
                '.shtml') and sonUrls[i].startswith(meta_1['parentUrls'])

            if(if_belong):
                item = DeepnewsItem()
                item['parentTitle'] = meta_1['parentTitle']
                item['parentUrls'] = meta_1['parentUrls']
                item['subUrls'] = meta_1['subUrls']
                item['subTitle'] = meta_1['subTitle']
                item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = sonUrls[i]

                items.append(item)

        for item in items:
            yield scrapy.Request(url=item['sonUrls'], meta={'meta_2': item}, callback=self.detail_parse)

    def detail_parse(self, response):
        item = response.meta['meta_2']

        content = ''
        # title = response.xpath("/html/head/title/text()")
        title = response.xpath('/html/head/meta[@property="og:title"]/@content').extract()

        if not title:
            title = response.xpath("//h1[@id='artibodyTitle' or @class='main-title' or id='main_title' ]/text()").extract()

        content_list = response.xpath("//div[@id='artibody' or @id='article_content']/p/text()").extract()

        for prow in content_list:
            content += prow

        item['title'] = title
        item['content'] = content

        yield item
