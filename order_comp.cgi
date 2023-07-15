#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os
import session
#----------------------------------------------------------------
# 処理
# セッション処理
session = session.Session(cookies.SimpleCookie(os.environ.get('HTTP_COOKIE','')))
session.sessionProcess()
#----------------------------------------------------------------
# HTML部
print("Content-Type: text/html")
print(session.setSessionId())
print(session.setSessionUser())
htmlText = '''
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>sample file</title>
    </head>

    <body>
        <h1>Success!!</h1>
        <p>注文を確定しました</p>
        <input type="button" onclick="location.href='./top.cgi'" value="トップページへ戻る">
    </body>
</html>
'''

print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
