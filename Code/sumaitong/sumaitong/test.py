# import requests
#
# params = {
#     'keyword': "injector"
# }
# res = requests.get('http://127.0.0.1:5000/api/hello_world', params=params)
# print(res.json())
import asyncio
import aiohttp

"""async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = [
        'http://127.0.0.1:5000/api/hello_world?keyword=injector',
    ]
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

# 运行主函数
asyncio.run(main())"""


if __name__ == '__main__':
    # 传入多个关键词处理方式
    keywords = ['injector', 'fuel']
    base_url = 'https://www.aliexpress.us/w/wholesale'
    for keyword in keywords:
        base_url += f'-{keyword}'
    base_url += '.html?spm=a2g0o.productlist.search.0'
    print(base_url)
