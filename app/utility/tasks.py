#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth


def create_task(data, task_url):
    auth_data = HTTPBasicAuth('admin', 'admin')
    r = requests.post(task_url, auth=auth_data, json=data)
    return r.json()


def get_tasks(flower_url):
    url = flower_url + '/api/tasks'
    print(url)
    r = requests.get(url)
    return r.json()


def get_task_id(flower_url, uuid):
    url = flower_url + '/api/task/info/' + uuid
    r = requests.get(url)
    return r.json
