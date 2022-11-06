from flask import Blueprint, request, make_response, jsonify, render_template
from app.managers.filemanager import filemanager
from app.managers.ns3manager import Ns3manager

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
  
  ns3man = Ns3manager()
  ns3man.load(file_path)

  return jsonify({"status": "scenario uploaded"})


@api.route('/run', methods=['POST'])
def run():
  return jsonify({"todo": "xxx"}), 204


@api.route('/status', methods=['POST'])
def status():
  return jsonify({"todo": "xxx"}), 204


@api.route('/trace', methods=['POST'])
def trace():
  return jsonify({"todo": "xxx"}), 204