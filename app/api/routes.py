from flask import Blueprint, send_file, request, make_response, redirect, jsonify, render_template
from app.managers.filemanager import filemanager
from app.managers.ns3manager import ns3manager

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def index():
  return render_template('upload.html')

@api.route('/', methods=['POST'])
def upload():
  file = request.files['simulation']

  file_path, err = filemanager.load(file)

  if err != None:
    return jsonify({"error": "yes", "reason": why}), 400
  
  ns3manager.load(file_path)

  return render_template('upload.html')

@api.route('/run', methods=['POST'])
def run():
  content = request.json
  out, err = ns3manager.run()
  
  logs = filemanager.get_logs()

  return jsonify({
    "output": out.decode(),
    "logs": logs
  })

@api.route('/trace', methods=['POST'])
def trace():
  content = request.json

  if 'name' not in content:
    return jsonify({}), 400
  
  file = filemanager.get_file(content['name'])
  if file is None:
    return jsonify({}), 204

  return send_file(file)

@api.route('/tracejson', methods=['POST'])
def tracejson():
  content = request.json

  print(content)
  file = filemanager.save_json(content)
  if file is None:
    return jsonify({}), 204
  
  ns3manager.load(file)
  return run()