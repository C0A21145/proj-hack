#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os
import session
#----------------------------------------------------------------
# 処理
form = cgi.FieldStorage()
show_more_flag = form.getfirst('show_more_flag')

# セッション処理
session = session.Session(cookies.SimpleCookie(os.environ.get('HTTP_COOKIE','')))
session.sessionProcess()

if show_more_flag is None:
	#グローバル変数
	#「show more」を押されているかの判定
	show_more_flag = False

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
print(session.setSessionId())
print(session.setSessionUser())

if session.login_status == 1:
    htmlText = '''
    <!DOCTYPE html>
    <html lang="ja">
        <head>
            <meta charset="utf-8">
            <title>sample file</title>
        </head>

        <body>
            <p>スライドショー部分</p>
            <p>Products</p>
    '''
    for row in rows:
        # 商品画像のパスはimgs + merchandise_id + jpg
        merchandise_img = "./imgs/" + str(row[0]) + ".png"
        merchandise_id = row[0]
        merchandise_name = row[1]
        price = row[2]
        if show_more_flag != "True" and merchandise_id > 9:
            break
        htmlText += '''
        <form action="./detail.cgi" name="merchandise_form" method="post"><div class=merchandise_box>
            <input type="hidden" name="mer_id" value="%s">
            <img class=merchandise_img src=%s alt=%s>
            <p>%s</p>
            <p>%s</p>
            <input type="submit" value="詳しく見る">
        </div>
        </form>
        '''%(merchandise_id, merchandise_img, merchandise_name, merchandise_name, price)

        #「show more」押されていなかったら「show more」ボタンを表示
    if show_more_flag !="True":
        htmlText += '''
        <form action="./top.cgi" name="show_more_form" method="post">
        <input type="hidden" name="show_more_flag" value="True">
        <input type="submit" value="SHOW MORE→">
        </form>
        '''

    htmlText+='''
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
