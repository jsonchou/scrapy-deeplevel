# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DeepnewsItem(scrapy.Item):
    # define the fields for your item here like:
    # 大类
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()

    # 小类
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()

    # 小类目录存储路径
    subFilename = scrapy.Field()

    # 小类下的子链接
    sonUrls = scrapy.Field()

    # 文章标题内容
    title = scrapy.Field()
    content = scrapy.Field()
    pass
