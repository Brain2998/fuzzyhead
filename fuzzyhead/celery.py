from __future__ import absolute_import
from celery import Celery

app = Celery('fuzzyhead',
             broker='amqp://vicot:pnKKTCd5q42O@10.1.38.14',
             backend='rpc://',
             include=['fuzzyhead.tasks'])
