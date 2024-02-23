import pymysql
from app import app
from config import mysql
from flask import jsonify, request
from datetime import datetime


@app.route('/Adicionar', methods=['POST'])
def CriarUsuario():
    try:
        _json = request.json
        _Nome = _json.get('NM_USUARIO', '')
        _Dt_Nascimento = _json.get('DT_NASCIMENTO', '')
        _EstadoCivil = _json.get('ESTADO_CIVIL', '')
        _Cpf = _json.get('NR_CPF', '')
        _Endereco = _json.get('ENDERECO', '') 

        StringConection = mysql.connect()
        cursor = StringConection.cursor(pymysql.cursors.DictCursor)

        if not _Nome or not _Dt_Nascimento:
            return jsonify({'message': 'Existem campos incompletos, por gentileza preencha corretamente'}), 400
        
        if datetime.strptime(_Dt_Nascimento, '%Y-%m-%d') > datetime.now():
            return jsonify({'message': 'Data de nascimento inválida'}), 400

        if (len(_Cpf) != 11):
            return jsonify({'message': 'CPF invalido, coloque os campos sem pontuações'}), 400
        
        sqlQuery = "INSERT INTO TB_PESSOAS(NM_USUARIO, DT_NASCIMENTO, ENDERECO, NR_CPF, ESTADO_CIVIL) VALUES(%s, %s, %s, %s, %s)"
        bindData = (_Nome, _Dt_Nascimento, _Endereco, _Cpf, _EstadoCivil)
        cursor.execute(sqlQuery, bindData)
        StringConection.commit()
        
        response = jsonify('Usuário adicionado com sucesso!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return jsonify({'message': 'Erro ao adicionar usuário'}), 500
    finally:
        cursor.close() 
        StringConection.close()
     
@app.route('/Listar', methods=['GET'])
def ListarUsuarios():
    try:
        StringConection = mysql.connect()
        cursor = StringConection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM TB_PESSOAS")    
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        StringConection.close() 

@app.route('/Editar', methods=['PUT'])
def EditarUsuario():
    try:
        _json = request.json
        _Id = _json['ID_USUARIO']
        _Nome = _json['NM_USUARIO']
        _Dt_Nascimento = _json['DT_NASCIMENTO']
        _EstadoCivil = _json['ESTADO_CIVIL']
        _Cpf = _json['NR_CPF']
        _Endereco = _json['ENDERECO']
        if _Nome and _Dt_Nascimento and _Cpf and _EstadoCivil and _Endereco and _Id and request.method == 'PUT':			
            sqlQuery = "UPDATE TB_PESSOAS SET NM_USUARIO=%s, ESTADO_CIVIL=%s, DT_NASCIMENTO=%s, NR_CPF=%s, ENDERECO=%s WHERE ID_USUARIO=%s"
            bindData = (_Nome, _EstadoCivil, _Dt_Nascimento, _Cpf, _Endereco, _Id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Usuario atualizado com sucesso!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()      

@app.route('/Excluir/<int:id>', methods=['DELETE'])
def delete_emp(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM TB_PESSOAS WHERE ID_USUARIO = %s", (id,))
		conn.commit()
		response = jsonify('Usuário excluído com sucesso!')
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
		return jsonify({'message': 'Erro ao excluir usuário'}), 500
	finally:
		cursor.close() 
		conn.close()
              
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Usuario não encontrado... ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == '__main__':
    app.debug = True
    app.run()
