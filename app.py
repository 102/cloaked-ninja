from flask import Flask, request, Response, send_from_directory, jsonify, redirect
import os
from json import JSONDecoder
import subprocess
import stat
import shutil
import threading
from config import *
from functools import wraps
from models import ProjectManager

app = Flask(__name__, static_url_path='')
DEFAULT_DIR = os.getcwd()
pm = ProjectManager()

def check_auth(username, password):
  return username == 'admin' and password == 'admin'

def authenticate():
  return Response(
    'Unauthorized',
    401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'}
  )

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
      return authenticate()
    return f(*args, **kwargs)
  return decorated

@app.route('/', defaults={'path': 'index.html'})
@app.route("/<path:path>")
@requires_auth
def serve_static(path):
    return send_from_directory('static', path)

@requires_auth
@app.route('/projects.json')
def projects_list():
  return pm.projects_list()
 
@app.route('/edit/<pname>/<fname>', methods=['POST'])
@requires_auth
def edit(pname, fname):
  data = JSONDecoder().decode(request.data)['content']
  pm.edit_file(pname, fname, data)
  return 'success'

@requires_auth
@app.route('/make/<pname>')
def make_project(pname):
  pm.make_project(pname)
  return redirect('/')
    
@requires_auth
@app.route('/run/<pname>', methods=['GET', 'POST'])
def run_project(pname):
  filename = 'run'
  try: filename = JSONDecoder().decode(request.data)['filename']
  except: pass
  print 'filename is {0}'.format(filename)
  pm.run_project(pname, filename)
  return redirect('/')
    
@requires_auth
@app.route('/delete-file/<pname>/<fname>')
def delete_file(pname, fname):
  pm.delete_file(pname, fname)
  return redirect('/')
    
@requires_auth
@app.route('/add-file/<pname>/<fname>')
def add_file(pname, fname):
  pm.add_file(pname, fname)
  return redirect('/')
    
@requires_auth
@app.route('/delete/<pname>')
def delete_project(pname):
  pm.delete(pname)
  return redirect('/')

@requires_auth
@app.route('/add/<pname>')
def add_project(pname):
  pm.create(pname)  
  return redirect('/')

@app.route('/<pname>/<fname>', methods=['POST', 'DELETE', 'PATCH'])
def files(pname, fname):
  if request.method == 'POST':
    pm.add_file(pname, fname)
    return 'File {0} was created'.format(fname)
  if request.method == 'DELETE':
    pm.delete_file(pname, fname)
    return 'File {0} was deleted'.format(fname)
  if request.method == 'PATCH':
    data = JSONDecoder().decode(request.data)['content']
    pm.edit_file(pname, fname, data)
    return 'File {0} was edited'.format(fname)
  abort(400)


@app.route('/<pname>', methods=['POST', 'DELETE'])
def projects(pname):
  if request.method == 'POST':
    pm.create(pname)
    return 'Project {0} was created'.format(pname)
  if request.method == 'DELETE':
    pm.delete(pname)
    return 'Project {0} was deleted'.format(pname)
  abort(400)
