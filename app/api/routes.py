from flask import Blueprint, send_file, request, make_response, redirect, jsonify, render_template
from app.managers.filemanager import filemanager
from app.managers.ns3manager import ns3manager
from app.managers.security import validate_scenario, validate_uuid

api = Blueprint('api', __name__)

@api.route('/isalive')
def isalive():
  return jsonify({
    "error": False,
    "isalive": True
  })


@api.route('/pcap', methods=['GET'])
def get_pcap_logs():
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

@api.route('/logs', methods=['GET'])
def get_output_logs():
  return "", 501

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
def delete_scenario():
  if 'code' not in request.args:
    return jsonify({
      "error": True,
      "message": "scenario code not specified."
    })
  code = request.args.get('code')
  if validate_uuid(code) == False:
    return jsonify({
      "error": True,
      "message": "wrong code format. dir traversal attempt?"
    })
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
  
  