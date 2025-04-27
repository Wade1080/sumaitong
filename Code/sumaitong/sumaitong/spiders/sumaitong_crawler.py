import math
import time

import requests
import scrapy
from scrapy import Request
import re
import json
import sys
import os
import random

from sumaitong.items import SumaitongItem, SumaitongShopItem, ProductListItem, ShopDetailItem
from sumaitong_login import SumaitongLogin


class SumaitongCrawlerSpider(scrapy.Spider):
    name = "sumaitong_crawler"
    allowed_domains = ["aliexpress.us"]

     # keyword = input('请输入关键词：')
    keyword = 'injector'
    # 传入一个数组[], 多个关键词
    # injector的位置 和 后面拼接page参数调整即可拿到对应页面的数据
    start_urls = [f"https://www.aliexpress.us/w/wholesale-{keyword}.html?spm=a2g0o.productlist.search.0"]
    # start_urls = ["https://www.aliexpress.us/w/wholesale-injector-fuel.html?spm=a2g0o.home.search.0"]

    # def __init__(self, keyword='injector', start_page=1, *args, **kwargs):
    #     super(SumaitongCrawlerSpider, self).__init__(*args, **kwargs)
    #     self.keyword = keyword
    #     self.start_page = start_page
    #     self.start_urls = [f"https://www.aliexpress.us/w/wholesale-{keyword}.html?page={start_page}&spm=a2g0o.productlist.search.0"]
    # login_url = "https://login.aliexpress.com/"
    # custom_settings = {'FEED_URI': 'tutorial/outputfile.json',
    #                    'CLOSESPIDER_TIMEOUT': 15}  # This will tell scrapy to store the scraped data to outputfile.json and for how long the spider should run.

    # def __init__(self, category='', **kwargs):  # The category variable will have the input URL.
    #     self.myBaseUrl = category
    #     self.start_urls.append(self.myBaseUrl)
    #     super().__init__(**kwargs)
    # def start_requests(self):
    #     print(self.keyword)
    #     with open('cookies.txt', 'r') as f:
    #         cookies = f.read()
    #         try:
    #             cookies = json.loads(cookies)
    #         except json.JSONDecodeError:
    #             cookies = {}
    #
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse, cookies=cookies)

    # 数据放在respoonse 中script标签中的window._dida_config_._init_data_
    def parse(self, response, **kwargs):
        # 检查是否是中间件处理完滑块验证后的响应
        # print(f'response.status: {response.status}')
        # print(f'response.text: {response.text}')
        if response.meta.get('callback') == 'parse_specific_store_products':
            return self.parse_specific_store_products(response)

        base_url = 'https://www.aliexpress.us/w/wholesale-injector.html?page={}spm=a2g0o.productlist.search.0'
        content = response.text
        # with open('./content.html', 'w', encoding='utf-8') as f:
        #     f.write(content)

        # print(content)
        # 使用正则表达式提取window._dida_config_变量值
        # pattern = r'window\._dida_config_ = (.*?);'
        pattern = r'/\*!-->init-data-start--\*/\s*?window\._dida_config_\._init_data_\s*=\s*{ data: (.*)}/\*!-->init-data-end'
        match1 = re.search(pattern, content, re.DOTALL)
        print(match1)
        if not match1:
            # 如果未找到数据，这里要重新登录获取cookie，增加爬虫稳定性
            print('未找到数据', response.url)
            yield scrapy.Request(url=response.url, callback=self.parse)
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
                # print(f'current_page:{current_page}, total_page:{total_page}')
                next_page_flag = True if current_page < total_page else False
            # 正则提取
            for info in data["data"]["root"]["fields"]["mods"]["itemList"]["content"]:
                product_name = info.get('title').get('displayTitle', None)
                price = info["prices"].get('salePrice').get('minPrice', None)
                store_name = info.get('store').get('storeName')
                seller_id = info.get('store', {}).get('aliMemberId', None)
                # 获取到的商店地址，如 www.aliexpress.com/store/1101348591
                store_id = info.get('store',{}).get('storeId', None)
                sales = int(
                    info["trade"]["tradeDesc"].split("sold")[0].strip().replace("+", "").replace(",", "")) if info.get(
                    'trade',
                    {}).get(
                    'tradeDesc') else None

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
                yield items
                # print('提交完item...')
                # print(f'{response.url}爬取成功')

                # 商家主页接口
                shop_api = 'https://shoprenderview.aliexpress.com/async/execute'
                # print(f'seller_id:{seller_id}')
                params = {
                    'componentKey': 'allitems_choice',
                    # 'deviceId': '1x6IL1R0BUCAbeyVerUp2ai',
                    'SortType': 'bestmatch_sort',
                    'page': '1',
                    'pageSize': '30',
                    'country': 'US',
                    "site": "glo",
                    "sellerId": seller_id,
                    "groupId": "1",
                    "currency": "USD",
                    "locale": "en_US",
                    # "buyerId": "6340368875",
                    "callback": f"jsonp_{int(time.time()) * 1000}_{math.ceil(1e5 * random.random())}",
                }
                url = shop_api + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
                # print(f'商家主页url===>{url}')
                # cookies = {
                #
                # }
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'priority': 'u=0, i',
                    # 'referer': 'https://shoprenderview.aliexpress.com//async/execute/_____tmd_____/punish?x5secdata=xc3Pdt26Kqyva6PVnoVWy11YnD0URdVdMZ8GdHWrWP%2fLx1d%2f9cv2aW5HiX4LrucczA5BU2tmUwLZFsb9DiGP3CUURDoVN5U4KyiqmdLmsVHH9SyMgHY6e%2f8mZ6QcKshVtxbEnK8cugxUSbqwpnlIWLDZs6BEHefSCLxebifCCEdb4A3y1sqngAA0exPQGCvtJbT%2f58wZQJ9K8OhFCxWqK1U5XBQq0f1y8AIb%2fWGrSWDt4ARbuatRnPfoEZjdVLIb542CQWcFiKi8Fks42ovUPWZwZ3YXt9rluGpLZaW4x4HXg%3d__bx__shoprenderview.aliexpress.com%2fasync%2fexecute&x5step=1',
                    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                    # 'cookie': 'cna=+1x6IL1R0BUCAbeyVerUp2ai; ali_apache_id=33.102.97.193.174469945229.089285.3; xman_us_f=x_locale=en_US&x_l=1&x_c_chg=1&acs_rt=869428fdf3a24c299e5958a33dce3ca4; account_v=1; intl_locale=en_US; xman_f=zYTE/Z1gw29Y8EqsrqKTtuFejzwFITkJje4IjFJP0h/jqzHOpazFQuWgSyTpH5IELsRSuQ7GxQ4VkpLEWSXSMXRNPhgnhmX7djnzyRxu2xZPgq8SUKSPHg==; acs_usuc_t=x_csrf=zeq84k3zg4up&acs_rt=869428fdf3a24c299e5958a33dce3ca4; xman_t=a3O5doSEq9WHaScIACmpw8vvbExYS6SRmzdXLUVv+dpxzxOvSOwMln9rqVDstPM9; aep_usuc_f=site=glo&c_tp=USD&region=CN&b_locale=en_US; x5sec=7b22617365727665722d696e746c3b33223a22307c434c71412b4c384745502b44717051424d4c69386873542b2f2f2f2f2f77453d222c22733b32223a2261356166653663653332643162336538227d; c_csrf=4ff15f2c-d3f7-4cdf-9156-4f627ac3f9f0; JSESSIONID=6817B3A73FD8C0FCDF6E33D16C9F4F43; isg=BJGRy2ADkl4fYP5K4-H5UDkuoJ0r_gVwN_In7HMnYNh3GrNsu071Qms5vO78Ep2o; tfstk=fxinc0TjR2zB9wXJtcqBoJPPhpTOd6ZS4bI8wuFy75P1vbEL2zSosjuLe83dq_PiZuHpdgHzzjH5vzRQv0cg_bjdpYdIsgDIiDQLwpGi6Vu6OBN-p8ct7VGuPpN8a7c-U2p9DnHIduZzqIKvD1JZ61c3UzPyUGyLHB0xDnkIduZPB_8x7v1lIuJyKulzbPyzFuSUabPwb5w7U6yPYdDa18rzL77F_hyYnJSz8jJC4SmrfcR_ZrR-Yu3xjJ4wWvPas5p8dycxL5A2gcfz-SkUsgRXFJVTZ5i26FDsi2lLCbxDsoujs044qHfbKVk0bWE2oNqnBXi0YmAhvRET9ruzSp-EIkV3zcUVewZnzXiuR2XWhArE1qNb8FO_IDnYrSaG_BktIWzmrXd14W3mQf4xX1IY0qGiqrrV45_NuyeNVRJ-ba_78RwgGSAmZDZA8ZJ9IdbXRyy_pIpMIa_78RwgMdvGl_aUCJdA.; intl_common_forever=P6JX1/mwzk42sgcVMbKMiXUgOuLoueGiJ7tK8IC+MovFNSI+KZ0qmg==',
                }
                # 暂不清楚为什么这里会被过滤器给拦住啊，明明前面没有访问这个链接，我猜测是指纹没识别到了
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_specific_store_products,
                    # cookies=cookies,
                    headers=headers,
                    dont_filter=True,
                    meta={
                        'url': url,
                        'seller_id': seller_id,
                        'store_name': store_name,
                        'shop_api': shop_api,
                        'callback': 'parse_specific_store_products',  # 添加callback标记
                        'keyword': self.keyword
                    }
                )

                # res = requests.get(url=url, cookies=cookies, headers=headers)
                # print('结束啦', res.text)
                # with open('./assets/shop_info.txt', 'w', encoding='utf-8') as f:
                #     f.write(res.text)
                # return  # 测试

            # Xpath 提取 （失效）
            # div_list = response.xpath('//div[@class="hs_ht"]/div')
            # print(f'长度为{len(div_list)}')
            # for div in div_list:
            #     title = div.xpath('./div[@class="l5_kq"]//h3[@class="l5_j0"]/text()').extract_first()
            #     total_sales = div.xpath('./div[@class="l5_kq"]//span[@class="l5_jv"]/text()').extract_first()
            #     price = div.xpath('./div[@class="l5_kq"]//div[@class="l5_k6"]//text()').extract()
            #     price = ''.join(price)
            #     store = div.xpath('./div[@class="l5_kq"]//span[@class="io_ip"]//text()').extract_first()
            #     print(title, total_sales, price, store)
            #     yield {
            #         "title": title,
            #         "total_sales": total_sales,
            #         "price": price,
            #         "store": store
            #     }
            # 测试
            # return
            # 翻页

            if next_page_flag:
                print(f'开始爬取{current_page + 1}页')
                yield Request(base_url.format(current_page + 1), callback=self.parse)
            else:
                print('商品页爬取完毕')
        except UnboundLocalError as e:
            # 一般是出现滑块验证码了，用selenium解决，并保存cookie等待下次请求
            print(f'无数据', e, response.url)
            return
            # 中间件会自动处理滑块验证码
            yield scrapy.Request(url=response.url, callback=self.parse)
        except Exception as e:
            print(f'解析数据时出错: {e}')
            yield scrapy.Request(url=response.url, callback=self.parse)
    def parse_specific_store_products(self, response):
        print(f'正在解析商铺主页...{response.url}')
        jsonp_data = response.text
        with open('./assets/jsonp.txt', 'w', encoding='utf-8') as f:
            f.write(jsonp_data)
        pattern = r'jsonp_\d{13}_\d{5}\((.*?"success":true})\)'
        match = re.search(pattern, jsonp_data)

        if match:
            output = json.loads(match.group(1))
            print('match!!!')
            # 安全地获取数据
            try:
                result = output.get('result', {})
                products = result.get('products', {})

                if not products:
                    print('未找到商品数据')
                    return

                current_page = products.get('currentPage')
                total_page = products.get('totalPage')
                datas = products.get('data', [])
                total_count = products.get('totalCount')
                if not datas:
                    print('商品数据为空')
                    return

                print(f'current page: {current_page} total_page: {total_page}')

                # 处理商品数据
                for data in datas:
                    try:
                        subject = data.get('subject', '')
                        price = data.get('promotionPiecePriceMoney', {}).get('amount') or \
                                data.get('previewPromotionPiecePriceMoney', {}).get('amount')
                        sales = data.get('sales', 0) or data.get('orders', 0)
                        product_id = data.get('id')
                        img_url = data.get('image350Url')
                        average_star_rate = data.get('averageStarRate')
                        average_star = data.get('averageStar')
                        print(f'average_star=====>{average_star}')
                        feedbacks = data.get('feedbacks')

                        # print(f'subject: {subject}')
                        # print(f'price: {price}')
                        # print(f'sales: {sales}')
                        items = ShopDetailItem()
                        items['product_name'] = subject
                        items['price'] = price
                        items['store_name'] = response.meta["store_name"]
                        items['sales'] = sales
                        items['seller_id'] = response.meta["seller_id"]
                        items['total_count'] = total_count
                        items['product_id'] = product_id
                        items['img_url'] = img_url
                        items['average_star_rate'] = average_star_rate
                        items['average_star'] = average_star
                        items['feedbacks'] = feedbacks
                        # items['keyword'] = response.meta["keyword"]
                        yield items
                    except Exception as e:
                        print(f'处理商品数据时出错: {e}')
                        continue

                # 处理翻页
                if current_page and total_page and current_page < total_page:
                    next_page = current_page + 1
                    seller_id = response.meta.get('seller_id')
                    shop_api = response.meta.get('shop_api')

                    if not all([seller_id, shop_api]):
                        print('缺少必要的翻页参数')
                        return

                    # 构建下一页的请求参数
                    params = {
                        'componentKey': 'allitems_choice',
                        'deviceId': '1x6IL1R0BUCAbeyVerUp2ai',
                        'SortType': 'bestmatch_sort',
                        'page': str(next_page),  # 确保是字符串
                        'pageSize': '30',
                        'country': 'US',
                        'site': 'glo',
                        'sellerId': seller_id,
                        'groupId': '1',
                        'currency': 'USD',
                        'locale': 'en_US',
                        # 'buyerId': '6340368875',
                        'buyerId': '6119750368',
                        'callback': f'jsonp_{int(time.time() * 1000)}_{math.ceil(1e5 * random.random())}',
                    }

                    next_url = f'{shop_api}?{"&".join(f"{k}={v}" for k, v in params.items())}'
                    print(f'准备爬取下一页: {next_url}')

                    # 使用与初始请求相同的 cookies 和 headers
                    # cookies = {
                    #     'cna': '+1x6IL1R0BUCAbeyVerUp2ai',
                    #     'ali_apache_id': '33.102.97.193.174469945229.089285.3',
                    #     'xman_us_f': 'x_locale=en_US&x_l=1&x_c_chg=1&acs_rt=869428fdf3a24c299e5958a33dce3ca4',
                    #     'account_v': '1',
                    #     'intl_locale': 'en_US',
                    #     'xman_f': 'zYTE/Z1gw29Y8EqsrqKTtuFejzwFITkJje4IjFJP0h/jqzHOpazFQuWgSyTpH5IELsRSuQ7GxQ4VkpLEWSXSMXRNPhgnhmX7djnzyRxu2xZPgq8SUKSPHg==',
                    #     'acs_usuc_t': 'x_csrf=zeq84k3zg4up&acs_rt=869428fdf3a24c299e5958a33dce3ca4',
                    #     'xman_t': 'a3O5doSEq9WHaScIACmpw8vvbExYS6SRmzdXLUVv+dpxzxOvSOwMln9rqVDstPM9',
                    #     'aep_usuc_f': 'site=glo&c_tp=USD&region=CN&b_locale=en_US',
                    #     'x5sec': '7b22617365727665722d696e746c3b33223a22307c434c71412b4c384745502b44717051424d4c69386873542b2f2f2f2f2f77453d222c22733b32223a2261356166653663653332643162336538227d',
                    #     'c_csrf': '4ff15f2c-d3f7-4cdf-9156-4f627ac3f9f0',
                    #     'JSESSIONID': '6817B3A73FD8C0FCDF6E33D16C9F4F43',
                    #     'isg': 'BJGRy2ADkl4fYP5K4-H5UDkuoJ0r_gVwN_In7HMnYNh3GrNsu071Qms5vO78Ep2o',
                    #     'tfstk': 'fxinc0TjR2zB9wXJtcqBoJPPhpTOd6ZS4bI8wuFy75P1vbEL2zSosjuLe83dq_PiZuHpdgHzzjH5vzRQv0cg_bjdpYdIsgDIiDQLwpGi6Vu6OBN-p8ct7VGuPpN8a7c-U2p9DnHIduZzqIKvD1JZ61c3UzPyUGyLHB0xDnkIduZPB_8x7v1lIuJyKulzbPyzFuSUabPwb5w7U6yPYdDa18rzL77F_hyYnJSz8jJC4SmrfcR_ZrR-Yu3xjJ4wWvPas5p8dycxL5A2gcfz-SkUsgRXFJVTZ5i26FDsi2lLCbxDsoujs044qHfbKVk0bWE2oNqnBXi0YmAhvRET9ruzSp-EIkV3zcUVewZnzXiuR2XWhArE1qNb8FO_IDnYrSaG_BktIWzmrXd14W3mQf4xX1IY0qGiqrrV45_NuyeNVRJ-ba_78RwgGSAmZDZA8ZJ9IdbXRyy_pIpMIa_78RwgMdvGl_aUCJdA.',
                    #     'intl_common_forever': 'P6JX1/mwzk42sgcVMbKMiXUgOuLoueGiJ7tK8IC+MovFNSI+KZ0qmg==',
                    # }
                    cookies = {
                        'x5sec': '7b22617365727665722d696e746c3b33223a22307c434943392f4c3847454d434b6f4f6f474d5036503668513d222c22733b32223a2231626539346262323164353932353731227d',
                        'isg': 'BMHBNfLpQu_RjK7XFnrQJPm80A3b7jXgx-JXnCMWe0gnCuDcaz8nsqhL7H5MAs0Y',
                        'tfstk': 'fVRxco9eW0mcdtDMGEMuI4G5HlgkHIL2zn8QsGj0C3KJRercCx-i65L25Nvcmiv81FsPcofbiPK94HFmuh02wfKJmKAcjsX6en8Cn1fjg3xkFLPGncl2q3f2ZKVGmm595HftxDcntE8Va1inx9z6F7CC7-N_jZa5V7yQpKhntE84oZgHPXADlKDRXG11hO65Vg7a11sff4I5Wwy_ch1syUsPRZ_1fGa5PwbgfbOEXgafj5peW2f1Fom8s5ARPcSBkAPOrQ_AFMTXM5NsdZBAAEs-YK9w7TTNBCza6OLXLh7BcoiObQLWGptIq-jXpNLHBEGbNsA2lp66Ocy6osjANI9L55TRMgBM6Trx2MO2PB55EXgpPQ-DuQLg5f_kxgT2G1hI8sCfc_Qys0PfXL96it5accIwwUOXBg-JtBeLdkjdS-g-yRyNhamKxNJq8Nr0yaInkfeaQTuPyM0-yRyNha7RxqnYQRWrz',
                        'x_router_us_f': 'x_alimid=6345377806',
                        'xman_us_t': 'x_lid=us1896755806rtwae&sign=y&rmb_pp=zcw1080@163.com&x_user=LUJ/Dqkw6H44DbaVgoSNEeFz+YZSErtnyhCIx8qat0I=&ctoken=1a95c5x0ri04q&l_source=aliexpress',
                        'aep_usuc_f': 'isb=y&x_alimid=6345377806',
                        'acs_usuc_t': 'acs_rt=500a2d7bb0ef44c8bf75688fac73e509&x_csrf=cn1bxhwj9_6j',
                        'sgcookie': 'E100zplimpfB5TR+yoSCH32Sm0EbwmV8tPdi3lXMwVyRoC6ReXrfeFou9wTrJjuiyPxMAAOGP8yD+k3RQ4RBlUZjUYCV6tFneu1JvGUdBW7PTuM=',
                        'aep_common_f': 'fOfFvYQpDFsHBeHzWKT3tbyPWvHuSqGWQoFnPydi0FdNg5G2Y2NsIQ==',
                        'xman_t': 'KH4FDqwTloBS/4Mauuxv4EeZrsz9n2aKVyAG5u79y2bfXsCqSN15PvJ6T8ddToQEDzUnVVeVyGMOD2M/zoiWdOy/CWusE9Nasax7Te6QrZua89ohSU/h10Dch3BnSjjj/XFgzSthKzwSKVkxZnvCM397szoJ0NvCQuAMQzIYt/hilZqsVHqvR2PCm6j+B9LOnR6sbAtxhAaMkIFO04Wc41oWjk9FbxNGcBUvMc6JZO5/VCSY9pPknY/oCPU8OEhRQInCUsgm3w+12ASffzbMh72ToqSNU+TrJi7+JRTUeGH4s4sUnSynfGyvZejvA7WqnM6WEcfufFMcVwgaZP67hw1C/07KQWrau94GYzeiSAKAPSOZfUBCjZq+ztvwAcrdZQYFg14D0x6jBD3V9eTNREoXA1c/d0Q54f1+6nVE0KW1fa8VzBrDFpJkGX3yw3H5/Bz0qRWyKs/nBMb/faHyaGDooUwgPdVvupQlYZc6hAvPtKdIrGaDj7QYfFiCunclW5cP9uynYi1DaAjmHee1ykJlsOMELXdhQVUQbgjxcyo89+SLfzMAnKx8KVIweX/LZj03EC6oTZem2FrA77Yn0Pyr1YtnHCGLAVMeX9jBWGLm5vORvSErA4AGR6wVJVe7N/NcYfMUZxgRGE/zU2ZmgszCBh3k2kVDTQTATWeSnD7DFezVi8LZKzshU+LJFXmxGwaWOZMLuk//lRNR3WzMPzxbB3XbBbvkaj9R4DcqIhk=',
                        'xman_us_f': 'x_lid=us1896755806rtwae&x_l=1&x_user=US|zcw1080|user|ifm|6345377806&zero_order=y&acs_rt=2d80dc2cf3a449b8aaebfc75f15c82d0',
                        '_ga': 'GA1.1.1995285917.1744706971',
                        '_ga_save': 'yes',
                        'xman_f': 'zGDgNvYbW1S6mUDPrXimCF/mB4ilEG1bLb+8ZvVFeCFZMyS/Jh0udZv8j6wrTzLvp12N/yPtcRUjuNbz/IKuHf5zCuiEOo12Xw9QuWHjPqDYeb43FM6F72SdEmvgI/31H5A27qYBOybbuHrCKtM9RPFM3eheCZ9mExb7k/qiF0OqVaLTbixsumhce+3BzT4SEp4FJkVPxSuGmggPjieQZPPRvVeedg3k56pD5Lm3Q0DU6/TJXqU1nT41YnO8ZhIT4C+4AmXJhY2GzrjXMTZBTbzFThLIUrvxuSWQGiHEy0jvbwImrJCz/BF5fBHH+0sTXcxaeDR2/tAyDGRN2FrUINIJet1voykOLKEr5I3/ibSXFpbAbqz+jofjqUDWlm+U',
                    }
                    headers = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'cache-control': 'no-cache',
                        'pragma': 'no-cache',
                        'priority': 'u=0, i',
                        'referer': 'https://www.aliexpress.us/',  # 使用当前页面作为 referer
                        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'same-origin',
                        # 'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                    }

                    yield scrapy.Request(
                        url=next_url,
                        callback=self.parse_specific_store_products,
                        cookies=cookies,
                        headers=headers,
                        meta={
                            'seller_id': seller_id,
                            'shop_api': shop_api,
                            'retry_count': response.meta.get('retry_count', 0) + 1,
                            'callback': 'parse_specific_store_products',  # 添加 callback 标记
                            'store_name': response.meta.get('store_name', '')
                        },
                        dont_filter=True  # 允许重复请求
                    )

            except Exception as e:
                print(f'处理数据时出错: {e}')
                return
        else:
            print('failed')
            # 重试
            yield Request(url=response.url, callback=self.parse_specific_store_products, dont_filter=True)
        # # 保存响应内容用于调试
        # with open('./assets/products.jsonp', 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        #     print(f'已将返回商品内容写入products.jsonp')


