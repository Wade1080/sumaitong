# Scrapy settings for sumaitong project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'sumaitong'

SPIDER_MODULES = ['sumaitong.spiders']
NEWSPIDER_MODULE = 'sumaitong.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "sumaitong (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 13

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
RETRY_TIMES = 2
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    'referer': 'https://www.aliexpress.us/',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    # 正常登录
    "cookie": 'aep_common_f=PsPck/FUrf7budK5K5/G6qnODbD1Ty17Ar/kTTx7V7kgNfXfL+Y9zw==; _ga_save=yes; lwrid=AgGWPiJ6iULJAsc5dGogX39uI4bN; xlly_s=1; cna=xnOGIBOcsGECAbeyVephA8IK; join_status=; _gid=GA1.2.159792830.1744799172; _gcl_au=1.1.467193814.1744799172; _fbp=fb.1.1744799172892.669475780484070787; _pin_unauth=dWlkPVpqZzJNamd5T1RZdFpHWTJZUzAwTWpCbUxXSTJOVGt0TkRGa1lqQXpNREJsWkdGaA; AB_DATA_TRACK=112185_8922; AB_ALG=global_union_ab_exp_4%3D0; AB_STG=st_SE_1736852788277%23stg_4159; intl_locale=en_US; lwrtk=AAIEaADEIMjuU7L6lxM3PjGOeml08PKUG/YWtxJLJVZvwK5t87M9QtA=; _m_h5_tk=e3d81e1e778b0874cfdeae980be1f776_1744857787147; _m_h5_tk_enc=0977a995bacb14f25a390f17f83b6af2; acs_usuc_t=x_csrf=1aq9vvlf3zxs3&acs_rt=f0181b4613874f34bfe3075194f99af6; _gat=1; _history_login_user_info={"userName":"zcw1080","avatar":"","accountNumber":"Wade1080@163.com","phonePrefix":"","hasPwd":false,"expiresTime":1747447409405}; x_router_us_f=x_alimid=6340368875; xman_us_t=x_lid=us1893585475dqoae&sign=y&rmb_pp=wade1080@163.com&x_user=c5I24mX5V3PQRAuSnliQrEPfszMTP9ItjlwlLBFOJ5E=&ctoken=10da9vyf78ju&l_source=aliexpress; sgcookie=E1002LqzrAIMqGEptNBToEDFRx0gEM05xec1QYpcQHWhRosQfb0VKQtmGFtJjVg0ZqFRXGywhmFpQ7FeLqnwDS5FjEKjG1AMP6AznOfUVDLe/rE=; xman_t=KO57PtCV2ysNmk4u9sFiyahR5wRDuiWER24bYeYcE/II5eBKJkQo6kdnq7f7TTRS0y8EmJ1ass134XyjxWE6tHqMXpHeH5U1IBBN3YLgQbOeN3zdBZ5Rk8lj0bhF/i+cgC/hxcK42Gq3+drB3B4+9D0ot+jpaPBCNQEFccXPKN8bg1/3U4ogd1F4tehQYklowJ/ADXl5M63+dLjrtJ1R4J9EbT4na/BZ1+/Kbo88h3Td1qUT9Qy0wRZg7wvK+JgXvWhuRkyTyJgOzfWyULMreR+h2hu9ds0f48cetuNbWHowR2jK3p+aUFmkgRdKpVv7csl3D+Rnh54Y9Y2KmvTV53igJI3eXEX48u/z4X2tU/jCnRq8tNEcQwY3OmnrB9igwREXLAGE8A/G/pY7irDuzabuSvhLLamlul52Lyq+qVuTCBDw8oVRO0lREUrLt1nf0FubiaQQ2M3fyLYSW+7rJ3KIpic8vy9K053ztFqt0PFqItsOpH4HBWEuZ2wSg1JncG7meD3K2gb3yJid9CBGah5pOGQln/RuxPP89Q3SIvts3Zg4Gc59/2oEPPvQom+2XDCEzkcjSBr0tdqrfEq/DnAGP0P3wA91aYmf31ivDhKWn0/dE+NzUMlBzHGkMWs1L3804w/KdL3fJrJtjHwXyhS7cABEvzCZOW57p0n4d2HufwyWVxkmQ7oNZFXmpV5/4YldI5iZTaLJw37INuJl0NQACovPzNw/oq0Tqx0QGZCA6p1LPlsXeg==; xman_f=l18CzvBK/xGJfGf6tE2bqbBc9EH3GFhpBVCHWxnCbmf5q+w4HjBVrKU2N4ix/Bb1rDcmtQH+wR1Ly411pwEaqIZRQTzNVRVmr6nSqRIOrPi/rXKKrWO1Sv+e0+fx2NW0C3plGQL2ojU0dcOgzw970yFmp82acTanPOX8tAC2MzN9t0WNwECCAeJwofC3zgbZIE1ksi1T13FAsC1wD2DY63zy4dwiNl7l1qSIxD0KwtVrStiilP01FMLYHyIFbysfdifSa5q1p/hMI1iJvErp/qqoqmerLtnu7NAy+I+bw4ANtvb1fs9BqW0GO206hOJmB9G80AIQaIBSHW3dPQG40fNhOLiepUWXKUUgksIJju41NybOpkiaN85WFgaLb3JaGabLJ6jfVXc=; xman_us_f=zero_order=y&x_locale=en_US&x_l=1&x_user=US|wade1080|user|ifm|6340368875&x_lid=us1893585475dqoae&x_c_chg=1&acs_rt=b28020b8466c4be69a3e0e187648a8c4; aep_usuc_f=site=usa&c_tp=USD&x_alimid=6340368875&isb=y&region=CN&b_locale=en_US&ae_u_p_s=2; _ga_VED1YSGNC7=GS1.1.1744855354.7.1.1744855412.2.0.0; _ga=GA1.1.766801087.1744799121; epssw=9*mmC2BmhOTH4DWcV7utX2zR33jGA70tV73tjmpd0qmmCi8uZGut_mmAvOdS6O8STyAXbBDOx95RHmYdQZlkT19Le3IyZ7KXBJukJRVAcunkKnMMXo-2WIJDmxREIlT5bB8t77etymm1mRmmmmI9JWfraYNtuuuOtuvDUFKV3CIZfM-6QyaYPles_ZFmNI-oHOQfdBpE7X6duuC5lLimmm3w5BdYCXd2CXdcRCKH58gtG6DLKAP0FkYkokFNIHmBImdkmdeEvIWcZ2Ou2dNwxcalgps-2AT7clMfSLEG5b9R03ZOYr; isg=BGRk2Z-o0NebZCvoq8ldw8wfNWJW_Yhn0qGSw36F8S_yKQTzpgkD9gGL7YEx8cC_; tfstk=gztrfvqPc0nzpj-rttjU7YVBnOSR4gc_qH1CKpvhF_fuVuNHuBODFUZCAwqeKpQ3P_sutIJMZ_sIe_sELC12FwTIe6WHip_HO69SL8K2_kZSw4p3YMsn1fisfLHRvMc6uId8r_Bpn6DfrCHHkeSn1fiXyU6KTMAI14B73KfALuf3rBmDnT1cEyXktsbcIONlxMAn3mXRQk4htkfm39CctMjHtKcSQLv30O_odT8eguuVha5MEsrwHnWlrzplgkre0E7Psk14xkxVUKa83fZZR1YONN1MimZPYKXegNTr_uReKdLhuHPoFCAD8BXvkXzF_evWWnQbKzv2Y_7MqZygAdjRKBbekfr1UgTV738-pSvk1_8G2pwZNK7wuNBcoJzlVF96vNxo45CfW9RV5Ula4CjztWBcH1-pzW4FrtBV1xk2ee36WhDHgl4LJZjO31M5FyUdrtBV1xk4JyQcMt5sFT1..; cto_bundle=OPX2XV8wclFRcmtaU1ZrZEtLWmVldnkzS2NDTWt1U3dUc3o3MVZybHdtNWVKbWpIQjROTk1jJTJCb1VFUDNoSW4lMkZUeFBuS3QwV3hqYXhVMDRVZWpoR3V4SmRYZkZFZFNDdHJGOXRKQ3N2OGpXY09rSVdzQTg2N0ZQSm5TOVNsaFlTeE50YVlZbVNjSzc0c052RDVEelNWdUV2ajFpbGR1TlNqMjZpejI4b2cwZ3JqUjJFJTNE; _uetsid=386100f01aad11f0ab566d87c63d5ae6; _uetvid=386135a01aad11f08fe9abdc93b5cd01; intl_common_forever=vnJZLct0idkgSbGVdZMNC5d5YWgBIBIWsmlvLmSFs5e4E+IySLDT0w=='
    # 未登录
    # "cookie": 'x5sec=7b22617365727665722d696e746c3b33223a22307c4349712b334c3847454c6e6139504c342f2f2f2f2f7745772f6f2f7146413d3d222c22733b32223a2238646562336232613732386230316165227d; aep_common_f=Y48THeQrhtf13cYeuXjZIqwCkU8zDvAgDgQQyvIno2eYDXwkxmhEdA==; _ga_save=yes; intl_locale=en_US; lwrid=AgGWHVH6q3n1frvNC9eNX39uI4bN; join_status=; xlly_s=1; lwrtk=AAIEZ/ePurZmcsSDOLqvlztAi0DNKtO/d5ink7JazDRUGyT3AQmsOO4=; cna=+1x6IL1R0BUCAbeyVerUp2ai; _m_h5_tk=e638e2fe77c162dccc054a4838accfe9_1744250798404; _m_h5_tk_enc=491a7fdbcfaf6aa3bd998c6afe115dcc; _gid=GA1.2.1822060007.1744248637; _gcl_au=1.1.716709881.1744248637; _fbp=fb.1.1744248637258.125644684523997597; _pin_unauth=dWlkPU9ERTBaVGd4TXpVdE1UWXhNaTAwT0RsbUxUZzNNV1l0WkRka05HWmlZMlUxTURrMQ; AB_DATA_TRACK=112185_8922; AB_ALG=global_union_ab_exp_4%3D0; AB_STG=st_SE_1736852788277%23stg_4159; XSRF-TOKEN=f975587f-d683-410a-b153-0cb118a29829; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%091005007476725583%091005008606750209; acs_usuc_t=x_csrf=19b1899ux2a_b&acs_rt=a170ce95fe1e4702aabafaee5f446fac; JSESSIONID=E00F8A513C120C6C71EC5DCFE1B43C3C; _history_login_user_info={"userName":"Wade2513473008","avatar":"","accountNumber":"Wade1080@163.com","phonePrefix":"","hasPwd":false,"expiresTime":1746841601634}; x_router_us_f=x_alimid=6340368875; xman_us_t=x_lid=us1893585475dqoae&sign=y&rmb_pp=wade1080@163.com&x_user=p2IeXmW2XDoZYCzaKHI3PAxTdYnMP5HdlqXZ5+V8Mb4=&ctoken=3iiozlgmh7z_&l_source=aliexpress; sgcookie=E100TwjZciyTu/weafJ6PyoqgSyw+lJWkAb14EGrCWfJ5k3tZZGTl+O/B8sHvq75lWoZBE7i/fpH+6dQ5Fuy3cSqQ9m9KGmKCpdKUHSF+2YSlzA=; xman_t=qh3xg/E2oKqLqFTEr1R1Kox7EZN0N9knwNbeFyp/Nt/cQc88eIqp+04LS0hLR4llv1LhiQmd9D2z1NJW0Z4lBGtMTNXnwYrV24eWJSQRve4Q3LCztp5/qdjIjPZD8mMk6F5tZeQn32WMvpY/mIvttRo29EgfV9gWdERKChDZLGVnwHVDSb/4ifXIvzjlWrJ3eUiuGnhyyYBzkC/x6/pZ0zhOlPCVRCSWlNJB7/oYHpUvmtBP61UIJ40hcaGzYPMPzWwqeuLFOY0tJgGWMy77Vs2oufiW4FyUCJHQw0TZWhzWEHnKLUwn1DAZ/vr8W16p10ENUIGQOSCtDXs998IsQGythq7X2Cmwl1vMsmvyBdEbiqz1xVJ8q9NcXsRQePvoR9tgZgqFdFzmRQy4Fh3WfZp7n2WEM/RHkcMPOofU0Sfux11Z39m1AtiokVaxi7mri+VKXZvRWiKTPS7lkQ3FuhNfLloZENdSjG9P1EUKfdniWTyo5yrg3lGgUn9dN4X0qvHoDlKMLTZuAyj5ldsYn1wOIoKIgr69cYTthHnibea1K51BH+kKelpOXEDWyiZvF1deE27ioJreqjZ9zasYmL9CT7aWeqF9P5W3zJUFX0ATH1tUXru4VE8FasARYrgdCxzxoEYujcYXw7FjgVDN0+vWrb60PSrn5uHgMvq0OwmiZhRFCBCtidG7uTlcQIemOp8vEZx5wY0ksu6frJzb2eoeT1Mg2AgLvlNNdgla5Qo0kz3MYrQR1w==; xman_f=LKXPAGfbEUs6nwTDmApCZIBEIHQns2rAkbvRVNRmziI4Bdh2OxcFFLeoQ3GMipYS/4ZlQ9IwgGokyGuAu/AcMvzL0QK7CIEyW04TZ4rafBJuL+VIlm5+1X/NEzHa+V3/WB4vjG/+mP6yuyNuaSks3JrT5mP0lgozHxCp2jtcFFA56FlD7cI8X6SgMZzmin8RZGAxUHdJAS259BEL8x5bza7bzNoVxsbxdhdelJYwE03hrGNabEjudm0EiVFrZXcfzLKR45zmYTIZfb8IjEILuBzrkpb0GRg77znwUAbHUGrYXTL2ZvBlSye04BDcdiq8dBjOeclQ8Bu2pEIVuHNLNcMnqJX6eThFzqGuNClFBzbkyiaIMRrFtv3qmNkNFNiWx8P7Qr3Fgz8=; xman_us_f=zero_order=y&x_locale=en_US&x_l=1&x_user=US|wade1080|user|ifm|6340368875&x_lid=us1893585475dqoae&x_c_chg=1&acs_rt=16c4e765a170479d954afd5f7fb70c2f; aep_usuc_f=site=usa&c_tp=USD&x_alimid=6340368875&isb=y&region=CN&b_locale=en_US&ae_u_p_s=2; _ga=GA1.1.1926294751.1744183970; _uetsid=67c86e9015ab11f0a50f5585f09d7ade; _uetvid=67c87ed015ab11f0ac10071f5ece544e; cto_bundle=VUYRGF80T2RiQk9YMkc1cWNVUm9OODZpZ1JLVTVxb0tCdkV4Qmg5VFQ3d3FoSldsZ0ExR05MSWdDRXQzNHU0RktRaUU4dktNaHdzWlpNSjlZTEYlMkIzRkwwdldPTjBMeEM4UzFnTWhKQ0o2UWxNbk9YMG53ZHROU3RoVzJ1OXViJTJGVWt6NHN1JTJCb08lMkJwaktPVkdncjl0JTJCOVVQZ1htSWpnNmpKVEpBVU5mQmpyMTM3VU9jJTNE; isg=BE9PmfCedLEOXHDJ1DAmMttm3uNZdKOWpUgp4mFc5L7FMG8yaUJb5P1jMmCOSHsO; _ga_VED1YSGNC7=GS1.1.1744246771.13.1.1744249764.29.0.0; epssw=9*mmCOcmIKLORUWcvR3ts2zR33z3uO7tV7ut-OB0-63tZ3s-aOutG4dImmmoZO8trpfuv5zNinABmO0DmhsV97mem3dqhCu8KJuyFr9LLunkKnslg42GIkOxclJuIBcbWB8t77J39R5Aw5rN93BLjG9Lmmm5ViL8y4uVuuuu3d3r5xtl7u3Bn9pgnO6HbbeS5D-cfYagrmX2XEC9CA40tceT1xHdHXdluv3tv3uALRmmLRHbR14mQmswnOYzOm4_N9wmmjmtXtTwNfSp6D5Ffhw9GhrwcaoLexnf3PBPteSs_RHWsuYT7Bh8HDBm..; tfstk=g7XKGOfV2P4neM90KJNiZ9bWJBqGJTIUtwSjEUYnNNQOciuHNW7ueYIFV3fH-eftFgTNyQrerUTRrg13j-2cYMJyFLU0n-c1Lo8OpUgkFpJ1nJfvh-2cYMwj3ZG7n9mBWr8pPLOBRCG673nBAH_W1htk5vtSd3g_X386F4MIOFg62HgWFL_5flKy5UG7uzLsAUDRg_1HV9hXIYM5BHd_sMTsQ369vIYfA9HSFStp9EsBWr55ZhA14QBr4YdRAs7ycwgQyUWOf91flPcHRsKRm_IQdA9hLM1XNtarNMvHJd6CM0M5XpL9ZTdZJPLfLG62CC2bDG6N-MWOq0wWjZY1Y998hoJpde99bT4ZdUC1N9AeU2aJzOI1d_IP9tXxMjgDk3cQXlhraBtakrxPTU7g2dx9oke-abRabhL0XlhraBtwXEqLJbly_l5..; intl_common_forever=MCCGXtuVVdHfzTKZAjDBXriw+EGnziXSttR7TVajPe27LIKlTXrndw=='
}
with open(r'E:\Code\sumaitong\ip_test\valid_ip.txt', 'r') as f:
    valid_ip = f.read().splitlines()
    # print(valid_ip)
    # print(f.read())
