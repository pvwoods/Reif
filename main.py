#! /usr/local/bin/python3
from reif.storage.lsm.logstore import LoggingKeyStore
import json
import random

store = LoggingKeyStore('test.db')



for i in range(30):
    store.set(str(i), json.dumps([random.randint(0, 100) for _ in range(5)]))