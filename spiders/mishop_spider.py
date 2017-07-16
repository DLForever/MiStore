#-*- coding: utf-8 -*-
from scrapy.selector import Selector
from  scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from mistore.items import MistoreItem
from scrapy import log
import scrapy


class MiSpider(CrawlSpider):
    name = 'xxiaomi22'


    def parse_a(self, response):
        sel = Selector(response)
        #sites = sel.css('div.main')
        #quotes = []
        #for quotee in response.xpath(r'/html/body/div[4]/div/div[1]/div[2]/div'):
        for quotee in response.css('div.main'):
        #for quotee in sel.xpath('//*[@id="all-applist"]'):
            quote = MistoreItem()
            quote['app_name'] = quotee.css('div.intro-titles h3::text').extract_first()
            quote['app_size'] = quotee.xpath(r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[2]/text()').extract_first()
            quote['app_version'] = quotee.xpath(r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[4]/text()').extract_first()
            quote['app_updatetime'] = quotee.xpath(r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[6]/text()').extract_first()
            quote['app_package'] = quotee.xpath(r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[8]/text()').extract_first()
            quote['app_company'] = quotee.xpath(r'/html/body/div[4]/div[1]/div[2]/div[1]/div/p[1]/text()').extract_first()
            #quotes.append(quote)
            return quote
        next_page = response.css('div.page a.next::text').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            #yield scrapy.Request(next_page, callback=self.parse_a())


            #yield {
                #'app_name' : quote.css('div.intro-titles h3::text').extract_first(),
                #'app_size' : quote.xpath(r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[2]/text()').extract(),

            #}


    def parse_item(self, response):
        sels = Selector(response)
        items = []
        for sel in response.css('div.app-info'):
            item = MistoreItem()
            #yield {
                #'app_name': sel.css('div.intro-titles h3::text').extract_first()
            #}
            item['app_name'] = sel.xpath(r'/html/body/div[4]/div[1]/div[2]/div[1]/div/h3/text()').extract()
            #item['app_size'] = sel.xpath(r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[2]/text()').extract()
            #item['app_version'] = sel.xpath(r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[4]/text()').extract()
            #item['app_updatetime'] = sel.xpath(r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[6]/text()').extract()
            #item['app_package'] = sel.xpath(r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[8]/text()').extract()
            #item['app_company'] = sel.xpath(r'/html/body/div[4]/div[1]/div[2]/div[1]/div/p[1]/text()').extract()
            #item['company_tel'] = sel.xpath(r'/html/body/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/span[2]/text()').extract()
            #item['company_email'] = sel.xpath(r'/html/body/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[2]/text()').extract()
            #item['company_address'] = sel.xpath(r'/html/body/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div[2]/span[2]/text()').extract()
            #item['company_url'] = sel.xpath(r'/html/body/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div[1]/span[2]/text()').extract()
            #items.append(item)
            next_page = response.css('div.page a.next::text').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse())

                log('A response from %s just arrived' % response.url)



