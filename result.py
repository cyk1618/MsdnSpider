import json

with open('xt.txt', 'r', encoding='utf-8')as f:
    file = f.readlines()
    for i in file:
        x = json.loads(i)
        for i in x:
            # print(i['id'])
            print(i['name'])
