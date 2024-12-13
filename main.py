import requests
import json
from bs4 import BeautifulSoup as bs #подключение библиотек

url = "https://mgkct.minskedu.gov.by/%D0%BE-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6%D0%B5/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D0%B8%D0%B2" #url сайта
page = requests.get(url) #запрос странице
soup = bs(page.text, "html.parser") #код сайта
id =0

jsonTxt = [] #список для передачи в json файл
Post = list()#список всех должностей

allTeacher = soup.findAll('h3')#все имена преподователей и теги где находятся
allPost = soup.findAll('li', class_="tss")#должность преподавателя и теги где находится

for post in allPost:
    Post.append(post.text)#список всех должностей

for prepods in allTeacher: 
    info = {'num':id+1, 'Teacher':(prepods.parent).text.split()[0]+ ' '+ (prepods.parent).text.split()[1]+' '+(prepods.parent).text.split()[2], 'Post':Post[id]}#библиотека для каждого репозитория
    print(f"{info['num']}. преподователь: {info['Teacher']}; {info['Post']};") #вывод на экран
    jsonTxt.append(info)#добавление информации в список для json файла
    id+=1

with open("data.json", "w", encoding='utf-8') as file:
    json.dump(jsonTxt, file, indent=4, ensure_ascii=True)#запись в json

with open("index.html", "w", encoding='utf-8') as file:#создаётся html файл
    file.write("<html><head><title>преподователи</title>\n<style>div{text-align: center;width: 70%;margin: auto;min-height: 500px;background: #222b24; } \n a{text-decoration: none;color:aliceblue;} \n a:visited{text-decoration: none;color:aliceblue;} \n a:hover{text-decoration: none;color: antiquewhite;}\n body{background: linear-gradient(#262e36, #00140e);color:aliceblue;}\nh2{color:aliceblue}\ntable {width: 100%;border-collapse: collapse;}\ntd, th{border: 1px solid #001405;padding: 8px;text-align: center;}\n</style>\n</head>\n<body>\n<div>\n")#заголовок и стили
    file.write("<h2>\nинформация о преподователях\n<table>\n<tr>\n<th>№</th>\n<th>Teacher</th>\n<th>Post</th>\n</tr>\n")#начало таблицы
    for i in range(len(jsonTxt)):
        file.write(f"<tr>\n<td>{jsonTxt[i]['num']}</td>\n<td>{jsonTxt[i]['Teacher']}</td>\n<td>{jsonTxt[i]['Post']}</td>\n<td>\n</tr>")#заполнение строк
    file.write("</table>\n<a href='https://mgkct.minskedu.gov.by/%D0%BE-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6%D0%B5/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D0%B8%D0%B2'>To mgkct.minskedu.gov.by</a>\n")#конец таблицы и ссылка на оригинал
    file.write("</div>\n</body></html>")#конец файла html
