import os
import sqlite3


def user_login(username, password):
    file_dir = os.path.abspath(os.path.dirname(__file__))
    conn = sqlite3.connect(file_dir + '/utils/users.db')
    cursor = conn.cursor()
    sql = f"SELECT password FROM users WHERE client_name = '{username}'"
    result = cursor.execute(sql)
    pwd_query = result.fetchall()
    if len(pwd_query) == 0:
        return {"status": "Failure", "message": "Username or password does not match database"}
    else:
        if pwd_query[0][0] == password:
            return {"status": "Success", "message": "Successfully logged in"}
        else:
            return {"status": "Failure", "message": "Username or password does not match database"}

