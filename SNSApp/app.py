from flask import Flask, render_template, request, redirect, url_for

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

# posts.html
@app.get("/posts")
def posts_view():
    return "posts page" #未完成です。

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
