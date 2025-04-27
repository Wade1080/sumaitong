# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals, Request
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from selenium.common import NoSuchElementException, TimeoutException

from sumaitong import settings
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent

import email, sys
from imapclient import IMAPClient
from bs4 import BeautifulSoup
import re


class SumaitongSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn't have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SumaitongDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ProxyMiddleware:
    def __init__(self, ip):
        self.ip = ip
        self.failed_proxies = set()  # 记录失败的代理

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(ip=crawler.settings.get('PROXY_IP'))

    def process_request(self, request, spider):
        # 如果所有代理都失败了，就不使用代理
        if len(self.failed_proxies) >= len(self.ip):
            return None

        # 选择一个未失败的代理
        available_proxies = [p for p in self.ip if p not in self.failed_proxies]
        if not available_proxies:
            return None

        ip = random.choice(available_proxies)
        request.meta['proxy'] = ip
        request.meta['download_timeout'] = 10  # 设置超时时间
        print(f'使用代理: {ip}')

    def process_exception(self, request, exception, spider):
        # 处理代理连接错误
        if 'proxy' in request.meta:
            failed_proxy = request.meta['proxy']
            self.failed_proxies.add(failed_proxy)
            print(f'代理 {failed_proxy} 连接失败，已加入黑名单')

            # 如果所有代理都失败了，清空黑名单重新尝试
            if len(self.failed_proxies) >= len(self.ip):
                print('所有代理都失败了，清空黑名单重新尝试')
                self.failed_proxies.clear()

            # 返回一个新的请求，使用新的代理
            return request.replace(dont_filter=True)


