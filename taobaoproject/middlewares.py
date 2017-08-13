# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from time import sleep

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TaobaoprojectSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class IndexDownloaderMiddleware(object):
    def __init__(self, service_args):
        self.service_args = service_args

    def process_request(self, request, spider):
        if request.meta['cp'] == 1:
            try:
                # spider.logger.info('Begin to crawl Index~~~~~~~~~~~~~~~~~~')
                browser = webdriver.PhantomJS(service_args=self.service_args)
                browser.get(request.url)
                html = browser.page_source
                html = html.replace('&lt;', '<').replace('&gt;', '>')
                return HtmlResponse(browser.current_url, body=html, encoding='utf-8', request=request)
            except Exception as e:
                spider.logger.info('wrong....', e.args)
                return IgnoreRequest
            finally:
                browser.quit()
        else:
            return None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            service_args=crawler.settings.get('SERVICE_ARGS')
        )


class ChangePageDownloaderMiddleware(object):
    def __init__(self, service_args):
        self.service_args = service_args

    def process_request(self, request, spider):
        if request.meta['cp'] == 2:
            browser = webdriver.PhantomJS(service_args=self.service_args)
            wait = WebDriverWait(browser, 5)
            try:
                # print('Begin to crawl Info in page~~~~~~~~~~~~~~~~~~')
                browser.get(request.url)
                submit = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '#shopsearch-pager > div > div > div > ul > li.item.next > a')))
                submit.click()
                sleep(1)
                html = browser.page_source
                html = html.replace('&lt;', '<').replace('&gt;', '>')
                if html:
                    #get_info(k1, k2, location, html, store_number)
                    return HtmlResponse(url=browser.current_url, body=html, encoding='utf-8', request=request)
                else:
                    return None
            except Exception as e:
                spider.logger.info('Fail to get index------------------------',e.args)
                browser.quit()
            finally:
                browser.quit()
        else:
            return None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            service_args=crawler.settings.get('SERVICE_ARGS')
        )
