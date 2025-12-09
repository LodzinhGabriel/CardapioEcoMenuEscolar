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
    aviso = db.Column(db.Boolean, nullable=False)

    def __init__(self, nome, tipo, email, senha, aviso):
        self.nome = nome
        self.tipo = tipo
        self.email = email
        self.senha = senha
        self.aviso = aviso

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
    data = db.Column(db.String, nullable=False)
    divisao = db.Column(db.String, nullable=False)
    turma = db.Column(db.String, nullable=False)
    qtdAlunos = db.Column(db.Integer, nullable=False)
    comidaFeita = db.Column(db.Float, nullable=False)
    sobras = db.Column(db.Float, nullable=False)
    percentual = db.Column(db.Float, nullable=False)
    mediaAluno = db.Column(db.Float, nullable=False)

    def __init__(self, data, divisao, turma, qtdAlunos, sobras, comidaFeita, percentual, mediaAluno):
        self.data = data
        self.divisao = divisao
        self.turma = turma
        self.qtdAlunos = qtdAlunos
        self.sobras = sobras
        self.comidaFeita = comidaFeita
        self.percentual = percentual
        self.mediaAluno = mediaAluno

class Voto(db.Model):
    __tablename__ = 'voto'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    semana = db.Column(db.Integer, nullable=False)
    opcao = db.Column(db.String(15), nullable=False)

    def __init__(self, id_usuario, semana, opcao):
        self.id_usuario = id_usuario
        self.semana = semana
        self.opcao = opcao

with app.app_context():
    db.create_all()

# ===================================== DADOS AVISO ==============================================

aviso_principal = {
    "ativo": False,
    "titulo": "",
    "imagem": "",
    "mensagem": ""
}

# ===================================== FUNCÕES BASE ===========================================

def verificarEntrada(temp: str, tipo: str):
    if not session.get('usuario_id'):
        return redirect(url_for("pagina_inicial"))
    
    usuario = Usuario.query.get(session["usuario_id"])

    if not tipo == None:
        if not usuario.tipo == tipo:
            return redirect(url_for("pagina_inicial"))

    return render_template(temp, usuario=usuario, aviso=aviso_principal)

# ===================================== SITE PRINCIPAL ===========================================

# --------------------------------------------------------------------------------- Página Inicial

@app.route("/", methods=['GET', 'POST'])
def pagina_inicial():
    funcionario = Usuario.query.filter_by(email='funcionario@portalsesisp.org.br').first()
    aluno = Usuario.query.filter_by(email='aluno@portalsesisp.org.br').first()

    if not funcionario:
        funcionario = Usuario(nome='funcionario', tipo='funcionario', email='funcionario@portalsesisp.org.br', senha='funcionario', aviso=False)
        db.session.add(funcionario)
        db.session.commit()
        
    if not aluno:
        aluno = Usuario(nome='aluno', tipo='aluno', email='aluno@portalsesisp.org.br', senha='aluno', aviso=False)
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

@app.route("/enquete/voto", methods=['POST'])
def voto():
    if session.get('usuario_id'):
        usuario = Usuario.query.get(session['usuario_id'])

        if usuario:
            if not usuario.tipo == "aluno":
                return redirect(url_for("pagina_inicial"))
            
    try:
        if "dia" not in request.form:
            return jsonify({"erro": "Respota do cliente vazia"}), 400

        dia = request.form.get('dia')

        if dia == "":
            return jsonify({"erro": "Dia vazio"}), 400

        semana_atual = datetime.now().isocalendar().week

        voto = Voto(
            id_usuario = session.get('usuario_id'),
            semana = semana_atual,
            opcao = dia
        )

        db.session.add(voto)
        db.session.commit()
        return jsonify({"mensagem": "Voto enviado com sucesso!"})
    except Exception as e:
        print(e)
        return jsonify({"erro": "Ocorreu uma falha na hora de mandar seu voto.", "detalhamento": str(e)}), 400

# --------------------------------------------------------------------------------- Enquete (nutrição)

@app.route("/enquete/resultados")
def enquete_resultados():
    if session.get('usuario_id'):
        usuario = Usuario.query.get(session['usuario_id'])

        if usuario:
            if not usuario.tipo == "funcionario":
                return redirect(url_for("pagina_inicial"))
            
    votos = Voto.query.all()  
    # Cada item deve ter: usuario_id, semana, opcao

    votos_json = [
        {
            "id_usuario": v.id_usuario,
            "semana": v.semana,
            "opcao": v.opcao
        }
        for v in votos
    ]

    return render_template("enquete_resultados.html", usuario=usuario, votos=votos_json)


# --------------------------------------------------------------------------------- Cardápio

@app.route("/cardapio")
def cardapio():
    if not session.get('usuario_id'):
        return redirect(url_for("pagina_inicial"))
    
    usuario = Usuario.query.get(session["usuario_id"])
        
    cardapios = Calendario.query.order_by(Calendario.data.desc())
    cardapioAtual = cardapios.first()

    return render_template("cardapio.html", usuario=usuario, cardapio=cardapioAtual, aviso=aviso_principal)

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

