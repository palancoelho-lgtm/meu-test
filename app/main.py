from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configura o banco de dados SQLite — vai criar um arquivo tarefas.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarefas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Cria o objeto que vai gerenciar o banco de dados
db = SQLAlchemy(app)


# Model — representa a tabela "tarefas" no banco de dados
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    concluida = db.Column(db.Boolean, default=False)


# Cria as tabelas no banco de dados se ainda não existirem
with app.app_context():
    db.create_all()


# GET — lista todas as tarefas
@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    tarefas = Tarefa.query.all()
    resultado = []
    for t in tarefas:
        resultado.append({"id": t.id, "titulo": t.titulo, "concluida": t.concluida})
    return jsonify(resultado)


# POST — cria uma nova tarefa
@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    dados = request.get_json()
    nova = Tarefa(titulo=dados["titulo"])
    db.session.add(nova)
    db.session.commit()
    return (
        jsonify({"id": nova.id, "titulo": nova.titulo, "concluida": nova.concluida}),
        201,
    )


# PUT — marca uma tarefa como concluída
@app.route("/tarefas/<int:id>", methods=["PUT"])
def concluir_tarefa(id):
    tarefa = Tarefa.query.get(id)
    if not tarefa:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    tarefa.concluida = True
    db.session.commit()
    return jsonify(
        {"id": tarefa.id, "titulo": tarefa.titulo, "concluida": tarefa.concluida}
    )


# DELETE — remove uma tarefa
@app.route("/tarefas/<int:id>", methods=["DELETE"])
def deletar_tarefa(id):
    tarefa = Tarefa.query.get(id)
    if not tarefa:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({"message": "Tarefa deletada com sucesso"}), 200


if __name__ == "__main__":
    app.run(debug=True)
