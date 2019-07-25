from __future__ import absolute_import
from fuzzyhead.celery import app
from celery import current_task
import os

import requests
import urllib.request

import docker

dicts_source = "http://backend/"
remove_dict_url = "http://backend:5000/remover"

@app.task
def fuzzer(taskid, fuzzer_container, fuzzer_start, fuzzer_options):

    if fuzzer_container == "registry:443/patator:latest":
        open('/tmp/passwords.txt', 'w').close()
        urllib.request.urlretrieve(dicts_source + str(taskid),'/tmp/passwords.txt')
        cmd = fuzzer_start + " " + fuzzer_options
        vol = {'/tmp/passwords.txt': {'bind': '/patator/passwords.txt', 'mode': 'ro'}}
        client = docker.from_env()
        result = str(client.containers.run(fuzzer_container, command=cmd, volumes=vol, stdin_open=True, stderr=True, remove=True))
        requests.get(remove_dict_url+'/'+str(taskid))

    if fuzzer_container == "registry:443/dirsearch:latest":

        open('/tmp/result.txt', 'w').close()
        open('/tmp/wordlist.txt', 'w').close()

        urllib.request.urlretrieve(dicts_source + str(taskid),'/tmp/wordlist.txt')

        cmd = fuzzer_start + " " + fuzzer_options

        vol = {'/tmp/wordlist.txt': {'bind': '/dirsearch/wordlist.txt','mode': 'ro'},
               '/tmp/result.txt': {'bind': '/dirsearch/result.txt', 'mode': 'rw'}}

        client = docker.from_env()
        client.containers.run(fuzzer_container, command=cmd, volumes=vol, stdin_open=True, stderr=True, remove=True)

        requests.get(remove_dict_url+'/'+str(taskid))

        with open('/tmp/result.txt', 'r') as file:
            result = file.read()

    return result
