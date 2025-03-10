from flask import (Flask, render_template, request)

app = Flask(__name__)

@app.route("/")
def pagina_incial():
    return render_template("paginainicial.html")
