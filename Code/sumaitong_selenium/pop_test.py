import imaplib
import poplib
import ssl
import email
from email.header import decode_header
from email.parser import Parser
from email.header import make_header, decode_header
from email.utils import parsedate_to_datetime



def get_qq_email_by_pop3():
    # QQ邮箱POP3服务器配置
    pop3_server = "pop.163.com"
    email_address = "Wade1080@163.com"
    password = "MTbMEHqHYr9nHQBv"  # 授权码
    port = 995

    # 创建SSL上下文
    context = ssl.create_default_context()

    try:
        # 连接QQ邮箱POP3服务器
        server = poplib.POP3_SSL(pop3_server, port, context=context)
        
        # 身份认证
        server.user(email_address)
        server.pass_(password)
        
        print("登录成功!")
        print(f"邮件数量: {server.stat()[0]}")
        print(f"邮箱大小: {server.stat()[1]} bytes")

        # 获取最新的一封邮件
        resp, lines, octets = server.retr(1)
        
        # 解析邮件内容
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        
        # 获取邮件主题
        subject = decode_header(msg.get('Subject'))[0]
        if subject[1]:  # 如果有编码信息
            subject = subject[0].decode(subject[1])
        else:
            subject = subject[0]
        print(f"邮件主题: {subject}")
        
        # 获取发件人
        from_addr = decode_header(msg.get('From'))[0]
        if from_addr[1]:
            from_addr = from_addr[0].decode(from_addr[1])
        else:
            from_addr = from_addr[0]
        print(f"发件人: {from_addr}")
        
        # 获取邮件内容
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                content = part.get_payload(decode=True).decode()
                print(f"邮件内容:\n{content}")
                break
                
        # 关闭连接
        server.quit()
        
    except Exception as e:
        print(f"发生错误: {e}")

def get_email_by_imap():

    try:
        email_value_config = {
            'imap_server': "imap.163.com",
            'username': "Wade1080@163.com",
            'password': "MTbMEHqHYr9nHQBv",
        }
        port = 995
        email_server = imaplib.IMAP4_SSL(email_value_config['imap_server'])  # 这样就已经链接到目标邮箱了
        context = ssl.create_default_context()
        email_server = imaplib.IMAP4_SSL(email_value_config['imap_server'])  # 这样就已经链接到目标邮箱了
        email_server.login(email_value_config["username"], email_value_config['password'])  # 这里登录
        email_server.select('INBOX')
        '''
            INBOX 收件箱
            Sent Messages 已发送
            Drafts 草稿箱
            Deleted Messages 已删除
            Junk 垃圾箱
        
        '''
        # 选择收件箱
        _typ, _search_data = email_server.search(None, 'ALL')
        # 开始解析
        mailidlist = _search_data[0].split()  # 转成标准列表,获得所有邮件的ID

        print(f'一共解析邮件数量：{len(mailidlist)}')
        # 解析内容：
        for mail_id in mailidlist:
            result, data = email_server.fetch(mail_id, '(RFC822)')  # 通过邮件id获取邮件
            email_message = email.message_from_bytes(data[0][1])  # 邮件内容（未解析）
            subject = make_header(decode_header(email_message['SUBJECT']))  # 主题
            mail_from = make_header(decode_header(email_message['From']))  # 发件人
            mail_dt = parsedate_to_datetime(email_message['Date']).strftime("%Y-%m-%d %H:%M:%S")  # 收件时间
            email_info = {
                "主题": str(subject),
                "发件人": str(mail_from),
                "收件时间": mail_dt,
            }
            print(email_info)
        print('success')
    except Exception as e:
        print('failed to connect to imap server',e )

def get_email_content_by_imap():
    try:
        # 邮箱配置
        email_config = {
            'imap_server': "imap.163.com",
            'username': "Wade1080@163.com", 
            'password': "MTbMEHqHYr9nHQBv",
        }
        
        # 连接IMAP服务器
        email_server = imaplib.IMAP4_SSL(email_config['imap_server'])
        email_server.login(email_config['username'], email_config['password'])
        
        # 选择收件箱
        email_server.select('INBOX')  # 必须先选择邮箱文件夹
        
        # 搜索最新的5封邮件
        status, data = email_server.search(None, 'ALL')
        if status != 'OK':
            raise Exception("搜索邮件失败")
            
        email_ids = data[0].split()[-5:]  # 获取最新的5封邮件
        
        email_contents = []
        for email_id in email_ids:
            # 获取邮件内容
            status, msg_data = email_server.fetch(email_id, '(RFC822)')
            if status != 'OK':
                continue
                
            email_body = msg_data[0][1]
            message = email.message_from_bytes(email_body)
            
            # 解析邮件内容
            content = ""
            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_type() == "text/plain":
                        content = part.get_payload(decode=True).decode()
                        break
            else:
                content = message.get_payload(decode=True).decode()
                
            # 获取邮件信息
            subject = str(make_header(decode_header(message['Subject'])))
            sender = str(make_header(decode_header(message['From'])))
            date = parsedate_to_datetime(message['Date']).strftime("%Y-%m-%d %H:%M:%S")
            
            email_info = {
                "主题": subject,
                "发件人": sender,
                "时间": date,
                "内容": content
            }
            email_contents.append(email_info)
            
        # 关闭连接
        email_server.close()
        email_server.logout()
        
        return email_contents
        
    except Exception as e:
        print(f"获取邮件内容失败: {e}")
        return None
if __name__ == "__main__":
    # get_qq_email_by_pop3()
    get_email_content_by_imap()