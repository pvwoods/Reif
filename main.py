#! /usr/local/bin/python3
from reif.storage.lsm.logstore import LoggingKeyStore
import json
import random

class Repl():

    def __init__(self):
        self.store = None

    def handle(self, command):
        instructions = command.split(" ")
        func = instructions[0].lower()

        if func == "exit":
            exit()
        elif func == "load" and len(instructions) == 2:
            self.store = LoggingKeyStore(instructions[1])
            print("DB loaded")
        elif self.store:
            if func == "snapshot":
                self.store.writeSnapshot()
                print("OK")
            elif func == "set" and len(instructions) > 2:
                self.store.set(instructions[1], " ".join(instructions[2:]))
                print("OK")
            elif func == "get" and len(instructions) == 2:
                print(self.store.get(instructions[1]))
            else:
                print("command not recognized")
        else:
            print("No database selected")


repl = Repl()
while True:
    command = repl.handle(input("> "))
