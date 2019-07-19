#!/usr/bin/python
from .tasks import fuzzer
from celery import uuid
from celery.result import AsyncResult
from celery.task.control import inspect
from celery.task.control import revoke

import os
import requests
import time
import json

from .config_parser import registry, dict_upload, flower

def start_fuzzing(fuzzer_type, dict_path, divide_number, cli_args, rps, task_id, conn, cursor):
    try:
        start_time=time.time()
        fuzzer_options = cli_args
        if fuzzer_type=='patator':
            fuzzer_container = registry+"/patator:latest"
            fuzzer_start = "python2 -W ignore patator.py"
            fuzzer_options = cli_args
            parse_func = parsePatator
        if fuzzer_type == "dirsearch":
            fuzzer_container = registry+"/dirsearch:latest"
            fuzzer_start = "python3 -W ignore dirsearch.py"
            parse_func = parseDirsearch

        result_id_list = []
        taskid_list = []
        output = ""

        with open(dict_path) as f:
            content=f.readlines()

        dictLength=len(content)
        partStartIndex=0
        partEndIndex=divide_number if divide_number < dictLength else dictLength
        dictExceed=False

        flower_api_ratelimit_url = flower+'/api/task/rate-limit/fuzzyhead.tasks.fuzzer'

        workers = json.loads(requests.get(flower+'/api/workers').text).keys()

        for worker in workers:
            params = (('ratelimit', rps),('workername', worker))
            requests.post(flower_api_ratelimit_url,params)

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
            requests.post(dict_upload, files=files)
            os.remove('dict/'+str(taskid))

            result = fuzzer.delay(taskid, fuzzer_container, fuzzer_start, fuzzer_options)
            result_id_list.append(result.id)

            if (dictExceed):
                break
        l = len(result_id_list)
        a = len(result_id_list)
        result_ids=json.dumps(result_id_list)

        #Inserting result_ids into database for possible revoke while executing
        cursor.execute('UPDATE tasks SET result_id=? WHERE id=?', (result_ids, task_id))
        conn.commit()

        #Waiting for fuzzing to be finished
        while l != 0:
            for result_id in result_id_list:
                if AsyncResult(result_id,app=fuzzer).state == 'REVOKED':
                    l = l - 1
                    result_id_list.remove(result_id)
                    #print (round(100 - l/a * 100), "Task ",result_id, " REVOKED")
                    continue

                if (AsyncResult(result_id,app=fuzzer).ready() == True) and (AsyncResult(result_id,app=fuzzer).state != 'REVOKED'):
                    output = output+AsyncResult(result_id,app=fuzzer).get()
                    l = l - 1
                    result_id_list.remove(result_id)
                    #print (round(100 - l/a * 100), "Task ",result_id, " SUCCESS")

        if os.path.exists(dict_path):
            os.remove(dict_path)
        output=parse_func(output, round(time.time()-start_time, 2))
        cursor.execute('UPDATE tasks SET status=?, result=? WHERE id=?', ('Finished', output, task_id))
        conn.commit()
        return output
    except:
        cursor.execute('UPDATE tasks SET status=? WHERE id=?', ('Failed', task_id))
        conn.commit()

def abort_fuzzing(result_id_list):
    for result_id in result_id_list:
        if AsyncResult(result_id,app=fuzzer).ready() == False:
            flower_api_revoke_url = flower+'/api/task/revoke/'+str(result_id)
            requests.post(flower_api_revoke_url,data={'terminate':'true'})
        #print("Task ", AsyncResult(result_id,app=fuzzer).state, result_id, " is terminated")

def parsePatator(output, fuztime):
    blocks=output.split("b'")
    if '' in blocks:
        blocks.remove('')
    hits=0
    done=0
    skip=0
    fail=0
    size=0
    match = []
    speedRate=[]
    for b in blocks:
        strings=b.split('\\n')
        resultLng=len(strings)
        if resultLng>6:
            for i in range(4, resultLng-2):
                result=strings[i].split('|')
                match.append(result[1])
        stats=strings[-2]
        values=stats[stats.index('Size: ', )+6:stats.index('Avg')-2].split('/')
        hits+=int(values[0])
        done+=int(values[1])
        skip+=int(values[2])
        fail+=int(values[3])
        size+=int(values[4])
        speedRate.append(int(stats[stats.index('Avg')+5:stats.index(' r/s')]))
    return json.dumps({'match':match, 'hits':hits, 'done':done, 'skip':skip, 'fail':fail, 
    'size':size, 'avg': sum(speedRate), 'time': fuztime})

def parseDirsearch(output, fuztime):
    strings=output.split('\n')
    if '' in strings:
        strings.remove('')
    match=[]
    for s in strings:
        match.append(s[s.rindex('/')+1:])
    return json.dumps({'match': match, 'time': fuztime})
