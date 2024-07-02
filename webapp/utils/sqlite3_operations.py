import sqlite3

conn = sqlite3.connect(r"users.db")
cursor = conn.cursor()
sql = """CREATE TABLE users (client_name TEXT PRIMARY KEY, password TEXT)"""
cursor.execute(sql)
