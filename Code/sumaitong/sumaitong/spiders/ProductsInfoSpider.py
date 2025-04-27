import json
import os
import re
import time

import scrapy
from scrapy import Request, signals

# from ip_test.test_ip import process_ip_pool
from sumaitong.items import ProductListItem


# 特定商品关键词列表页前60页的爬虫
class ProductsInfoSpider(scrapy.Spider):
    name = 'ProductsInfoSpider'
    allowed_domains = ["aliexpress.us"]
    keyword = 'injector'
    start_time = None
    spend_time = None
    count = 0

    start_urls = [f"https://www.aliexpress.us/w/wholesale-{keyword}.html?spm=a2g0o.productlist.search.0"]

    # def start_requests(self):
    #     working_dir = os.getcwd()
    #     print(f'working_dir: {working_dir}')
    #     os.chdir(r'E:\Code\sumaitong\ip_test')
    #     print(f'working_dir: {working_dir}')
    #     process_ip_pool()
    #     os.chdir(working_dir)
    #     print(f'working_dir: {working_dir}')
    #     # woring_dir = os.getcwd()
    #     # ip_dir = '../../ip_test'
    #     # os.chdir(ip_dir)
    #     # os.chdir(woring_dir)
    #     for url in self.start_urls:
    #         yield Request(url, callback=self.parse)


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls()
        spider.crawler = crawler
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_opened(self, spider):
        print(f"Spider {spider.name} opened.")
        self.start_time = time.time()

    def spider_closed(self, spider):
        print(f"Spider {spider.name} closed.")
        self.spend_time = time.time() - self.start_time
        print('running time: ', self.spend_time)


    def start_requests(self):
        base_url = 'https://www.aliexpress.us/w/wholesale-{keyword}.html?page={page}spm=a2g0o.productlist.search.0'
        for page in range(1, 61):  # 直接生成前60页URL
            url = base_url.format(keyword=self.keyword, page=page)
            yield Request(url, callback=self.parse)
    def parse(self, response, **kwargs):
        # print(response.text)
        base_url = 'https://www.aliexpress.us/w/wholesale-injector.html?page={}spm=a2g0o.productlist.search.0'
        content = response.text
        # with open('./content.html', 'w', encoding='utf-8') as f:
        #     f.write(content)
        # print(content)
        # 使用正则表达式提取window._dida_config_变量值
        # pattern = r'window\._dida_config_ = (.*?);'
        pattern = r'/\*!-->init-data-start--\*/\s*?window\._dida_config_\._init_data_\s*=\s*{ data: (.*)}/\*!-->init-data-end'
        match1 = re.search(pattern, content, re.DOTALL)
        if not match1:
            print(f'未找到数据, 页面源代码已保存到 error.html ')
            with open('./error.html', 'w', encoding='utf-8') as f:
                f.write(content)
            yield scrapy.Request(url=base_url.format(response.url), callback=self.parse)
            return
        data = match1.group(1)

        try:
            data = json.loads(data)
            # print(data["data"]["root"]["fields"]["mods"]["itemList"]["content"])
            with open('data.json', 'w') as f:
                json.dump(data, f)

            # print(data)
            # print(f"data========>: {data["data"]["root"]["fields"]["mods"]["itemList"]["content"]}")
            page_info = data["data"]["root"]["fields"].get('pageInfo')

            current_page = None
            total_page = None
            next_page_flag = False

            if page_info:
                current_page = page_info.get('page', None)
                total_results = page_info.get('totalResults', None)
                page_size = page_info.get('pageSize', None)
                # print(f'total results====> : {total_results}')

                # 接口最多只能允许调到60页
                total_page = total_results / page_size if total_results / page_size < 60 else 60
                # 测试先尝试三页
                # total_page = 3
                # print(f'current_page:{current_page}, total_page:{total_page}')
                next_page_flag = True if current_page < total_page else False
            rank_list = []  # 测试是不是拿全了
            # 正则提取
            for info in data["data"]["root"]["fields"]["mods"]["itemList"]["content"]:
                product_name = info.get('title').get('displayTitle', None)
                price = info["prices"].get('salePrice').get('minPrice', None)
                store_name = info.get('store').get('storeName')
                seller_id = info.get('store', {}).get('aliMemberId', None)
                sales = int(
                    info["trade"]["tradeDesc"].split("sold")[0].strip().replace("+", "").replace(",", "")) if info.get(
                    'trade',
                    {}).get(
                    'tradeDesc') else None
                ranking = (current_page - 1) * page_size + data["data"]["root"]["fields"]["mods"]["itemList"]["content"].index(info) + 1 if page_info else -1
                rank_list.append(ranking)
                print(f'理论ranking=====> {ranking}, 当前len===>{len(rank_list)}')
                print(
                    f"单品页 store_name:{store_name}, product_name:{product_name}, price:{price}, sales:{sales}, url:{response.url}")

                items = ProductListItem()
                items['product_name'] = product_name
                items['price'] = price
                items['store_name'] = store_name
                items['sales'] = sales
                items['seller_id'] = seller_id
                items['keyword'] = self.keyword
                items['seller_id'] = seller_id
                items['ranking'] = ranking
                yield items


                # print('提交完item...')
                # print(f'{response.url}爬取成功')
            self.count += 1
            print(f'{current_page}页爬取完毕，进度{self.count}/{total_page}')

            # if next_page_flag:
            #     print(f'开始爬取{current_page + 1}页')
            #     yield Request(base_url.format(current_page + 1), callback=self.parse)
            # else:
            #     print('商品页爬取完毕')
        except UnboundLocalError as e:
            # 一般是出现滑块验证码了，用selenium解决，并保存cookie等待下次请求
            print(f'无数据', e, response.url)
            return
            # 中间件会自动处理滑块验证码
            yield scrapy.Request(url=response.url, callback=self.parse)
        except Exception as e:
            print(f'解析数据时出错: {e}')
            yield scrapy.Request(url=response.url, callback=self.parse)
