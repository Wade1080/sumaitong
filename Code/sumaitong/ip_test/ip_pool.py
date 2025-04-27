import requests
from lxml import etree

# 自动获取 站大爷公开免费 IP
class IPPool():
    def __init__(self):
        self.ip_list = {}
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        }

    def get_zdaye_ip(self):
        res = requests.get(
            'https://www.zdaye.com/free/?ip=&adr=&checktime=&sleep=&cunhuo=&dengji=&nadr=&https=1&yys=&post=&px=',
            headers=self.headers)

        print(res.text)
        tree = etree.HTML(res.text)
        trs = tree.xpath('//table[@id="ipc"]/tbody/tr')
        ips = {}
        for tr in trs:
            ip = tr.xpath('./td[1]/text()')[0]
            port = tr.xpath('./td[2]/text()')[0]
            ips[str(ip)] = str(port)

        with open('./ip_free.txt', 'r') as f:
            content = f.read()
        with open('./ip_free.txt', 'a') as f:
            f.write('\n')
            for ip, port in ips.items():
                if ip + ':' + port not in content:
                    f.write(ip + ':' + port + '\n')

        print(f'全部ip: {ips}')


if __name__ == '__main__':
    ip_pool = IPPool()
    ip_pool.get_zdaye_ip()
