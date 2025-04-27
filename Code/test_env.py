import time

import requests
import json
from datetime import datetime, timedelta


def test_get_data():
    """测试获取数据的基本功能"""
    print("\n=== 测试获取数据 ===")

    # 测试1：获取默认数据（当天）
    params = {
        'limit': 10,
        'offset': 0
    }
    response = requests.get('http://127.0.0.1:5000/api/data', params=params)
    print(f"测试1 - 获取当天数据:")
    print(f"状态码: {response.status_code}")
    print(f"数据条数: {len(response.json()['data'])}")
    print(f"总记录数: {response.json()['total']}")

    # 测试2：获取指定日期的数据
    test_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    params = {
        'date': test_date,
        'limit': 5,
        'offset': 0
    }
    response = requests.get('http://127.0.0.1:5000/api/data', params=params)
    print(f"\n测试2 - 获取指定日期({test_date})数据:")
    print(f"状态码: {response.status_code}")
    print(f"数据条数: {len(response.json()['data'])}")

    # 测试3：测试分页
    params = {
        'limit': 3,
        'offset': 5
    }
    response = requests.get('http://127.0.0.1:5000/api/data', params=params)
    print(f"\n测试3 - 测试分页:")
    print(f"状态码: {response.status_code}")
    print(f"数据条数: {len(response.json()['data'])}")
    print(f"当前页数据: {json.dumps(response.json()['data'], ensure_ascii=False, indent=2)}")


def test_get_data_range():
    """测试获取日期范围数据"""
    print("\n=== 测试获取日期范围数据 ===")

    # 测试1：获取最近3天的数据
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

    params = {
        'start_date': start_date,
        'end_date': end_date,
        'limit': 10,
        'offset': 0
    }
    response = requests.get('http://127.0.0.1:5000/api/data/range', params=params)
    print(f"测试1 - 获取{start_date}到{end_date}的数据:")
    print(f"状态码: {response.status_code}")
    print(f"数据条数: {len(response.json()['data'])}")
    print(f"总记录数: {response.json()['total']}")

    # 测试2：测试错误情况 - 缺少日期参数
    params = {
        'start_date': start_date,
        'limit': 10
    }
    response = requests.get('http://127.0.0.1:5000/api/data/range', params=params)
    print(f"\n测试2 - 测试缺少日期参数:")
    print(f"状态码: {response.status_code}")
    print(f"错误信息: {response.json()['message']}")

    # 测试3：测试错误情况 - 日期格式错误
    params = {
        'start_date': '2024-03-01',
        'end_date': '2024/03/10',
        'limit': 10
    }
    response = requests.get('http://127.0.0.1:5000/api/data/range', params=params)
    print(f"\n测试3 - 测试日期格式错误:")
    print(f"状态码: {response.status_code}")
    print(f"错误信息: {response.json()['message']}")


def test_large_data():
    """测试大数据量查询"""
    print("\n=== 测试大数据量查询 ===")

    params = {
        'limit': 3600,
        'offset': 0
    }
    response = requests.get('http://127.0.0.1:5000/api/data', params=params)
    print(f"测试获取300条数据:")
    print(f"状态码: {response.status_code}")
    print(f"实际获取数据条数: {len(response.json()['data'])}")
    print(f"总记录数: {response.json()['total']}")


def test_get_shop_data():
    params = {
        'seller_id': '2668273644',
        'limit': 10,
        'offset': 0
    }
    response = requests.get('http://127.0.0.1:5000/api/shop_data', params=params)
    print(response.json())


def test_run_crawler():
    params = {
        'keyword': 'injector',
        'page': 1
    }
    response = requests.get('http://127.0.0.1:5000/api/crawler', params=params)
    print(response.json())


def test_crawl_listing():
    data = {
        'seller_id': '2668273644',
    }
    res = requests.post('http://127.0.0.1:5000/api/get_shop_listing', data=data)


def test_get_shop_listing():
    data = {
        'seller_id': '6000376855'
    }
    res = requests.post('http://127.0.0.1:5000/api/get_shop_listing', data=data)
    print(res.text)


def test_hello_world():
    params = {
        'seller_id': '6000624154'
    }
    res = requests.get('http://127.0.0.1:5000/api/hello_world', params=params)
    # print(res.json())


def test_read_html():
    with open(r'E:\Code\sumaitong\error.html') as f:
        content = f.read()
        print(content)
        return content


def retry_decorator(max_retries=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    print(f'调用{func.__name__}失败,错误信息{e},重试第{retries}次')
            print(f'达到最大重试次数,{func.__name__}调用失败')

        return wrapper

    return decorator

# 测算函数运行时间
def spend_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'{func.__name__} spend time:', end_time - start_time)
        return result
    return wrapper


@spend_time
@retry_decorator(max_retries=3)
def devision(a, b):
    time.sleep(2)
    return a / b






if __name__ == '__main__':
    # 运行所有测试
    # test_get_data()
    # test_get_data_range()
    # test_large_data()
    # test_get_shop_data()
    # content = test_read_html()
    # test_hello_world()
    devision(2, 0)
    # test_run_crawler()
