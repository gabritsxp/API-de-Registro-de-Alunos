from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Definição da função de conexão com o banco de dados
def get_db_cursor():
    con = mysql.connector.connect(host='localhost', database='db_Alunos', user='root', password='123')
    if con.is_connected():
        db_info = con.get_server_info()
        print("Conectado ao servidor MySQL versão ", db_info)
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)
        return cursor

# Rota que busca todos os registros no banco de dados
@app.route('/registros', methods=['GET'])
def get_registros():
    cursor = get_db_cursor()
    cursor.execute('SELECT * FROM tabela')
    registros = cursor.fetchall()
    cursor.close()
    return jsonify(registros)

# Rota que cadastra novos registros no banco de dados
@app.route('/registros', methods=['POST'])
def post_registros():
    cursor = get_db_cursor()
    id = request.args.get('id')
    nome = request.args.get('nome')
    nota = request.args.get('nota')
    query = 'INSERT INTO tabela (id, nome, nota) VALUES (%s, %s, %s)'
    values = (id, nome, nota)
    cursor.execute(query, values)
    cursor.commit()
    cursor.close()
    return 'Registro cadastrado com sucesso!'

# Rota que exclui um registro do banco de dados
@app.route('/registros/<int:id>', methods=['DELETE'])
def delete_registro(id):
    cursor = get_db_cursor()
    query = 'DELETE FROM tabela WHERE id = %s'
    value = (id,)
    cursor.execute(query, value)
    cursor.commit()
    cursor.close()
    return 'Registro excluído com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)