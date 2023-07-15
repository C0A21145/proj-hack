import cgi
import MySQLdb
from http import cookies
import random, string, os

class Session:
    def __init__(self, cookie):
        self.my_id = ""
        self.my_username = ""
        self.cookie_session_id = ""
        self.cookie_session_user = ""
        self.sql_session_id = ""
        self.sql_session_user = ""
        self.login_status = 0

        # sql接続
        connection = MySQLdb.connect(
            host='localhost',
            user='akinori',
            passwd='P@ssw0rd',
            db='EC',
            charset='utf8'
        )
        self.connection = connection
        self.cursor = connection.cursor()
        # cookie
        self.cookie = cookie

    # SessionID作成
    def setRandomSessionId(self):
        num = 64
        char_data = string.digits + string.ascii_lowercase + string.ascii_uppercase
        session_id = ''.join([random.choice(char_data) for i in range(num)])

        return session_id

    # Cookieに保存されている値の抽出
    def getCookie(self):
        # cookieは cookies.SimpleCookie(os.environ.get('HTTP_COOKIE',''))
        try:
            session_id = self.cookie["session_id"].value
            session_user = self.cookie["session_user"].value
        except KeyError:
            session_id = ''
            session_user = ''

        self.cookie_session_id = session_id
        self.cookie_session_user = session_user

    # SQLからSession_idを取得
    def getSQL(self):
        sql = "select session_id from Session where user_id = '" + self.cookie_session_user  + "'"
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            self.sql_session_id = rows[0][0]
            self.sql_session_user = self.cookie_session_user
        except:
            self.sql_session_id = "hoge"

    # SQLに新規session_idを保存
    def writeSessionId(self, username):
        new_session_id = self.setRandomSessionId()

        # cookieに保存
        self.cookie_session_id = new_session_id

        try:
            sql = "select session_id from user_id'" + username + "'"
            self.cursor.execute(sql)
            self.connection.commit()

            sql = "update Session set session_id = '" + new_session_id + "' where user_id = '" + username + "'"
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            # SQLに保存
            sql = "insert into Session (`user_id`, `session_id`) values ('" + username + "', '" + new_session_id + "')"
            self.cursor.execute(sql)
            self.connection.commit()

    # セッションIDをCookieに保存
    def setSessionId(self):
        return f"Set-Cookie: session_id={self.cookie_session_id}; Expires=Wed, 21 Oct 2025 07:28:00 JST"

    # ユーザ名をCookieに保存
    def setSessionUser(self):
        return f"Set-Cookie: session_user={self.cookie_session_user}; Expires=Wed, 21 Oct 2025 07:28:00 JST"

    def sessionProcess(self, username=None):
        self.getCookie()
        self.getSQL()

        if self.cookie_session_user != "":
            if self.cookie_session_id == self.sql_session_id:
                self.login_status = 1
            else:
                self.login_status = 0
        if self.login_status == 0:
            if username != None:
                self.writeSessionId(username)
                self.cookie_session_user = username
                self.getSQL()
                self.login_status = 1
            else:
                self.login_status = 0
