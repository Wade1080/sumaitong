import requests
from ip_pool import IPPool

def test_proxy(proxy):
    """
    测试代理IP是否有效
    :param proxy: 代理IP，格式为'ip:port'
    :return: 是否有效 (True/False), 响应时间 (秒), 返回的IP地址
    """
    url = "http://httpbin.org/ip"  # 用于测试的URL
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=5)  # 设置超时时间为5秒
        if response.status_code == 200:
            response_ip = response.json().get("origin")  # 获取返回的IP地址
            return True, response.elapsed.total_seconds(), response_ip
        else:
            return False, None, None
    except Exception as e:
        print(f"代理 {proxy} 测试失败: {e}")
        return False, None, None

def process_ip_pool():
    with open("./ip_free.txt", "r", encoding="utf-8") as f:
        ips = f.readlines()
        ips = [ip.strip() for ip in ips]
        valid_ips = []
        invalid_ips = []
        for proxy in ips:
            # proxy = "202.101.213.150:23984"  # 替换为你要测试的代理IP
            is_valid, response_time, response_ip = test_proxy(proxy)
            if is_valid:
                valid_ips.append(proxy)
                # with open('./valid_ip.txt', 'w+', encoding="utf-8") as f:
                #     f.write(proxy)
                print(f"代理 {proxy} 有效，响应时间: {response_time:.2f}秒，返回的IP: {response_ip}")
            else:
                invalid_ips.append(proxy)
                print(f"代理 {proxy} 无效")
        '''
        for proxy in invalid_ips:
            is_valid, response_time, response_ip = test_proxy(proxy)
            if is_valid:
                valid_ips.append(proxy)
                # with open('./valid_ip.txt', 'w+', encoding="utf-8") as f:
                #     f.write(proxy)
                print(f"代理 {proxy} 有效，响应时间: {response_time:.2f}秒，返回的IP: {response_ip}")
            else:
                print(f'代理{proxy}二次重试未通过...')
        '''
        with open("./valid_ip.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(set(valid_ips)))

# 去重
def elimate_duplicate():
    with open("./ip_free.txt", "r", encoding="utf-8") as f:
        ips = f.read().split("\n")
        ips = list(set(ips))
    with open("./ip_free.txt", "w", encoding="utf-8") as f:
        for ip in ips:
            f.write(ip+'\n')
        print('finished eliminating duplicate ips')




if __name__ == "__main__":
    # 获取公开IP列表——站大爷
    ip_pool = IPPool()
    ip_pool.get_zdaye_ip()
    # 加载IP代理池
    process_ip_pool()
    # 去重
    elimate_duplicate()
    print('处理完毕')


