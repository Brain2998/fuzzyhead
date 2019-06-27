from __future__ import absolute_import
from fuzzyhead.celery import app
from celery import current_task
import os

import urllib.request

import docker

dicts_source = "http://backend/"

@app.task
def fuzzer(taskid, fuzzer_container, fuzzer_start, fuzzer_options):

    urllib.request.urlretrieve(dicts_source + str(taskid),'/tmp/passwords.txt')

    cmd = fuzzer_start + " " + fuzzer_options
    vol = {'/tmp/passwords.txt': {'bind': '/patator/passwords.txt', 'mode': 'ro'}}

    client = docker.from_env()
    result = str(client.containers.run(fuzzer_container, command=cmd, volumes=vol, stdin_open=True, stderr=True, remove=True))

    return result
