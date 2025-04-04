# api de lancamento de produtos com sqlite3 e flask
from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

def init_db():
    if not os.path.exists('produtos.db'):
        conn = sqlite3.connect('produtos.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT, 
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

@app.route('/produtos', methods=['POST'])
def add_produto():
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
    
    if not all([nome, descricao, preco, quantidade, preco_real, desconto, tag, imge_url, categoria]):
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

@app.route('/cad', methods=['GET'])
def get_produtos():
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
    init_db()
    app.run(debug=True)
