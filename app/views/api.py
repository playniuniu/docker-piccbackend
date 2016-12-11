#!/usr/env/bin python3
import os
from flask import jsonify, Blueprint, request
from werkzeug import secure_filename
from app import app
from app.utility import inventory, tasks


api = Blueprint('api', __name__)


@api.route('/inventory', methods=['GET'])
def get_inventory():
    host_url = app.config['HOST_URL']
    res = inventory.get_inventory(host_url)
    return jsonify(res)


@api.route('/inventory', methods=['POST'])
def post_inventory():
    host_url = app.config['HOST_URL']
    data = request.get_json(force=True)
    inventory.set_inventory(host_url, data)
    return jsonify({"status": "ok"})


@api.route('/newtask', methods=['POST'])
def post_newtask():
    task_url = app.config['FLANSIBLE_URL']
    data = request.get_json(force=True)
    res = tasks.create_task(data, task_url)
    return jsonify(res)


@api.route('/upload', methods=['POST'])
def post_upload():
    file = request.files['file']
    if file is not None:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error"})


@api.route('/increupdate', methods=['POST'])
def post_increupdate():
    file = request.files['file']
    if file is not None:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['INCREUPDATE_FOLDER'], filename))
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error"})


@api.route('/tasks', methods=['GET'])
def get_tasks():
    flower_url = app.config['FLOWER_URL']
    res = tasks.get_tasks(flower_url)
    return jsonify(res)


@api.route('/task/<uuid>', methods=['GET'])
def get_task(uuid):
    ''' Have bug with flower'''
    flower_url = app.config['FLOWER_URL']
    res = tasks.get_task_id(flower_url, uuid)
    return jsonify(res)
