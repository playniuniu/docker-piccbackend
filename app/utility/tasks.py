#!/usr/bin/env python3
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth


def parse_tasks(el):
    unix_time = datetime.fromtimestamp(el['timestamp'])

    res = {
        'uuid': el['uuid'],
        'state': el['state'],
        'result': el['result'],
        'timestamp': el['timestamp'],
        'endtime': unix_time.strftime("%Y-%m-%d %H:%M"),
    }

    if 'runtime' in el and isinstance(el['runtime'], float):
        res['runtime'] = round(el['runtime'], 1)
    else:
        res['runtime'] = 0.0

    return res


def create_task(data, task_url):
    auth_data = HTTPBasicAuth('admin', 'admin')
    r = requests.post(task_url, auth=auth_data, json=data)
    return r.json()


def get_tasks(flower_url):
    task_list = []
    url = flower_url + '/api/tasks'
    r = requests.get(url)
    task_dict = r.json()
    for index in task_dict:
        el = task_dict[index]
        task_list.append(parse_tasks(el))

    task_list = sorted(task_list, key=lambda el: el['timestamp'], reverse=True)
    return task_list


def get_task_id(flower_url, uuid):
    url = flower_url + '/api/task/info/' + uuid
    r = requests.get(url)
    return r.json()
