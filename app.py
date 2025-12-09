from flask import (Flask, render_template, request, redirect, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import jsonify

app = Flask(__name__)

# ===================================== BANCO DE DADOOS ===========================================

app.config['SECRET_KEY'] = 'meu_segredo_super_seguro'  # Usado para sessão
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Caminho do banco
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    def __init__(self, nome, tipo, email, senha):
        self.nome = nome
        self.tipo = tipo
        self.email = email
        self.senha = senha

class Calendario(db.Model):
    __tablename__ = 'calendario'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    anexo = db.Column(db.String(100), nullable=False)

    def __init__(self, data, anexo):
        self.data = data
        self.anexo = anexo

class Desperdicio(db.Model):
    __tablename__ = 'desperdicio'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    turma = db.Column(db.String, nullable=False)
    qtdAlunos = db.Column(db.Integer, nullable=False)
    sobras = db.Column(db.Float, nullable=False)
    comidaFeita = db.Column(db.Float, nullable=False)

    def __init__(self, data, turma, qtdAlunos, sobras, comidaFeita):
        self.data = data
        self.turma = turma
        self.qtdAlunos = qtdAlunos
        self.sobras = sobras
        self.comidaFeita = comidaFeita

class Voto(db.Model):
    __tablename__ = 'voto'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    semana = db.Column(db.Integer, nullable=False)
    opcao = db.Column(db.Integer, nullable=False)

    def __init__(self, id_usuario, semana, votoenquete, opcao):
        self.id_usuario = id_usuario
        self.semana = semana
        self.votoenquete = votoenquete
        self.opcao = opcao

with app.app_context():
    db.create_all()

# ===================================== FUNCÕES BASE ===========================================

def verificarEntrada(temp: str, tipo: str):
    if not session.get('usuario_id'):
        return redirect(url_for("pagina_inicial"))
    
    usuario = Usuario.query.get(session["usuario_id"])

    if tipo:
        if not usuario.tipo == tipo:
            return redirect(url_for("pagina_inicial"))

    return render_template(temp, usuario=usuario)


# ===================================== SITE PRINCIPAL ===========================================

# --------------------------------------------------------------------------------- Página Inicial

@app.route("/", methods=['GET', 'POST'])
def pagina_inicial():
    funcionario = Usuario.query.filter_by(email='funcionario@portalsesisp.org.br').first()
    aluno = Usuario.query.filter_by(email='aluno@portalsesisp.org.br').first()

    if not funcionario:
        funcionario = Usuario(nome='funcionario', tipo='funcionario', email='funcionario@portalsesisp.org.br', senha='funcionario')
        db.session.add(funcionario)
        db.session.commit()
        
    if not aluno:
        aluno = Usuario(nome='aluno', tipo='aluno', email='aluno@portalsesisp.org.br', senha='aluno')
        db.session.add(aluno)
        db.session.commit()

    if session.get('usuario_id'):
        usuario = Usuario.query.get(session['usuario_id'])

        if usuario:
            if usuario.tipo == "aluno":
                return redirect(url_for("aluno"))
            if usuario.tipo == "funcionario":
                return redirect(url_for("nutri"))

    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        print(email, senha)

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            return render_template("paginainicial.html", erro="Usuário não encontrado.")
        
        senha_correta = bcrypt.generate_password_hash(usuario.senha).decode('utf-8')
        
        if not bcrypt.check_password_hash(senha_correta, senha):
            return render_template("paginainicial.html", erro="Senha incorreta.")

        session["usuario_id"] = usuario.id

        if usuario.tipo == "aluno":
            return redirect(url_for("aluno"))
        if usuario.tipo == "funcionario":
            return redirect(url_for("nutri"))


    return render_template("paginainicial.html")

# --------------------------------------------------------------------------------- Sair (interno)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()

    return redirect(url_for("pagina_inicial"))

# --------------------------------------------------------------------------------- Página do Aluno

@app.route("/aluno")
def aluno():
    return verificarEntrada("homealuno.html", "aluno")

# --------------------------------------------------------------------------------- Página da Nutrição

@app.route("/nutri")
def nutri():
    return verificarEntrada("homenutri.html", "funcionario")

# --------------------------------------------------------------------------------- Enquete (aluno)

@app.route("/enquete")
def enquete():
    return verificarEntrada("enquete.html", "aluno")

# --------------------------------------------------------------------------------- Envio do voto (interno, aluno)



# --------------------------------------------------------------------------------- Enquete (nutrição)

@app.route("/enquete/resultados")
def enquete_resultados():
    return verificarEntrada("enqueteadm.html", "funcionario")

# --------------------------------------------------------------------------------- Cardápio

@app.route("/cardapio")
def cardapio():
    if not session.get('usuario_id'):
        return redirect(url_for("pagina_inicial"))
    
    usuario = Usuario.query.get(session["usuario_id"])
        
    cardapios = Calendario.query.order_by(Calendario.data.desc())
    cardapioAtual = cardapios.first()
    outrosCardapios = []

    for cardapio in cardapios:
        outrosCardapios.append(cardapio)

    del outrosCardapios[0]

    print(cardapios)

    print(outrosCardapios)

    return render_template("cardapio.html", usuario=usuario, cardapio=cardapioAtual, cardapios=outrosCardapios)

# --------------------------------------------------------------------------------- Cardápio (nutrição)

@app.route("/cardapio/enviar")
def cardapioadm():
    return verificarEntrada("cardapioadm.html", "funcionario")

# --------------------------------------------------------------------------------- Envio do cardápio (interno, nutrição)

@app.route("/cardapio/enviar/upload", methods=["POST"])
def upload():
    if session.get('usuario_id'):
        usuario = Usuario.query.get(session['usuario_id'])

        if usuario:
            if not usuario.tipo == "funcionario":
                return redirect(url_for("pagina_inicial"))
            
    try:
        if "arquivo" not in request.files:
            return jsonify({"erro": "Respota do cliente vazia"}), 400

        arq = request.files["arquivo"]

        if arq.filename == "":
            return jsonify({"erro": "Nome vazio"}), 400

        data_atual = datetime.now().strftime('%Y-%m-%d')

        pasta_data = os.path.join(app.config['UPLOAD_FOLDER'], data_atual)

        os.makedirs(pasta_data, exist_ok=True)

        nome_seguro = secure_filename(arq.filename)
        caminho = os.path.join(pasta_data, nome_seguro)
        arq.save(caminho)

        calendario = Calendario(
            data=datetime.now(),
            anexo=caminho
        )

        db.session.add(calendario)
        db.session.commit()
        return jsonify({"mensagem": "Arquivo enviado com sucesso!"})
    except Exception as e:
        print(e)
        return jsonify({"erro": "Ocorreu uma falha na hora de mandar seu arquivo.", "detalhamento": str(e)}), 400
    
    

# --------------------------------------------------------------------------------- Desperdício (aluno)



# --------------------------------------------------------------------------------- Desperdício (nutrição)

@app.route("/desperdicio/enviar")
def desperdicioadm():
    return verificarEntrada("desperdicioadm.html", "funcionario")

# --------------------------------------------------------------------------------- Envio do Desperdício (interno, nutrição)



# --------------------------------------------------------------------------------- Aviso (nutrição)

@app.route("/aviso/enviar")
def editar_aviso():
    return verificarEntrada("avisoadm.html", "funcionario")

# --------------------------------------------------------------------------------- Envio do Aviso (interno, nutrição)



# --------------------------------------------------------------------------------- Sobre

@app.route("/sobre")
def sobre():
    if not session.get('usuario_id'):
        return redirect(url_for("pagina_inicial"))
    
    usuario = Usuario.query.get(session["usuario_id"])

    return render_template("sobre.html", usuario=usuario)

# --------------------------------------------------------------------------------- Paginas de apoio para erros internos

@app.errorhandler(404)
def erro404(e):
    if not session.get('usuario_id'):
        return redirect(url_for("pagina_inicial"))
    
    usuario = Usuario.query.get(session["usuario_id"])

    return render_template("erropagina.html", usuario=usuario, erro="404", descricao_erro="A pagina que você solicitou não foi encontrada. Verifique se digitou correto.")

@app.errorhandler(500)
def erro500(e):
    if not session.get('usuario_id'):
        return redirect(url_for("pagina_inicial"))
    
    usuario = Usuario.query.get(session["usuario_id"])

    return render_template("erropagina.html", usuario=usuario, erro="INTERNO (500)", descricao_erro="Ocorreu uma falha interna em nosso servidores. Aguarde mais um pouco e tente novamente.")