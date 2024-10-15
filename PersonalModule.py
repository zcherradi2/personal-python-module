#handles multithreading shared variables
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

#handles logging txt data
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
            
#transforms a list of strings to a single string
def lstToStr(lst):
    res = ''
    for el in lst:
        res += el+'\n'
    return res
#random string functions
def getRandElement(lst):
    i = rd.randrange(0,len(lst))
    return lst[i]
def getRandWithRatio(length,type='an',alphaToNumRatio=0.6):
    chars = 'ABCDEFJHIGKLMNOPQRSTUVWXYZabcdefjhigklmnopqrstuvwxyz'
    nums = '123456789'
    res = ''
    if type == 'an':
        for i in range(length):
            n = int(10*alphaToNumRatio)
            coinStates = [0]*n
            coinStates.extend([1]*(10-n))
            coin = rd.choice(coinStates)
            if coin == 0:
                res += getRandElement(chars)
            else:
                res += getRandElement(nums)
        return res
    else:
        for i in range(length):
            res += getRandElement(nums)
        return res
def getRand(length,type='an'):
    chars = 'ABCDEFJHIGKLMNOPQRSTUVWXYZabcdefjhigklmnopqrstuvwxyz'
    nums = '123456789'
    res = ''
    if type == 'an':
        for i in range(length):
            res += getRandElement(chars+nums+nums)
        return res
    else:
        for i in range(length):
            res += getRandElement(nums)
        return res

#proxyManager
class ProxyManager:
    def __init__(self,lst) -> None:
        lines = lst
        self.validProxies = []
        self.proxies = []
        for line in lines:
            proxy = line.split(':')
            if len(proxy)==4:
                ip,port,user,passwd = proxy
                self.proxies.append(proxify(ip,port,user,passwd))
            else:
                ip,port = proxy
                self.proxies.append(proxify(ip,port))
        print(self.proxies)
        self.testProxies()
    def checkProxy(self,proxy):
        if self.isProxyValid(proxy):
            self.validProxies.append(proxy)
    def testProxies(self):
        # self.validProxies = []
        processes = []
        for proxy in self.proxies:
            processes.append(partial(self.checkProxy,proxy))
        print('testing proxies...')
        run_threads(processes)
    def getValidProxy2(self):
        if len(self.validProxies)==0:
            return {}
        else:
            return self.validProxies[0]
    def getValidProxy(self):
        try:
            if(len(self.validProxies)>0):
                return getRandElement(self.validProxies)
        except:
            return {}
        if len(self.validProxies)==0:
            return {}
        else:
            return self.validProxies[0]
    def invalidProxy(self):
        del self.validProxies[0]
    def isProxyValid(self,proxy):
        response = myRequest.get(
            'https://api.ipify.org?format=json',
            proxies=proxy
        )
        return proxy['http'].split('@')[1].split(':')[0] == response.json()['ip']
