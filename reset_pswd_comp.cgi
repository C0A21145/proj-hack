#!/usr/bin/python3

import cgi
import MySQLdb
from http import cookies
import random, string, os

#----------------------------------------------------------------

#フォームのデータ取得
form = cgi.FieldStorage()
password = form.getfirst('password')
ch_password = form.getfirst('ch_password')
email = form.getfirst('email')

not_match = 0
if (password == None) or (ch_password == None):
    not_match = 1
elif (password != ch_password):
    not_match = 1

connection = MySQLdb.connect(
		host='localhost',
		user='user1',
		passwd='passwordA1!',
		db='EC',
		charset='utf8'
	)
cursor = connection.cursor()

#----------------------------------------------------------------
# HTML部

print("Content-Type: text/html")
if not_match:
    htmlText = '''
	<!DOCTYPE html>
	<html lang="ja">
	    <head>
		<meta charset="utf-8">
		<title>パスワード変更完了</title>
		<META http-equiv="Refresh" content="2;URL=forgot_pswd.cgi">
	    </head>

	    <body>
	    	パスワードと確認用パスワードが一致しません。<br>
		やり直してください。<br>
	    </body>
	</html>
    '''

else:
    sql = "insert into `UserInfo` (`password`, `mail_address`) values ('" + password + "', '" + email + "') on duplicate key update password = '" + password +"', mail_address='" + email +"'"
    cursor.execute(sql)
    connection.commit()
    connection.close()

    htmlText = '''
	<!DOCTYPE html>
	<html lang="ja">
	    <head>
		<meta charset="utf-8">
		<title>パスワード変更完了</title>
	    </head>

	    <body>
	    	パスワードを変更しました。<br>
	    	<button type=“button” onclick="location.href='./top.cgi'">トップページに戻る</button><br>
	    </body>
	</html>
    '''

print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
