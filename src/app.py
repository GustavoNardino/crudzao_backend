from flask import Flask, jsonify, request
from mariadb import mariadb

from config import config

app=Flask(__name__)

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'user',
    'password': '12345',
    'database': 'crudzao'
}

crud_connection = mariadb.connect(**db_config)        

@app.route('/listusers', methods=['GET'])
def list_users():
    try:
        cursor = crud_connection.cursor()
        sql = "SELECT id, nome, email, created_at FROM cadastro"
        cursor.execute(sql)
        data = cursor.fetchall()
        crud_users = []
        for u in data:
            user = {'id': u[0], 'nome': u[1], 'email': u[2], 'created_at': u[3]}
            crud_users.append(user)
        return jsonify({'crud_users': crud_users, 'mensagem':'lista de usuários'})
    except Exception as ex:
        return jsonify({'mensagem':'erro'})
    
def page_not_found(error):
    return "<h1>Página não encontrada</h1>", 404

@app.route('/listusers/<id>', methods=['GET'])
def show_user(id):
    try:
        cursor = crud_connection.cursor()
        sql = "SELECT id, nome, email, created_at FROM cadastro WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data != None:
            user = {'id': data[0], 'nome': data[1], 'email': data[2], 'created_at': data[3]}
            return jsonify({'user': user, 'mensagem':'lista de usuários'})
        else:
            return jsonify({'mensagem':'curso não encontrado'})
    except Exception as ex:
        return jsonify({'mensagem':'erro'})

@app.route('/adduser', methods=['POST'])
def add_user():
    try:
        cursor = crud_connection.cursor()
        sql = """INSERT INTO cadastro (nome, email) VALUES ('{0}','{1}')""".format(request.json['nome'],request.json['email'],)
        cursor.execute(sql)
        crud_connection.commit()
        return jsonify({'mensagem':'usuário cadastrado'})
    except Exception as ex:
        return jsonify({'mensagem':'erro'})

@app.route('/removeuser/<id>', methods=['DELETE'])
def remove_user(id):
    try:
        cursor = crud_connection.cursor()
        sql = "DELETE FROM cadastro WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        crud_connection.commit()
        return jsonify({'mensagem':'usuário removido'})
    except Exception as ex:
        return jsonify({'mensagem':'erro'})

@app.route('/modifyuser/<id>', methods=['PUT'])
def modify_user(id):
    try:
        cursor = crud_connection.cursor()
        sql = "UPDATE cadastro SET nome = '{0}', email = '{1}', id = '{2}'".format(request.json['nome'],request.json['email'], id)
        cursor.execute(sql)
        crud_connection.commit()
        return jsonify({'mensagem':'usuário modificado'})
    except Exception as ex:
        return jsonify({'mensagem':'erro'})

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()