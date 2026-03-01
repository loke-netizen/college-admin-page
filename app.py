from flask import Flask,render_template,request
app=Flask(__name__)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/homepage", methods=["POST"])
def home():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return render_template("index.html")
    else:
        return render_template("login.html", error="Invalid Username or Password")

if __name__=="__main__":
    app.run(debug=True)