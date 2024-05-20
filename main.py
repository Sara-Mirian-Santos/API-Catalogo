import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
from auth import auth_required

@app.route('/criar', methods=['POST'])
def adicionar_produto():
    try:        
        _json = request.json
        _produto = _json['produto']
        _tamanho = _json['tamanho']
        _sabor = _json['sabor']
        _quantidade = _json['quantidade']	
        if _produto and _tamanho and _sabor and _quantidade and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO catalogo (produto, tamanho, sabor, quantidade) VALUES(%s, %s, %s, %s)"
            bindData = (_produto, _tamanho, _sabor, _quantidade)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Produto adicionado com sucesso!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
     
@app.route('/busca', methods=['GET'])
@auth_required
def buscar():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, produto, tamanho, sabor, quantidade FROM catalogo")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close() 

@app.route('/busca_produto/<int:id>')
def buscar_produtos(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, produto, tamanho, sabor, quantidade FROM catalogo WHERE id =%s", id)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/update', methods=['PUT'])
def atualizar_produto():
    try:
        _json = request.json
        _id = _json['id']
        _produto = _json['produto']
        _tamanho = _json['tamanho']
        _sabor = _json['sabor']
        _quantidade = _json['quantidade']
        if _produto and _tamanho and _sabor and _quantidade and _id and request.method == 'PUT':
            sqlQuery = "UPDATE catalogo SET produto=%s, tamanho=%s, sabor =%s, quantidade=%s WHERE id=%s"
            bindData = (_produto, _tamanho, _sabor, _quantidade, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Atualizado com sucesso!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/produtos/<id>', methods=['DELETE'])
def deletar_produto(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM catalogo WHERE id =%s", (id,))
		conn.commit()
		respone = jsonify('Deletado com sucesso!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
        
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()