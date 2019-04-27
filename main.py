#! /usr/local/bin/python3
from reif.storage.lsm.logstore import LoggingKeyStore
import json
import random

store = LoggingKeyStore('data/test.db')

x = 5

#for i in range(x):
#    store.set(str(i), json.dumps([i] + [random.randint(0, 100) for _ in range(5)]))

for i in range(x):
    print(store.get(str(i)))

#store.writeSnapshot()

