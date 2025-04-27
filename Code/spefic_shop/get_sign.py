import hashlib
import time


def generate_sign(token, timestamp, app_key, data):
    # 拼接输入字符串
    input_str = f"{token}&{timestamp}&{app_key}&{data}"

    # 计算 MD5 哈希值
    md5_hash = hashlib.md5(input_str.encode('utf-8')).hexdigest()

    # 转换为小写
    sign = md5_hash.lower()

    return sign


def build_request_params(token, app_key, data):
    # 获取当前时间戳（秒级）
    # timestamp = str(int(time.time()))
    timestamp = '1744358175855'

    # 生成 sign
    sign = generate_sign(token, timestamp, app_key, data)

    # 构建请求参数
    params = {
        "jsv": "2.5.1",
        "appKey": app_key,
        "t": timestamp,
        "sign": sign
    }

    return params


# 示例输入
data = '{"sellerId":231389366,"storeId":4538016,"_country":"US","_lang":"en","needReset":true}'

# 生成请求参数
request_params = build_request_params(token, app_key, data)

# 打印结果
print("请求参数:", request_params)