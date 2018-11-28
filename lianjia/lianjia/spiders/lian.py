# -*- coding: utf-8 -*-
import scrapy
from lianjia.items import LianjiaItem
import re
from scrapy.http import Request
from lxml import etree
import json



class LiSpider(scrapy.Spider):
    name = 'lian'
    allowed_domains = ['bj.lianjia.com']
    regions = {
        'dongcheng': '东城',
        'xicheng': '西城',
        'chaoyang': '朝阳',
        'haidian': '海淀',
        'fengtai': '丰台',
        'shijingshan': '石景山',
        'tongzhou': '通州',
        'changping': '昌平',
        'daxing': '大兴',
        'yizhuangkaifaqu': '亦庄开发区',
        'shunyi': '顺义',
        'fangshan': '房山',
        'mentougou': '门头沟',
        'pinggu': '平谷',
        'huairou': '怀柔',
        'miyun': '密云',
        'yanqing': '延庆',
    }
    region_list = ['dongcheng', 'xicheng', 'chaoyang', 'haidian', 'fengtai', 'shijingshan', 'tongzhou', 'changping',
                   'daxing', 'yizhuangkaifaqu', 'shunyi', 'fangshan', 'mentougou', 'pinggu', 'huairou', 'miyun',
                   'yanqing']

    def start_requests(self):
        for region in list(self.regions.keys()):
            url = 'https://bj.lianjia.com/zufang/' + region + '/rp1rp0/'
            yield Request(url=url, callback=self.parse, meta={'region': region})

    # 返回每个小区
    def parse(self, response):
        xiaoqus = response.xpath('.//div[@class="option-list sub-option-list"]/a/@href').extract()
        if len(xiaoqus):
            xiaoqu_list = []
            for xiaoqu in xiaoqus:
                xiaoqu = str(xiaoqu)
                xiaoqu = xiaoqu.split('/')
                xiaoqu_list.append(xiaoqu[2])
            for xiao_name in xiaoqu_list[1:]:
                url = 'https://bj.lianjia.com/zufang/' + xiao_name + '/'
                yield Request(url=url, meta={'xiao_name': xiao_name, 'region': response.meta['region']},
                              callback=self.parse_zufang)

    # 返回每个小区每页的连接
    def parse_zufang(self, response):
        xiao_names = response.meta['xiao_name']

        selector = etree.HTML(response.text)
        content = selector.xpath('//div[@class="page-box house-lst-page-box"]')
        total_pages = 0
        if (len(content)):
            page_data = json.loads(content[0].xpath('./@page-data')[0])
            total_pages = page_data.get("totalPage")
        #防止网页链接产生重复
        for i in range(int(total_pages)):
            if xiao_names in self.region_list:
                continue
            else:
                url_page = 'https://bj.lianjia.com/zufang/' + xiao_names + '/pg' + str(i + 1) + '/'
                print(url_page)
                print('---------------------------')
                yield Request(url=url_page, callback=self.parse_content,
                              meta={'xiao_name': xiao_names, 'region': response.meta['region']},
                              dont_filter=False)

    def parse_content(self, response):
        selector = etree.HTML(response.text)
        cj_list = selector.xpath("//ul[@class='house-lst']/li")

        # 获取所在区和房屋链接
        for cj in cj_list:
            i = LianjiaItem()

            i['room_region'] = self.regions.get(response.meta['region'])
            link = cj.xpath('.//div[@class="info-panel"]/h2/a/@href')
            if not len(link):
                continue
            i['room_link'] = link[0]
            # 房屋小区
            room_area = cj.xpath('.//div[@class="where"]/a[@class="laisuzhou"]/span/text()')
            i['room_area'] = room_area[0].replace(u'\xa0', u'')
            # 房屋类型
            room_type = cj.xpath('.//div[@class="where"]/span[@class="zone"]/span/text()')
            i['room_type'] = room_type[0].replace(u'\xa0', u'')
            # 房屋大小
            room_size = cj.xpath('.//div[@class="where"]/span[@class="meters"]/text()')
            room_size = room_size[0].replace(u'\xa0', u'')
            i['room_size'] = re.compile(r'\d+\.?\d*').search(room_size).group()
            # 房屋租金
            i['room_money'] = cj.xpath('.//div[@class="price"]/span[@class="num"]/text()')[0]
            # 房屋被几人看过
            i['room_person'] = cj.xpath('.//div[@class="square"]/div/span[@class="num"]/text()')[0]
            # 房屋是否近地铁
            room_subway = cj.xpath('.//span[@class="fang-subway-ex"]/span/text()')
            if not len(room_subway):
                i['room_subway'] = 0
            else:
                i['room_subway'] = 1
            # 是否可以随时看房
            room_view = cj.xpath('.//span[@class="haskey-ex"]/span/text()')
            if not len(room_view):
                i['room_view'] = 0
            else:
                i['room_view'] = 1
            # 房屋是否集中供暖
            room_heating = cj.xpath('.//span[@class="heating-ex"]/span/text()')
            if not len(room_heating):
                i['room_heating'] = 0
            else:
                i['room_heating'] = 1

            content = cj.xpath('.//div[@class="con"]/text()')
            # 楼层高度
            i['room_floor'] = re.compile('\d+').search(content[0]).group()
            # 建造年代
            room_year = re.compile('\d+').search(content[1]).group()
            if room_year != '':
                i['room_year'] = re.compile('\d+').search(content[1]).group()
            else:
                i['room_year'] = 0
            yield i
