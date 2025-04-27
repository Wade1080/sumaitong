import json
import math
import random
import re
import time

import requests
import scrapy
from scrapy import Request

from sumaitong.items import ShopDetailItem
import logging

# 店铺页的爬虫
class ShopInfoSpider(scrapy.Spider):
    name = 'ShopInfoSpider'
    allowed_domains = ["aliexpress.us"]
    start_urls = ['https://shoprenderview.aliexpress.com/async/execute?']
    seller_id = ''

    def start_requests(self):
        self.logger.warning('Start requests , the message is from the logging package')
        print('开始预处理请求头')
        for url in self.start_urls:
            params = {
                'componentKey': 'allitems_choice',
                # 'deviceId': '1x6IL1R0BUCAbeyVerUp2ai',
                'SortType': 'bestmatch_sort',
                'page': '1',
                'pageSize': '30',
                'country': 'US',
                "site": "glo",
                "sellerId": self.seller_id,
                "groupId": "1",
                "currency": "USD",
                "locale": "en_US",
                "buyerId": "6340368875",
                'deviceId': '1x6IL1R0BUCAbeyVerUp2ai',
                "callback": f"jsonp_{int(time.time()) * 1000}_{math.ceil(1e5 * random.random())}",
            }
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
            # 修改请求携带参数
            yield scrapy.FormRequest(url=url, method='GET', formdata=params, callback=self.parse, dont_filter=True,
                                     headers=headers)

    def parse(self, response, **kwargs):
        print(f'正在解析商铺主页...{response.url}')
        jsonp_data = response.text
        with open('./assets/jsonp.txt', 'w', encoding='utf-8') as f:
            f.write(jsonp_data)
        pattern = r'jsonp_\d+_\d+\((.*?"success":true})\)'
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
                        price = data.get('promotionPiecePriceMoney', {}).get('amount') or data.get(
                            'previewPromotionPiecePriceMoney', {}).get('amount')
                        sales = data.get('sales', 0) or data.get('orders', 0)
                        product_id = data.get('id')
                        img_url = data.get('image350Url')
                        average_star_rate = data.get('averageStarRate')
                        average_star = data.get('averageStar')
                        print(f'average_star=====>{average_star}')
                        feedbacks = data.get('feedbacks')

                        items = ShopDetailItem()
                        items['product_name'] = subject
                        items['price'] = price
                        # items['store_name'] = response.meta["store_name"]
                        items['sales'] = sales
                        # items['seller_id'] = response.meta["seller_id"]
                        items['total_count'] = total_count
                        items['product_id'] = product_id
                        items['img_url'] = img_url
                        items['average_star_rate'] = average_star_rate
                        items['average_star'] = average_star
                        items['feedbacks'] = feedbacks
                        items['seller_id'] = self.seller_id
                        # items['keyword'] = response.meta["keyword"]
                        yield items
                    except Exception as e:
                        print(f'处理商品数据时出错: {e}')
                        continue

                # 处理翻页，耗时操作在翻页上，翻页是可以并行
                if current_page and total_page and current_page < total_page:
                    next_page = current_page + 1
                    shop_api = 'https://shoprenderview.aliexpress.com/async/execute'
                    # 构建下一页的请求参数
                    params = {
                        'componentKey': 'allitems_choice',
                        'deviceId': '1x6IL1R0BUCAbeyVerUp2ai',
                        'SortType': 'bestmatch_sort',
                        'page': str(next_page),  # 确保是字符串
                        'pageSize': '30',
                        'country': 'US',
                        'site': 'glo',
                        'sellerId': self.seller_id,
                        'groupId': '1',
                        'currency': 'USD',
                        'locale': 'en_US',
                        # 'buyerId': '6340368875',
                        'buyerId': '6119750368',
                        'callback': f'jsonp_{int(time.time() * 1000)}_{math.ceil(1e5 * random.random())}',
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

                    yield scrapy.FormRequest(
                        url=shop_api, method='GET', formdata=params, callback=self.parse, dont_filter=True,
                        headers=headers
                    )


            except Exception as e:
                print(f'处理数据时出错: {e}')
                return
        else:
            print('failed')
            # 重试
            yield Request(url=response.url, dont_filter=True)
