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
    

    # プロフィールの更新
    @classmethod
    def update_profile(cls, user_id,name,introduce):
        pool = get_db_pool()
        conn = pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE users SET name = %s, introduce = %s WHERE id = %s;"
                cur.execute(sql, (name,introduce,user_id))
                conn.commit()
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

    # IDからユーザー情報を取得
    @classmethod
    def get_user_by_id(cls, user_id):
        pool = get_db_pool()
        conn = pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT name,introduce FROM users WHERE id=%s;"
                cur.execute(sql, (user_id,))
                user = cur.fetchone()
            return {"name": user["name"], "introduce": user["introduce"]} if user else None
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            pool.release(conn)

# 投稿クラス
class Post:
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM posts WHERE deleted_at IS NULL ORDER BY created_at DESC;"
                cur.execute(sql)
                posts = cur.fetchall()
            return posts
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    #ユーザーIDで投稿を取得
    @classmethod
    def get_by_user_id(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM posts WHERE user_id = %s AND deleted_at IS NULL ORDER BY created_at DESC;"
                cur.execute(sql,(user_id,))
                posts = cur.fetchall()
            return posts
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)    


    # 投稿作成処理
    @classmethod
    def create(cls, user_id, content):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO posts (user_id, content) VALUES (%s, %s);"
                cur.execute(sql, (user_id, content))
                new_post_id = cur.lastrowid
                conn.commit()
                return new_post_id
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # 削除処理
    @classmethod
    def delete(cls, post_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE posts SET deleted_at = NOW() WHERE id = %s;"
                cur.execute(sql, (post_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_id(cls, post_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM posts WHERE id=%s AND deleted_at IS NULL;"
                cur.execute(sql, (post_id))
                post = cur.fetchone()
            return post
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

# コメントクラス
class Comment:
    @classmethod
    def create(cls, user_id, post_id, content):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO comments (user_id, post_id, content) VALUES (%s, %s, %s);"
                cur.execute(sql, (user_id, post_id, content))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    @classmethod
    def get_by_post_id(cls, post_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM comments WHERE post_id=%s ORDER BY created_at DESC;"
                cur.execute(sql, (post_id,))
                comments = cur.fetchall()
            return comments
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

# メディアクラス
class Media:
    # 画像登録処理
    @classmethod
    def create(cls, user_id, file_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO medias (user_id, file_name) VALUES (%s, %s);"
                cur.execute(sql, (user_id, file_name))
                new_media_id = cur.lastrowid
                conn.commit()
                return new_media_id
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            conn.rollback()
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_post_id(cls, post_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT m.file_name FROM medias m JOIN post_medias pm ON m.id = pm.media_id WHERE pm.post_id = %s;"
                cur.execute(sql, (post_id,))
                return cur.fetchall()
        finally:
            db_pool.release(conn)

# ポストメディアクラス
class PostMedia:
    @classmethod
    def create(cls, post_id, media_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO post_medias (post_id, media_id) VALUES (%s, %s);"
                cur.execute(sql, (post_id, media_id))
                new_post_media_id = cur.lastrowid
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            conn.rollback()
            abort(500)
        finally:
            db_pool.release(conn)

# いいねクラス
class Like:
    @classmethod
    def toggle(cls, user_id, post_id, comment_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                check_sql = "SELECT id FROM likes WHERE user_id = %s AND post_id = %s;"
                cur.execute(check_sql, (user_id, post_id))
                is_existing = cur.fetchone()

                if is_existing:
                    delete_sql = "DELETE FROM likes WHERE user_id = %s AND post_id = %s;"
                    cur.execute(delete_sql, (user_id, post_id))
                    status = False
                else:
                    insert_sql = "INSERT INTO likes (user_id, post_id, comment_id) VALUES (%s, %s, %s);"
                    cur.execute(insert_sql, (user_id, post_id, comment_id))
                    status = True
            conn.commit()
            return status
        except pymysql.Error as e:
            conn.rollback()
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

# フォロークラス
class Follow:
    @classmethod
    def create(cls, follower_id, followed_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT IGNORE INTO follows (follower_id, followed_id) VALUES (%s, %s);"
                cur.execute(sql, (follower_id, followed_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, follower_id, followed_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM follows WHERE follower_id = %s AND followed_id = %s;"
                cur.execute(sql, (follower_id, followed_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    
    #フォロワー数をカウント
    @classmethod
    def count_followers(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT COUNT(*) AS cnt FROM follows WHERE followed_id = %s;"
                cur.execute(sql, (user_id,))
                row = cur.fetchone()
            return row["cnt"]
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    
    #フォロー数をカウント
    @classmethod
    def count_follows(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT COUNT(*) AS cnt FROM follows WHERE follower_id = %s;"
                cur.execute(sql, (user_id,))
                row = cur.fetchone()
            return row["cnt"]
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    
    #フォロー一覧ページの表示
    @classmethod
    def get_follows(cls, user_id):
        conn = db_pool.get_conn()
        cur = conn.cursor()

        sql = "SELECT users.id, users.name FROM follows JOIN users ON follows.followed_id = users.id WHERE follows.follower_id = %s"

        cur.execute(sql, (user_id,))
        result = cur.fetchall()

        cur.close()
        db_pool.release(conn)

        return result

    #フォロワー一覧ページの表示
    @classmethod
    def get_followers(cls, user_id):
        conn = db_pool.get_conn()
        cur = conn.cursor()

        sql = "SELECT users.id, users.name FROM follows JOIN users ON follows.follower_id = users.id WHERE follows.followed_id = %s"

        cur.execute(sql, (user_id,))
        result = cur.fetchall()

        cur.close()
        db_pool.release(conn)

        return result
    
    #follower_id が followed_id をフォローしている場合
    @classmethod
    def is_following(cls, follower_id, followed_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT 1 FROM follows WHERE follower_id=%s AND followed_id=%s LIMIT 1;"
                cur.execute(sql, (follower_id, followed_id))
                return cur.fetchone() is not None
        except pymysql.Error as e:
            print(f'エラーが発生しています:{e}')
            abort(500)
        finally:
            db_pool.release(conn)

''' 
    @classmethod
    def delete(cls, like_id):
    conn = pool.get_conn()
    try:
        with conn.cursor() as cur:
            sql = "DELETE FROM likes WHERE user_id = %s AND post_id = %s;"
            cur.execute(sql, (user_id, post_id, comment_id))
        conn.commit()
    except pymysql.Error as e:
        print(f'エラーが発生しています:{e}')
        abort(500)
    finally:
        db_pool.release(conn)
'''
'''
    @classmethod
    def get_count_by_post_id(cls, id):
    pool = get_db_pool()
    conn = pool.get_conn()
    try:
        with conn.cursor() as cur:
            sql = "SELECT COUNT(*) FROM likes;"
            cur.execute(sql, )
            conn.commit
    except pymysql.Error as e:
        print(f'エラーが発生しています:{e}')
        abort(500)
    finally:
        db_pool.release(conn)
'''
