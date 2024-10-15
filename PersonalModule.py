class ThreadFetchHandler:
    def __init__(self,initVal,fetcher) -> None:
        self.val = initVal
        self.state = 'ready'
        self.fetcher = fetcher
    def updateVal(self):
        if self.state == "pending":
            return self.get()
        self.state = 'pending'
        self.val = self.fetcher()
        self.state = 'ready'
        print('got new token')
        return self.val
    def get(self):
        if self.state == 'ready':
            return self.val
        time.sleep(0.25)
        return self.get()
class Writer:
    writers = []
    def __init__(self,file,rate=10) -> None:
        self.file = file
        self.rate = rate
        self.pendingLines = []
        self.writers.append(self)
    def appendLine(self,line):
        self.pendingLines.append(line)
        if len(self.pendingLines)>=self.rate:
            self.pushLines()
    def pushLines(self):
        res = ''
        lines = self.pendingLines.copy()
        self.pendingLines = []
        for line in lines:
            res += line+'\n'
        with FileLock(f"./{self.file}.txt.lock"):
            with open(self.file,'a') as file:
                file.write(res)
    def exit(self):
        self.pushLines()
    @classmethod
    def killSession(cls):
        for writer in cls.writers:
            writer.exit()
            print('+ writer killed')
