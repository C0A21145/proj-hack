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

#登録情報をDBに追加

sql = "INSERT INTO `UserInfo` (`password`, `first_name`, `last_name`, `post_code`, `address`, `phone_number`, `mail_address`, `credit_card_number`, `credit_card_security_number`) VALUES (' " + password +"', '" + first_name + "', '" + last_name + "', '" + post_code + "', '" + address + "', '" + phone + "', '" + email + "', '" + ccn + "', '" + ccsn + "')"
cursor.execute(sql)
connection.commit()
connection.close()

#----------------------------------------------------------------
# HTML部

print("Content-Type: text/html")
htmlText = '''
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>登録内容の確認</title>
    </head>

    <body>
        登録が完了しました！<br>
    <button type=“button” onclick="location.href='./top.cgi'">トップページに戻る</button>

    </body>
</html>
'''

print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
