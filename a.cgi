#!/usr/bin/python3
import cgi
import MySQLdb
from http import cookies
import random, string, os
import session
#----------------------------------------------------------------
# セッション処理

#----------------------------------------------------------------
# 処理
# form保存
form = cgi.FieldStorage()
user = form.getfirst('user')


session = session.Session(cookies.SimpleCookie(os.environ.get('HTTP_COOKIE','')))
session.getCookie()
session.sessionProcess(user)
#----------------------------------------------------------------
# HTML部
print("Content-Type: text/html")
print(session.setSessionId())
print(session.setSessionUser())
if session.login_status == 0:
    htmlText = '''
    <!DOCTYPE html>
    <html lang="ja">
        <head>
            <meta charset="utf-8">
            <title>sample file</title>
        </head>

        <body>
            <p>スライドショー部分</p>

            <p>%s</p>

            <form action="./a.cgi" method="post"><div>
                ユーザ名<input type="text" name="user" size="20"><br>
                <input type="submit" value="ログイン">
            </div></form>
        </body>
    </html>
    '''%(user)
else:
    htmlText = '''
    <!DOCTYPE html>
    <html lang="ja">
        <head>
            <meta charset="utf-8">
            <title>sample file</title>
        </head>

        <body>
        <p>login success</p>
        <p>%s</p>
        <p>%s</p>

        </body>
    </html>
    '''%([session.cookie_session_user, session.cookie_session_id], [session.sql_session_user, session.sql_session_id])
print(htmlText.encode("utf-8", 'ignore').decode('utf-8'))
(END)
