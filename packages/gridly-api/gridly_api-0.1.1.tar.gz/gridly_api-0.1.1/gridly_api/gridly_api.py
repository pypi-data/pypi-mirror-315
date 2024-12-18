#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import csv
import json
import logging
from io import StringIO
from dotenv import load_dotenv

log = logging.getLogger(__name__)
load_dotenv()


__URL__ = "https://eu-central-1.api.gridly.com"
__AUTH__ = f"ApiKey {os.getenv('GRIDLY_API_KEY')}"
__VIEW_ID__ = os.getenv('GRIDLY_VIEW_ID')

def export():
    url = f"{__URL__}/v1/views/{__VIEW_ID__}/export?fileHeader=columnId"
    web_csv = requests.get(url, headers={'Authorization': __AUTH__})
    f = StringIO(web_csv.text)
    csv_content = csv.reader(f, delimiter=',')

    for row in csv_content:
        langs = row[1:]
        break

    trans = {}
    for lang in langs:
        trans[lang] = {}

    for row_index, row in enumerate(csv_content):
        for l_index, lang in enumerate(langs):
            trans[lang][row[0]] = row[l_index + 1].replace("\n", "\\\n")

    return trans

def import_from_csv(csv_file_name):
    url = f"{__URL__}/v1/views/{__VIEW_ID__}/records"

    records = []

    with open(csv_file_name, newline='') as csvfile:
        csv_content = csv.reader(csvfile, delimiter=';')

        for row in csv_content:
            records.append({
                "id": row[0],
                "cells": [
                    {
                        "columnId": "uk",
                        "value": row[1],
                        "dependencyStatus": "outOfDate"
                    }
                ]
            })

    data = json.dumps(records)
    log.debug("Request = {}", data)
    response = requests.post(url, headers={'Authorization': __AUTH__, "Content-Type": "application/json"}, data=data)
    log.debug("Response: {}", response)
    log.debug(response.json())
