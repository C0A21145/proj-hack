#!/usr/bin/python3

import cgi
import MySQLdb
from http import cookies
import random, string, os

#----------------------------------------------------------------


#----------------------------------------------------------------
# HTML部

print("Content-Type: text/html")
htmlText = '''
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>アカウントの作成</title>
        <! 見た目調整->
        <style>
        .center{
        	text-align: center;
        }
        </style>
    </head>

    <body>
    	<! 郵便番号検索ライブラリの読み込み ->
	<script src="https://yubinbango.github.io/yubinbango/yubinbango.js" charset="UTF-8"></script>
    	
	<! フォームの送信->
	<! 2023/07/09 変更点　action="./register_check.cgi"->
        <form action="./register_check.cgi" method="post" class="h-adr"><div>
	   <input type="text" required name="first_name" size="60" placeholder="姓"><br>
	   <input type="text" required name="last_name" size="60" placeholder="名"><br>
	   <input type="password" required name="password" size="60" minlength="4" maxlength="22" placeholder="パスワード"><br>
	   
	   <! 国の設定 ->
	   <span class="p-country-name" style="display:none;">Japan</span>
	   <input type="text" required class="p-postal-code" name="post_code" size="8" maxlength="8" placeholder="郵便番号"><br>
	   
	   <input type="text" required class="p-region p-locality p-street-address p-extended-address" name="address" size="60" placeholder="住所"><br>
	   <input type="text" required name="phone_number" size="15" maxlength="15" placeholder="電話番号"><br>
	   <input type="email" required name="mail_address" size="60" placeholder="メールアドレス"><br>
	   <input type="text" required name="credit_card_number" size="19" maxlength="19" placeholder="クレジットカード番号"><br>
	   セキュリティコード　<input type="text" required name="credit_card_security_number" size="1" maxlength="3" class="center" placeholder=""><br>
	  
	    <input type="submit" value="登録">
	    <input type="reset" value="リセット">
	  </form>
    </body>
</html>
'''

print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
