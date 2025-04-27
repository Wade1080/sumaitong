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
