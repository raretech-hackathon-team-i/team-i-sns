from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
import os

from models import User , Post, Comment, get_db_pool, Like

# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")
csrf = CSRFProtect(app)

posts = []

# top.html
@app.route("/")
def top_view():
    return render_template("auth/top.html")

# signin.html
@app.get("/signin")
def signin_view():
    return render_template("auth/signin.html")

@app.post("/signin")
def signin_process():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    if not email or not password:
        flash("メールアドレスとパスワードを入力してください")
        return redirect(url_for("signin_view"))

    return redirect(url_for("posts_view"))

# signup.html
@app.get("/signup")
def signup_view():
    return render_template("auth/signup.html")

@app.post("/signup")
def signup_process():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    
    if not email or not password:
        flash("未入力の項目があります")
        return redirect(url_for("signup_view"))

    return redirect(url_for("posts_view"))


    #既存ユーザーチェック
    registered_user = User.find_by_email(email)
    if registered_user is not None:
        flash('既に登録されているメールアドレスです','error')
        return redirect(url_for('signup_view'))

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    user_id = User.create(name, email, hashed_password)

    session['user_id'] = user_id

    return redirect(url_for('posts_view'))


# 投稿ページ
# 投稿一覧ページ
@app.route("/posts", method=['GET'])
def posts_view():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('signin_view'))
    else:
        posts = Post.get_all() 
        for post in posts:
            post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
            post['user_name'] = User.get_name_by_id(post['user_id'])
            post['like_count'] = Like.get_count_by_post_id(post['id'])
        return render_template('post/posts.html', posts=posts, user_id=user_id)

@app.post("/posts")
def posts_process():
    content = request.form.get("content","").strip()
    if content:
        posts.append(content)
    return redirect(url_for("posts_view"))

# posts.detail_view
@app.get("/posts/<int:post_id>")
def posts_detail_view(post_id):
    if post_id < 0 or post_id >= len(posts):
        return "Not Found", 404

    post = {"id": post_id, "body": posts[post_id], "comments": []}
    return render_template("post/post_detail.html", post=post)

@app.post("/posts/<int:post_id>/comment")
def comment_process(post_id):
    comment = request.form.get("comment", "").strip()
    return redirect(url_for("posts_detail_view", post_id=post_id))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
