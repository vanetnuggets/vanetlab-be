from flask import Flask, jsonify
from app.api.routes import api

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/')