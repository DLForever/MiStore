# -*- coding: utf-8

from scrapy.spider import Spider
from scrapy.http.request import Request
import scrapy
import json
from mistore.items import MistoreItem
from selenium import webdriver
import time


class MiSpider(Spider):
    name = 'xiao'
    start_urls = ['http://app.mi.com/categotyAllListApi?page=0&categoryId=5&pageSize=50' ]#pageSize自定义app个数

    #解析app信息
    def parse(self, response):
        item = MistoreItem()
        browser = webdriver.Chrome()
        browser.get(self.start_urls[0])
        jsonresponse = json.loads(response.body_as_unicode())
        a = jsonresponse['data'][:]  # 取所有data数据
        for i in range(0, len(a)):
            href = 'http://app.mi.com/details?id=%s' % a[i]['packageName']
            browser.get(href)
            time.sleep(1)
            try:
                item = MistoreItem()
                browser.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]').click()
                item['app_name'] = browser.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[1]/div/h3').text
                item['app_size'] = browser.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[2]').text
                item['app_version'] = browser.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[4]').text
                item['app_updatetime'] = browser.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[6]').text
                item['app_package'] = browser.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[8]').text
                item['app_company'] = browser.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[1]/div/p[1]').text

                if href and i ==0:
                    browser.get('http://www.tianyancha.com/login')


                    browser.find_element_by_xpath(r"/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input").send_keys("18879451035")  # 修改为自己的用户名

                    browser.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input").send_keys("lyh915348696")
                    browser.find_element_by_xpath(r'/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]').click()
                    time.sleep(2)

                link = 'http://www.tianyancha.com/search?key=%s&checkFrom=searchBox' % item['app_company']
                browser.get(link)

                #browser.get('http://www.tianyancha.com')
                #elem_keyword = browser.find_element_by_xpath('//*[@id="live-search"]')
                #elem_keyword.send_keys(item['app_company'])
                #browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div/span').click()
                time.sleep(2)
                href = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/a').get_attribute('href')

                browser.get(href)
                time.sleep(2)
            except Exception:
                print 'NoSuchElementException'


            try:
                item['company_email'] = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/span[2]').text
            except Exception:
                print 'NoSuchElementException  email'
                item['company_email'] = 'NONE'
            try:
                item['company_address'] = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[2]').text
            except Exception:
                print 'NoSuchElementException addres'
                item['company_address'] = 'NONE'

            try:
                item['company_url'] = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/a').text
            except Exception:
                print 'NoSuchElementException url'
                item['company_url'] = 'NONE'
            try:
                item['company_tel'] = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/span[2]').text
            except Exception:
                print 'NoSuchElementException tel'
                item['company_tel'] = 'NONE'




            yield item
            item = ''

        if i == len(a):
            browser.close()



        #request = scrapy.Request('http://www.tianyancha.com/search?key=%s&checkFrom=searchBox'% item['app_company'],cookies=self.cookie,headers=self.headers,callback=self.parse_tianyan)#通过公司名称到天眼查查询
        #request.meta['item'] = item
        #return request

    def parse_tianyan(self, response):
        link = response.css('div.col-xs-10.search_repadding2.f18 a::attr(href)').extract_first()#取得公司信息链接
        if link:
            yield Request(
                url=link,
                callback=self.parse_details2,
                meta={'item':response.meta['item'],'cookiejar':1},

            )
    #解析app所在公司信息
    def parse_details2(self,response):
        item = response.meta['item']
        item['company_tel'] = response.css('div.in-block.vertical-top.overflow-width.mr20 span:nth-child(2)::text').extract_first()
        item['company_email'] = response.css('div.in-block.vertical-top span.in-block.vertical-top.overflow-width.emailWidth::text').extract_first()
        item['company_address'] = response.xpath(r'/html/body/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[2]/text()').extract_first()
        item['company_url'] = response.css('div.in-block.vertical-top.overflow-width.mr20 a::text').extract_first()

        yield item

    def get_cooki(self, response):
        browser = webdriver.Chrome()
        browser.get('http://www.tianyancha.com/login')

        browser.find_element_by_xpath(r"/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input").send_keys("18879451035")  # 修改为自己的用户名

        browser.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input").send_keys("53")
        browser.find_element_by_xpath(r'/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]').click()

        link = response.css('div.col-xs-10.search_repadding2.f18 a::attr(href)').extract_first()  # 取得公司信息链接
        if link:
            yield Request(
                url=link,
                callback=self.parse_details2,
                meta={'item': response.meta['item'], 'cookiejar': 1},

            )



        #return [scrapy.FormRequest.from_response(response,meta={'cookiejar': 1,'item':response.meta['item']},callback=self.parse_tianyan)]

    #def start_requests(self):
       # return [Request('https://www.douban.com/accounts/login',meta={'cookiejar': 1},callback=self.get_cooki)]

    def parse_(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        a = jsonresponse['data'][:]  # 取所有data数据
        item = MistoreItem()

        item['app_name'] = response.css('div.intro-titles h3::text').extract_first()
        item['app_size'] = response.xpath(
            r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[2]/text()').extract_first()
        item['app_version'] = response.xpath(
            r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[4]/text()').extract_first()
        item['app_updatetime'] = response.xpath(
            r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[6]/text()').extract_first()
        item['app_package'] = response.xpath(
            r'/html/body/div[4]/div[1]/div[2]/div[2]/div/ul[1]/li[8]/text()').extract_first()
        item['app_company'] = response.xpath(r'/html/body/div[4]/div[1]/div[2]/div[1]/div/p[1]/text()').extract_first()

        for i in range(0, len(a)):
            href = 'http://app.mi.com/details?id=%s' % a[i]['packageName']  # 将app名称传入

            if href:
                yield Request(
                    url=href,
                    callback=self.parse_details,
                )