@app.route("/desperdicio")
def desperdicio():
    if session.get('usuario_id'):
        usuario = Usuario.query.get(session['usuario_id'])

        if usuario:
            if not usuario.tipo == "aluno":
                return redirect(url_for("pagina_inicial"))

    # Recebe filtros da URL
    filtro_divisao = request.args.get("divisao")
    filtro_turma = request.args.get("turma")
    filtro_data = request.args.get("data")

    # Query base
    query = Desperdicio.query

    # Aplica filtros se existirem
    if filtro_divisao:
        query = query.filter_by(divisao=filtro_divisao)

    if filtro_turma:
        query = query.filter_by(turma=filtro_turma)

    if filtro_data:
        query = query.filter_by(data=filtro_data)

    # Coleta resultados
    dados = query.order_by(Desperdicio.data.desc()).all()

    # Coleta listas de divisões e turmas disponíveis (para preencher os selects)
    divisoes = sorted({d.divisao for d in Desperdicio.query.all()})
    turmas = sorted({d.turma for d in Desperdicio.query.all()})

    # Envia para o template
    return render_template(
        "desperdicio.html",
        usuario=usuario,
        dados=dados,
        divisoes=divisoes,
        turmas=turmas
    )

# --------------------------------------------------------------------------------- Desperdício (nutrição)

@app.route("/desperdicio/enviar")
def desperdicioadm():
    return verificarEntrada("desperdicioadm.html", "funcionario")

# --------------------------------------------------------------------------------- Envio do Desperdício (interno, nutrição)

@app.route("/desperdicio/enviar/upload")
def desperdicioadm_upload():
    if session.get('usuario_id'):
        usuario = Usuario.query.get(session['usuario_id'])

        if usuario:
            if not usuario.tipo == "funcionario":
                return redirect(url_for("pagina_inicial"))
    
    try:
        if "dadosCompletos" not in request.form:
            return jsonify({"erro": "Respota do cliente vazia"}), 400

        dadosCompletos = request.form.get('dadosCompletos')

        data_atual = datetime.now().strftime('%Y-%m-%d')

        desperdicio = Desperdicio(
            data = data_atual,
            divisão = dadosCompletos.divisao,
            turma = dadosCompletos.turma,
            qtdAlunos = dadosCompletos.qtdAlunos,
            sobras = dadosCompletos.sobras,
            comidaFeita = dadosCompletos.comidaFeita,
            percentual = dadosCompletos.percentual,
            mediaAluno = dadosCompletos.mediaAluno
        )

        db.session.add(desperdicio)
        db.session.commit()
        return jsonify({"mensagem": "Desperdicio enviado com sucesso!"})
    except Exception as e:
        print(e)
        return jsonify({"erro": "Ocorreu uma falha na hora de mandar seu calculo.", "detalhamento": str(e)}), 400
    

# --------------------------------------------------------------------------------- Leitura do Aviso (interno, aluno)

@app.route("/aviso/leitura", methods=['POST'])
def aviso_leitura():
    if session.get('usuario_id'):
        usuario = Usuario.query.get(session['usuario_id'])

        if usuario:
            if usuario.tipo == "aluno":
                usuario.aviso = True
                db.session.commit()
                return jsonify({"mensagem": "Aviso lido com sucesso!"})

    return jsonify({"erro": "Usuario não é aluno ou não está registrado."})

# --------------------------------------------------------------------------------- Aviso (nutrição)

@app.route("/aviso/enviar")
def editar_aviso():
    return verificarEntrada("avisoadm.html", "funcionario")

# --------------------------------------------------------------------------------- Envio do Aviso (interno, nutrição)

@app.route("/aviso/enviar/upload", methods=['POST'])
def enviar_aviso():
    if session.get('usuario_id'):
        usuario = Usuario.query.get(session['usuario_id'])

        if usuario:
            if not usuario.tipo == "funcionario":
                return redirect(url_for("pagina_inicial"))
            
    if "titulo" not in request.form:
        return jsonify({"erro": "Titulo vazio"}), 400
            
    if "imagem" not in request.files:
            return jsonify({"erro": "Imagem vazia"}), 400
    
    if "texto" not in request.form:
            return jsonify({"erro": "Texto vazio"}), 400
    
    titulo = request.form.get('titulo')
    imagem = request.files.get('imagem')
    texto = request.form.get('texto')

    if imagem.filename == "":
        return jsonify({"erro": "Nome vazio"}), 400

    data_atual = datetime.now().strftime('%Y-%m-%d')

    pasta_data = os.path.join(app.config['UPLOAD_FOLDER'], data_atual)

    os.makedirs(pasta_data, exist_ok=True)

    nome_seguro = secure_filename(imagem.filename)
    caminho = os.path.join(pasta_data, nome_seguro)
    imagem.save(caminho)
    
    aviso_principal["titulo"] = titulo
    aviso_principal["imagem"] = caminho
    aviso_principal["mensagem"] = texto

    aviso_principal["ativo"] = True

    Usuario.query.update({Usuario.aviso: False})
    db.session.commit()

    return jsonify({"mensagem": "Aviso criado com sucesso!"})

# --------------------------------------------------------------------------------- Sobre

@app.route("/sobre")
def sobre():
    return verificarEntrada("sobre.html", None)

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