# 代理配置
# PROXY_IP = [
#     'http://106.14.251.34:7897',  # 本地代理测试
#     'http://1.202.174.38:80',  # 本地代理测试
#     'http://119.84.46.226:5566',  # 本地代理测试
#     'http://119.84.46.227:5566',  # 本地代理测试
#     'http://139.159.102.236:3128',  # 本地代理测试
#     'http://120.25.1.15:7890'  # √
# ]
PROXY_IP = ['http://' + item for item in valid_ip]
# print(PROXY_IP)

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "sumaitong.middlewares.SumaitongSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 禁用默认的UserAgentMiddleware
    'sumaitong.middlewares.RandomUserAgentMiddleware': 400,  # 用户代理中间件
    'sumaitong.middlewares.ProxyMiddleware': 500,  # 代理中间件
    'sumaitong.middlewares.SliderMiddleware': 600,  # 滑块验证码中间件
    # 'sumaitong.middlewares.SliderMiddleware2': 600,  # 滑块验证码中间件2    ——测试
    # 'sumaitong.middlewares.ProxyDownloaderMiddleware': 100,  # 代理中间件 （快代理、站大爷）
    # 'sumaitong.middlewares.FakeUserAgentMiddleware': 200,  # 用户代理
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'sumaitong.pipelines.ProductListPipeline': 300,
    'sumaitong.pipelines.ShopDetailPipeline': 400,
    'sumaitong.pipelines.ProductDetailPipeline': 500,
    'sumaitong.pipelines.SumaitongPipeline': 600,
}

