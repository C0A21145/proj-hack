#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os
#----------------------------------------------------------------
# 処理
form = cgi.FieldStorage()
cart_info = form.getfirst('cart_info')
cart_info_name = form.getfirst('cart_info_name')
cnt = form.getfirst('cnt')
print("Content-Type: text/html\n")

print(cnt)
print(cart_info_name)
#データベース接続
connection = MySQLdb.connect(
	host='localhost',
	user='user1',
	passwd='passwordA1!',
	db='EC',
	charset='utf8'
)
cursor = connection.cursor()

#カートに追加する情報をデータベースに書き込む
#postしてきた値がNoneでないとき
if(cart_info is not None):
    sql_cart_add = "INSERT INTO `BuyInfo` (`user_id`, `merchandise_id`, `merchandise_count`) values (1, '" + cart_info[1] + "', '" + cnt + "');"
    cursor.execute(sql_cart_add)
    connection.commit()
    cart_add = cursor.fetchall()

#カートに追加した商品名を取得
sql = "select * from Merchandise where merchandise_id ='" + cart_info_name[0] + "'"
cursor.execute(sql)

rows = cursor.fetchall()
merchandise_img = "./imgs/" + str(rows[0][0]) + ".png"
merchandise_name = rows[0][1]

#----------------------------------------------------------------
# HTML部

htmlText = '''
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>cart_add_page</title>
    </head>

    <body>
        <h1>こちらの商品をカートに追加しました。</h1>
        
        <!--商品の画像と商品の名前の表示 -->
        <img src="%s" align="top" alt = "%s">
        <p>%s</p>
        
        <!--買い物を続けるボタン、カートページへのボタンの設置 -->
        <input type="button" onclick="location.href='./top.cgi'" value="買い物を続ける">
        <input type="button" onclick="location.href='./cart_page.cgi'" value="カートへ移動">
        
        '''%(merchandise_img, merchandise_name, merchandise_name)
        
htmlText += '''
    </body>
</html>
'''

print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
