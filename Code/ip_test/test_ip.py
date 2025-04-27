import requests

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

if __name__ == "__main__":
    with open("./ip_free.txt", "r", encoding="utf-8") as f:
        ips = f.readlines()
        ips = [ip.strip() for ip in ips]
        valid_ips = []
        for proxy in ips:
            # proxy = "202.101.213.150:23984"  # 替换为你要测试的代理IP
            is_valid, response_time, response_ip = test_proxy(proxy)
            if is_valid:
                valid_ips.append(proxy)
                # with open('./valid_ip.txt', 'w+', encoding="utf-8") as f:
                #     f.write(proxy)
                print(f"代理 {proxy} 有效，响应时间: {response_time:.2f}秒，返回的IP: {response_ip}")
            else:
                print(f"代理 {proxy} 无效")
        with open("./valid_ip.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(valid_ips))