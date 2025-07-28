from flask import (Flask, render_template, request)

app = Flask(__name__)

@app.route("/")
def pagina_incial():
    return render_template("paginainicial.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastrarse")
def cadastrarse():
    return render_template("cadastrarse.html")

@app.route("/calendario")
def calendario():
    return render_template("calendario.html")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")