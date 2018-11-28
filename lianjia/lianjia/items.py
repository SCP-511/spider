# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    room_region = scrapy.Field()    #房屋所在区
    room_link = scrapy.Field()  #房屋链接
    room_area = scrapy.Field()  #房屋小区
    room_type = scrapy.Field()  #房屋类型
    room_size = scrapy.Field()  #房屋大小
    room_money = scrapy.Field()  #房屋租金
    room_person = scrapy.Field()    #房屋被几人看过
    room_subway = scrapy.Field()    #房屋是否近地铁
    room_heating = scrapy.Field()   #房屋是否集中供暖
    room_decoration = scrapy.Field()    #房屋是否精装修
    room_floor = scrapy.Field()  #楼层高度
    room_year = scrapy.Field()  #建造年代
    room_style = scrapy.Field()   #楼层类型
    room_view = scrapy.Field()   #是否可以随时看房
