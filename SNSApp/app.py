from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from models import User, Post, Comment, Like

app = Flask(__name__)

# login.html
@app.route("/")
def login_view():
    return render_template("auth/login.html")

# loign.signin.html
@app.get("/signin")
def signin_view():
    return render_template("auth/login.signin.html")

# login.signup.html
@app.get("/signup")
def signup_view():
    return render_template("auth/login.signup.html")

@app.post("/signin")
def signin_process():
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    return redirect(url_for("posts_view"))

# 投稿一覧ページ
@app.route("/posts", method=['GET')
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
