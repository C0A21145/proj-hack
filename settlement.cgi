#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os
#----------------------------------------------------------------
# 処理
# sql接続
connection = MySQLdb.connect(
    host='localhost',
    user='akinori',
    passwd='P@ssw0rd',
    db='EC',
    charset='utf8'
)
cursor = connection.cursor()

sql = "select credit_card_number, credit_card_security_number from UserInfo where user_id = 1"
cursor.execute(sql)
rows = cursor.fetchall()

card_num = rows[0][0]
card_security_num = rows[0][1]

#----------------------------------------------------------------
# HTML部
print("Content-Type: text/html")
htmlText = '''
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>sample file</title>
    </head>

    <body>
        <form action="#" id="form">
        <div class="selector-box">
            <h1>決済ページ</h1>
            <h2>支払い情報の選択</h2>
            <div class="credit">
                <p>クレジットカード番号</p>
                <p>%s</p>
                <p>セキュリティ番号</p>
                <input type="text" name="security_num"><br>
            </div>
            <div class="confirm-button">
                <input type="submit" value="決済">
            </div>
        </div>
        </form>

        <script>
        document.getElementById("form").onsubmit = function(event) {
            event.preventDefault();
            let security = document.getElementById("form").security_num.value;
            if (security == %s) {
                location = "./top.cgi"
            } else {
                alert(%s, security)
            }
        }
        </script>
    </body>
</html>
'''%(card_num, card_security_num, card_security_num)


print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
