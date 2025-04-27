# -*- encoding: utf-8 -*-
import email, sys
from imapclient import IMAPClient
from bs4 import BeautifulSoup
import re


def get_validation_code():
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


if __name__ == '__main__':
    code = get_validation_code()
    print(code)

    obj = {"itemType": "productV3", "productType": "ad", "nativeCardType": "nt_srp_cell_g",
           "itemCardType": "app_us_local_card", "transitionaryExpFrame": False, "productId": "3256808336991512",
           "lunchTime": "2025-02-19 00:00:00",
           "image": {"imgUrl": "//ae-pic-a1.aliexpress-media.com/kf/S50c608689e654a12a61b7d5db1aa5136s.jpg",
                     "imgWidth": 350, "imgHeight": 350, "imgType": "0"},
           "title": {"displayTitle": "0445110682 55263233 Brand New Common Rail Injector Assembly 0445110300"},
           "prices": {"skuId": "12000045551429236", "pricesStyle": "default", "builderType": "skuCoupon",
                      "currencySymbol": "$", "prefix": "Sale price:",
                      "originalPrice": {"priceType": "original_price", "currencyCode": "USD", "minPrice": 23,
                                        "formattedPrice": "US $23.00", "cent": 2300},
                      "salePrice": {"discount": 15, "minPriceDiscount": 15, "priceType": "sale_price",
                                    "currencyCode": "USD", "minPrice": 19.55, "formattedPrice": "US $19.55",
                                    "cent": 1955}, "taxRate": "0"}, "sellingPoints": [
            {"sellingPointTagId": "m0000026", "tagStyleType": "default", "tagContent": {"displayTagType": "image",
                                                                                        "tagImgUrl": "https://ae01.alicdn.com/kf/Sb6a0486896c44dd8b19b117646c39e36J/116x64.png",
                                                                                        "tagImgWidth": 116,
                                                                                        "tagImgHeight": 64,
                                                                                        "tagStyle": {"position": "1"}},
             "source": "bigSale_atm", "resourceCode": "searchItemCard"},
            {"sellingPointTagId": "m0000155", "tagStyleType": "default",
             "tagContent": {"displayTagType": "image_text", "tagText": "Save $3.45",
                            "tagImgUrl": "https://ae01.alicdn.com/kf/S0f1bc1aeb2ab4de98568b86f99bcd0991/42x60.png",
                            "tagImgWidth": 42, "tagImgHeight": 60, "tagStyle": {"color": "#FD384F", "position": "4"}},
             "source": "bigSale_discount", "resourceCode": "searchItemCard"},
            {"sellingPointTagId": "m0000063", "tagStyleType": "default",
             "tagContent": {"displayTagType": "text", "tagText": "Extra 3% off with coins",
                            "tagStyle": {"color": "#D3031C", "position": "4"}}, "source": "flexiCoin_new_atm",
             "resourceCode": "searchItemCard"}, {"sellingPointTagId": "m0000419", "tagStyleType": "default",
                                                 "tagContent": {"displayTagType": "text", "tagText": "Sellers' pick",
                                                                "tagStyle": {"color": "#D3031C", "position": "4"}},
                                                 "source": "without_atm_fake_sellers_picked",
                                                 "resourceCode": "searchItemCard"}],
           "moreAction": {
            "actions": [{"actionText": "Add to cart", "actionType": "shopCart"},
                        {"actionText": "See preview", "actionType": "quickView"},
                        {"actionText": "Similar items", "actionType": "similarItems"}]},
           "trace": {"pdpParams": {
            "pdp_cdi": "%7B%22traceId%22%3A%2221059dbe17448523118705317ea911%22%2C%22itemId%22%3A%223256808336991512%22%2C%22fromPage%22%3A%22search%22%2C%22skuId%22%3A%2212000045551429236%22%2C%22shipFrom%22%3A%22CN%22%2C%22order%22%3A%22-1%22%2C%22star%22%3A%22%22%7D",
            "channel": "direct",
            "pdp_npi": "4%40dis%21USD%2123.00%2119.55%21%21%2123.00%2119.55%21%4021059dbe17448523118705317ea911%2112000045551429236%21sea%21US%216345377806%21ABX",
            "pdp_perf": "main_img=%2F%2Fae-pic-a1.aliexpress-media.com%2Fkf%2FS50c608689e654a12a61b7d5db1aa5136s.jpg",
            "pdp_ext_f": "%7B%22order%22%3A%22-1%22%2C%22eval%22%3A%221%22%7D"}, "exposure": {
            "session_id": "202504161811521025997348973900002169486",
            "selling_point": "m0000026,m0000155,m0000063,m0000419", "aem_p4p_exposure": "1005008523306264",
            "displayCategoryId": "", "postCategoryId": "200004103",
            "algo_exp_id": "195c1c04-d705-49d9-b45b-b707946f02a2-59"}, "p4pExposure": {}, "click": {
            "algo_pvid": "195c1c04-d705-49d9-b45b-b707946f02a2", "aem_p4p_click": "1005008523306264",
            "haveSellingPoint": "true"}, "detailPage": {"aem_p4p_detail": "202504161811521025997348973900002169486",
                                                        "algo_pvid": "195c1c04-d705-49d9-b45b-b707946f02a2",
                                                        "algo_exp_id": "195c1c04-d705-49d9-b45b-b707946f02a2-59"},
            "custom": {
                "p4pExtendParam": "{\"company_name\":\"\u5341\u5830\u534e\u7ff0\u6c7d\u8f66\u96f6\u90e8\u4ef6\u6709\u9650\u516c\u53f8\",\"store_name\":\"DFCZY Truck house Store\"}"},
            "utLogMap": {
                "formatted_price": "US $19.55",
                "csp": "19.55,1",
                "x_object_type": "productV3",
                "is_detail_next": "1",
                "dress_plan_log_info": "",
                "mixrank_success": "False",
                "hitNasaStrategy": "",
                "spu_best_flags": "0,0,0",
                "oip": "23.0,1",
                "spu_type": "group",
                "if_store_enter": "0",
                "image_type": "0",
                "dress_txt_flag": "",
                "pro_tool_code": "proEngine",
                "algo_pvid": "195c1c04-d705-49d9-b45b-b707946f02a2",
                "hit_19_forbidden": False,
                "session_id": "202504161811521025997348973900002169486",
                "sku_id": "12000045551429236",
                "sku_ic_tags": "[]",
                "dress_creative_flag": "",
                "img_url_trace": "S50c608689e654a12a61b7d5db1aa5136s.jpg",
                "is_adult_certified": False,
                "mixrank_enable": "False",
                "ump_atmospheres": "none",
                "BlackCardBizType": "app_us_local_card",
                "spBizType": "p4p",
                "selling_point": "m0000026,m0000155,m0000063,m0000419",
                "nasa_tag_ids": [],
                "x_object_id": "1005008523306264"}},
           "config": {"action": {"closeAnimation": "False"}}, "images": [
            {"imgUrl": "//ae-pic-a1.aliexpress-media.com/kf/S50c608689e654a12a61b7d5db1aa5136s.jpg", "imgWidth": 350,
             "imgHeight": 350, "imgType": "0"},
            {"imgUrl": "//ae-pic-a1.aliexpress-media.com/kf/S83d07a9bcf31467481717cefbdec3176y.jpg", "imgWidth": 350,
             "imgHeight": 350, "imgType": "0"},
            {"imgUrl": "//ae-pic-a1.aliexpress-media.com/kf/S0d9c893ef63a42a5b16c3428848bce5dy.jpg", "imgWidth": 350,
             "imgHeight": 350, "imgType": "0"},
            {"imgUrl": "//ae-pic-a1.aliexpress-media.com/kf/Sb5937938ac87460784974d9ab8d3b284M.jpg", "imgWidth": 350,
             "imgHeight": 350, "imgType": "0"}], "p4p": {
            "clickUrl": "//us-click.aliexpress.com/ci_bb?ot=hippo-033001245007.us44&a=411419964&e=ZIzuC-KS9C.oTLXi55BW6MfRPgMNKT8Ntpz9jURa4oxxFVPubhTBuL6Z8APAnOgUaNMcIQttck2nBdgkYxYUC7bzXWO20eNKxAztuzm9h5hcAFTQU.FS784sZeesRjIz-.9JRIYu4PbcdtGLIGJndxIDP312xHu3ZQ4ZbnfRVcaWNl8150NgSWgNOSwam79vYDlkbRFgvHT.71dCIBcZIIg.dhd8jNerRItqnA888zO4JEQTSyjxOse9j2E4OWcc.IQwK609K4IpKZ5OXE45Q6NJQnEADQXylT79yF2LPF79i1RadlzQCtK1sY2.hCOplryzM0XVQKd6zjPvu9CJxHuXtsZlOqTcCcRy1Hd10lIvIRe8Z7EZOlp6K9Usr8eWYoZqsnvmRy56l.6Q8PSfl14TmXxKdKqiJd6pRrP.FlhKQSwt.Yb9YqN0fGWVikQRU7ZylEgzA5q7sf6zhVgNZfKXmzY8OmsPtm6Ful1vALHjzW3NUdRpHDyRIi-JhW5GWZgx9DNImn8zJWVDK.1xNfwA0llsWh9mFI6gDrlMu1WkRlzQCIjOmRK7XZ.suqVRkFXB7XBEb5DXR9CELdeJzfDB.Pgt98vld66jpdRnbZ6QeE1vz0fgKNHImXwTffoJD6c7-REZ1XZ1t667j1ry3Z2W0Zkgvc8-1LnmNkmvHU4qO8zhwXZp3PNvF2T2eoarAKoe53ghTMT3kiTOR767aCcB1o1FKYBg4o3jk4SDw4UqsvXJbDmPucBXbul0hp0LgG-3VIGq-4b9ZAK7jzpl6mCC6Rb-uoFu4lH9KPoB7e7uhy3eFV3NT8rldU-tlV9ho26B2XZJZsW3FpgJDwYlMZdR-x1jg9dLsFVIqvzY3pA_&ap=15&rp=15",
            "sessionId": "202504161811521025997348973900002169486",
            "adTag": {"displayTagType": "text", "tagText": "Ad", "tagStyle": {"backgroundColor": "rgba(0,0,0,0.20)"}}},
           "seoWhite": "true"}
