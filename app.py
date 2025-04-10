from flask import Flask, jsonify, request
from flask_cors import CORS  # Importação correta do CORS
import sqlite3
import os
app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

@app.route('/Produto/<int:id>', methods=['GET'])
def get_produto(id):
    # Rota para obter um produto específico pelo ID
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        produto = {
            'id': row[0],
            'nome': row[1],
            'descricao': row[2],
            'preco': row[3],
            'quantidade': row[4],
            'preco_real': row[5],
            'desconto': row[6],
            'tag': row[7],
            'imge_url': row[8],
            'categoria': row[9]
        }
        return jsonify(produto), 200
    return jsonify({'message': 'Produto não encontrado!'}), 404

@app.route('/Produto/<int:id>', methods=['PUT'])
def update_produto(id):
    # Rota para atualizar um produto pelo ID
    data = request.get_json()
    nome = data.get('nome')
    descricao = data.get('descricao')
    preco = data.get('preco')
    quantidade = data.get('quantidade')
    preco_real = data.get('preco_real')
    desconto = data.get('desconto')
    tag = data.get('tag')
    imge_url = data.get('imge_url')
    categoria = data.get('categoria')

    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE produtos
        SET nome = ?, descricao = ?, preco = ?, quantidade = ?, preco_real = ?, desconto = ?, tag = ?, imge_url = ?, categoria = ?
        WHERE id = ?
    ''', (nome, descricao, preco, quantidade, preco_real, desconto, tag, imge_url, categoria, id))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'message': 'Produto não encontrado!'}), 404
    return jsonify({'message': 'Produto atualizado com sucesso!'}), 200

@app.route('/Produto/<int:id>', methods=['DELETE'])
def delete_produto(id):
    # Rota para deletar um produto pelo ID
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'message': 'Produto não encontrado!'}), 404
    return jsonify({'message': 'Produto deletado com sucesso!'}), 200
app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

def init_db():
    # Criação do banco de dados, se não existir
    if not os.path.exists('produtos.db'):
        conn = sqlite3.connect('produtos.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_real REAL NOT NULL,
                desconto REAL NOT NULL,
                tag TEXT NOT NULL,
                imge_url TEXT NOT NULL,
                categoria TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/Cad', methods=['POST'])
def add_produto():
    # Rota para adicionar um produto
    data = request.get_json()
    nome = data.get('nome')
    descricao = data.get('descricao')
    preco = data.get('preco')
    quantidade = data.get('quantidade')
    preco_real = data.get('preco_real')
    desconto = data.get('desconto')
    tag = data.get('tag')
    imge_url = data.get('imge_url')
    categoria = data.get('categoria')
    
    # Validação para garantir que todos os campos sejam preenchidos
    if not all([nome, preco, preco_real, desconto, tag, imge_url]):
        return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400

    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO produtos (nome, descricao, preco, quantidade, preco_real, desconto, tag, imge_url, categoria)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, descricao, preco, quantidade, preco_real, desconto, tag, imge_url, categoria))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Produto adicionado com sucesso!'}), 201

@app.route('/Produtos', methods=['GET'])
def get_produtos():
    # Rota para listar os produtos
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = [
        {
            'id': row[0],
            'nome': row[1],
            'descricao': row[2],
            'preco': row[3],
            'quantidade': row[4],
            'preco_real': row[5],
            'desconto': row[6],
            'tag': row[7],
            'imge_url': row[8],
            'categoria': row[9]
        } for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(produtos), 200

if __name__ == '__main__':
    # Inicializa o banco de dados antes de iniciar o servidor
    init_db()
    # Vinculando ao host e porta correta
    port = int(os.environ.get("PORT", 5000))  # Usa a variável PORT ou padrão 5000
    app.run(host='0.0.0.0', port=port)
