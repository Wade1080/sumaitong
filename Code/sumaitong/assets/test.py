import json
import re
with open('jsonp.txt', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'jsonp_\d{13}_\d{5}\((.*?"success":true})\)'
match = re.search(pattern, content)
# print(match.group(1))
with open('./result.txt','w',encoding='utf-8') as f:
    f.write(match.group(1))



data = json.loads(match.group(1))
print(data)