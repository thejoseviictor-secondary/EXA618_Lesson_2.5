from flask import Flask, request, render_template, make_response, redirect, session
from datetime import timedelta
import os
from dotenv import load_dotenv

app = Flask(__name__)

app.secret_key = os.getenv("APP_SECRET_KEY")

default_username = os.getenv("USERNAME")
default_password = os.getenv("PASSWORD")

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

@app.route("/")
def home():
    name = request.cookies.get("name")

    if not name:
        name = "."

    counter = request.cookies.get("counter")

    if counter:
        counter = int(counter) + 1
    else:
        counter = 1

    resp = make_response(
        render_template(
            "counter.html",
            name=name,
            counter=counter
        )
    )

    resp.set_cookie("counter", str(counter), max_age=60*60)

    return resp

@app.route("/nome/<name>")
def save_name(name):
    resp = make_response(redirect("/"))
    resp.set_cookie("name", name, max_age=60*60)
    return resp

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username == default_username and password == default_password:
        session["username"] = username
        return redirect("/perfil")
    
    return "Credenciais Inválidas!"

@app.route("/perfil")
def perfil():
    if "username" not in session:
        return redirect("/login")

    return f"""
    <h1>Perfil</h1>
    <p>Usuário logado: {session["username"]}</p>
    <a href="/logout">Sair</a>
    """

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