'''
        try:
            # 尝试多种方式提取 JSONP 数据
            jsonp_data = None
            patterns = [
                r'^[^(]*$({.*})$$'
                # r'jsonp_\d+_\d+\((.*?)\)'  # 标准格式
                # r'jsonp_\d+_\d+\((.*)\)',  # 宽松格式
                # r'\((.*?)\)',  # 最宽松格式
            ]

            for pattern in patterns:
                match = re.search(pattern, response.text, re.DOTALL)
                if match:
                    jsonp_data = match.group(1)
                    print((f'jsonp_data===>{jsonp_data}'))
                    print(f'使用模式 {pattern} 匹配到 JSONP 数据')
                    break

            if not jsonp_data:
                print('未匹配到 JSONP 数据')
                return

            # 清理 JSON 数据
            jsonp_data = jsonp_data.strip()
            if jsonp_data.endswith(';'):
                jsonp_data = jsonp_data[:-1]

            # 尝试修复 JSON 数据
            try:
                # # 移除可能的非法字符
                jsonp_data = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', jsonp_data)
                # # 处理可能的转义字符
                jsonp_data = jsonp_data.replace('\\/', '/')
                # # 处理可能的未闭合引号
                jsonp_data = re.sub(r'(?<!\\)"(?!\s*[}\]])', '\\"', jsonp_data)
                #
                output = json.loads(jsonp_data)
            except json.JSONDecodeError as e:
                print(f'JSON 解析错误: {e}')
                # 尝试更激进的修复
                try:
                    # 移除所有控制字符
                    jsonp_data = ''.join(char for char in jsonp_data if ord(char) >= 32)
                    # 处理可能的未闭合对象
                    if jsonp_data.count('{') > jsonp_data.count('}'):
                        jsonp_data += '}' * (jsonp_data.count('{') - jsonp_data.count('}'))
                    output = json.loads(jsonp_data)
                except json.JSONDecodeError as e2:
                    print(f'修复后仍然无法解析 JSON: {e2}')
                    with open('track_error.txt', 'w', encoding='utf-8') as f:
                        try:
                            print('正在用json格式保存修复前数据')
                            json.dump(jsonp_data, f, ensure_ascii=False, indent=2)
                        except json.JSONDecodeError as e:
                            print('保存失败，将数据转写为文本格式')
                            f.write(jsonp_data)
                            print('写入成功')

                    return

            # 保存解析后的 JSON 数据
            with open('./assets/products.json', 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)

            # 安全地获取数据
            try:
                result = output.get('result', {})
                products = result.get('products', {})

                if not products:
                    print('未找到商品数据')
                    return

                current_page = products.get('currentPage')
                total_page = products.get('totalPage')
                datas = products.get('data', [])

                if not datas:
                    print('商品数据为空')
                    return

                print(f'current page: {current_page} total_page: {total_page}')

                # 处理商品数据
                for data in datas:
                    try:
                        subject = data.get('subject', '')
                        price = data.get('promotionPiecePriceMoney', {}).get('amount') or \
                                data.get('previewPromotionPiecePriceMoney', {}).get('amount')
                        sales = data.get('sales', 0)

                        print(f'subject: {subject}')
                        print(f'price: {price}')
                        print(f'sales: {sales}')

                    except Exception as e:
                        print(f'处理商品数据时出错: {e}')
                        continue

                # 处理翻页
                if current_page and total_page and current_page < total_page:
                    next_page = current_page + 1
                    seller_id = response.meta.get('seller_id')
                    shop_api = response.meta.get('shop_api')

                    if not all([seller_id, shop_api]):
                        print('缺少必要的翻页参数')
                        return

                    # 构建下一页的请求参数
                    params = {
                        'componentKey': 'allitems_choice',
                        'deviceId': '1x6IL1R0BUCAbeyVerUp2ai',
                        'SortType': 'bestmatch_sort',
                        'page': str(next_page),  # 确保是字符串
                        'pageSize': '30',
                        'country': 'US',
                        'site': 'glo',
                        'sellerId': seller_id,
                        'groupId': '1',
                        'currency': 'USD',
                        'locale': 'en_US',
                        # 'buyerId': '6340368875',
                        'buyerId': '6119750368',
                        'callback': f'jsonp_{int(time.time() * 1000)}_{math.ceil(1e5 * random.random())}',
                    }

                    next_url = f'{shop_api}?{"&".join(f"{k}={v}" for k, v in params.items())}'
                    print(f'准备爬取下一页: {next_url}')

                    # 使用与初始请求相同的 cookies 和 headers
                    # cookies = {
                    #     'cna': '+1x6IL1R0BUCAbeyVerUp2ai',
                    #     'ali_apache_id': '33.102.97.193.174469945229.089285.3',
                    #     'xman_us_f': 'x_locale=en_US&x_l=1&x_c_chg=1&acs_rt=869428fdf3a24c299e5958a33dce3ca4',
                    #     'account_v': '1',
                    #     'intl_locale': 'en_US',
                    #     'xman_f': 'zYTE/Z1gw29Y8EqsrqKTtuFejzwFITkJje4IjFJP0h/jqzHOpazFQuWgSyTpH5IELsRSuQ7GxQ4VkpLEWSXSMXRNPhgnhmX7djnzyRxu2xZPgq8SUKSPHg==',
                    #     'acs_usuc_t': 'x_csrf=zeq84k3zg4up&acs_rt=869428fdf3a24c299e5958a33dce3ca4',
                    #     'xman_t': 'a3O5doSEq9WHaScIACmpw8vvbExYS6SRmzdXLUVv+dpxzxOvSOwMln9rqVDstPM9',
                    #     'aep_usuc_f': 'site=glo&c_tp=USD&region=CN&b_locale=en_US',
                    #     'x5sec': '7b22617365727665722d696e746c3b33223a22307c434c71412b4c384745502b44717051424d4c69386873542b2f2f2f2f2f77453d222c22733b32223a2261356166653663653332643162336538227d',
                    #     'c_csrf': '4ff15f2c-d3f7-4cdf-9156-4f627ac3f9f0',
                    #     'JSESSIONID': '6817B3A73FD8C0FCDF6E33D16C9F4F43',
                    #     'isg': 'BJGRy2ADkl4fYP5K4-H5UDkuoJ0r_gVwN_In7HMnYNh3GrNsu071Qms5vO78Ep2o',
                    #     'tfstk': 'fxinc0TjR2zB9wXJtcqBoJPPhpTOd6ZS4bI8wuFy75P1vbEL2zSosjuLe83dq_PiZuHpdgHzzjH5vzRQv0cg_bjdpYdIsgDIiDQLwpGi6Vu6OBN-p8ct7VGuPpN8a7c-U2p9DnHIduZzqIKvD1JZ61c3UzPyUGyLHB0xDnkIduZPB_8x7v1lIuJyKulzbPyzFuSUabPwb5w7U6yPYdDa18rzL77F_hyYnJSz8jJC4SmrfcR_ZrR-Yu3xjJ4wWvPas5p8dycxL5A2gcfz-SkUsgRXFJVTZ5i26FDsi2lLCbxDsoujs044qHfbKVk0bWE2oNqnBXi0YmAhvRET9ruzSp-EIkV3zcUVewZnzXiuR2XWhArE1qNb8FO_IDnYrSaG_BktIWzmrXd14W3mQf4xX1IY0qGiqrrV45_NuyeNVRJ-ba_78RwgGSAmZDZA8ZJ9IdbXRyy_pIpMIa_78RwgMdvGl_aUCJdA.',
                    #     'intl_common_forever': 'P6JX1/mwzk42sgcVMbKMiXUgOuLoueGiJ7tK8IC+MovFNSI+KZ0qmg==',
                    # }
                    cookies = {
                        'x5sec': '7b22617365727665722d696e746c3b33223a22307c434943392f4c3847454d434b6f4f6f474d5036503668513d222c22733b32223a2231626539346262323164353932353731227d',
                        'isg': 'BMHBNfLpQu_RjK7XFnrQJPm80A3b7jXgx-JXnCMWe0gnCuDcaz8nsqhL7H5MAs0Y',
                        'tfstk': 'fVRxco9eW0mcdtDMGEMuI4G5HlgkHIL2zn8QsGj0C3KJRercCx-i65L25Nvcmiv81FsPcofbiPK94HFmuh02wfKJmKAcjsX6en8Cn1fjg3xkFLPGncl2q3f2ZKVGmm595HftxDcntE8Va1inx9z6F7CC7-N_jZa5V7yQpKhntE84oZgHPXADlKDRXG11hO65Vg7a11sff4I5Wwy_ch1syUsPRZ_1fGa5PwbgfbOEXgafj5peW2f1Fom8s5ARPcSBkAPOrQ_AFMTXM5NsdZBAAEs-YK9w7TTNBCza6OLXLh7BcoiObQLWGptIq-jXpNLHBEGbNsA2lp66Ocy6osjANI9L55TRMgBM6Trx2MO2PB55EXgpPQ-DuQLg5f_kxgT2G1hI8sCfc_Qys0PfXL96it5accIwwUOXBg-JtBeLdkjdS-g-yRyNhamKxNJq8Nr0yaInkfeaQTuPyM0-yRyNha7RxqnYQRWrz',
                        'x_router_us_f': 'x_alimid=6345377806',
                        'xman_us_t': 'x_lid=us1896755806rtwae&sign=y&rmb_pp=zcw1080@163.com&x_user=LUJ/Dqkw6H44DbaVgoSNEeFz+YZSErtnyhCIx8qat0I=&ctoken=1a95c5x0ri04q&l_source=aliexpress',
                        'aep_usuc_f': 'isb=y&x_alimid=6345377806',
                        'acs_usuc_t': 'acs_rt=500a2d7bb0ef44c8bf75688fac73e509&x_csrf=cn1bxhwj9_6j',
                        'sgcookie': 'E100zplimpfB5TR+yoSCH32Sm0EbwmV8tPdi3lXMwVyRoC6ReXrfeFou9wTrJjuiyPxMAAOGP8yD+k3RQ4RBlUZjUYCV6tFneu1JvGUdBW7PTuM=',
                        'aep_common_f': 'fOfFvYQpDFsHBeHzWKT3tbyPWvHuSqGWQoFnPydi0FdNg5G2Y2NsIQ==',
                        'xman_t': 'KH4FDqwTloBS/4Mauuxv4EeZrsz9n2aKVyAG5u79y2bfXsCqSN15PvJ6T8ddToQEDzUnVVeVyGMOD2M/zoiWdOy/CWusE9Nasax7Te6QrZua89ohSU/h10Dch3BnSjjj/XFgzSthKzwSKVkxZnvCM397szoJ0NvCQuAMQzIYt/hilZqsVHqvR2PCm6j+B9LOnR6sbAtxhAaMkIFO04Wc41oWjk9FbxNGcBUvMc6JZO5/VCSY9pPknY/oCPU8OEhRQInCUsgm3w+12ASffzbMh72ToqSNU+TrJi7+JRTUeGH4s4sUnSynfGyvZejvA7WqnM6WEcfufFMcVwgaZP67hw1C/07KQWrau94GYzeiSAKAPSOZfUBCjZq+ztvwAcrdZQYFg14D0x6jBD3V9eTNREoXA1c/d0Q54f1+6nVE0KW1fa8VzBrDFpJkGX3yw3H5/Bz0qRWyKs/nBMb/faHyaGDooUwgPdVvupQlYZc6hAvPtKdIrGaDj7QYfFiCunclW5cP9uynYi1DaAjmHee1ykJlsOMELXdhQVUQbgjxcyo89+SLfzMAnKx8KVIweX/LZj03EC6oTZem2FrA77Yn0Pyr1YtnHCGLAVMeX9jBWGLm5vORvSErA4AGR6wVJVe7N/NcYfMUZxgRGE/zU2ZmgszCBh3k2kVDTQTATWeSnD7DFezVi8LZKzshU+LJFXmxGwaWOZMLuk//lRNR3WzMPzxbB3XbBbvkaj9R4DcqIhk=',
                        'xman_us_f': 'x_lid=us1896755806rtwae&x_l=1&x_user=US|zcw1080|user|ifm|6345377806&zero_order=y&acs_rt=2d80dc2cf3a449b8aaebfc75f15c82d0',
                        '_ga': 'GA1.1.1995285917.1744706971',
                        '_ga_save': 'yes',
                        'xman_f': 'zGDgNvYbW1S6mUDPrXimCF/mB4ilEG1bLb+8ZvVFeCFZMyS/Jh0udZv8j6wrTzLvp12N/yPtcRUjuNbz/IKuHf5zCuiEOo12Xw9QuWHjPqDYeb43FM6F72SdEmvgI/31H5A27qYBOybbuHrCKtM9RPFM3eheCZ9mExb7k/qiF0OqVaLTbixsumhce+3BzT4SEp4FJkVPxSuGmggPjieQZPPRvVeedg3k56pD5Lm3Q0DU6/TJXqU1nT41YnO8ZhIT4C+4AmXJhY2GzrjXMTZBTbzFThLIUrvxuSWQGiHEy0jvbwImrJCz/BF5fBHH+0sTXcxaeDR2/tAyDGRN2FrUINIJet1voykOLKEr5I3/ibSXFpbAbqz+jofjqUDWlm+U',
                    }
                    headers = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'cache-control': 'no-cache',
                        'pragma': 'no-cache',
                        'priority': 'u=0, i',
                        'referer': 'https://www.aliexpress.us/',  # 使用当前页面作为 referer
                        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'same-origin',
                        # 'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                    }

                    yield scrapy.Request(
                        url=next_url,
                        callback=self.parse_specific_store_products,
                        cookies=cookies,
                        headers=headers,
                        meta={
                            'seller_id': seller_id,
                            'shop_api': shop_api,
                            'retry_count': response.meta.get('retry_count', 0) + 1,
                            'callback': 'parse_specific_store_products'  # 添加 callback 标记
                        },
                        dont_filter=True  # 允许重复请求
                    )

            except Exception as e:
                print(f'处理数据时出错: {e}')
                return

        except Exception as e:
            print(f'解析商铺主页时出错: {e}')
            return
'''
