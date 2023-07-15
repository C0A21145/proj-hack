#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os
#----------------------------------------------------------------
# 処理
#フォームのデータ取得
form = cgi.FieldStorage()
check = form.getfirst('check')
correct = form.getfirst('correct')
email = form.getfirst('email')

not_match = 0
if check != correct:
    not_match = 1

#----------------------------------------------------------------
# HTML部

print("Content-Type: text/html")
if not_match:
    htmlText = '''
        <!DOCTYPE html>
	<html lang="ja">
	    <head>
		<meta charset="utf-8">
		<title>パスワードの変更</title>
		<META http-equiv="Refresh" content="2;URL=forgot_pswd.cgi">
	    </head>
	    <body>
	        コードが正しくありません。<br>
	        やり直してください。<br>
	    </body>
	</html>
    '''
    
else:
    htmlText = '''
	<!DOCTYPE html>
	<html lang="ja">
	    <head>
	    
		<meta charset="utf-8">
		<title>パスワードの変更</title>
	    </head>
	    <body>
		<form action="./reset_pswd_comp.cgi" method="post">
			<input type="password" name="password" size="60" minlength="4" maxlength="22"><br>
			確認のため再度入力して下さい。<br>
			<input type="password" name="ch_password" size="60" minlength="4" maxlength="22"><br>
			<input type="hidden" name="email" value="%s">
			<input type="submit" name="submit" value="送信">
		</form>
	 
	    </body>
	</html>
	'''%(email)

print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
