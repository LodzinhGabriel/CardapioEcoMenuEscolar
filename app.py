from flask import (Flask, render_template, request)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'meu_segredo_super_seguro'  # Usado para sessão
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Caminho do banco
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False)

class Calendario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    anexo = db.Column(db.String(100), nullable=False)

class Desperdicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)
    qtdAlunos = db.Column(db.Integer, nullable=False)
    sobras = db.Column(db.Float, nullable=False)
    comidaFeita = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET'])
def pagina_incial():
    return render_template("paginainicial.html")

@app.route("/aluno")
def aluno():
    return render_template("homealuno.html")

@app.route("/cadastrarse")
def cadastrarse():
    return render_template("cadastrarse.html")

@app.route("/nutri")
def nutri():
    return render_template("homenutri.html")

@app.route("/cardapio")
def cardapio():
    return render_template("")

@app.route("/cardapioadm")
def cardapioadm():
    return render_template("cardapioadm.html")

@app.route("/calendario")
def calendario():
    return render_template("calendario.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

