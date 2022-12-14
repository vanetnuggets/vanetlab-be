from flask import Flask, jsonify
from app.api.routes import api
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/api/*')

app.register_blueprint(api, url_prefix='/api')
