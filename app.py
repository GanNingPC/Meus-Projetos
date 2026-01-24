from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///farmacia.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.nome


@app.route ('/')
def home():
    return render_template("home.html")

@app.route ('/sobre')
def sobre():
    return render_template("sobre.html")

@app.route ("/login", methods=['get', 'post'])
def login():
    if request.method == 'post':
        email = request.form.get("email")
        senha = request.form.get("senha")

        return render_template('login.html', mensagem=f"Email: {email} | Senha: {senha}")

    return render_template('login.html')

@app.route("/cadastro", methods = ['get', 'post'])
def cadastro():
    if request.method == 'post':
        nome = request.form.get('nome')
        email = request.form.get("email")
        senha = request.form.get("senha")

        return render_template('cadastro.html', mensagem = f'Usuário cadastrado: {nome} - {email}')
   
    return render_template('cadastro.html')

@app.route("/produtos", methods=["GET", "POST"])
def produtos():
    if request.method == "POST":
        nome = request.form.get("nome")
        preco = request.form.get("preco")
        estoque = request.form.get("estoque")

        novo_produto = Produto(nome=nome, preco=preco, estoque=estoque)
        db.session.add(novo_produto)
        db.session.commit()

        return redirect(url_for("produtos"))

    lista_produtos = Produto.query.all()
    return render_template("produtos.html", produtos=lista_produtos)

@app.route("/deletar/<int:id>")
def deletar(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for("produtos"))

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    produto = Produto.query.get_or_404(id)

    if request.method == "POST":
        produto.nome = request.form["nome"]
        produto.preco = request.form["preco"]
        produto.estoque = request.form["estoque"]
        db.session.commit()
        return redirect(url_for("produtos"))

    return render_template("editar.html", produto=produto)


if __name__ == "__main__":
    app.run(debug=True)

