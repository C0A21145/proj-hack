#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os
import session
#----------------------------------------------------------------
# セッション処理
session = session.Session(cookies.SimpleCookie(os.environ.get('HTTP_COOKIE','')))
session.sessionProcess()
# 処理
form = cgi.FieldStorage()

#削除するカートのカートid
cart_num = form.getfirst("cart_info_id")

mer_count = form.getfirst("mer_count")
count_num = form.getfirst("count_num")
mer_count_type = form.getfirst("count_type")

#データベース接続
#データベース名など自分のものに変更
connection = MySQLdb.connect(
	host='localhost',
	user='akinori',
	passwd='P@ssw0rd',
	db='EC',
	charset='utf8'
)
cursor = connection.cursor()

#カートの商品を削除
if cart_num is not None:
    sql_delete = "delete from BuyInfo where cart_id='" + str(cart_num) + "'"
    cursor.execute(sql_delete)
    connection.commit()


#カートの終了を変更する「+」「-」ボタンのSQL文
if mer_count_type == "reduce":
	mer_count = int(mer_count) -1
	sql_count = "update BuyInfo set merchandise_count = '" + str(mer_count) + "' where cart_id='" + str(count_num) + "'"
	cursor.execute(sql_count)
	connection.commit()

elif mer_count_type == "add":
	mer_count = int(mer_count) +1
	sql_count = "update BuyInfo set merchandise_count = '" + str(mer_count) + "' where cart_id='" + str(count_num) + "'"
	cursor.execute(sql_count)
	connection.commit()

#カートに追加した最新の情報を取得
sql_cart = "select * from BuyInfo where user_id=1;"
cursor.execute(sql_cart)
rows = cursor.fetchall()

#お勧めする商品のmerchandise_idをランダムで3つ生成
def random_nums(lst):
	sql = "select merchandise_id from Merchandise;"
	cursor.execute(sql)
	rows_mer_id = cursor.fetchall()
	max_num = rows_mer_id[-1][0]
	while len(nums_lst) < 3:
		num = random.randint(1, max_num)
		if not num in nums_lst and num != rows_mer_id[0][0]:
			nums_lst.append(num)



#----------------------------------------------------------------
print("Content-Type: text/html")
print(session.setSessionId())
print(session.setSessionUser())

if session.login_status == 1:
	# HTML部
	htmlText = '''
	<!DOCTYPE html>
	<html lang="ja">
		<head>
			<meta charset="utf-8">
			<title>cart_page</title>
		</head>

		<body>
			<h1>ショッピングカート</h1>
			'''
	for row in rows:
		#カートに追加した商品の詳細を取得（セッションID処理完成したらuser_idごとの情報を取得）
		sql_mer = "select * from Merchandise where merchandise_id ='" + str(row[2]) + "'"
		cursor.execute(sql_mer)
		mer_rows = cursor.fetchall()
		mer_row = mer_rows[0]
		merchandise_img = "./imgs/products/" + str(mer_row[0]) + ".jpg"
		merchandise_name = mer_row[1]

		htmlText+='''
			<table>
			<tr>
				<!--カート内の商品情報の表示と削除するxボタンの表示-->
			<form action="./cart_page.cgi" method="post"><div>
				<input type="hidden" name="cart_info_id" value="%s">
				<th><input type="submit" name="cart_delete" value="x"></th>
				</form></div>

				<th><img src="%s" align="top" alt = "%s"></th> <td>%s</td>

				<!--「-」ボタンのフォーム-->
				<form action="./cart_page.cgi" name="count_reduce" method="post"><div>
				<input type="hidden" name="count_type" value="reduce">
				<input type="hidden" name="count_num" value="%s">
				<input type="hidden" name="mer_count" value=%s>
				<th><input type="submit" name="redu_btn" value="-"></th>
				</form></div>

				<td>%s</td>

				<!--「+」ボタンのフォーム-->
				<form action="./cart_page.cgi" name="count_add" method="post"><div>
				<input type="hidden" name="count_type" value="add">
				<input type="hidden" name="count_num" value="%s">
				<input type="hidden" name="mer_count" value=%s>
				<th><input type="submit" name="add_btn" value="+"></th>
				</form></div>
				<td>%s</td>
			</tr>
			</table>
			</div>

			'''%(row[0], merchandise_img, merchandise_name, merchandise_name, row[0], row[3], row[3], row[0], row[3], mer_row[2])



	htmlText+='''
		<p>こちらもおすすめ</p>
		'''

	nums_lst = []
	random_nums(nums_lst)
	for i in nums_lst:
		#商品DBの情報をデータベースからランダムで3つ取得
		sql_all_mer = "select * from Merchandise where merchandise_id='" + str(i) +"'"
		cursor.execute(sql_all_mer)
		all_mer = cursor.fetchall()
		recomend_img = "./imgs/products/" + str(i) + ".jpg"
		recomend_id = all_mer[0][0]
		recomend_name = all_mer[0][1]
		recomend_price = all_mer[0][2]


		#おすすめの商品をデータベースからランダムで3つ取り出して表示する
		htmlText+='''
			<form action="./detail.cgi" name="count_add" method="post">
			<img src="%s" align="top" alt = "%s">
			<p>%s</p>
			<p>%s</p>
			<input type="hidden" name="recomend_id" value="%s">
			<input type="submit" value="詳しく見る"></form><br>
			'''%(recomend_img, recomend_name, recomend_name, recomend_price, recomend_id)

	htmlText+='''
			<input type="button" onclick="location.href='./order_page.cgi'" value="注文画面へ">
			</body>
		</html>
		'''
else:
    htmlText = '''
    	<!DOCTYPE html>
		<html lang="ja">
	    <head>
		<meta charset="utf-8">
		<title>ログイン</title>
		<! content秒後にページ移動 ->
		<META http-equiv="Refresh" content="0.5;URL=login.cgi">
	    </head>

	    </html>
    	'''
print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
