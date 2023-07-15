#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os
#----------------------------------------------------------------
# 処理

form = cgi.FieldStorage()

email = form.getfirst('email')
password = form.getfirst('password')

#データベース名など自分のものに変更
connection = MySQLdb.connect(
	host='localhost',
	user='user1',
	passwd='passwordA1!',
	db='EC',
	charset='utf8'
)
cursor = connection.cursor()

#ログインできたか確認する変数
ch_login = 0

pas = ""
no_account = ""
not_match_pass = ""
if (email != None):
    cursor.execute("select * from UserInfo where mail_address='" + email + "'")
    row = cursor.fetchone()

    #MySQLに登録されているパスワードの先頭にある空白文字の削除
    if row != None:
        pas = row[1].lstrip()
        if (password == pas):
            ch_login = 1
        else:
            not_match_pass = "メールアドレスかパスワードが違います。<br>再度入力して下さい。<br>"
    else:
        no_account = "アカウントがありません。<br>新規作成(無料)してください。<br>"
#----------------------------------------------------------------
# HTML部

print("Content-Type: text/html")

#ログイン時の表示・ページ移動
if ch_login:
    	htmlText = '''
    	<!DOCTYPE html>
	<html lang="ja">
	    <head>
		<meta charset="utf-8">
		<title>ログイン</title>
		<! content秒後にページ移動 ->
		<META http-equiv="Refresh" content="2;URL=top.cgi">
	    </head>

	    <body>
    		ログインしました。<br>
		トップページに戻ります。<br>
    	    </body>
	</html>
    	'''

#非ログイン時の表示
else:
	htmlText = '''
	<!DOCTYPE html>
	<html lang="ja">
	    <head>
		<meta charset="utf-8">
		<title>ログイン完了</title>
	    </head>
		
	    <body>
	        %s
	        %s
		<form action="./login.cgi" method="post">
		<input type="email" name="email" placeholder="メールアドレス"><br>
		<input type="password" name="password" placeholder="パスワード"><br>
		<input type="submit" name="submit" value="ログイン">
		</form>
		<a href="register.cgi">アカウントを新規作成する</a><br>
		<a href="forgot_pswd.cgi">パスワードを忘れた方はこちら</a><br>
	    </body>
	</html>
	'''%(no_account, not_match_pass)

print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
