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
        self.fp = open(self.filepath, 'r')
    
    def get(self, offset):
        self.fp.seek(offset)
        return self.fp.readline()

class LoggingKeyStoreWriter():
    
    def __init__(self, filepath):
        
        self.filepath = filepath
        self.fp = open(self.filepath, 'a+')
        
    def set(self, value):
        self.fp.write(value + "\n")
        
    def getCurOffset(self, key):
        return self.fp.tell()


class LoggingKeyStore():
    
    def __init__(self, filepath):
        self.writer = LoggingKeyStoreWriter(filepath)
        self.reader = LoggingKeyStoreReader(filepath)
        self.keyMap = LoggingKeyStoreMap()
        
    def set(self, key, value):
        bo = self.writer.getCurOffset(key)
        if self.keyMap.setKeyOffset(key, bo):
            self.writer.set(value)
            print("WROTE %s to %s" % (key, bo))
        else:
            print("ERROR WRITING %s" % key) 
    
    def get(self, key):
        bo = self.keyMap.getOffset(key)
        if bo < 0:
            return ""
        else:
            return self.reader.get(bo).strip('\n')