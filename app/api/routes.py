from flask import Blueprint, send_file, request, make_response, redirect, jsonify, render_template
from app.managers.filemanager import filemanager
from app.managers.ns3manager import ns3manager
from app.managers.security import validate_scenario, validate_code

api = Blueprint('api', __name__)

@api.route('/isalive')
def isalive():
  return jsonify({
    "error": False,
    "isalive": True
  })

@api.route('/pcap', methods=['GET'])
@validate_code
def get_pcap_logs():
  if 'name' not in request.args:
    return jsonify({
      "error": True,
      "message": "File not specified"
    }), 400

  name = request.args.get('name')
  code = request.args.get('code')

  file = filemanager.get_file(name, code)
  if file is None:
    return jsonify({
      "error": True,
      "message": "pcap not found"
    }), 204

  return send_file(file)

@api.route('/logs', methods=['GET'])
def get_output_logs():
  return "", 501

@api.route('/info', methods=['GET'])
@validate_code
def get_info():
  code = request.args.get('code')
  data = filemanager.get_console_output(code)
  pcaps = filemanager.get_pcap_logs(code)
  source = filemanager.get_scenario_source(code)
  return jsonify({
    "error": False,
    "output": data,
    "logs": pcaps,
    "source": source
  })

@api.route('/asciitrace', methods=['GET'])
def get_ascii_trace():
  return "", 501

@api.route('/simulate', methods=['POST'])
@validate_scenario
def run_scenario():
  content = request.json
  file, uuid = filemanager.save_json(content)
  if file is None:
    return jsonify({
      "error": True,
      "message": "could not save scenario."
    }), 204
  
  out, err = ns3manager.run(file, uuid)
  if err != None:
    return jsonify({
      "error": True,
      "message": "error while running the simulation.",
      "trace": out
    })
  
  logs = filemanager.get_pcap_logs(uuid)

  return jsonify({
    "error": False,
    "output": out,
    "scenario_code": uuid,
    "pcap_logs": logs
  })

@api.route('/delete', methods=['DELETE'])
@validate_code
def delete_scenario():
  code = request.args.get('code')
  res = filemanager.delete_scenario(code)
  if res == True:
    return jsonify({
      "error": False
    }), 204
  else:
    return jsonify({
      "error": True,
      "message": f"scenario with code {code} does not exist"
    })
  
@api.route('/list', methods=['GET'])
def get_scenarios():
  return jsonify({
    "error": False,
    "scenarios": filemanager.get_all_scenarios()
  })