import requests
import json
from bs4 import BeautifulSoup as bs, Tag #импорт библиотек

url = "https://mgkct.minskedu.gov.by/%D0%BE-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6%D0%B5/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D0%B8%D0%B2" #url сайта
page = requests.get(url)
soup = bs(page.text, "html.parser") 
id = 0 #счетчик для num

jsonTxt = [] 
Post = []  

allTeacher = soup.findAll('h3')  #все имена преподователей и теги где находятся
allPost = soup.findAll('li', class_="tss")  #должность преподавателя и теги где находится

for post in allPost:
    Post.append(post.text)  #список всех должностей

for prepods in allTeacher:
    info = {
        'num': id + 1,
        'Teacher': ' '.join((prepods.parent).text.split()[:3]),  #добавление фио
        'Post': Post[id]
    }
    print(f"{info['num']}. преподаватель: {info['Teacher']}; {info['Post']};")  #вывод на консоль
    jsonTxt.append(info)  #добавление в json
    id += 1

with open("data.json", "w", encoding='utf-8') as file:
    json.dump(jsonTxt, file, indent=4, ensure_ascii=False)# сохранение в json

with open('index.html', 'r', encoding='utf-8') as file:
    filedata = file.read() # сохранение в html

soup = bs(filedata, "html.parser")

table = soup.new_tag("table") #создание table для сохранения 
table.append(soup.new_tag("tr"))
table.tr.append(soup.new_tag("th", string="№"))
table.tr.append(soup.new_tag("th", string="Teacher"))
table.tr.append(soup.new_tag("th", string="Post"))

for item in jsonTxt:
    row = soup.new_tag("tr")
    row.append(soup.new_tag("td", string=str(item['num'])))
    row.append(soup.new_tag("td", string=item['Teacher']))
    row.append(soup.new_tag("td", string=item['Post']))
    table.append(row)

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify()) #запись в html
