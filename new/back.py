from flask import Flask, Response, request
import json
import shutil
import os

app = Flask(__name__)


base_path = os.path.dirname(os.path.realpath(__file__))
storage = os.path.join(base_path, 'box')

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

#удаление файлов и папок
@app.route('/del', methods=['DELETE'])
def delete():
	req_path = request.form ['req_path'] 
	path = os.path.join(storage, req_path)
	try:
		if os.path.isfile(path):
			os.remove(path)
		else:
			os.rmdir(path)
		return response(status=200)
	except OSError:
		return 'Error: Папка не пуста', 500

#добавление папок
@app.route('/add_dir', methods=['POST'])
def add_dir():
	new_dir = request.form['new_dir']
	try:
		os.mkdir(os.path.join(storage, new_dir))
		return Response(status=200)
	except OSError:
		return 'Error: Папка с таким именем уже существует', 500	

		
#содержимое директории
@app.route('/dir_list', methods=['GET'])
def list_dir():
    path = request.args['path']
    dirlist = os.path.join(storage, path)
    list = os.listdir(dirlist)
    json_response = json.dumps(list)
    return Response(json_response, mimetype='application/json')	


	
if __name__ == '__main__':
    app.run()