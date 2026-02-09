from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User , Post, Comment, get_db_pool, Like

# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

csrf = CSRFProtect(app)

get_db_pool()


# ルートログインページ
@app.route("/")
def top_view():
    return render_template("auth/top.html")

# サインインページ
@app.get("/signin")
def signin_view():
    return render_template("auth/signin.html")

# サインイン処理
@app.route('/signin', methods=['POST'])
def signin_process():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    if email == '' or password == '':
        flash('メールアドレスかパスワードが空です','error')
    else:
        user = User.find_by_email(email)
        if user is None:
            flash('メールアドレスかパスワードが違います','error')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('メールアドレスかパスワードが違います','error')
            else:
                session['user_id'] = user["id"]
                return redirect(url_for('posts_view'))
    return redirect(url_for('signin_view'))
 

# サインアップページ
@app.route('/signup', methods=['GET'])
def signup_view():
    return render_template("auth/signup.html")

# サインアップ処理
@app.route('/signup',methods=['POST'])
def signup_process():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    password_confirmation = request.form.get('password_confirmation', '')

    # 空チェック
    if not name or not email or not password or not password_confirmation:
        flash("空の入力項目があります", 'error')
        return redirect(url_for('signup_view'))
    
    #パスワード一致チェック
    if password != password_confirmation:
        flash('確認用パスワードが一致していません','error')
        return redirect(url_for('signup_view'))

    #メール形式チェック
    if re.match(EMAIL_PATTERN, email) is None:
        flash('メールの形式が正しくありません','error')
        return redirect(url_for('signup_view'))

    #既存ユーザーチェック
    registered_user = User.find_by_email(email)
    if registered_user is not None:
        flash('既に登録されているメールアドレスです','error')
        return redirect(url_for('signup_view'))

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    user_id = User.create(name, email, hashed_password)

    session['user_id'] = user_id

    return redirect(url_for('posts_view'))

# プロフィールページ
@app.get("/profile/<int:user_id>")
def profile_view(user_id):
    my_user_id = session.get('user_id')
    if my_user_id is None:
        return redirect(url_for('signin_view'))
    else:
        user = User.get_user_by_id(user_id)
        posts = Post.get_by_user_id(user_id) 
        for post in posts:
            post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
            post['user_name'] = User.get_user_by_id(post['user_id'])

        return render_template("profile/profile.html",user=user,posts=posts)


# プロフィール編集ページ
@app.get("/profile/edit")
def profile_edit_view():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('signin_view'))
    else:
        user = User.get_user_by_id(user_id)
        return render_template("profile/edit.html",user=user)
    
#プロフィールの更新
@app.post("/profile/edit")
def profile_update():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("signin_view"))

    name = request.form.get("user_name", "").strip()
    introduce = request.form.get("user_introduce", "").strip()

    User.update_profile(user_id, name, introduce)
    flash("更新しました", "success")
    return redirect(url_for("profile_view", user_id=user_id))

# 投稿ページ
# 投稿一覧ページ
@app.route('/posts', methods=['GET'])
def posts_view():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('signin_view'))
    else:
        posts = Post.get_all() 
        for post in posts:
            post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
            post['user_name'] = User.get_user_by_id(post['user_id'])
            # post['like_count'] = Like.get_count_by_post_id(post['id'])
        return render_template('post/posts.html', posts=posts, user_id=user_id)

# 投稿処理
@app.route('/posts', methods=['POST'])
def posts_process():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('signin_view'))
    content = request.form.get("content","").strip()
    if content == '':
        flash('投稿内容が空です', 'error')
        return redirect(url_for("posts_view"))

    Post.create(user_id, content)
    flash('投稿が完了しました', 'success')
    return redirect(url_for('posts_view'))

# 削除処理
@app.route('/posts/<int:post_id>/delete', methods=['GET'])
def delete_post(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('signin_view'))

    post = Post.find_by_id(post_id)
    if post is None:
        abort(404)

    if post['user_id'] != user_id:
        flash('この投稿を削除することはできません', 'error')
        return redirect(url_for('posts_view'))

    Post.delete(post_id)
    flash('投稿が削除されました', 'success')
    return redirect(url_for('posts_view'))

# 投稿詳細ページの表示
@app.get("/posts/<int:post_id>")
def posts_detail_view(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('signin_view'))
    post = Post.find_by_id(post_id)
    if post is None:
        abort(404)
        
    post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
    post['user_name'] = User.get_user_by_id(post['user_id'])

    comments = Comment.get_by_post_id(post_id)
    for comment in comments:
        comment['created_at'] = comment['created_at'].strftime('%Y-%m-%d %H:%M')
        comment['user_name'] = User.get_user_by_id(comment['user_id'])

    return render_template('post/post_detail.html', post=post, comments = comments, user_id=user_id)

# コメント処理
@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('posts_view'))
    content = request.form.get('content', '').strip()
    if content == '':
        flash('コメント内容が空です','error')
        return redirect(url_for('posts_detail_view', post_id=post_id))
    Comment.create(user_id, post_id, content)
    flash('コメントの投稿が完了しました','success')
    return redirect(url_for('posts_detail_view', post_id=post_id))

# いいね処理
@app.route('/like', methods=['POST'])
def like():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('signin_view'))

@app.errorhandler(400)
def bad_request(error):
    return render_template('error/400.html'), 400

@app.errorhandler(404)
def not_found(error):
    return render_template("error/404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("error/500.html"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