MYSQL_DB_NAME = 'aliexpress_data'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '1234'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# SSL 证书验证配置
DOWNLOADER_CLIENTCONTEXTFACTORY = 'scrapy.core.downloader.contextfactory.ScrapyClientContextFactory'
DOWNLOADER_CLIENT_TLS_METHOD = 'TLSv1.2'
DOWNLOADER_CLIENT_TLS_VERIFY = False  # 禁用 SSL 证书验证

# 爬虫稳定性提升拓展
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 8


DOWNLOAD_TIMEOUT = 10

# 断点续爬
# JOBDIR = 'jobdir'
# DOWNLOAD_TIMEOUT = 540
# DOWNLOAD_DELAY = 1
# DEPTH_LIMIT = 10
# EXTENSIONS = {
#     'scrapy.extensions.telnet.TelnetConsole': None,
#     'scrapy.extensions.closespider.CloseSpider': 1
# }

# print(f'current_dir=====> {os.getcwd()}')

# 配置日志级别
# LOG_ENABLED = True
# LOG_LEVEL = 'INFO'  # DEBUG/INFO/WARNING/ERROR
LOG_LEVEL = "WARNING"
# # LOG_FILE = './logs/scrapy.log'  # 输出到文件
# LOG_STDOUT = True  # 同时打印到控制台
# LOG_FILE_APPEND = './logs'

# # 确保日志目录存在
# import os
# if not os.path.exists('logs'):
#     os.makedirs('logs')

# FEED_FORMAT = 'json',
# FEED_URI = 'shop_infos.json'
