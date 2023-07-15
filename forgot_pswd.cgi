#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os
#----------------------------------------------------------------
# 処理



#----------------------------------------------------------------
# HTML部

print("Content-Type: text/html")
htmlText = '''
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>パスワードの変更</title>
    </head>
        パスワードを再設定したいアカウントのメールアドレスを入力して下さい<br>
	<form action="./check_person.cgi" method="post">
		<input type="email" name="email" placeholder="メールアドレス">
		<input type="submit" name="submit" value="送信">
	</form>
    <body>
    
    </body>
</html>
'''

print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
