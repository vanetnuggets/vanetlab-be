from flask import Blueprint, send_file, request, make_response, redirect, jsonify, render_template
from app.managers.tcl_parser import tcl_parser
from app.managers.filemanager import filemanager
from app.managers.ns3manager import ns3manager

api = Blueprint('api', __name__)

@api.route('/isalive')
def isalive():
  return jsonify({
    "error": False,
    "isalive": True
  })

@api.route('/from-sumo', methods=['POST'])
def from_sumo():
  data = dict(request.form)
  print(data)

  name = data['name']
  trace_file = request.files['sumotrace']
  
  filemanager.create_scenario(name)
  filemanager.save_sumo(name, trace_file)

  ns3manager.generate_ns2_mobility(name)

  conf = tcl_parser.tcl_to_conf(filemanager.get_ns2tcl(name))
  filemanager.save_conf(name, conf)

  return conf, 201

@api.route('/simulate/<name>', methods=['POST'])
def simulate(name):
  res = ns3manager.simulate(name)
  
  return jsonify({
    "error": False,
    "data": res
  }), 400

@api.route('/validate/<name>', methods=['POST'])
def test_scenario(name):
  err = ns3manager.validate(name)

  if err == None:
    return jsonify({
      "error": False,
      "data": None
    }), 200
  
  return jsonify({
    "error": True,
    "data": err
  }), 400

@api.route('/netanim-trace/<name>', methods=['GET'])
def get_trace(name):
  path = filemanager.get_netanim_trace(name)
  return send_file(path)

@api.route('/list', methods=['GET'])
def get_scenarios():
  return jsonify({
    "error": False,
    "data": filemanager.get_all_scenarios()
  })
