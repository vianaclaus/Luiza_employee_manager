from flask import Flask, render_template, jsonify, request, url_for
import json
import time


app = Flask(__name__)

#função que permite abrir o arquivo json(database), reescrevê-lo e salvar
def save_db(data):
    with open("data.json", 'w') as outfile:
        json.dump(data, outfile)

#função que permite abrir o arquivo json(database) e retornar o conteúdo do arquivo
def read_db():
    with open("data.json", "r") as json_file:
        datafile = json.load(json_file)
    return datafile

#função que cria um id para cada funcionário(a)	com base no timestamp atual
def create_id():
	return int(str(time.time())[4:-8])

#função que permite inserir um funcionário(a) novo(a) no sistema ou excluir, retorna a página renderizada com as informações atualizadas
@app.route('/index', methods=['GET', 'POST'])
def index():
	data = read_db()	
	if request.method == 'POST':
		if request.form.get('delete'):
			employees = []
			for element in data:
				if len(data)==1 and int(request.form['delete']) == element['id']:
					employees = []
					save_db(employees)

				elif int(request.form['delete']) != element['id']:
					employees += [element]
					save_db(employees)	
				else:
					employees += []	
					save_db(employees)
			return render_template('index.html', employees=employees)	
			
		data += [{
			'id': create_id(), 
			'name': request.form['name'],
			'email': request.form['email'],
			'department': request.form['department']
		}]

		save_db(data)

		return render_template('index.html', employees=data)

	return render_template('index.html', employees=data)

#rota que vai retornar a lista atual de funcionários cadastrados via url
@app.route('/index2')	
def index2():
	data = read_db()
	return render_template('index2.html', employees=data)

#rota que vai trazer os dados dos funcionários em formato json via url
#exemplo: http://localhost:5000/api
@app.route('/api')
def api():
    data = read_db()
    return jsonify(data)

#rota que vai excluir algum funcionário do sistema via url
@app.route('/api/delete/<employee_id>')
def api_delete(employee_id):
	data = read_db()
	employees = []
	for employee in data:
		if len(data) == 1 and str(employee['id']) == employee_id:
			employees = []
			save_db(employees)
		elif str(employee['id']) != employee_id:
			employees += [employee]
		save_db(employees)
		return jsonify(employees)			
			
#rota que vai adicionar um funcionário novo via url	
# exemplo: http://localhost:5000/api/add?name=Carol&email=carol@luizalabs.com&department=vendas	
@app.route('/api/add', methods=['GET', 'POST'])
def api_add():
	data = read_db()
	identifier = create_id()
	data += [
		{
			'id': identifier,
			'name': request.args['name'],
			'email': request.args['email'],
			'department': request.args['department']
		}
	]
	save_db(data)
	return jsonify(data)
