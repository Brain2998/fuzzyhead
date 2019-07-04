from __future__ import absolute_import
from celery import Celery

app = Celery('fuzzyhead',
            backend='amqp',
            broker='amqp://vicot:pnKKTCd5q42O@10.1.38.14',
            include=['fuzzyhead.tasks'])

