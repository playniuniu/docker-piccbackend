#!/usr/bin/env python3
import csv
import os


def get_inventory(csv_url):
    if not os.path.exists(csv_url):
        return []

    with open(csv_url, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def set_inventory(csv_url, data):
    header = ['ip', 'port', 'user', 'passwd', 'group', 'area', 'desc']

    with open(csv_url, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for el in data:
            writer.writerow(el)

    return True
