from flask import Flask, jsonify, request

app = Flask(__name__)

# lista que vai guardar nossas tarefas na memoria
tarefas = []


# Rota para criar uma nova tarefa
@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    return jsonify(tarefas)


# Rota post - criar uma nova tarefa
@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    # Paga os dados enviados em formato JSON
    dados = request.get_json()

    # Cria a nova tarefa com id, titulo e status
    nova_tarefa = {
        "id": len(tarefas) + 1,
        "titulo": dados["titulo"],
        "concluida": False,
    }

    # Adicionar a tarefa na lista
    tarefas.append(nova_tarefa)
    return jsonify(nova_tarefa), 201


# Rota PUT - marcar uma tarefa como concluída
@app.route("/tarefas/<int:id>", methods=["PUT"])
def concluir_tarefa(id):
    # PERCORRE A LISTA DE TAREFAS PARA ENCONTRAR A TAREFA COM O ID ESPECIFICADO
    for tarefa in tarefas:
        if tarefa["id"] == id:
            tarefa["concluida"] = True
            #  MUDA DE FALSE PARA TRUE
            return jsonify(tarefa)
    return jsonify({"error": "Tarefa não encontrada"}), 404


# ROTA DELETE - REMOVER UMA TAREFA DA LISTA
@app.route("/tarefas/<int:id>", methods=["DELETE"])
def deletar_tarefa(id):
    # PERCOE A LISTA PROCURANDO A TAREFA COM O ID INFORMADO
    for tarefa in tarefas:
        if tarefa["id"] == id:
            tarefas.remove(tarefa)  # REMOVE A TAREFA DA LISTA
            return jsonify({"message": "Tarefa deletada com sucesso"}), 200
    return jsonify({"error": "Tarefa não encontrada"}), 404


if __name__ == "__main__":
    app.run(debug=True)
