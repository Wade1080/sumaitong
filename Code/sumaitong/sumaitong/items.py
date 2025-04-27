# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SumaitongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    price = scrapy.Field()
    store_name = scrapy.Field()
    sales = scrapy.Field()
    seller_id = scrapy.Field()
    keyword = scrapy.Field()

    # pass


# 定义商店类内信息管道
class SumaitongShopItem(scrapy.Item):
    store_name = scrapy.Field()
    seller_id = scrapy.Field()
    product_name = scrapy.Field()
    price = scrapy.Field()
    sales = scrapy.Field()
    keyword = scrapy.Field()


#
# # 定义商店主页内信息管道
# class SumaitonItem(scrapy.Item):

# 商品列表页的item
class ProductListItem(scrapy.Item):
    product_name = scrapy.Field()
    price = scrapy.Field()
    store_name = scrapy.Field()
    sales = scrapy.Field()
    seller_id = scrapy.Field()
    keyword = scrapy.Field()
    ranking = scrapy.Field()


# 店铺详情页的item
class ShopDetailItem(scrapy.Item):
    # store_name = scrapy.Field()
    seller_id = scrapy.Field()
    product_name = scrapy.Field()
    price = scrapy.Field()
    sales = scrapy.Field()
    # keyword = scrapy.Field()
    # shop_rating = scrapy.Field()  # 店铺评分
    total_count = scrapy.Field()  # 店铺商品总数
    product_id = scrapy.Field()
    # shop_url = scrapy.Field()  # 店铺链接
    img_url = scrapy.Field()
    average_star_rate = scrapy.Field()
    average_star = scrapy.Field()
    feedbacks = scrapy.Field()



# 商品详情页的item
class ProductDetailItem(scrapy.Item):
    product_name = scrapy.Field()
    price = scrapy.Field()
    seller_id = scrapy.Field()
    description = scrapy.Field()  # 商品描述
    specifications = scrapy.Field()  # 商品规格
    reviews = scrapy.Field()  # 商品评价
    shipping_info = scrapy.Field()  # 物流信息
    product_url = scrapy.Field()  # 商品链接
