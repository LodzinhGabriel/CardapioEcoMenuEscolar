from flask import (Flask, render_template, request, redirect, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'meu_segredo_super_seguro'  # Usado para sessão
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Caminho do banco
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, nome, tipo, email, password):
        self.nome = nome
        self.tipo = tipo
        self.email = email
        self.password = password


class Meta(db.Model):
    __tablename__ = 'meta'

    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False)

    def __init__(self, ano, valor):
        self.ano = ano
        self.valor = valor
        

class Calendario(db.Model):
    __tablename__ = 'calendario'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    anexo = db.Column(db.BLOB, nullable=False)

    def __init__(self, data, anexo):
        self.data = data
        self.anexo = anexo

class Desperdicio(db.Model):
    __tablename__ = 'desperdicio'

    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)
    qtdAlunos = db.Column(db.Integer, nullable=False)
    sobras = db.Column(db.Float, nullable=False)
    comidaFeita = db.Column(db.Float, nullable=False)

    def __init__(self, total, qtdAlunos, sobras, comidaFeita):
        self.total = total
        self.qtdAlunos = qtdAlunos
        self.sobras = sobras
        self.comidaFeita = comidaFeita

class Voto(db.Model):
    __tablename__ = 'voto'

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.relationship('Usuario', back_populates='voto')
    votoenquete = db.relationship('VotoEnquete', back_populates='voto')
    opcao = db.relationship('Opcao', back_populates='voto')

    def __init__(self, usuario, votoenquete, opcao):
        self.usuario = usuario
        self.votoenquete = votoenquete
        self.opcao = opcao
    

class VotoEnquete(db.Model):
    __tablename__ = 'votoenquete'

    id = db.Column(db.Integer, primary_key=True)
    enquete = db.relationship('Enquete', back_populates='votoenquete')
    voto = db.relationship('Voto', back_populates='votoenquete')

    def __init__(self, enquete, voto):
        self.enquete = enquete
        self.voto = voto

class Opcao(db.Model):
    __tablename__ = 'opcao'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    opcaoenquete = db.relationship('OpcaoEnquete', back_populates='opcao')

    def __init__(self, nome, opcaoenquete):
        self.nome = nome
        self.opcaoenquete = opcaoenquete

class OpcaoEnquete(db.Model):
    __tablename__ = 'opcaoenquete'

    id = db.Column(db.Integer, primary_key=True)
    enquete = db.relationship('Enquete', back_populates='opcaoenquete')
    opcao = db.relationship('Opcao', back_populates='opcaoenquete')

    def __init__(self, enquete, opcao):
        self.enquete = enquete
        self.opcao = opcao
        
    
class Enquete(db.Model):
    __tablename__ = 'enquete'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(20), nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    votoenquete = db.relationship('Votos', back_populates='enquete')
    opcaoenquete = db.relationship('Votos', back_populates='enquete')

    def __init__(self, titulo, data_inicio, data_fim, votoenquete, opcaoenquete):
        self.titulo = titulo
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.votoenquete = votoenquete
        self.opcaoenquete = opcaoenquete



with app.app_context():
    db.create_all()

@app.route("/", methods=['GET'])
def pagina_incial_get():
    funcionario = Usuario.query.filter_by(email='funcionario@portalsesisp.org.br').first()
    aluno = Usuario.query.filter_by(email='aluno@portalsesisp.org.br').first()

    if not funcionario:
        funcionario = Usuario(nome='funcionario', tipo='funcionario', email='funcionario@portalsesisp.org.br', password='funcionario')
        db.session.add(funcionario)
        db.session.commit()
        
    if not aluno:
        aluno = Usuario(nome='aluno', tipo='aluno', email='aluno@portalsesisp.org.br', password='aluno')
        db.session.add(aluno)
        db.session.commit()

    return render_template("paginainicial.html")

@app.route("/", methods=['POST'])
def pagina_inicial_post():
    email = request.form.get("email")
    senha = request.form.get("senha")

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return render_template("login.html", erro="Usuário não encontrado.")
    
    if not bcrypt.check_password_hash(usuario.senha, senha):
        return render_template("login.html", erro="Senha incorreta.")

    session["usuario_id"] = usuario.id

    if usuario.tipo == "aluno":
        return redirect(url_for("aluno"))
    if usuario.tipo == "funcionario":
        return redirect(url_for("nutri"))

@app.route("/aluno")
def aluno():
    if not session["usuario_id"]:
        return redirect(url_for(""))
    
    usuario = Usuario.query.get(session["usuario_id"])

    if not usuario.tipo == "aluno":
        session["usuario_id"] == None
        return redirect(url_for(""))

    return render_template("homealuno.html", usuario=usuario)

@app.route("/cadastrarse")
def cadastrarse():
    return render_template("cadastrarse.html")

@app.route("/nutri")
def nutri():
    if not session["usuario_id"]:
        return redirect(url_for(""))
    
    usuario = Usuario.query.get(session["usuario_id"])

    if not usuario.tipo == "funcionario":
        session["usuario_id"] == None
        return redirect(url_for(""))

    return render_template("homenutri.html", usuario=usuario)

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

