import json

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import time
from selenium.webdriver.common.action_chains import ActionChains
from imap_165 import get_validation_code


class SumaitongLogin:
    def __init__(self):
        # 设置Chrome选项
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-maximized')  # 最大化窗口
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 禁用自动化标志
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 禁用自动化提示
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })

        self.pop3_server = "pop.qq.com"
        self.email = "2513473008@qq.com"
        self.email_password = "hxsyrqtwoqiydiae"
        self.aliexpress_email = "wade1080@163.com"
        self.port = 995

        self.wait = WebDriverWait(self.driver, 20)  # 增加等待时间到20秒

    # def get_email_code(self):
    #     try:
    #         try:
    #             # 连接到POP3服务器
    #             pop3_server = "pop.163.com"
    #             server = poplib.POP3(pop3_server)
    #             server.user(self.email)
    #             server.pass_(self.email_password)
    #         except Exception as e:
    #             print('网易邮箱登录出错', e)
    #
    #         # 获取最新邮件
    #         try:
    #             resp, lines, octets = server.retr(len(server.list()[1]))
    #             msg_content = b'\r\n'.join(lines).decode('utf-8')
    #             msg = email.message_from_string(msg_content)
    #             print(f'msg: {msg}')
    #             # 查找验证码
    #             for part in msg.walk():
    #                 if part.get_content_type() == "text/plain":
    #                     content = part.get_payload(decode=True).decode()
    #                     match = re.search(r'\d{4}', content)
    #                     if match:
    #                         return match.group()
    #             return None
    #         except Exception as e:
    #             print('获取最新邮箱出错', e)
    #     except Exception as e:
    #         print(f"获取邮箱验证码出错: {str(e)}")
    #         return None
    # def get_origin_text(self):  # 获取邮件原始文本
    #     # 创建SSL上下文
    #     context = ssl.create_default_context()
    #
    #     try:
    #         # 使用SSL连接POP3服务器
    #         with poplib.POP3_SSL(self.pop3_server, self.port, context=context) as server:
    #             # 登录邮箱
    #             server.user(self.email)
    #             server.pass_(self.email_password)
    #             print("登录成功！")
    #
    #             # 获取邮箱状态
    #             num_messages, total_size = server.stat()
    #             print(f"邮件总数: {num_messages}, 总大小: {total_size} bytes")
    #
    #             # 获取第一封邮件
    #             if num_messages > 0:
    #                 response, lines, octets = server.retr(1)
    #                 email_content = b"\n".join(lines).decode("utf-8")
    #                 print("第一封邮件内容:")
    #                 print(email_content)
    #
    #     except poplib.error_proto as e:
    #         print(f"登录失败: {e}")
    #     except Exception as e:
    #         print(f"发生错误: {e}")

    def handle_slider(self):
        """处理滑块验证码"""
        try:
            print("开始寻找滑块...")

            # 首先检查是否在iframe中
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            print(f"找到 {len(iframes)} 个iframe")
            print(iframes)

            try:
                print(f"切换iframe")
                self.driver.switch_to.frame(iframes[-1])

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

            except Exception as e:
                print(f"切换iframe失败: {str(e)}")
            finally:
                # 切回主文档
                self.driver.switch_to.default_content()

        except Exception as e:
            print(f"处理滑块时出错: {str(e)}")
            # 保存页面源码以便调试
            with open('slider_error.html', 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            print("已保存错误页面源码到slider_error.html")

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
            code = get_validation_code()
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


if __name__ == "__main__":
    login = SumaitongLogin()
    cookie = login.login()
    # print(cookie)

    login.driver.get(
        'https://shoprenderview.aliexpress.com/async/execute?componentKey=allitems_choice&deviceId=1x6IL1R0BUCAbeyVerUp2ai&SortType=bestmatch_sort&page=1&pageSize=30&country=US&site=glo&sellerId=2675329572&groupId=1&currency=USD&locale=en_US&buyerId=6340368875&callback=jsonp_1744431181655_96752')
    # with open('./cookies.txt', 'r') as f:
    #     cookies = f.read().strip()  # 去除首尾空白字符
    #     print(cookies)
    #     print(type(cookies))
    #
    #     # 将键值对字符串转换为字典
    #     cookies_dict = {}
    #     for item in cookies.split('; '):
    #         key, value = item.split('=', 1)  # 只分割第一个等号
    #         cookies_dict[key] = value
    #
    #     print(cookies_dict)
    #
    # res = requests.get(
    #     'https://shoprenderview.aliexpress.com/async/execute?componentKey=allitems_choice&deviceId=1x6IL1R0BUCAbeyVerUp2ai&SortType=bestmatch_sort&page=1&pageSize=30&country=US&site=glo&sellerId=2675329572&groupId=1&currency=USD&locale=en_US&buyerId=6340368875&callback=jsonp_1744431181655_96752',
    #     cookies=cookies_dict
    # )

    print(login.driver.page_source)
