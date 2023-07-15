#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os

import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText
#----------------------------------------------------------------
# 処理

#フォームのデータ取得
form = cgi.FieldStorage()
email = form.getfirst('email')

#データベース名など自分のものに変更
connection = MySQLdb.connect(
	host='localhost',
	user='user1',
	passwd='passwordA1!',
	db='EC',
	charset='utf8'
)
cursor = connection.cursor()

#アカウントがあるか確認する変数
no_account = 0

if email == None:
    no_account = 1
else:
    cursor.execute("select * from UserInfo where mail_address='" + email + "'")
    row = cursor.fetchone()
    if (row == None):
        no_account = 1

#----------------------------------------------------------------
# HTML部

print("Content-Type: text/html")
if no_account:
    htmlText = '''
	<!DOCTYPE html>
	<html lang="ja">
	    <head>
		<meta charset="utf-8">
		<title></title>
	    </head>

	    <body>
		アカウントが見つかりません。<br>
		<a href="./register.cgi">アカウントの作成</a>か
		<a href="./login.cgi">ログイン</a>をしてください。<br><br>
		<a href="./top.cgi">トップページに戻る</a><br>
	    </body>
	</html>
	'''
else:
	check = ""
	for i in range(6):
	    ch = random.randint(0,9)
	    check += str(ch)
	
	#SMTPサーバーに接続
	smtp_server = "smtp.gmail.com"
	port = 587

	server = smtplib.SMTP(smtp_server, port)
	
	#TLS暗号化の設定
	server.starttls()
	
	#SMTPサーバーにログイン
	login_address = "c0a2103528@edu.teu.ac.jp"
	login_password = "fantrvltjekvvkvf"

	server.login(login_address, login_password)
	
	#メールの作成
	message = MIMEMultipart()

	message["Subject"] = "本人確認"
	message["From"] = "c0a2103528@edu.teu.ac.jp"
	message["To"] = email
	
	text = MIMEText("本人確認用コード：" + check)
	message.attach(text)
	
	#メールの送信
	server.send_message(message)
	
	#SMTPサーバーの切断
	server.quit()

	htmlText = '''
	<!DOCTYPE html>
	<html lang="ja">
	    <head>
		<meta charset="utf-8">
		<title>本人確認</title>
	    </head>

	    <body>
	    登録されたメールアドレスに送信された本人確認用コードを入力して下さい。
		<form action="reset_pswd.cgi" method="post">
		    <input type="text" name="check" placeholder="確認用コード">
		    <input type="hidden" name="correct" value="%s">
		    <input type="hidden" name="email" value="%s">
		    <input type="submit" name="submit" value="送信">
          	</form>
	    </body>
	</html>
	'''%(check, email)
print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
