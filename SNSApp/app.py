from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")

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

# posts.html
@app.get("/posts")
def posts_view():
    return render_template("post/posts.html", posts=posts)

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
