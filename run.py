from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Livro(db.Model):
    __tablename__ = "LIVROS"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)
    imagem_url = db.Column(db.String(255), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return "📚 Bem-vindo à API de Livros! Doe e descubra novos livros! 📖"


@app.route('/doar', methods=['POST'])
def doar_livro():
    data = request.json
    if not all(key in data for key in ["titulo", "categoria", "autor", "imagem_url"]):
        return jsonify({"erro": "Todos os campos são obrigatórios!"}), 400

    novo_livro = Livro(
        titulo=data["titulo"],
        categoria=data["categoria"],
        autor=data["autor"],
        imagem_url=data["imagem_url"]
    )

    db.session.add(novo_livro)
    db.session.commit()

    return jsonify({"mensagem": "Livro cadastrado com sucesso!"}), 201


@app.route('/livros', methods=['GET'])
def listar_livros():
    livros = Livro.query.all()
    return jsonify([{
        "id": livro.id,
        "titulo": livro.titulo,
        "categoria": livro.categoria,
        "autor": livro.autor,
        "imagem_url": livro.imagem_url
    } for livro in livros])


if __name__ == "__main__":
    app.run(debug=True)
