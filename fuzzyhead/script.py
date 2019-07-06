#!/usr/bin/python
from .tasks import fuzzer
from celery import uuid
from celery.result import AsyncResult
from celery.task.control import inspect

import os
import requests
import time
import json

def start_fuzzing(fuzzer_type, dict_path, divide_number, target_ip, task_id, conn, cursor):
    try:
        if fuzzer_type=='patator':
            fuzzer_container = "registry:443/patator:latest"
            fuzzer_start = "python2 -W ignore patator.py"
            fuzzer_options = "ssh_login host="+target_ip+" user=victim password=FILE0 0=passwords.txt -x ignore:mesg='Authentication failed.'"
            parse_func = parsePatator
        if fuzzer_type == "dirsearch":
            fuzzer_container = "registry:443/dirsearch:latest"
            fuzzer_start = "python3 -W ignore dirsearch.py"
            fuzzer_options = "--url "+target_ip+" -e html --wordlist=wordlist.txt --simple-report=/dirsearch/result.txt"
            parse_func = parseDirsearch
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

        os.remove(dict_path)
        output=parse_func(output)
        cursor.execute('UPDATE tasks SET status=?, result=? WHERE id=?', ('Finished', output, task_id))
        conn.commit()
        return output
    except:
        cursor.execute('UPDATE tasks SET status=? WHERE id=?', ('Failed', task_id))
        conn.commit()
    

def parsePatator(output):
    blocks=output.split("b'")
    if '' in blocks:
        blocks.remove('')
    hits=0
    done=0
    skip=0
    fail=0
    size=0
    match = []
    for b in blocks:
        strings=b.split('\\n')
        if len(strings)==7:
            result=strings[4].split('|')
            match.append(result[1])
        stats=strings[-2]
        valueIndex=stats.index('Size: ', )+6
        hits+=int(stats[valueIndex:valueIndex+1])
        done+=int(stats[valueIndex+2:valueIndex+3])
        skip+=int(stats[valueIndex+4:valueIndex+5])
        fail+=int(stats[valueIndex+6:valueIndex+7])
        size+=int(stats[valueIndex+8:valueIndex+9])
        #time+=stats[stats.index('Time: ')+6:]
    return json.dumps({'match':match, 'hits':hits, 'done':done, 
        'skip':skip, 'fail':fail, 'size':size})

def parseDirsearch(output):
    strings=output.split('\n')
    if '' in strings:
        strings.remove('')
    match=[]
    for s in strings:
        match.append(s[s.rindex('/')+1:])
    return json.dumps({'match':match})