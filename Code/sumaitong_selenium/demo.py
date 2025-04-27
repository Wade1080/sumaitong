from scrapy import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumCaptchaMiddleware:
    def __init__(self):
        # 初始化 Selenium
        self.driver = webdriver.Chrome()  # 或其他浏览器驱动

    def process_request(self, request, spider):
        # 检查是否需要处理验证码
        if self._needs_captcha(request):
            # 使用 Selenium 处理验证码
            self.driver.get(request.url)
            self._solve_captcha_with_selenium()

            # 获取验证码通过后的 Cookie
            cookies = self._get_cookies_from_selenium()

            # 将 Cookie 注入到 Scrapy 的请求中
            request.cookies.update(cookies)
            request.meta['selenium_cookies'] = True  # 标记为已处理

        return None  # 继续处理请求

    def process_response(self, request, response, spider):
        # 检查是否需要重新发起请求
        if request.meta.get('selenium_cookies') and self._needs_captcha(response):
            # 重新发起请求
            new_request = request.copy()
            new_request.dont_filter = True  # 避免被去重过滤器过滤
            return new_request

        return response

    def _needs_captcha(self, request_or_response):
        # 判断是否需要处理验证码
        # 例如：检查请求或响应中是否包含验证码标志
        return 'captcha' in request_or_response.url or 'captcha' in request_or_response.text

    def _solve_captcha_with_selenium(self):
        # 使用 Selenium 处理验证码
        captcha_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input#captcha'))
        )
        captcha_input.send_keys('1234')  # 输入验证码
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button#submit')
        submit_button.click()

    def _get_cookies_from_selenium(self):
        # 获取 Selenium 中的 Cookie
        cookies = {}
        for cookie in self.driver.get_cookies():
            cookies[cookie['name']] = cookie['value']
        return cookies

    def close_spider(self, spider):
        # 关闭 Selenium
        self.driver.quit()