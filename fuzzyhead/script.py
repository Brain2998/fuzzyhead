#!/usr/bin/python
from .tasks import fuzzer
from celery import uuid
from celery.result import AsyncResult
from celery.task.control import inspect

import os
import requests
import time

def start_fuzzing(fuzzer_type, dict_path, divide_number, target_ip):
    if fuzzer_type=='patator':
        fuzzer_container = "registry:443/patator:latest"
        fuzzer_start = "python2 -W ignore patator.py"
        fuzzer_options = "ssh_login host="+target_ip+" user=victim password=FILE0 0=passwords.txt -x ignore:mesg='Authentication failed.'"

    if fuzzer_type == "dirsearch":
        fuzzer_container = "registry:443/dirsearch:latest"
        fuzzer_start = "python3 -W ignore dirsearch.py"
        fuzzer_options = "--url "+target_ip+" -e html --wordlist=wordlist.txt --simple-report=/dirsearch/result.txt"
    upload_dict_url = "http://backend:5000/uploader"
    remove_dict_url = "http://backend:5000/remover"

    result_id_list = []
    taskid_list = []
    output = ""

    with open(dict_path) as f:
        content=f.readlines()

    dictLength=len(content)
    partStartIndex=0
    partEndIndex=divide_number if divide_number < dictLength else dictLength
    dictExceed=False

    while True:
        taskid = uuid()
        taskid_list.append(taskid)
        with open('dict/'+str(taskid), 'w') as f:
            for i in range(partStartIndex, partEndIndex):
                f.write(content[i])
        partStartIndex=partEndIndex
        partEndIndex=partEndIndex+divide_number
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
    l = len(result_id_list)
    a = len(result_id_list)

    while l != 0:
        for result_id in result_id_list:
           if AsyncResult(result_id,app=fuzzer).ready() == True:
               output = output+AsyncResult(result_id,app=fuzzer).get()
               l = l - 1
               result_id_list.remove(result_id)
               print(round(100 - l/a * 100))

    os.remove(dict_path)
    return output
