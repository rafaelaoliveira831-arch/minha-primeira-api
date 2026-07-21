from flask import Flask, jsonify, request
import os
from models import db, Tarefas
from dotenv import load_dotenv

from models import db, Alunos

load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'API com Banco de Dados funcionando!'}), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK!'}), 200


@app.route('/tarefas', methods=['POST'])
def criar_tarefas():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Nenhum dos dados foi encontrado"}), 400

    campos_obrigatorios = ["titulo", "descricao"]
    for campo in campos_obrigatorios:
        if campo not in data:
            return jsonify({"erro": f"O campo {campo} é obrigatório"}), 400

    nova_tarefa = Tarefas(
        titulo=data['titulo'],
        descricao=data['descricao'],
        concluida=data.get('concluida', False)
    )

    db.session.add(nova_tarefa)
    db.session.commit()

    return jsonify({'status': 'Tarefa criada com sucesso!'}), 201


@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    consulta = db.select(Tarefas).order_by(Tarefas.id)
    resultado = db.session.execute(consulta)
    tarefas = resultado.scalars().all()

    lista_tarefas = []
    for tarefa in tarefas:
        lista_tarefas.append({
            "id": tarefa.id,
            "titulo": tarefa.titulo,
            "descricao": tarefa.descricao,
            "concluida": tarefa.concluida
        })

    return jsonify({'lista_tarefas': lista_tarefas}), 200


@app.route('/tarefas/<int:id_tarefas>', methods=['GET'])
def buscar_tarefas_id(id_tarefas):
    tarefa = db.session.get(Tarefas, id_tarefas)

    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    # Retorna o dicionário manualmente de forma segura
    return jsonify({
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "concluida": tarefa.concluida
    }), 200


@app.route('/tarefas/<int:id_tarefas>', methods=['PUT'])
def atualizar_tarefas_id(id_tarefas):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado foi encontrado"}), 400

    campos_obrigatorios = ["titulo", "descricao", "concluida"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"Campo {campo} é obrigatorio"}), 400

    tarefa = db.session.get(Tarefas, id_tarefas)

    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    tarefa.titulo = dados['titulo']
    tarefa.descricao = dados['descricao']
    tarefa.concluida = dados['concluida']

    db.session.commit()  # Adicionado commit

    return jsonify({"mensagem": "Tarefa atualizada com sucesso!"}), 200


@app.route('/tarefas/<int:id_tarefas>', methods=['PATCH'])
def alterar_tarefa(id_tarefas):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado foi encontrado"}), 400

    tarefa = db.session.get(Tarefas, id_tarefas)

    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    if "titulo" in dados:
        tarefa.titulo = dados['titulo']
    if "descricao" in dados:
        tarefa.descricao = dados['descricao']
    if "concluida" in dados:
        tarefa.concluida = dados['concluida']

    db.session.commit()

    return jsonify({
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "concluida": tarefa.concluida
    }), 200


@app.route('/tarefas/<int:id_tarefas>', methods=['DELETE'])
def deletar_tarefa(id_tarefas):
    tarefa = db.session.get(Tarefas, id_tarefas)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    db.session.delete(tarefa)
    db.session.commit()

    return jsonify({"mensagem": "Tarefa deletada"}), 200


# ================= ROTAS DE ALUNOS =================

# 1. ROTA POST - Criar um aluno
@app.route('/alunos', methods=['POST'])
def criar_aluno():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Nenhum dado foi encontrado"}), 400

    campos_obrigatorios = ["nome", "email", "idade"]
    for campo in campos_obrigatorios:
        if campo not in data:
            return jsonify({"erro": f"O campo {campo} é obrigatório"}), 400

    novo_aluno = Alunos(
        nome=data['nome'],
        email=data['email'],
        idade=data['idade']
    )

    db.session.add(novo_aluno)
    db.session.commit()

    return jsonify({'status': 'Aluno criado com sucesso!'}), 201


# 2. ROTA GET - Listar todos os alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    consulta = db.select(Alunos).order_by(Alunos.id)
    resultado = db.session.execute(consulta)
    alunos = resultado.scalars().all()

    lista_alunos = []
    for aluno in alunos:
        lista_alunos.append({
            "id": aluno.id,
            "nome": aluno.nome,
            "email": aluno.email,
            "idade": aluno.idade
        })

    return jsonify({'lista_alunos': lista_alunos}), 200


# 3. ROTA GET por ID - Buscar um aluno específico
@app.route('/alunos/<int:id_aluno>', methods=['GET'])
def buscar_aluno_id(id_aluno):
    aluno = db.session.get(Alunos, id_aluno)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    return jsonify({
        "id": aluno.id,
        "nome": aluno.nome,
        "email": aluno.email,
        "idade": aluno.idade
    }), 200


# 4. ROTA PUT - Atualizar todos os dados do aluno
@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno_id(id_aluno):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado foi encontrado"}), 400

    campos_obrigatorios = ["nome", "email", "idade"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"Campo {campo} é obrigatório"}), 400

    aluno = db.session.get(Alunos, id_aluno)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    aluno.nome = dados['nome']
    aluno.email = dados['email']
    aluno.idade = dados['idade']

    db.session.commit()

    return jsonify({"mensagem": "Aluno atualizado com sucesso!"}), 200


# 5. ROTA PATCH - Alterar dados parciais do aluno
@app.route('/alunos/<int:id_aluno>', methods=['PATCH'])
def alterar_aluno(id_aluno):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado foi encontrado"}), 400

    aluno = db.session.get(Alunos, id_aluno)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    if "nome" in dados:
        aluno.nome = dados['nome']
    if "email" in dados:
        aluno.email = dados['email']
    if "idade" in dados:
        aluno.idade = dados['idade']

    db.session.commit()

    return jsonify({
        "id": aluno.id,
        "nome": aluno.nome,
        "email": aluno.email,
        "idade": aluno.idade
    }), 200


# 6. ROTA DELETE - Remover um aluno
@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def deletar_aluno(id_aluno):
    aluno = db.session.get(Alunos, id_aluno)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    db.session.delete(aluno)
    db.session.commit()

    return jsonify({"mensagem": "Aluno deletado com sucesso!"}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

#Criar a classe Alunos no models.py. Depois:
# - criar rotas GET para alunos
# - criar rotas GET para alunos especifico (por ID)
# - criar rotas POST para alunos
# - criar rotas PUT para alunos
# - criar rotas PATCH para alunos
# - criar rotas DELETE para alunos