import requests
from bs4 import BeautifulSoup

# 目标URL
url = "https://www.zdaye.com/free/?ip=&adr=&checktime=&sleep=&cunhuo=&dengji=&nadr=&https=1&yys=&post=&px="
with open('./valid_ip.txt', 'r') as f:
    ips = f.readlines()
print(ips)
proxies = {'http': item.strip() for item in ips}

# 发送HTTP请求
response = requests.get(url, proxies=proxies)

# 检查请求是否成功
if response.status_code == 200:
    valid_result = []
    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找包含IP地址和接口信息的表格行
    rows = soup.find_all('tr')

    # 遍历每一行，提取IP地址和接口信息
    with open('./ip_free.txt', 'a') as f:
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 1:  # 确保行中有足够的单元格
                ip_address = cells[0].text.strip()
                port = cells[1].text.strip()
                print(f"IP地址: {ip_address}, 端口: {port}")
                valid_result.append(ip_address + ':' + port)


else:
    print(f"请求失败，状态码: {response.status_code}")
