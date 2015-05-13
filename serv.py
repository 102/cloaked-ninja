from flask import Flask, request, send_from_directory, jsonify
import os
from json import JSONDecoder

app = Flask(__name__, static_url_path='')

def readfile(path):
    with open(path, 'r') as content_file:
        content = content_file.read()
    return content
    
def writefile(path, string):
    with open(path, 'w') as content_file:
        content_file.write(string)

PROJECTS_FOLDER = 'projects'

@app.route('/', defaults={'path': 'index.html'})
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/projects.json')
def projects_list():
    projects = os.listdir(PROJECTS_FOLDER)
    response = {'projects':[]}
    for project in projects:
        _fls = os.listdir(PROJECTS_FOLDER + '/' + project)
        files = []
        for fl in _fls:
            files.append({
                'name': fl,
                'content': readfile(PROJECTS_FOLDER + '/' + project + '/' + fl)
            })
        response['projects'].append({
            'name': project,
            'files': files
        })
    return jsonify(response)
    
@app.route('/edit/<pname>/<fname>', methods=['POST'])
def edit(pname, fname):
    writefile(PROJECTS_FOLDER + '/' + pname + '/' + fname, JSONDecoder().decode(request.data)['content'])
    return 'success'
	
if __name__ == "__main__":
    app.run(debug=True)
