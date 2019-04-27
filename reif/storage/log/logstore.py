import logging
import os
import struct

class LoggingKeyStoreMap():
    
    def __init__(self):
        self.keyToFileOffsets = {}
    
    def setKeyOffset(self, key, offset):
        if not key.isalnum():
            return False
        else:
            self.keyToFileOffsets[key] = offset
            return True
    
    def getOffset(self, key):
        if key not in self.keyToFileOffsets:
            return -1
        return self.keyToFileOffsets[key]
    
    def snapshot(self):
        return "\n".join([f'{k},{self.keyToFileOffsets[k]}' for k in self.keyToFileOffsets])

class LoggingKeyStoreReader():
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.fp = open(self.filepath, 'r+b')
    
    def get(self, offset):
        self.fp.seek(offset, os.SEEK_SET)
        return self.fp.readline().strip().decode('utf-8')

class LoggingKeyStoreWriter():
    
    def __init__(self, filepath):
        
        self.filepath = filepath
        self.fp = open(self.filepath, 'a+b', buffering=0)
        
    def set(self, value):
        self.fp.write(("%s\n" % value).encode('utf-8'))
        
    def getCurOffset(self, key):
        return self.fp.tell()


class LoggingKeyStore():
    
    def __init__(self, filepath):

        self.filepath = filepath
        self.writer = LoggingKeyStoreWriter(filepath)
        self.reader = LoggingKeyStoreReader(filepath)
        self.keyMap = LoggingKeyStoreMap()
        
        if os.path.isfile(self.snapshotFilePath):
            self.loadSnapshot()
        
    def set(self, key, value):
        bo = self.writer.getCurOffset(key)
        if self.keyMap.setKeyOffset(key, bo):
            self.writer.set(value)
            logging.info("WROTE %s to %s" % (key, bo))
        else:
            logging.error("Could not write key %s" % key) 
    
    def get(self, key):
        bo = self.keyMap.getOffset(key)
        logging.info("Key  %s found at offset %s" % (key, bo))
        if bo < 0:
            return ""
        else:
            return self.reader.get(bo)

    def writeSnapshot(self):
        fp = open(self.snapshotFilePath, "w+")
        fp.write(self.keyMap.snapshot())
        fp.close()

    def loadSnapshot(self):
        fp = open(self.snapshotFilePath, "r+")
        for line in fp:
            k, v = line.strip().split(",")
            self.keyMap.keyToFileOffsets[k] = int(v)
        fp.close()

    @property
    def snapshotFilePath(self):
        return f"{self.filepath}.snapshot"