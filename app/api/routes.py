from flask import Blueprint, send_file, request, make_response, redirect, jsonify, render_template
from app.managers.filemanager import filemanager
from app.managers.ns3manager import ns3manager
from app.managers.security import validate_scenario

api = Blueprint('api', __name__)

@api.route('/isalive')
def isalive():
  return jsonify({
    "error": False,
    "isalive": True
  })


@api.route('/trace', methods=['GET'])
def trace():
  if 'name' not in request.args:
    return jsonify({
      "error": True,
      "message": "File not specified"
    }), 400

  name = request.args.get('name')

  file = filemanager.get_file(name)
  if file is None:
    return jsonify({
      "error": True,
      "message": "pcap not found"
    }), 204

  return send_file(file)


@api.route('/tracejson', methods=['POST'])
@validate_scenario
def tracejson():
  content = request.json
  file = filemanager.save_json(content)
  if file is None:
    return jsonify({
      "error": True,
      "message": "could not save scenario."
    }), 204
  
  ns3manager.load(file)
  
  out, err = ns3manager.run()
  
  logs = filemanager.get_logs()

  return jsonify({
    "error": False,
    "output": out,
    "logs": logs
  })