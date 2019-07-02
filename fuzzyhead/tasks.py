from __future__ import absolute_import
from fuzzyhead.celery import app
from celery import current_task
import os

import urllib.request

import docker

dicts_source = "http://backend/"

@app.task
def fuzzer(taskid, fuzzer_container, fuzzer_start, fuzzer_options):

    if fuzzer_container == "registry:443/patator:latest":
        urllib.request.urlretrieve(dicts_source + str(taskid),'/tmp/passwords.txt')
        cmd = fuzzer_start + " " + fuzzer_options
        vol = {'/tmp/passwords.txt': {'bind': '/patator/passwords.txt', 'mode': 'ro'}}
        client = docker.from_env()
        result = str(client.containers.run(fuzzer_container, command=cmd, volumes=vol, stdin_open=True, stderr=True, remove=True))

    if fuzzer_container == "registry:443/dirsearch:latest":
        urllib.request.urlretrieve(dicts_source + str(taskid),'/tmp/wordlist.txt')
        cmd = fuzzer_start + " " + fuzzer_options
        
        vol = {'/tmp/wordlist.txt': {'bind': '/dirsearch/wordlist.txt','mode': 'ro'},
               '/tmp/result.txt': {'bind': '/dirsearch/result.txt', 'mode': 'rw'}}

        client = docker.from_env()
        client.containers.run(fuzzer_container, command=cmd, volumes=vol, stdin_open=True, stderr=True, remove=True)

        with open('/tmp/result.txt', 'r') as file:
            result = file.read()

    return result