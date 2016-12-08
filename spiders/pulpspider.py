# __author__ = "Qianchao"
# -*- coding: utf-8 -*-
# target: http://www.chinapulp.cn/zhishu/
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import request, Request
from scrapy.selector import Selector
from chinapulp_spider.items import ChinapulpSpiderItem



class Pulp(CrawlSpider):
    name = "pulpspider"
    pingjie_url = "http://www.chinapulp.cn"  # 拼接url
    # redis_key = "pulpspider: start_urls"
    start_urls = ['http://www.chinapulp.cn/zhishu/zs_data_list_index.php?page=1']
    url = 'http://www.chinapulp.cn/zhishu/zs_data_list_index.php?page=1'

    def parse(self, response):
        item = ChinapulpSpiderItem()  # 网页数据
        selector = Selector(response)
        pulp_datas = selector.xpath('//tr[@class="data_row"]')
        # print len(pulp_datas)
        for each_row in pulp_datas:
            index_kind = each_row.xpath('td[1]/text()').extract()
            index = each_row.xpath('td[2]/text()').extract()
            change_ratio = each_row.xpath('td[3]/text()').extract()
            date = each_row.xpath('td[4]/text()').extract()
            pic = each_row.xpath('td[3]/img/@src').extract()

            item['index_kind'] = index_kind[0].replace('\n', '').replace(' ', '').encode('utf8')
            item['index'] = index[0].encode('utf8')
            item['change_ratio'] = change_ratio[0].encode('utf8')
            item['date'] = date[0].encode('utf8')
            item['pic'] = pic[0]
            print index_kind[0], index[0], change_ratio[0], date[0], pic[0]

            yield item

        nextpages = set()
        nextpage = selector.xpath('//div[@class="pages"]/a/@href').extract()[-2]
        if nextpage not in nextpages:
            # 去重用
            nextpages.add(nextpage)
            yield Request(self.pingjie_url+nextpage, callback=self.parse)

    # def parse_page(self, response):
    #     url = "http://www.chinapulp.cn"  # 拼接url
    #     url_lists = {}
    #     selector = Selector(response)
    #     nextpage = selector.xpath('//div[@class="pages"]/a/@href').extract()[-2]
    #     url_lists.add(nextpage)





