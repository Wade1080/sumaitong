# app.py
import asyncio
import os
import logging
from logging.handlers import RotatingFileHandler
from threading import Thread

import pyfiglet
from twisted.internet import reactor, defer
from flask import Flask, jsonify, request, make_response
import pymysql
from datetime import datetime, timedelta
import json
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.cmdline import execute

import crochet

from sumaitong.spiders.ProductsInfoSpider import ProductsInfoSpider
from sumaitong.spiders.ShopInfoSpider import ShopInfoSpider

crochet.setup()

from flask import Flask, render_template, jsonify, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time
import subprocess

# Importing our Scraping Function from the amazon_scraping file
from sumaitong.spiders.sumaitong_crawler import SumaitongCrawlerSpider

app = Flask(__name__)
runner = CrawlerRunner(get_project_settings())
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 创建文件处理器
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# 创建日志格式器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 将格式器添加到日志记录器
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将处理器添加到日志记录器
logger.addHandler(console_handler)
logger.addHandler(file_handler)
# output_data = []

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'aliexpress_data',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


# 爬虫结果文件路径
# CRAWLER_RESULT_FILE = 'crawler_results.json'
# 异步执行爬虫（使用 asyncio 兼容的 Deferred）
async def crawl_and_save(keyword):
    settings = get_project_settings()
    settings.update({
        'FEED_FORMAT': 'json',
        'FEED_URI': 'product_infos.json',
    })
    deferred = runner.crawl('ProductsInfoSpider', keyword=keyword)
    return await deferred  # 直接等待 Deferred（无需 from_deferred）


class MySpiderDataCollector:
    def __init__(self):
        self.data = []

    def collect_item(self, item):
        self.data.append(dict(item))


@app.route('/start_crawl', methods=['GET'])
def start_crawl():
    global crawl_data
    crawl_data = []
    collector = MySpiderDataCollector()

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl(SumaitongCrawlerSpider, callback=collector.collect_item)
    process.start()

    crawl_data = collector.data
    print(crawl_data)
    return json.dumps(crawl_data, ensure_ascii=False)


