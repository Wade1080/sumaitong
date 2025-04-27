import time

from scrapy import cmdline
# cmdline.execute('scrapy crawl sumaitong_crawler -o output.json'.split())


# cmdline.execute('scrapy crawl ProductsInfoSpider -a keyword=injector -o product_infos.json'.split())
cmdline.execute('scrapy crawl ShopInfoSpider -a seller_id=6001082689 -o shop_infos.json'.split())
'''
    https://shoprenderview.aliexpress.com/async/execute?componentKey=allitems_choice&deviceId=1x6IL1R0BUCAbeyVerUp2ai&SortType=bestmatch_sort&page=2&pageSize=30&country=US&site=glo&sellerId=6001142477&groupId=1&currency=USD&locale=en_US&buyerId=6119750368&callback=jsonp_1745201556628_2601
    https://shoprenderview.aliexpress.com/async/execute?componentKey=allitems_choice&deviceId=1x6IL1R0BUCAbeyVerUp2ai&SortType=bestmatch_sort&page=1&pageSize=30&country=US&site=glo&sellerId=%222676553908%22&groupId=1&currency=USD&locale=en_US&buyerId=6340368875&callback=jsonp_1745201774000_64535
'''
