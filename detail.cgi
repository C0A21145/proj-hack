#!/usr/bin/python3


import cgi
import MySQLdb
from http import cookies
import random, string, os
#---------------------------------------------------------------
# 処理

form = cgi.FieldStorage()
review = form.getfirst("review")
star_num = form.getfirst("star_num")
print("Content-Type: text/html\n")

#使用するデータベースに接続
connection = MySQLdb.connect(
	host='localhost',
	user='user1',
	passwd='passwordA1!',
	db='EC',
	charset='utf8'
)
cursor = connection.cursor()


#商品DBから詳細を表示する商品の情報を取得する
sql_mer = "select * from Merchandise where merchandise_id=1;"
cursor.execute(sql_mer)
rows_mer = cursor.fetchall()
mer_exp = rows_mer[0]

#カートに追加した商品の情報を取得
sql_cart = "select * from BuyInfo;"
cursor.execute(sql_cart)
rows = cursor.fetchall()
row = rows[len(rows) -1][1]

#商品をカートに追加した際のページへのパス
page = "./cart_add.cgi"

#レビュー内容をデータベースに書き込む
if(review is not None and star_num is not None):
    sql_add = "insert into `Review` (`merchandise_id`, `user_id`, `star`, `comment`) values (1, 1, '" + star_num + "', '" + review + "');"
    cursor.execute(sql_add)
    connection.commit()

#レビュー内容をWeb上で表示させるSQL文の設定
sql_display = "select * from Review;"
cursor.execute(sql_display)
disp_rows = cursor.fetchall()

connection.close()


#----------------------------------------------------------------
# HTML部
htmlText = '''
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>merchandise_detail</title>
    </head>

    <body>
        <!--画面のタイトル文字 -->
        <h1>商品詳細</h1>
        
        <!--商品関係 -->
        <div class="merchandise_detail">
        <img src=".png" align="top" alt = "ここに商品画像">
        <P>%s</P>
        '''%(mer_exp[-1])
htmlText += '''
        <form action="%s" method="post" id="cartForm">
        <input type="hidden" name="cart_info_name" value="%s">
        <input type="hidden" name="cart_info" value="%s">
        <input type="submit" name="cart_submit" value="カートに追加">
        </form>
        </div>
        '''%(page,row, mer_exp)
        
htmlText += '''
        <!--レビューボックス入力部分 -->
        <form action="./detail.cgi" method="post"><div>
          review_wirte_box<br>
            <textarea cols="60" rows="5" name="review"></textarea><br>
            
                <!-- レビューの星表示部分 -->
        	<div class="rate-form">
  		  <input id="star5" type="radio" name="star_num" value="1">
  		  <label for="star5">★</label>
  		  <input id="star4" type="radio" name="star_num" value="2">
  		  <label for="star4">★</label>
  		  <input id="star3" type="radio" name="star_num" value="3">
  		  <label for="star3">★</label>
  		  <input id="star2" type="radio" name="star_num" value="4">
  		  <label for="star2">★</label>
  		  <input id="star1" type="radio" name="star_num" value="5">
  		  <label for="star1">★</label>
		</div>
		
	    <!--レビュー書き込みボタン -->
            <input type="submit" value="write">
        </div>
        '''
        
#レビュー表示部分 
for disp_row in reversed(disp_rows):
    htmlText+='''
    <p>review: %s</p>
    <p>star_num: %s</p>
    '''%(disp_row[-1], disp_row[-2])
    
htmlText+='''
    </body>
</html>
'''
print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
