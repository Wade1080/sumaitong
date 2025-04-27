import re

with open('./cookies.txt','r') as f:
    content = f.read()
    match = re.search("x_alimid=(\d+)",content)
    if match:
        print(match.group(1))
