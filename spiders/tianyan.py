# -*- coding: utf-8 -*-
from selenium import webdriver
import scrapy
import time
from scrapy import Selector
from mistore.items import MistoreItem
class TianYanSpider(scrapy.Spider):
    name = 'tianyan'
    allowed_domains = ['www.tianyancha.com']
    start_urls = ('http://www.tianyancha.com/login',)

    def parse(self, response):
        return scrapy.Request(url=self.start_urls[0], callback=self.get_cook)

    def get_cook(self, response):
        item = MistoreItem()
        sel = Selector(response)
        browser = webdriver.Chrome()
        browser.get(self.start_urls[0])
        #browser.find_element_by_name("account").clear()
        browser.find_element_by_xpath(r"/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input").send_keys("18879451035")  # 修改为自己的用户名
        #browser.find_element_by_name("password").clear()
        browser.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input").send_keys("lyh915348696")
        browser.find_element_by_xpath(r'/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]').click()
        time.sleep(5)

        browser.get('http://www.tianyancha.com')
        elem_keyword = browser.find_element_by_xpath('//*[@id="live-search"]')
        elem_keyword.send_keys(u'百度')
        browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div/span').click()
        time.sleep(4)
        href = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/a').get_attribute('href')
        browser.get(href)

        time.sleep(5)




        #a = response.css('div.in-block.vertical-top.overflow-width.mr20 span:nth-child(2)::text').extract_first()
        #  = response.css('div.in-block.vertical-top span.in-block.vertical-top.overflow-width.emailWidth::text').extract_first()
        item['company_tel'] = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/span[2]').text

        #d = response.css('div.in-block.vertical-top.overflow-width.mr20 a::text').extract_first()

        print '%s'% item['company_tel']
        time.sleep(5)

        browser.close()






