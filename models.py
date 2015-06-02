import os
import subprocess
from config import *
import shutil
import stat
from flask import jsonify

def writefile(path, string):
  with open(path, 'w') as content_file:
    content_file.write(string)
    print 'file ' + path + ' was changed'

def readfile(path):
  with open(path, 'r') as content_file:
    content = content_file.read()
  return content

def make_async(pname):
  print pname
  prev_dir = os.getcwd()
  try:
    os.chdir( + '/' + PROJECTS_FOLDER + '/' + pname)
    output = subprocess.check_output(["make", "all"])
    print output
  except: pass
  finally: os.chdir(prev_dir)

class ProjectManager():
  def create(self, name):
    try:
      os.mkdir(os.getcwd() + '/' + PROJECTS_FOLDER + '/' + name)
    except:
      print 'Cant create project {0}'.format(name)

  def delete(self, name):
    try:
      print os.getcwd() + '/' + PROJECTS_FOLDER + '/' + name
      shutil.rmtree(os.getcwd() + '/' + PROJECTS_FOLDER + '/' + name)
    except:
      print 'Cant delete project {0}'.format(name)

  def add_file(self, project, name):
#    try:
      writefile(os.getcwd() + '/' + project + '/'  + name, '')
#    except:
#      print 'Cant add file {0} to {1} project'.format(project, name)

  def writefile(path, string):
    with open(path, 'w+') as content_file:
      content_file.write(string)
      print 'file ' + path + ' was changed'

  def readfile(path):
    with open(path, 'r') as content_file:
      content = content_file.read()
    return content

  def delete_file(self, project, name):
    try:
      os.remove(os.getcwd() + '/' + PROJECTS_FOLDER + '/' + project + '/' + name)
    except:
      print 'Cant delete file {0} from {1} project'.format(project, name)

  def edit_file(self, project, name, data):
    try:
      writefile(PROJECTS_FOLDER + '/' + project + '/' + name, data)
    except:
      print 'Cant edit file {0} from {1} project'.format(name, project)

  def projects_list(self):
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

  def make_project(self, name):
    t = threading.Thread(target=make_async, args=(name,))
    t.start()
  
  def run_project(self, projectname, exename):
    prev_dir = os.getcwd()
    try:
      os.chdir(prev_dir + '/' + PROJECTS_FOLDER + '/' + projectname)
      output = subprocess.check_output("./" + exename, shell=True)
      writefile(os.getcwd() + '/output', output)
    except: pass
    finally: os.chdir(prev_dir)

