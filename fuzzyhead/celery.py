from __future__ import absolute_import
from celery import Celery
from .config_parser import backend, broker

app = Celery('fuzzyhead',
            backend=backend,
            broker=broker,
            include=['fuzzyhead.tasks'])

