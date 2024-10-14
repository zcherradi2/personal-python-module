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
