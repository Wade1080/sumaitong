# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import json
import os

from sumaitong import settings
from sumaitong.items import ProductListItem, ShopDetailItem, ProductDetailItem


class BasePipeline:
    def __init__(self):
        self.conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            port=settings.MYSQL_PORT,
            database=settings.MYSQL_DB_NAME,
            use_unicode=True
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        pass


'''
class SumaitongPipeline(BasePipeline):
    def process_item(self, item, spider):
        try:
            self.cur.execute(
                'insert into products(store_name, product_name, price, sales, keyword) values (%s, %s, %s, %s, %s)',
                (item['store_name'], item['product_name'], item['price'], item['sales'], item['keyword'])
            )
            self.conn.commit()
        except Exception as e:
            print(f'Pipeline Error: {e}')
            self.conn.rollback()
        finally:
            return item


class SumaitongShopPipeline(BasePipeline):
    def process_item(self, item, spider):
        print(f'item====>{item}')
        try:
            self.cur.execute(
                'insert into shop_listing(store_name, seller_id, product_name, price, sales) values (%s, %s, %s, %s, %s)',
                (item['store_name'], item['seller_id'], item['product_name'], item['price'], item['sales'])
            )
            self.conn.commit()
        except Exception as e:
            print(f'Pipeline Error: {e}')
            self.conn.rollback()
        finally:
            return item

'''


class ProductListPipeline(BasePipeline):
    def process_item(self, item, spider):
        if isinstance(item, ProductListItem):
            # 处理商品列表页的数据————这里处理搜索单一商品的存储
            # print(f'item====>{item}')
            try:
                self.cur.execute(
                    'insert into products(store_name, product_name, price, sales, keyword, seller_id,ranking) values (%s, %s, %s, %s, %s, %s, %s)',
                    (item['store_name'], item['product_name'], item['price'], item['sales'], item['keyword'],
                     item['seller_id'], item['ranking'])
                )
                self.conn.commit()
                print(f'商品页数据爬取成功')
            except Exception as e:
                print(f'Pipeline Error: {e}')
                self.conn.rollback()
            finally:
                return item
        return item


class ShopDetailPipeline(BasePipeline):

    def process_item(self, item, spider):
        if isinstance(item, ShopDetailItem):
            # 处理店铺详情页的数据—————这里处理单一店铺的售货商品页
            # 可以在这里添加特定的处理逻辑
            '''
            store_name, seller_id, product_name, price, sales, shop_rating, total_count, product_id, img_url, average_star_rate, average_star, feedbacks
            '''

            try:
                self.cur.execute(
                    'insert into shop_listing(seller_id, product_name, price, sales, total_count, product_id, img_url, average_star_rate, average_star, feedbacks) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (item["seller_id"], item["product_name"], item["price"], item["sales"],
                     item["total_count"], item["product_id"], item["img_url"],
                     item["average_star_rate"], item["average_star"], item["feedbacks"])
                )
                self.conn.commit()
                print(f'店铺页数据爬取成功')

            except Exception as e:
                print(f'Pipeline Error: {e}')
                self.conn.rollback()
            finally:
                return item
        return item


class ProductDetailPipeline(BasePipeline):
    def process_item(self, item, spider):
        if isinstance(item, ProductDetailItem):
            # 处理商品详情页的数据
            # 可以在这里添加特定的处理逻辑
            return item
        return item


class SumaitongPipeline:
    def __init__(self):
        self.results = []

    def process_item(self, item, spider):
        self.results.append(dict(item))
        return item

    def close_spider(self, spider):
        # 确保目录存在
        os.makedirs('results', exist_ok=True)
        # 保存结果到 JSON 文件
        with open('results/crawler_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
