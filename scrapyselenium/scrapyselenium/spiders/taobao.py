# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib.parse import quote
from scrapyseleniumtest.items import ProductItem
from scrapyseleniumtest.tools import register

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com','g.alicdn.com','s.taobao.com']
    #start_urls = ['https://www.taobao.com/']
    base_url = 'https://s.taobao.com/search?q='
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'referer': 'https://www.taobao.com/',
        'accept-encoding': 'gzip, deflate, b',
    }

    def parse(self, response):
        products = response.xpath(
            '//div[@id="mainsrp-itemlist"]//div[@class="items"][1]//div[contains(@class, "item")]')
        for product in products:
            item = ProductItem()
            item['price'] = ''.join(product.xpath('.//div[contains(@class, "price")]//text()').extract()).strip()
            item['title'] = ''.join(product.xpath('.//div[contains(@class, "title")]//text()').extract()).strip()
            item['shop'] = ''.join(product.xpath('.//div[contains(@class, "shop")]//text()').extract()).strip()
            item['image'] = ''.join(
                product.xpath('.//div[@class="pic"]//img[contains(@class, "img")]/@data-src').extract()).strip()
            item['deal'] = product.xpath('.//div[contains(@class, "deal-cnt")]//text()').extract_first()
            item['location'] = product.xpath('.//div[contains(@class, "location")]//text()').extract_first()
            yield item

    def start_requests(self):
        self.browser, cookies = register()  # 这里调用selenium登录的方法并返回browser和一个cookies
        for keyword in self.settings.get('KEYWORDS'):#获取要搜索的关键词
            for page in range(1, self.settings.get('MAX_PAGE') +1):
                url = self.base_url + quote(keyword)
                yield Request(url=url, headers=self.headers, cookies=cookies, callback=self.parse, meta={'page':page,'browser':self.browser}, dont_filter=True)



