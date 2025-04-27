from selenium import webdriver
from sumaitong_login import SumaitongLogin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import time
from selenium.webdriver.common.action_chains import ActionChains
from imap_165 import get_validation_code

# 本文件用于错误检测。
'''
    检测思路用selenium打开网页，检查是否有验证码，如果有则解决滑块验证码，如果无则通过
'''


class ErrorCheck:
    def __init__(self, url):
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
        self.addr = url

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
            self.driver.get(self.addr)
            print("开始寻找滑块...")

            # 首先检查是否在iframe中
            try:
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                print(f"找到 {len(iframes)} 个iframe")
                print(iframes)
            except:
                print('没有找到iframe')

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
                print(f"出错了: {str(e)}")


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

            time.sleep(30)  # 等待一会儿再关闭浏览器
            self.driver.quit()
        return cookies

    def error_check(self):
        # self.driver.get("https://www.aliexpress.us/w/wholesale-injector.html?g=y&SearchText=injector")
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
            print(e)


# check = ErrorCheck()
# url = 'https://www.aliexpress.us/w/wholesale-injector.html?g=y&SearchText=injector'
# obj = SumaitongLogin()
# obj.driver.get(url)
# obj.handle_slider()
if __name__ == '__main__':
    check = ErrorCheck(
        'https://www.aliexpress.us//item/3256808569518267.html/_____tmd_____/punish?x5secdata=xcV95oGQD69A%2fNLkF3t%2f9d4UOaFI%2bn73nI53J8uVAGJ%2b95US1AfywgOYHEQHPAAkmu9rYWLATd3oEqdL%2fzSrszwbJ41zC3Wpx89DIXkwnKUcxd%2bmgX2d6zHqmE8D5kNDK8kVdmtQMupZc3qp%2bFpKMbTV1U0s6kQa87Z33toUaOhvuB0H4xhP0VfQa7%2fv7VGpCegw1ORyzda6u9%2b%2fFs92OSbJG%2b81eIgswNz%2fHjAFqfWb%2fkNLNtPKVFgzZHwMxforBS3HVnQdRehdxY2dg0EW4Qc8%2fRqico148GVcXy7WX3vEI%3d__bx__www.aliexpress.us%2fitem%2f3256808569518267.html&x5step=1')
    check.error_check()
    obj = {
        "itemType": "productV3",
        "productType": "natural",
        "nativeCardType": "nt_srp_cell_g",
        "itemCardType": "app_us_local_card",
        "transitionaryExpFrame": false,
        "productId": "3256808480483977",
        "lunchTime": "2025-03-17 00:00:00",
        "image": {
            "imgUrl": "//ae-pic-a1.aliexpress-media.com/kf/Sb09f639702134c349df7fcfeda132dd3e.jpg",
            "imgWidth": 350,
            "imgHeight": 350,
            "imgType": "0"
        },
        "title": {
            "displayTitle": "Genuine Denso OEM Fuel Injectors Nozzle Fit for Prius 23250\u201121020 Fuel Fit"
        },
        "prices": {
            "skuId": "12000046156856732",
            "pricesStyle": "default",
            "builderType": "skuCoupon",
            "currencySymbol": "$",
            "prefix": "Sale price:",
            "originalPrice": {
                "priceType": "original_price",
                "currencyCode": "USD",
                "minPrice": 23.38,
                "formattedPrice": "US $23.38",
                "cent": 2338
            },
            "salePrice": {
                "discount": 80,
                "minPriceDiscount": 80,
                "priceType": "sale_price",
                "currencyCode": "USD",
                "minPrice": 4.46,
                "formattedPrice": "US $4.46",
                "cent": 446
            },
            "taxRate": "0"
        },
        "sellingPoints": [
            {
                "sellingPointTagId": "m0000430",
                "tagStyleType": "default",
                "tagContent": {
                    "displayTagType": "image",
                    "tagImgUrl": "https://ae01.alicdn.com/kf/Sbd36ca6043d0446dbe96b6263eded7fcC.png",
                    "tagImgWidth": 167,
                    "tagImgHeight": 32,
                    "tagStyle": {
                        "position": "1"
                    }
                },
                "source": "local_flag",
                "resourceCode": "searchItemCard"
            }, {
                "sellingPointTagId": "m0000026",
                "tagStyleType": "default",
                "tagContent": {
                    "displayTagType": "image",
                    "tagImgUrl": "https://ae01.alicdn.com/kf/Sb6a0486896c44dd8b19b117646c39e36J/116x64.png",
                    "tagImgWidth": 116,
                    "tagImgHeight": 64,
                    "tagStyle": {
                        "position": "1"
                    }
                },
                "source": "bigSale_atm",
                "resourceCode": "searchItemCard"
            }, {
                "sellingPointTagId": "m0000469",
                "tagStyleType": "default",
                "tagContent": {
                    "displayTagType": "image_text",
                    "tagText": "New shoppers save $18.92",
                    "tagImgUrl": "https://ae01.alicdn.com/kf/S0f1bc1aeb2ab4de98568b86f99bcd0991/42x60.png",
                    "tagImgWidth": 42,
                    "tagImgHeight": 60,
                    "tagStyle": {
                        "color": "#D3031C",
                        "position": "4"
                    }
                },
                "source": "welcomedeal_test",
                "resourceCode": "searchItemCard"
            }, {
                "sellingPointTagId": "m0000376",
                "tagStyleType": "default",
                "tagContent": {
                    "displayTagType": "text",
                    "tagText": "Free shipping",
                    "tagStyle": {
                        "color": "#333333",
                        "position": "4"
                    }
                },
                "source": "Free_Shipping_atm",
                "resourceCode": "searchItemCard"
            }],
        "moreAction": {
            "actions": [{
                "actionText": "Add to cart",
                "actionType": "shopCart"
            }, {
                "actionText": "See preview",
                "actionType": "quickView"
            }, {
                "actionText": "Similar items",
                "actionType": "similarItems"
            }]
        },
        "trace": {
            "pdpParams": {
                "pdp_cdi": "%7B%22traceId%22%3A%22213ee07a17448530551585307e20c7%22%2C%22itemId%22%3A%223256808480483977%22%2C%22fromPage%22%3A%22search%22%2C%22skuId%22%3A%2212000046156856732%22%2C%22shipFrom%22%3A%22US%22%2C%22order%22%3A%22-1%22%2C%22star%22%3A%22%22%7D",
                "channel": "direct",
                "pdp_npi": "4%40dis%21USD%2123.38%214.46%21%21%2123.38%214.46%21%40213ee07a17448530551585307e20c7%2112000046156856732%21sea%21US%216345377806%21ABX",
                "pdp_perf": "main_img=%2F%2Fae-pic-a1.aliexpress-media.com%2Fkf%2FSb09f639702134c349df7fcfeda132dd3e.jpg",
                "pdp_ext_f": "%7B%22order%22%3A%22-1%22%2C%22eval%22%3A%221%22%7D"
            },
            "exposure": {
                "selling_point": "m0000430,m0000026,m0000469,m0000376",
                "displayCategoryId": "",
                "postCategoryId": "200002226",
                "algo_exp_id": "2786f6c0-566e-4c0a-a542-1b21ee1ee6f8-0"
            },
            "p4pExposure": {},
            "click": {
                "algo_pvid": "2786f6c0-566e-4c0a-a542-1b21ee1ee6f8",
                "haveSellingPoint": "true"
            },
            "detailPage": {
                "algo_pvid": "2786f6c0-566e-4c0a-a542-1b21ee1ee6f8",
                "algo_exp_id": "2786f6c0-566e-4c0a-a542-1b21ee1ee6f8-0"
            },
            "custom": {},
            "utLogMap": {
                "formatted_price": "US $4.46",
                "csp": "4.46,1",
                "x_object_type": "productV3",
                "is_detail_next": "1",
                "dress_plan_log_info": "",
                "mixrank_success": "false",
                "title_type": "origin_title",
                "hitNasaStrategy": "3#1170005#1;1#1436007#0",
                "spu_best_flags": "0,0,0",
                "oip": "23.38,1",
                "spu_type": "group",
                "if_store_enter": "0",
                "spu_id": "1005008666798729",
                "image_type": "0",
                "dress_txt_flag": "",
                "pro_tool_code": "platformItemSubsidy,proEngine",
                "algo_pvid": "2786f6c0-566e-4c0a-a542-1b21ee1ee6f8",
                "hit_19_forbidden": false,
                "model_ctr": "0.11876944452524185",
                "spu_replace_id": "-1",
                "sku_id": "12000046156856732",
                "custom_group": 3,
                "sku_ic_tags": "[721998,721996]",
                "dress_creative_flag": "",
                "img_url_trace": "Sb09f639702134c349df7fcfeda132dd3e.jpg",
                "is_adult_certified": false,
                "mixrank_enable": "false",
                "ump_atmospheres": "new_user_platform_allowance,none",
                "BlackCardBizType": "app_us_local_card",
                "spBizType": "normal",
                "selling_point": "m0000430,m0000026,m0000469,m0000376",
                "nasaCode": "3#1170005#-101150002",
                "nasa_tag_ids": [],
                "x_object_id": "1005008666798729"
            }
        },
        "config": {
            "action": {
                "closeAnimation": "false"
            }
        },
        "images": [{
            "imgUrl": "//ae-pic-a1.aliexpress-media.com/kf/Sb09f639702134c349df7fcfeda132dd3e.jpg",
            "imgWidth": 350,
            "imgHeight": 350,
            "imgType": "0"
        }, {
            "imgUrl": "//ae-pic-a1.aliexpress-media.com/kf/S6ad94953207e4d5f855bfc3bf7086b8eV.jpg",
            "imgWidth": 350,
            "imgHeight": 350,
            "imgType": "0"
        }, {
            "imgUrl": "//ae-pic-a1.aliexpress-media.com/kf/S7dbeb307642444e9b49eda4888eec6aeg.jpg",
            "imgWidth": 350,
            "imgHeight": 350,
            "imgType": "0"
        }, {
            "imgUrl": "//ae-pic-a1.aliexpress-media.com/kf/S6670abf2b58e42fca10ac69a55bb64a6t.jpg",
            "imgWidth": 350,
            "imgHeight": 350,
            "imgType": "0"
        }, {
            "imgUrl": "//ae-pic-a1.aliexpress-media.com/kf/S82c610c1a2434222b1fe56090cea52dcG.jpg",
            "imgWidth": 350,
            "imgHeight": 350,
            "imgType": "0"
        }, {
            "imgUrl": "//ae-pic-a1.aliexpress-media.com/kf/Sefdbe648766747de87e780fe117514ef1.jpg",
            "imgWidth": 350,
            "imgHeight": 350,
            "imgType": "0"
        }],
        "seoWhite": "false"
    }
