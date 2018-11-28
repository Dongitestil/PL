from flask import Flask, Response, send_from_directory, request
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
@app.route('/ls', methods=['GET'])
def list_dir():
    path = request.args['path']
    dirlist = os.path.join(storage, path)
    list = os.listdir(dirlist)
    response = {'dirs': [], 'files': []}

    for name in list:
        full_path = os.path.join(dirlist, name)

        if os.path.isdir(full_path):
            response['dirs'].append(name)
        else:
            response['files'].append(name)

    json_response = json.dumps(response)
    return Response(json_response, mimetype='application/json')	
	
	
		
@app.route('/download', methods=['GET'])
def download_file():
    file = request.args['file']
    path = os.path.join(storage, file)
    return send_from_directory('box', path, as_attachment=True)

	
if __name__ == '__main__':
    app.run()