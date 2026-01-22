from flask import abort
import pymysql
from util.DB import DB

db_pool = None

def get_db_pool():
    global db_pool
    if db_pool is None:
        db_pool = DB.init_db_pool()
    return db_pool

# ユーザークラス
class User:
    @classmethod
    def create(cls, name, email, password):
        pool = get_db_pool()
        conn = pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s);"
                cur.execute(sql, (name, email, password))
            conn.commit()
            return cur.lastrowid
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            pool.release(conn)
    
    # メールから既存ユーザーを発見
    @classmethod
    def find_by_email(cls, email):
        pool = get_db_pool()
        conn = pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s;"
                cur.execute(sql, (email,))
                user = cur.fetchone()
                return user
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            pool.release(conn)

    # IDから名前を取得
    @classmethod
    def get_name_by_id(cls, user_id):
        pool = get_db_pool()
        conn = pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT name FROM users WHERE id=%s;"
                cur.execute(sql, (user_id,))
                user = cur.fetchone()
            return user["name"] if user else None
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            pool.release(conn)


# 投稿クラス
class Post:
    pass

# コメントクラス
class Comment:
    pass