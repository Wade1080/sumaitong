import pandas as pd

def get_value(unique_values):
    for value in unique_values:
        yield value
# 读取CSV文件
df = pd.read_csv('products.csv', header=None)

# 获取C列并去重
unique_values = df.iloc[:, 1].unique()
get_value(unique_values)
# print(len(unique_values), type(unique_values))

# 打印去重后的结果
print(unique_values)

flag = True
value_generator = get_value(unique_values)
with open('shop_name.txt', 'w') as f:
    while flag:
        try:
            value = next(value_generator)
            print(value)
            f.write(next(value_generator)+'\n')
        except Exception as e:
            flag = False



