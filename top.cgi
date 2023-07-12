#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os
#----------------------------------------------------------------
# 処理
# sql接続
connection = MySQLdb.connect(
    host='localhost',
    user='akinori',
    passwd='P@ssw0rd',
    db='EC',
    charset='utf8'
)
cursor = connection.cursor()

# SQLより商品取り出し
sql = "select * from Merchandise"
cursor.execute(sql)
rows = cursor.fetchall()
#----------------------------------------------------------------
# HTML部
print("Content-Type: text/html")
htmlText = '''
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>sample file</title>
    </head>

    <body>
        <p>スライドショー部分</p>
'''
for row in rows:
    # 商品画像のパスはimgs + merchandise_id + jpg
    merchandise_img = "./imgs/" + str(row[0]) + ".png"
    merchandise_name = row[1]
    price = row[2]
    htmlText += '''
    <div class=merchandise_box>
        <img class=merchandise_img src=%s alt=%s>
        <p>%s</p>
        <p>%s</p>
    </div>
    '''%(merchandise_img, merchandise_name, merchandise_name, price)

htmlText += '''
    </body>
</html>
'''

print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
