#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os
import session
#----------------------------------------------------------------
# 処理
#グローバル変数
#合計金額を保存するtotal_amountを設定する
total_amount = 0

form = cgi.FieldStorage()

# セッション処理
session = session.Session(cookies.SimpleCookie(os.environ.get('HTTP_COOKIE','')))
session.sessionProcess()

#データベース接続
connection = MySQLdb.connect(
	host='localhost',
	user='akinori',
	passwd='P@ssw0rd',
	db='EC',
	charset='utf8'
)
cursor = connection.cursor()

#ユーザ情報の取得
sql_user = "select * from UserInfo where user_id = 1;"
cursor.execute(sql_user)
user_rows = cursor.fetchall()
#郵便番号、住所、クレジットカードの番号を変数に代入
post_num = user_rows[0][4]
address = user_rows[0][5]
credit_num = user_rows[0][8]

#カート情報を取得して注文合計金額を設定する
sql_order = "select * from BuyInfo where user_id = 1;"
cursor.execute(sql_order)
order_rows = cursor.fetchall()
for order_row in order_rows:
	merchandise_id = order_row[2]
	buy_count = order_row[3]
	sql_mer = "select * from Merchandise where merchandise_id ='" + str(merchandise_id) + "'"
	cursor.execute(sql_mer)
	mer_rows = cursor.fetchall()
	price = mer_rows[0][2]
	total_amount += price * buy_count

#----------------------------------------------------------------
# HTML部
print("Content-Type: text/html")
print(session.setSessionId())
print(session.setSessionUser())

htmlText = '''
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>order_page</title>
    </head>

    <body>
	<p>注文内容確認</p>

	<!--注文内容部分 -->
	<table name="order_conf">
	  <tr align="left"><th>〒%s%sにお届けします。</th></tr>
	  <tr align="left"><th>商品合計</th><td>￥%s</td></tr>
	  <tr align="left"><th>送料</th><td>￥0</td></tr>
	  <th align="left">-----------</th>
	  <tr align="left"><th>お支払い合計</th><td>￥%s</td></tr>
	</table>
	'''%(post_num, address, total_amount, total_amount)

htmlText+='''
	<table>
	  <p>お届け先</p>
	  <tr align="left"><th>〒%s%s</th><tr>
	</table>
	<input type="button" onclick="location.href='./change_address.cgi'" value="変更する">
        '''%(post_num, address)

htmlText+='''
	<div class="pay_method">
	  <p>お支払い方法</p>
	  <p>クレジットカード</p>
	  <p>%s</p>
	  <input type="button" onclick="location.href='./settrement.cgi'" value="変更する">
	</div>
	  '''%(credit_num)

htmlText+='''
	<input type="button" onclick="location.href='./order_comp.cgi'" value="注文を確定する">
    </body>
</html>
'''

print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
