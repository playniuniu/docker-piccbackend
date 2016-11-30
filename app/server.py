#!/usr/env/bin python3
import os
from flask import Flask, jsonify, request
from werkzeug import secure_filename
from utility import inventory, tasks

app = Flask(__name__)
app.config.from_pyfile('config/config_prod.py', silent=True)


@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp


@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']

    return resp


@app.route('/inventory', methods=['GET'])
def get_inventory():
    host_url = app.config['HOST_URL']
    res = inventory.get_inventory(host_url)
    return jsonify(res)


@app.route('/inventory', methods=['POST'])
def post_inventory():
    host_url = app.config['HOST_URL']
    data = request.get_json(force=True)
    inventory.set_inventory(host_url, data)
    return jsonify({"status": "ok"})


@app.route('/newtask', methods=['POST'])
def post_newtask():
    task_url = app.config['FLANSIBLE_URL']
    data = request.get_json(force=True)
    res = tasks.create_task(data, task_url)
    return jsonify(res)


@app.route('/upload', methods=['POST'])
def post_upload():
    file = request.files['file']
    if file is not None:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error"})


@app.route('/tasks', methods=['GET'])
def get_tasks():
    flower_url = app.config['FLOWER_URL']
    res = tasks.get_tasks(flower_url)
    return jsonify(res)


@app.route('/task/<uuid>', methods=['GET'])
def get_task(uuid):
    flower_url = app.config['FLOWER_URL']
    res = tasks.get_task_id(flower_url, uuid)
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4000)