# 获取数据的 API
@app.route('/api/get_ranking_data', methods=['GET'])
def get_ranking_data():
    # 从请求参数中获取查询条件
    date_str = request.args.get('date')  # 可选，格式：YYYY-MM-DD
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    keyword = request.args.get('keyword', type=str)
    if not keyword:
        return jsonify({
            'status': 'error',
            'message': '请输入关键词',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    # 连接数据库
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 构建SQL查询
            sql = "SELECT * FROM products WHERE 1=1"
            params = []
            # 如果指定了日期
            if date_str:
                try:
                    # 将日期字符串转换为datetime对象
                    target_date = datetime.strptime(date_str, "%Y-%m-%d")
                    next_date = target_date + timedelta(days=1)
                    sql += " AND created_at >= %s AND created_at < %s"
                    params.extend([target_date, next_date])
                except ValueError:
                    return jsonify({
                        "status": "error",
                        "message": "日期格式错误，请使用 YYYY-MM-DD 格式"
                    }), 400

            # 添加分页
            sql += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            # 执行查询
            cursor.execute(sql, params)
            result = cursor.fetchall()

            # 获取总记录数（用于分页）
            count_sql = "SELECT COUNT(*) as total FROM products"
            if date_str:
                count_sql += " WHERE created_at >= %s AND created_at < %s"
            cursor.execute(count_sql, params[:-2] if date_str else [])
            total = cursor.fetchone()['total']
            return jsonify({
                "status": "success",
                "date": date_str or datetime.now().strftime("%Y-%m-%d"),
                "total": total,
                "data": result
            })
    finally:
        connection.close()


# 获取日期范围数据的 API
@app.route('/api/data/range', methods=['GET'])
def get_data_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    if not start_date or not end_date:
        return jsonify({
            "status": "error",
            "message": "请提供开始日期和结束日期"
        }), 400

    try:
        # 将日期字符串转换为datetime对象
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "日期格式错误，请使用 YYYY-MM-DD 格式"
        }), 400

    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 查询日期范围内的数据
            sql = """
                SELECT * FROM products 
                WHERE created_at >= %s AND created_at < %s
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (start, end, limit, offset))
            result = cursor.fetchall()

            # 获取总记录数
            count_sql = "SELECT COUNT(*) as total FROM products WHERE created_at >= %s AND created_at < %s"
            cursor.execute(count_sql, (start, end))
            total = cursor.fetchone()['total']

            return jsonify({
                "status": "success",
                "date_range": {
                    "start": start_date,
                    "end": end_date
                },
                "total": total,
                "data": result
            })
    finally:
        connection.close()


# 根路由，用于测试
@app.route('/', methods=['GET', 'POST'])
def index():
    return "<pre>" + pyfiglet.figlet_format("WELCOME TO SHUMATT", font="block") + "</pre>"


# 获取商店数据
@app.route('/api/get_shop_data', methods=['GET'])
def get_shop_data():
    # 从请求参数中获取查询条件
    seller_id = request.args.get('seller_id')
    # 如果没有指定 limit 和 offset，则返回所有数据
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', default=0, type=int)
    date_str = request.args.get('date')

    if not seller_id:
        return jsonify({
            "status": "error",
            "message": "请提供商店 ID"
        }), 400

    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM shop_listing where seller_id = %s"
            params = [seller_id]
            if date_str:
                try:
                    # 将日期字符串转换为datetime对象
                    target_date = datetime.strptime(date_str, "%Y-%m-%d")
                    next_date = target_date + timedelta(days=1)
                    sql += " AND created_at >= %s AND created_at < %s"
                    params.extend([target_date, next_date])
                except ValueError:
                    return jsonify({
                        "status": "error",
                        "message": "日期格式错误，请使用 YYYY-MM-DD 格式"
                    }), 400

            # 只有在提供了 limit 和 offset 时才添加分页
            if limit and offset:
                sql += ' ORDER BY created_at DESC LIMIT %s OFFSET %s'
                params.extend([limit, offset])
            else:
                sql += ' ORDER BY created_at DESC'

            cursor.execute(sql, params)
            result = cursor.fetchall()

            # 获取总记录数
            count_sql = "SELECT COUNT(*) as total FROM shop_listing where seller_id = %s"
            if date_str:
                count_sql += " AND created_at >= %s AND created_at < %s"
            cursor.execute(count_sql, params[:-2] if date_str else [seller_id])
            total = cursor.fetchone()['total']

            return jsonify({
                "status": "success",
                "seller_id": seller_id,
                "data": result,
                "count": limit if limit else total,
                "limit": limit,
                "offset": offset
            })
    finally:
        connection.close()


# # 爬取指定商品前60页数据
# @app.route('/api/get_products_ranking', methods=['GET'])
# async def get_products_ranking():
#     keyword = request.args.get('keyword', 'injector')
#
#     try:
#         # 启动爬虫并等待完成
#         await crawl_and_save(keyword)
#
#         # 读取结果文件
#         with open('product_infos.json', 'r', encoding='utf-8') as f:
#             data = json.load(f)
#         return jsonify({
#             "status": "success",
#             "data": data,
#         })
#     except FileNotFoundError:
#         return jsonify({
#             "status": "error",
#             "message": "文件未找到"
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": f"爬取失败：{str(e)}"
#         })
#
#
# # 爬取指定店铺所有商品(自动化爬虫)
@app.route('/api/scrape_shop_listing', methods=['POST'])
def scrape_shop_listing():
    seller_id = request.form.get('seller_id')
    settings = get_project_settings()
    subprocess.Popen(f'scrapy crawl ShopInfoSpider -a seller_id={seller_id} -o output.json')
    return jsonify({
        "status": "success",
        'message': f'{seller_id} 爬虫程序启动成功'
    })
    # process = CrawlerProcess(
    #     # settings={
    #     #     'FEED_FORMAT': 'json',
    #     #     'FEED_URI': 'shop_infos.json'
    #     # }
    #     settings
    # )
    #
    # process.crawl(ShopInfoSpider, seller_id=seller_id)
    # process.start()
    # with open('shop_infos.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    #     return jsonify({
    #         "status": "success",
    #         "data": data
    #     })


@app.route('/api/hello_world')
def hello_world():
    spider_name = 'ShopInfoSpider'
    seller_id = request.args.get('seller_id')
    # subprocess.check_output(['scrapy', 'crawl', spider_name, '-a', f'seller_id={seller_id}', '-o', "hello_world.json"])
    subprocess.check_output(f'scrapy crawl {spider_name} -a seller_id={seller_id} -o shop_infos.json'.split())
    with open('hello_world.json', 'r', encoding='utf-8') as f:
        data = f.read()
    return jsonify({
        "status": "success",
        "data": data
    })


@app.route('/api/test', methods=['GET'])
def test():
    # logger.debug('11111')
    return 'This is the message'


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
