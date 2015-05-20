from flask import Flask, request, send_from_directory, jsonify, redirect
import os
from json import JSONDecoder
import subprocess
import stat
import shutil
import threading
from config import *

app = Flask(__name__, static_url_path='')

def readfile(path):
    with open(path, 'r') as content_file:
        content = content_file.read()
    return content
    
def writefile(path, string):
    with open(path, 'w+') as content_file:
        content_file.write(string)
        print 'file ' + path + ' was changed'

@app.route('/', defaults={'path': 'index.html'})
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/projects.json')
def projects_list():
    os.chdir(DEFAULT_DIR)
    projects = os.listdir(PROJECTS_FOLDER)
    response = {'projects':[]}
    for project in projects:
        _fls = os.listdir(PROJECTS_FOLDER + '/' + project)
        files = []
        for fl in _fls:
            filepath = PROJECTS_FOLDER + '/' + project + '/' + fl
            if not (stat.S_IXUSR & os.stat(filepath)[stat.ST_MODE]):
                content = readfile(filepath)
                files.append({
                    'name': fl,
                    'content': content
                })
            else:
				files.append({
					'name': fl,
					'content': '###executable'
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

def make_async(pname):
    print pname
    prev_dir = os.getcwd()
    try:
        os.chdir(prev_dir + '/' + PROJECTS_FOLDER + '/' + pname)
        output = subprocess.check_output(["make", "all"])
    except: pass
    finally: os.chdir(prev_dir)

@app.route('/make/<pname>')
def make_project(pname):
    t = threading.Thread(target=make_async, args=(pname,))
    t.start()
    return redirect('/')
    
@app.route('/run/<pname>', methods=['GET', 'POST'])
def run_project(pname):
    filename = 'run'
    try: filename = JSONDecoder().decode(request.data)['filename']
    except: pass
    prev_dir = os.getcwd()
    try:
        os.chdir(prev_dir + '/' + PROJECTS_FOLDER + '/' + pname)
        output = subprocess.check_output("./" + filename, shell=True)
        writefile(os.getcwd() + '/output', output)
    except: pass
    finally: os.chdir(prev_dir)
    return redirect('/')
    
@app.route('/delete-file/<pname>/<fname>')
def delete_file(pname, fname):
    prev_dir = os.getcwd()
    try:
        os.chdir(prev_dir + '/' + PROJECTS_FOLDER + '/' + pname)
        os.remove(fname)
    except: pass
    finally: os.chdir(prev_dir)
    return redirect('/')
    
@app.route('/add-file/<pname>/<fname>')
def add_file(pname, fname):
    prev_dir = os.getcwd()
    try:
        os.chdir(prev_dir + '/' + PROJECTS_FOLDER + '/' + pname)
        writefile(os.getcwd() + '/' + fname, '')
    except: pass
    finally: os.chdir(prev_dir)
    return redirect('/')
    
@app.route('/delete/<pname>')
def delete_project(pname):
    try:
        shutil.rmtree(os.getcwd() + '/' + PROJECTS_FOLDER + '/' + pname)
    except: pass
    return redirect('/')

@app.route('/add/<pname>')
def add_project(pname):
    try:
        os.mkdir(os.getcwd() + '/' + PROJECTS_FOLDER + '/' + pname)
    except: pass
    return redirect('/')
    	
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
