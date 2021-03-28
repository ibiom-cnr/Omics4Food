from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

@app.route('/lims_api_mock/v1.0/api-status', methods=['GET'])
def get_status():

    return jsonify({'lims_api_mock': 'on-line' })

@app.route('/lims_api_mock/v1.0/update-output-url', methods=['POST'])
def update_job_status():

    print request.json

    return request.json