class SliderMiddleware:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 0.4)
        self.driver.maximize_window()
        self.max_retries = 3  # 最大重试次数
        '''
            处理逻辑：
                是否需要处理
                    是
                        _handle_with_selenium
                    否
        '''

    def process_response(self, request, response, spider):
        try:
            # 检查是否需要处理
            if self._need_handle(response):
                print('检测到需要处理的情况，使用 Selenium 获取页面内容...')
                return self._handle_with_selenium(response, request)

            if self._need_login(response):
                print('检测到需要登录啦 ~1，开始执行登录逻辑')
                return self.login()

            return response

        except Exception as e:
            print(f'处理响应时出现错误: {e}')
            with open(f'./assets/{e}.txt', 'w') as f:
                try:
                    f.write(response.text)
                except Exception as new_e:
                    print(new_e)
                    yield Request(request.url)
                    # f.write(response.json)

            return response

    def _need_handle(self, response):
        """检查响应是否需要使用 Selenium 处理"""

        if 'tmd' in response.url or '/_____tmd_____/punish?' in response.text:
            return True

        if not isinstance(response.text, str):
            print(f'response不是string,response text type===>{type(response.text)}')
            return True


        check_texts = [
            "punish",
            "sessionStorage.x5referer",
            "window.location.replace",
            "window._config_",
            "captcha"
        ]

        return any(text in response.text for text in check_texts)

    def _handle_with_selenium(self, response, request):
        """使用 Selenium 处理页面"""
        retry_count = request.meta.get('retry_count', 0)

        if retry_count >= self.max_retries:
            print(f'已达到最大重试次数 {self.max_retries}，放弃处理')
            with open('./assets/failed_responese_text.', 'w') as f:
                f.write(response.text)
                print('已将错误文件相应内容记录')
            return response

        try:
            # 更新重试计数，测试的时候先放开，后期count每次经过得加1
            request.meta['retry_count'] = retry_count + 1

            # 访问页面
            self.driver.get(response.url)
            self._wait_for_page_load()

            # 处理可能的滑块验证码
            self._handle_slider_if_exists()

            # 等待页面完全加载
            self._wait_for_page_load()

            # 获取页面内容
            page_source = self.driver.page_source

            # 创建新的 Response 对象
            new_response = HtmlResponse(
                url=self.driver.current_url,  # 使用最终URL
                body=page_source.encode('utf-8'),
                encoding='utf-8',
                request=request
            )

            # 复制原始 response 的 meta 信息
            if hasattr(response, 'meta'):
                new_response.meta = response.meta.copy()

            print('成功获取验证后的页面内容')

            # 更新request里的cookie
            cookies = self.driver.get_cookies()
            for cookie in cookies:
                request.cookies[cookie['name']] = cookie['value']
            return new_response

        except Exception as e:
            print(f"使用 Selenium 处理页面时出现错误: {str(e)}")
            # 如果出错，重试
            if retry_count < self.max_retries:
                print(f'准备第 {retry_count + 1} 次重试...')
                return self._handle_with_selenium(response, request)
            return response

    def _wait_for_page_load(self):
        """等待页面加载完成"""
        try:
            self.wait.until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            time.sleep(1)  # 额外等待1秒确保完全加载
        except Exception as e:
            print(f'等待页面加载时出错: {e}')

    def _handle_slider_if_exists(self):
        """处理滑块验证码（如果存在）"""
        try:
            # 等待滑块元素出现
            slider = self.wait.until(
                EC.presence_of_element_located((By.ID, "nc_1_n1z"))
            )
            wrapper = self.wait.until(
                EC.presence_of_element_located((By.ID, "nc_1_wrapper"))
            )

            # 执行滑动
            wrapper_size = wrapper.size
            action = ActionChains(self.driver)
            action.click_and_hold(slider) \
                .move_by_offset(wrapper_size['width'] * 0.9, 0) \
                .release() \
                .perform()

            # 等待验证完成
            time.sleep(1)

        except Exception as e:
            print(f"未找到滑块元素或处理滑块时出错: {str(e)}")

    def _get_cookies_from_selenium(self):
        # 获取 Selenium 中的 Cookie
        cookies = {}
        for cookie in self.driver.get_cookies():
            cookies[cookie['name']] = cookie['value']
        return cookies

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

    def _need_login(self, response):
        print(f'=======>{response.url}')
        # 登录思路
        if 'login' in response.url:
            print('监测到啦')
            return True
        else:
            print('没有发现需要登录！')
            return False

    # def login_with_selenium(self, response, request):
    #     pass

    def get_validation_code(self):
        # 服务器网址
        hostname = 'imap.163.com'
        # 用户名即邮箱账号
        username = 'wade1080'
        # 授权码不是邮箱原密码
        passwd = 'MTbMEHqHYr9nHQBv'
        # 链接服务器
        server = IMAPClient(hostname, ssl=True)
        # 登陆
        try:
            # 登陆账号
            server.login(username, passwd)
            # 上传客户端身份信息
            server.id_({"name": "IMAPClient", "version": "2.1.0"})
            # 导航目录的列表，'INBOX'，'草稿箱'、'已发送'等
            dictList = server.list_folders()
            # print(dictList)
            # 对收件箱只读
            info = server.select_folder('INBOX', readonly=True)
        except server.Error:
            print('Could not login')
            sys.exit(1)
        # 获取邮件列表
        result = server.search()
        print(len(result))
        print(result)
        result = [result[-1]]

        for uid in result:

            massageList = server.fetch(uid, ['BODY[]'])
            print(f'messages: {massageList}')
            mailBody = massageList[uid][b'BODY[]']
            print(f'body: {mailBody}')
            # 邮件内容解析最里面那层是按字节来解析邮件主题内容,这个过程生成Message类型
            try:
                email_content = email.message_from_string(mailBody)
                print(f'content: {email_content}')
            except TypeError:
                email_content = email.message_from_string(str(email.message_from_bytes(mailBody)))
                # print(email_content)
            # 标题
            subject = email.header.make_header(email.header.decode_header(email_content['SUBJECT']))
            # 发件人
            mail_from = email.header.make_header(email.header.decode_header(email_content['From']))
            # 收件日期
            envlope = (server.fetch(uid, ['ENVELOPE']))[uid][b'ENVELOPE']
            dates = envlope.date

            # 获取内容的type编码方式
            maintype = email_content.get_content_maintype()
            if maintype == 'multipart':
                for part in email_content.get_payload():
                    # 获取邮件中的文本
                    if part.get_content_maintype() == 'text':
                        # 下载
                        mail_content = part.get_payload(decode=True).strip()
            elif maintype == 'text':
                mail_content = email_content.get_payload(decode=True).strip()
            try:
                # 解码显示中文，如果utf-8不行用gbk或者其他
                mail_content = mail_content.decode('gbk')
                print(f'content: {mail_content}')
                pattern = 'Please enter the 4-digit code below on the email verification page: (\d+)'
                match = re.search(pattern, mail_content)
                if match:
                    code = str(match.group(1))
                    print(f'code: {code}')
                    return code
            except UnicodeDecodeError:
                try:
                    mail_content = mail_content.decode('utf-8')
                except UnicodeDecodeError:
                    print('decode error')
                    sys.exit(1)
            # 写进txt
            # with open(f'./{uid}.txt', 'w+', encoding="utf-8") as f:
            #     f.write(f'From:{mail_from}' + '\n')
            #     f.write(f'Subject:{subject}' + '\n')
            #     f.write(f'Date:{dates}' + '\n')
            #     f.write(f'正文内容：' + '\n')
            #     f.write((BeautifulSoup(mail_content, 'html.parser').get_text().strip()).replace('\n\n', '') + '\n')
        # print('From: ', mail_from)
        # print('Subject: ', subject)
        # print('Date:',dates)
        # print('-'*10, 'mail content', '-'*10)
        # print(mail_content.replace('<br>', '\n'))
        # print('-'*10, 'mail content', '-'*10)
        # 退出登陆
        server.logout()

    def login(self):
        try:
            # 打开登录页面
            self.driver.get("https://login.aliexpress.com/")
            # 等待邮箱输入框出现并输入邮箱
            try:
                email_input = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cosmos-input"))
                )
                email_input.clear()
                # time.sleep(1)
                email_input.send_keys(self.aliexpress_email)
                print("成功输入邮箱")
            except TimeoutException:
                print("未找到邮箱输入框，尝试其他定位方式")
                email_input = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "fm-login-id"))
                )
                email_input.send_keys(self.aliexpress_email)

            time.sleep(2)

            # 点击获取验证码按钮
            try:
                verify_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Continue')]"))
                )
                verify_button.click()
                print("成功点击获取验证码按钮")
            except:
                print("未找到验证码按钮，尝试其他定位方式")
            # 等待验证码邮件到达
            # time.sleep(15)

            # 判断是否有滑块验证码出现
            try:
                # 等待一段时间让页面完全加载
                time.sleep(3)

                # 打印当前页面源码中是否包含滑块相关元素
                page_source = self.driver.page_source
                if "nc_1_wrapper" in page_source:
                    print("页面源码中找到滑块相关元素")
                    # 尝试处理滑块
                    self.handle_slider()
                else:
                    print(f'未出现滑块验证')

            except Exception as e:
                print(f'处理滑块验证码时出错: {str(e)}')

            # 获取验证码
            # code = self.get_email_code()
            # if code:
            #     print(f"获取到验证码: {code}")
            #     # 输入验证码
            #     code_input = self.wait.until(
            #         EC.presence_of_element_located((By.ID, "fm-login-code"))
            #     )
            #     code_input.send_keys(code)
            #     time.sleep(2)
            #
            #     # 点击登录按钮
            #     login_button = self.wait.until(
            #         EC.element_to_be_clickable((By.CLASS_NAME, "fm-button"))
            #     )
            #     login_button.click()
            #
            #     # 等待登录成功
            #     time.sleep(10)
            #
            #     # 保存cookies
            #     cookies = self.driver.get_cookies()
            #     with open('cookies.json', 'w') as f:
            #         json.dump(cookies, f)
            #
            #     print("登录成功，cookies已保存")
            # else:
            #     print("未找到验证码")
            # with open('./origin_cookie.txt', 'w', encoding='utf-8') as f:
            #     json.dump(self.driver.get_cookies(), f)
            # 获取邮件验证码
            # 等待验证码
            time.sleep(2)
            # 获取邮箱验证码
            code = self.get_validation_code()
            code = str(code)
            # 输入邮箱验证码
            inputs = self.driver.find_elements(By.TAG_NAME, "input")

            print(f'找到{len(inputs)}个 input')
            if len(inputs) == len(code):
                # 遍历每个 input 和 code 的字符
                for i in range(len(code)):
                    inputs[i].send_keys(code[i])
            else:
                print(f'input 跟 code 数量不一致')


        except Exception as e:
            print(f"登录过程出错: {str(e)}")
            # 保存页面源码以便调试
            with open('error_page.html', 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            print("已保存错误页面源码到error_page.html")
        finally:
            print(f'即将关闭浏览器...')
            # self.driver.implicitly_wait(10)
            time.sleep(20)
            cookies = self.driver.get_cookies()
            # with open('cookies.json', 'w') as f:
            #     json.dump(cookies, f)
            print(cookies)
            data = {item['name']: item['value'] for item in cookies}
            print(f'data===>', data)
            with open('./cookies.txt', 'w') as f:
                f.write(str(data))
            # 隐式等待
            # time.sleep(30)  # 等待一会儿再关闭浏览器
            # self.driver.quit()
        return data


# 测试
class SliderMiddleware2:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 禁用自动化标志
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 禁用自动化提示

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.retry_flag = True

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        print('进入SliderMiddleware中间件2')
        return s

    def has_captcha(self):
        return 'punish' in self.driver.current_url

    def process_request(self, request, spider):
        # 检查是否有验证码
        if self.has_captcha():
            print('此时的链接为', request.url)
            print('发现验证码了')
            print('此时的request', request.meta)
            print(f'原始 cookie{request.cookies}')
            # 解决验证码
            self.deal_captcha()
            self.driver.implicitly_wait(10)
            # 保存Cookie
            cookies = self._get_cookies_from_selenium()
            print(f'获取到的cookies: {cookies}')
            if cookies:
                print(f'获取到新增的cookies: {cookies}')
            # 更新request里的cookie
            request.cookies.update(cookies)
            print(f'更新后的 cookie{request.cookies}')
            return request
        else:
            print('未被punish')
            return None
        # return None

    def deal_captcha(self):
        # 尝试查找滑块元素
        # try:
        #     self.driver.find_element(By.ID, "nc_1_n1z")
        #     print("找到滑块元素，开始处理验证码...")
        # except NoSuchElementException as e:
        #     print(f'未找到滑块元素,{e}')
        # 处理滑块验证码的代码...
        try:
            # 首先等待wrapper元素
            wrapper = self.wait.until(
                EC.presence_of_element_located((By.ID, "nc_1_wrapper"))
            )

            print("找到滑块容器")

            # 然后等待滑块元素
            slider = self.wait.until(
                EC.presence_of_element_located((By.ID, "nc_1_n1z"))
            )
            print("找到滑块元素")

            # 获取滑块容器的大小
            wrapper_size = wrapper.size
            print(f"滑块容器大小: {wrapper_size}")

            # 执行滑动 - 一步到位
            action = ActionChains(self.driver)
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            action.move_by_offset(x_offset, y_offset).perform()
            action.click_and_hold(slider) \
                .move_by_offset(wrapper_size['width'] * 0.9, 0) \
                .release() \
                .perform()
            print("完成滑动")

            self.driver.refresh()
            # capture_error = self.wait.until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "errloading"))
            # )
            # print('验证失败')
            # capture_error.click()


        except Exception as e:
            print(f"在当前iframe中未找到滑块: {str(e)}")

        # try:
        #     # 尝试查找滑块容器
        #     wrapper = self.driver.find_element(By.ID, "nc_1_wrapper")
        #     print("找到滑块容器，开始处理验证码...")
        #     # 处理滑块验证码的代码...
        # except:
        #     print("未找到验证码元素")

    def _get_cookies_from_selenium(self):
        # 获取 Selenium 中的 Cookie
        cookies = {}
        for cookie in self.driver.get_cookies():
            cookies[cookie['name']] = cookie['value']
        return cookies

    def spider_opened(self, spider):
        print('爬虫开启')
        spider.logger.info("Spider opened: %s" % spider.name)

    def process_response(self, request, response, spider):
        # print(f'request====>{request.cookies}')
        # print('获得返回内容')
        # print(response.text)

        try:
            if "punish" in response.text:
                # 检查是否出现滑块验证码
                self.driver.refresh()
                time.sleep(2)
                self.driver.get(response.url)
                page_source = self.driver.page_source
                print('发现punish......')
                time.sleep(2)
                # 使用更准确的元素检查方式
                try:
                    # 尝试查找滑块元素
                    slider = self.driver.find_element(By.ID, "nc_1_n1z")
                    print("找到滑块元素，开始处理验证码...")
                    # 处理滑块验证码的代码...
                    try:
                        # 首先等待wrapper元素
                        wrapper = self.wait.until(
                            EC.presence_of_element_located((By.ID, "nc_1_wrapper"))
                        )
                        print("找到滑块容器")

                        # 然后等待滑块元素
                        slider = self.wait.until(
                            EC.presence_of_element_located((By.ID, "nc_1_n1z"))
                        )
                        print("找到滑块元素")

                        # 获取滑块容器的大小
                        wrapper_size = wrapper.size
                        print(f"滑块容器大小: {wrapper_size}")

                        # 执行滑动 - 一步到位
                        action = ActionChains(self.driver)
                        action.click_and_hold(slider) \
                            .move_by_offset(wrapper_size['width'] * 0.9, 0) \
                            .release() \
                            .perform()

                        print("完成滑动")

                    except Exception as e:
                        print(f"在当前iframe中未找到滑块: {str(e)}")
                except:
                    try:
                        # 尝试查找滑块容器
                        wrapper = self.driver.find_element(By.ID, "nc_1_wrapper")
                        print("找到滑块容器，开始处理验证码...")
                        # 处理滑块验证码的代码...
                    except:
                        print("未找到验证码元素，可能验证码形式已改变")
                        # 打印页面内容以便调试
                        print(f'页面内容: {page_source[:500]}')
        except AttributeError as e:
            # print(f'response:{response}')
            print(e)

        # print(f"response.text=========>{response.text}")
        # response.meta["callback"] = "shop"
        return response

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()


class RandomUserAgentMiddleware:
    def __init__(self):
        self.user_agent = UserAgent()
        self.user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.254'
        ]

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def process_request(self, request, spider):
        # 随机选择一个User-Agent
        user_agent = random.choice(self.user_agent_list)
        request.headers["User-Agent"] = user_agent
        # 添加其他必要的请求头
        request.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        request.headers["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8"
        request.headers["Accept-Encoding"] = "gzip, deflate, br"
        request.headers["Connection"] = "keep-alive"
        request.headers["Upgrade-Insecure-Requests"] = "1"

    def process_exception(self, request, exception, spider):
        # 如果请求失败，可以在这里处理异常
        pass

    def spider_opened(self, spider):
        spider.logger.info("RandomUserAgentMiddleware is enabled.")

class SliderMiddleware3:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 禁用自动化标志
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 禁用自动化提示

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.retry_flag = True

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        print('进入SliderMiddleware中间件2')
        return s

    def has_captcha(self):
        return 'punish' in self.driver.current_url

    def process_request(self, request, spider):
        # 检查是否有验证码
        if self.has_captcha():
            print('此时的链接为', request.url)
            print('发现验证码了')
            print('此时的request', request.meta)
            print(f'原始 cookie{request.cookies}')
            # 解决验证码
            self.deal_captcha()
            self.driver.implicitly_wait(10)
            # 保存Cookie
            cookies = self._get_cookies_from_selenium()
            print(f'获取到的cookies: {cookies}')
            if cookies:
                print(f'获取到新增的cookies: {cookies}')
            # 更新request里的cookie
            request.cookies.update(cookies)
            print(f'更新后的 cookie{request.cookies}')
            return request
        else:
            print('未被punish')
            return None
        # return None

    def deal_captcha(self):
        # 尝试查找滑块元素
        # try:
        #     self.driver.find_element(By.ID, "nc_1_n1z")
        #     print("找到滑块元素，开始处理验证码...")
        # except NoSuchElementException as e:
        #     print(f'未找到滑块元素,{e}')
        # 处理滑块验证码的代码...
        try:
            # 首先等待wrapper元素
            wrapper = self.wait.until(
                EC.presence_of_element_located((By.ID, "nc_1_wrapper"))
            )

            print("找到滑块容器")

            # 然后等待滑块元素
            slider = self.wait.until(
                EC.presence_of_element_located((By.ID, "nc_1_n1z"))
            )
            print("找到滑块元素")

            # 获取滑块容器的大小
            wrapper_size = wrapper.size
            print(f"滑块容器大小: {wrapper_size}")

            # 执行滑动 - 一步到位
            action = ActionChains(self.driver)
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            action.move_by_offset(x_offset, y_offset).perform()
            action.click_and_hold(slider) \
                .move_by_offset(wrapper_size['width'] * 0.9, 0) \
                .release() \
                .perform()
            print("完成滑动")

            self.driver.refresh()
            # capture_error = self.wait.until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "errloading"))
            # )
            # print('验证失败')
            # capture_error.click()


        except Exception as e:
            print(f"在当前iframe中未找到滑块: {str(e)}")

        # try:
        #     # 尝试查找滑块容器
        #     wrapper = self.driver.find_element(By.ID, "nc_1_wrapper")
        #     print("找到滑块容器，开始处理验证码...")
        #     # 处理滑块验证码的代码...
        # except:
        #     print("未找到验证码元素")

    def _get_cookies_from_selenium(self):
        # 获取 Selenium 中的 Cookie
        cookies = {}
        for cookie in self.driver.get_cookies():
            cookies[cookie['name']] = cookie['value']
        return cookies

    def spider_opened(self, spider):
        print('爬虫开启')
        spider.logger.info("Spider opened: %s" % spider.name)

    def process_response(self, request, response, spider):
        # print(f'request====>{request.cookies}')
        # print('获得返回内容')
        # print(response.text)

        try:
            if "punish" in response.text:
                # 检查是否出现滑块验证码
                self.driver.refresh()
                time.sleep(2)
                self.driver.get(response.url)
                page_source = self.driver.page_source
                print('发现punish......')
                time.sleep(2)
                # 使用更准确的元素检查方式
                try:
                    # 尝试查找滑块元素
                    slider = self.driver.find_element(By.ID, "nc_1_n1z")
                    print("找到滑块元素，开始处理验证码...")
                    # 处理滑块验证码的代码...
                    try:
                        # 首先等待wrapper元素
                        wrapper = self.wait.until(
                            EC.presence_of_element_located((By.ID, "nc_1_wrapper"))
                        )
                        print("找到滑块容器")

                        # 然后等待滑块元素
                        slider = self.wait.until(
                            EC.presence_of_element_located((By.ID, "nc_1_n1z"))
                        )
                        print("找到滑块元素")

                        # 获取滑块容器的大小
                        wrapper_size = wrapper.size
                        print(f"滑块容器大小: {wrapper_size}")

                        # 执行滑动 - 一步到位
                        action = ActionChains(self.driver)
                        action.click_and_hold(slider) \
                            .move_by_offset(wrapper_size['width'] * 0.9, 0) \
                            .release() \
                            .perform()

                        print("完成滑动")

                    except Exception as e:
                        print(f"在当前iframe中未找到滑块: {str(e)}")
                except:
                    try:
                        # 尝试查找滑块容器
                        wrapper = self.driver.find_element(By.ID, "nc_1_wrapper")
                        print("找到滑块容器，开始处理验证码...")
                        # 处理滑块验证码的代码...
                    except:
                        print("未找到验证码元素，可能验证码形式已改变")
                        # 打印页面内容以便调试
                        print(f'页面内容: {page_source[:500]}')
        except AttributeError as e:
            # print(f'response:{response}')
            print(e)

        # print(f"response.text=========>{response.text}")
        # response.meta["callback"] = "shop"
        return response

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()



class ProxyDownloaderMiddleware:
    _proxy = ('a963.zdtps.com', '21166')

    def process_request(self, request, spider):
        # 用户名密码认证
        username = "202504181053433570"
        password = "fmzp53tl"
        request.meta['proxy'] = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password,
                                                                        "proxy": ':'.join(
                                                                            ProxyDownloaderMiddleware._proxy)}

        # 白名单认证
        # request.meta['proxy'] = "http://%(proxy)s/" % {"proxy": proxy}
        request.headers["Connection"] = "close"
        return None

    def process_exception(self, request, exception, spider):
        """捕获407异常"""
        if "'status': 407" in exception.__str__():  # 不同版本的exception的写法可能不一样，可以debug出当前版本的exception再修改条件
            from scrapy.resolver import dnscache
            dnscache.__delitem__(ProxyDownloaderMiddleware._proxy[0])  # 删除proxy host的dns缓存
        return exception


class CookiesMiddleware:

    def __init__(self):
        self.cookies = self.get_cookie()

    def get_cookie(self):
        opt = webdriver.ChromeOptions()
        # 设置selenium时，启动时浏览器不弹出
        opt.add_argument('--headless')
        opt.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=opt)
        # 加载页面
        driver.get()  # 这边填写能获取到网站cookies的网址
        time.sleep(4)
        # 由于我获取cookie的页面页面无需用户登陆，所以直接获取cookies
        # Selenium为我们提供了get_cookies来获取登录cookies
        cookies = driver.get_cookies()
        cookie = {}
        # scrapy使用cookies需要封装成dict，所以在这边将获取到的cookies处理成dict类型，方便使用
        for s in cookies:
            cookie[s['name']] = s['value']
        # 获取到数据后关闭浏览器
        driver.close()
        return cookie

    def process_request(self, request, spider):
        request.cookies = self.cookies
        return None



