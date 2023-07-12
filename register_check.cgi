#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os
#----------------------------------------------------------------
# 処理
#フォームのデータ取得
form = cgi.FieldStorage()

first_name = form.getfirst('first_name')
last_name = form.getfirst('last_name')
password = form.getfirst('password')
post_code = form.getfirst('post_code')
address = form.getfirst('address')
phone = form.getfirst('phone_number')
email = form.getfirst('mail_address')
ccn = form.getfirst('credit_card_number')
ccsn = form.getfirst('credit_card_security_number')

#データベース名など自分のものに変更
connection = MySQLdb.connect(
	host='localhost',
	user='user1',
	passwd='passwordA1!',
	db='EC',
	charset='utf8'
)
cursor = connection.cursor()

#すでに登録されているか確認する変数(初登録の時 1)
m_check = 1  #メールアドレス
p_check = 1  #電話番号

#メアドが被った時登録しない
cursor.execute("select * from UserInfo where mail_address='" + email + "'")
row = cursor.fetchone()
if (row != None):
    m_check = 0

#電話番号が被った時登録しない
cursor.execute("select * from UserInfo where phone_number='" + phone + "'")
row = cursor.fetchone()
if (row != None):
    p_check = 0

#すでに登録されていたとき用のメッセージ
message = ""
if (m_check == 0):
    message += "このメールアドレスはすでに登録されています。<br>"
if (p_check == 0):
    message += "この電話番号はすでに登録されています。<br>"

#----------------------------------------------------------------
# HTML部

print("Content-Type: text/html")
#何も被ってないとき
if p_check and m_check:
	htmlText = '''
	<!DOCTYPE html>
	<html lang="ja">
	    <head>
		<meta charset="utf-8">
		<title>登録内容の確認</title>
		
	    </head>

	    <body>
		登録内容の確認<br>
		first_name = %s<br>
		last_name = %s<br>
		password = %s<br>
		post_code = %s<br>
		address = %s<br>
		phone_number = %s<br>
		mail_address = %s<br>
		credit_card_number = %s<br>
		credit_card_security_number = %s<br>
		
		<form action="./register_comp.cgi" method="post"><div>
		   <input type="hidden" name="first_name" size="60" value=%s><br>
		   <input type="hidden" name="last_name" size="60" value=%s><br>
		   <input type="hidden" name="password" size="60" minlength="4" maxlength="22" value=%s><br>
		   <input type="hidden" name="post_code" size="8" maxlength="8" value=%s><br>
		   
		   <input type="hidden" name="address" size="60" value=%s><br>
		   <input type="hidden" name="phone_number" size="15" maxlength="15" value=%s><br>
		   <input type="hidden" name="mail_address" size="60" value=%s><br>
		   <input type="hidden" name="credit_card_number" size="19" maxlength="19" value=%s><br>
		   <input type="hidden" name="credit_card_security_number" size="1" maxlength="3" value=%s><br>
		   <input type="submit" value="登録">
		  </div></form>
		  <button type=“button” onclick="location.href='./register.cgi'">再入力</button>
	    </body>
	</html>
	'''%(first_name, last_name, password, post_code, address, phone, email, ccn, ccsn, first_name, last_name, password, post_code, address, phone, email, ccn, ccsn)
	
else:
	htmlText = '''
	<!DOCTYPE html>
	<html lang="ja">
	    <head>
		<meta charset="utf-8">
		<title>登録内容の確認</title>
	    </head>
	    <body>
	        %s
	        再入力またはログインしてください。<br>
	        
	    <! 登録画面(register,cgi)へ ->
	    <button type=“button” onclick="location.href='./register.cgi'">再入力</button>
	    
	    <! ログイン画面(login.cgi)へ ->
	    <button type=“button” onclick="location.href='./login.cgi'">ログイン</button>
	    </body>
	</html>
	'''%(message)
print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
