
import da
PatternExpr_0 = da.pat.TuplePattern([da.pat.ConstantPattern('PING'), da.pat.FreePattern('ping')])
PatternExpr_1 = da.pat.FreePattern('src_id')
PatternExpr_2 = da.pat.TuplePattern([da.pat.ConstantPattern('REQ'), da.pat.FreePattern('req')])
PatternExpr_3 = da.pat.FreePattern('src_id')
PatternExpr_4 = da.pat.TuplePattern([da.pat.ConstantPattern('ACK'), da.pat.FreePattern('ack')])
PatternExpr_5 = da.pat.FreePattern('prev')
PatternExpr_6 = da.pat.TuplePattern([da.pat.ConstantPattern('srvFail'), da.pat.TuplePattern([da.pat.FreePattern('prev'), da.pat.FreePattern('next')])])
PatternExpr_7 = da.pat.FreePattern('master')
PatternExpr_8 = da.pat.TuplePattern([da.pat.ConstantPattern('REPLY'), da.pat.FreePattern('reply')])
PatternExpr_9 = da.pat.FreePattern('src_id')
PatternExpr_10 = da.pat.TuplePattern([da.pat.ConstantPattern('newHead'), da.pat.FreePattern('newSrv')])
PatternExpr_11 = da.pat.FreePattern('master')
PatternExpr_12 = da.pat.TuplePattern([da.pat.ConstantPattern('newTail'), da.pat.FreePattern('newSrv')])
PatternExpr_13 = da.pat.FreePattern('master')
import re
import time
import sys
import collections
from init import *
import random

def parse_config(input_str):
    input_str = input_str.replace(' ', '')
    strs = input_str.split(',')
    if (not (int(strs[0]) == 0)):
        retrans = True
        print('Retransmission enabled')
    else:
        reTrans = False
    retrans_interval = int(strs[1])
    print('Timeout is:', retrans_interval)
    retrans_time = int(strs[2])
    print('nRetrans is:', retrans_time)
    if (not (int(strs[3]) == 0)):
        ifRandom = True
        print('Random request enabled')
    else:
        ifRandom = False
    return [retrans, retrans_interval, retrans_time, ifRandom]

def parse_server(input_str):
    input_str = input_str.strip()
    input_str = input_str.replace(' ', '')
    str = input_str.split(',')
    bankName = int(str[0])
    serverIP = str[1]
    startup_delay = str[2]
    life_time = str[3]
    return [bankName, serverIP, startup_delay, life_time]

def parse_client(input_str):
    input_str = input_str.replace(' ', '')
    str = input_str.split(',')
    bankName = str[0]
    account_no = str[1]
    clientIP = str[2]
    return [bankName, account_no, clientIP]

def parse_req(input_str):
    input_str = input_str.replace(' ', '')
    input_str = re.sub('[()]', '', input_str)
    strs = input_str.split(',')
    if (strs[0] == 'getBalance'):
        reqtype = ReqType.Query
    elif (strs[0] == 'deposit'):
        reqtype = ReqType.Deposit
    elif (strs[0] == 'withdraw'):
        reqtype = ReqType.Withdraw
    else:
        reqtype = ReqType.Transfer
    reqID = strs[1]
    account_num = strs[2]
    if (reqtype == ReqType.Query):
        amount = 0
    else:
        amount = strs[3]
    return [reqID, reqtype, account_num, amount]

def parse_randomReq(input_str):
    input_str = input_str.strip()
    input_str = input_str.replace(' ', '')
    input_str = re.sub('[()]', '', input_str)
    strs = input_str.split(',')
    seed_num = int(strs[0])
    num_req = int(strs[1])
    prob_query = float(strs[2])
    prob_deposit = float(strs[3])
    prob_withdraw = float(strs[4])
    prob_transfer = float(strs[5])
    return [seed_num, num_req, prob_query, prob_deposit, prob_withdraw, prob_transfer]

class Master(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_MasterReceivedEvent_0', PatternExpr_0, sources=[PatternExpr_1], destinations=None, timestamps=None, record_history=None, handlers=[self._Master_handler_0])])

    def setup(self, srvDic, cliDic):
        self.cliDic = cliDic
        self.srvDic = srvDic
        self.timesheet = {}
        self.srvDict = self.srvDic
        self.cliDict = self.cliDic

    def main(self):
        self.output((('Master  ' + str(self.id)) + '  has started.'))
        print('SERVER DICTIONARY STORED IN MASTER', self.srvDict)
        print('CLIENT DICTIONARY STORED IN MASTER', self.cliDict)
        while True:
            _st_label_136 = 0
            self._timer_start()
            while (_st_label_136 == 0):
                _st_label_136 += 1
                if False:
                    pass
                    _st_label_136 += 1
                elif self._timer_expired:
                    self.checkSrv(self.timesheet)
                    _st_label_136 += 1
                else:
                    super()._label('_st_label_136', block=True, timeout=5)
                    _st_label_136 -= 1
            else:
                if (_st_label_136 != 2):
                    continue
            if (_st_label_136 != 2):
                break

    def flush_srvDict(self, bankname):
        for (i, item) in enumerate(self.srvDict[bankname]):
            if (len(self.srvDict[bankname]) == 1):
                item[1] = None
                item[2] = None
                return
            if (i == 0):
                item[1] = None
                item[2] = self.srvDict[bankname][(i + 1)][0]
                continue
            elif (i == (len(self.srvDict[bankname]) - 1)):
                item[2] = None
                item[1] = self.srvDict[bankname][(i - 1)][0]
            else:
                item[1] = self.srvDict[bankname][(i - 1)][0]
                item[2] = self.srvDict[bankname][(i + 1)][0]

    def infoCli(self, bankName, type, newSrv):
        for cli in self.cliDict[str(bankName)]:
            if (type == 'head'):
                print('SENDING NEW HEAD TO CLIENT:', cli)
                self._send(('newHead', newSrv), cli)
            elif (type == 'tail'):
                self._send(('newTail', newSrv), cli)
            else:
                pass

    def updateSrvInfo(self, srv):
        port = srv[0]
        bankName = srv[1]
        prevInfo = []
        nextInfo = []
        for item in self.srvDict[bankName]:
            if (port == item[3]):
                prev = item[1]
                next = item[2]
                self.srvDict[bankName].remove(item)
                self.flush_srvDict(bankName)
                if (prev == None):
                    self.infoCli(bankName, 'head', next)
                if (next == None):
                    self.infoCli(bankName, 'tail', prev)
                else:
                    pass
        for item in self.srvDict[bankName]:
            if ((item[0] == prev) or (item[0] == next)):
                self._send(('srvFail', (item[1], item[2])), item[0])
            else:
                pass

    def checkSrv(self, timesheet):
        time_chec = self.logical_clock()
        failedSrv = []
        for key in timesheet.keys():
            if ((time_chec - timesheet.get(key)) > 5):
                print('Server ', key[0], ' has failed!')
                failedSrv.append(key)
        for srv in failedSrv:
            del timesheet[srv]
            self.updateSrvInfo(srv)

    def _Master_handler_0(self, ping, src_id):
        time_recv = self.logical_clock()
        print('Received PING from: ', ping.serverIP)
        self.timesheet.update({(ping.serverIP, ping.bankName): time_recv})
    _Master_handler_0._labels = None
    _Master_handler_0._notlabels = None

class Server(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_0', PatternExpr_2, sources=[PatternExpr_3], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_1]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_1', PatternExpr_4, sources=[PatternExpr_5], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_2]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_2', PatternExpr_6, sources=[PatternExpr_7], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_3])])

    def setup(self, bankName, serverIP, startup_delay, life_time, prev, next, master):
        self.life_time = life_time
        self.startup_delay = startup_delay
        self.prev = prev
        self.master = master
        self.bankName = bankName
        self.serverIP = serverIP
        self.next = next
        self.bankName = self.bankName
        self.serverIP = self.serverIP
        self.startup_delay = self.startup_delay
        self.life_time = int(self.life_time)
        self.prev = self.prev
        self.next = self.next
        self.master = self.master
        self.sentTrans = []
        self.procTrans = {}
        self.AccountInfo = {}

    def main(self):
        self.output(((((((((('Server: Bank Name is: ' + str(self.bankName)) + '  Server IP is: ') + str(self.serverIP)) + '  Life time is: ') + str(self.life_time)) + '  Previous server is: ') + str(self.prev)) + '  Next server is: ') + str(self.next)))
        ping = Ping(self.serverIP, self.bankName)
        while True:
            _st_label_226 = 0
            self._timer_start()
            while (_st_label_226 == 0):
                _st_label_226 += 1
                if False:
                    pass
                    _st_label_226 += 1
                elif self._timer_expired:
                    self._send(('PING', ping), self.master)
                    _st_label_226 += 1
                else:
                    super()._label('_st_label_226', block=True, timeout=1)
                    _st_label_226 -= 1
            else:
                if (_st_label_226 != 2):
                    continue
            if (_st_label_226 != 2):
                break

    def proc_balance(self, req):
        outcome = Outcome.Processed
        if (self.AccountInfo.get(req.account_num) == None):
            cur_balance = 0
        else:
            cur_balance = self.AccountInfo[req.account_num]
        if (not (self.procTrans.get(req.reqID) == None)):
            if (not (self.procTrans[req.reqID].reqtype == req.reqtype)):
                outcome = Outcome.InconsistentWithHistory
            else:
                pass
            new_balance = cur_balance
        elif (req.reqtype == ReqType.Query):
            new_balance = cur_balance
        elif (req.reqtype == ReqType.Deposit):
            new_balance = (cur_balance + req.amount)
        elif (req.reqtype == ReqType.Withdraw):
            if ((cur_balance - req.amount) < 0):
                new_balance = cur_balance
                outcome = Outcome.InsufficientFunds
            else:
                new_balance = (cur_balance - req.amount)
        if (not (req.reqtype == ReqType.Query)):
            self.sentTrans.append(req)
        self.AccountInfo.update({req.account_num: new_balance})
        return [new_balance, outcome]

    def update_procTrans(self, reqID):
        len_sentTrans = len(self.sentTrans)
        for i in range(len_sentTrans):
            if (self.sentTrans[i].reqID == reqID):
                req = self.sentTrans[i]
                self.sentTrans.pop(i)
                if (req.reqtype == ReqType.Query):
                    break
                proc_req = self.procTrans.get(req.reqID)
                if (proc_req == None):
                    self.procTrans.update({req.reqID: req})
                    self.output(('Request %s has been added to processed transaction' % req.reqID))
                elif (req.reqtype == proc_req.reqtype):
                    self.output('Duplicate request, donot add to processed transaction')
                else:
                    self.output('Inconsistent With Histroy request, donot add to processed transaction')
                break

    def _Server_handler_1(self, req, src_id):
        seqNo = req[0]
        self.output((((('Request ' + str(req[1].reqID)) + ' from client received! ') + 'Sequnce No. is: ') + str(seqNo)))
        if (self.life_time > 0):
            self.life_time = (self.life_time - 1)
            self.output(('the current life_time is: ' + str(self.life_time)))
        elif (self.life_time == 0):
            self.output((('Server: ' + str(self.serverIP)) + ' has expired!'))
            sys.exit()
        result = self.proc_balance(req[1])
        new_balance = result[0]
        outcome = result[1]
        reply = Reply(req[1].reqID, outcome, new_balance)
        ack = Ack(req[1].reqID)
        if (self.prev == None):
            self._send(('REQ', req), self.next)
        elif (self.next == None):
            self.update_procTrans(req[1].reqID)
            self._send(('REPLY', reply), req[1].client_id)
            if (not (req[1].reqtype == ReqType.Query)):
                self._send(('ACK', ack), self.prev)
                self.output((str(ack) + ' has been sent!'))
        else:
            self._send(('REQ', req), self.next)
        self.output(('Reply for Request %s has been sent' % reply.reqID))
    _Server_handler_1._labels = None
    _Server_handler_1._notlabels = None

    def _Server_handler_2(self, ack, prev):
        self.output((str(ack) + ' has been received!'))
        self.update_procTrans(ack.reqID)
    _Server_handler_2._labels = None
    _Server_handler_2._notlabels = None

    def _Server_handler_3(self, next, prev, master):
        print("I'm the prev or next of the failed server, changing my prev and next...")
        self.prev = prev
        self.next = next
        print('Setting my prev to: ', self.prev, ' and my next to: ', self.next)
    _Server_handler_3._labels = None
    _Server_handler_3._notlabels = None

class Client(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_0', PatternExpr_8, sources=[PatternExpr_9], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_4]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_1', PatternExpr_10, sources=[PatternExpr_11], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_5]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_2', PatternExpr_12, sources=[PatternExpr_13], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_6])])

    def setup(self, bankName, account_no, clientIP, input_req, ifRetrans, timeout, nRetrans, ifRandom, master, head_srvs, tail_srvs):
        self.account_no = account_no
        self.timeout = timeout
        self.ifRetrans = ifRetrans
        self.master = master
        self.clientIP = clientIP
        self.input_req = input_req
        self.bankName = bankName
        self.ifRandom = ifRandom
        self.nRetrans = nRetrans
        self.tail_srvs = tail_srvs
        self.head_srvs = head_srvs
        self.bankName = int(self.bankName)
        self.account_no = self.account_no
        self.clientIP = self.clientIP
        self.requests = self.input_req
        self.ifRetrans = self.ifRetrans
        self.timeout = self.timeout
        self.nRetrans = self.nRetrans
        self.ifRandom = self.ifRandom
        self.master = self.master
        self.head_srvs = self.head_srvs
        self.tail_srvs = self.tail_srvs

    def main(self):
        self.output(((('Client: Bank Name is: ' + str(self.bankName)) + '  Account number is: ') + str(self.account_no)))
        reqList = self.init_req()
        num_req = len(reqList)
        for i in range(num_req):
            req = reqList[i]
            if (req[1].reqtype == ReqType.Query):
                dst = self.tail_srvs.get(self.bankName)
                print('DESTINATION the dst is', dst)
            else:
                dst = self.head_srvs.get(self.bankName)
                print('DESTINATION the dst is', dst)
            self.output((((('Request ' + str(req[1].reqID)) + ' has been sent out,') + 'sequence No. is: ') + str(req[0])))
            time.sleep(1)
            clk = self.logical_clock()
            self._send(('REQ', req), dst)
            _st_label_304 = 0
            self._timer_start()
            while (_st_label_304 == 0):
                _st_label_304 += 1
                if False:
                    pass
                    _st_label_304 += 1
                elif self._timer_expired:
                    self.output('waiting for reply TIMEDOUT!')
                    self.output(('Resending the request:' + str(req[1].reqID)))
                    i = (i - 1)
                    _st_label_304 += 1
                else:
                    super()._label('_st_label_304', block=True, timeout=self.timeout)
                    _st_label_304 -= 1
            else:
                if (_st_label_304 != 2):
                    continue
            if (_st_label_304 != 2):
                break

    def init_req(self):
        reqList = []
        client_id = self.id
        if (self.ifRandom == True):
            input_str = self.input_req[0]
            strs = parse_randomReq(input_str)
            seed_num = strs[0]
            num_req = strs[1]
            prob_query = strs[2]
            prob_deposit = strs[3]
            prob_withdraw = strs[4]
            prob_transfer = strs[5]
            random.seed(seed_num)
            for i in range(num_req):
                seqNo = (i + 1)
                a = random.randint(1, 100)
                a = float((a / 100))
                amount = (random.randint(1, 10) * 100)
                if (a < prob_query):
                    reqtype = ReqType.Query
                elif (a < (prob_query + prob_deposit)):
                    reqtype = ReqType.Deposit
                elif (a < ((prob_query + prob_deposit) + prob_withdraw)):
                    reqtype = ReqType.Withdraw
                else:
                    reqtype = ReqType.Transfer
                reqID = ((((str(self.bankName) + '.') + str(self.account_no[0])) + '.') + str((i + 1)))
                req = [seqNo, Request(reqID, reqtype, self.account_no, amount, client_id)]
                self.output(('Generating randomized request: ' + str(req)))
                reqList.append(req)
        else:
            num_req = len(self.input_req)
            seqNo = 0
            for i in range(num_req):
                strs = parse_req(self.input_req[i])
                if (strs[0].startswith(str(self.bankName)) and (int(strs[2]) == int(self.account_no))):
                    seqNo = (seqNo + 1)
                    req = [seqNo, Request(strs[0], strs[1], strs[2], strs[3], client_id)]
                    reqList.append(req)
                else:
                    pass
        return reqList

    def _Client_handler_4(self, reply, src_id):
        self.output(('Reply received from server: ' + str(reply)))
    _Client_handler_4._labels = None
    _Client_handler_4._notlabels = None

    def _Client_handler_5(self, newSrv, master):
        print('CLIENT ', self.id, 'CHANGING NEW HEAD: ', newSrv)
        self.head_srvs.update({self.bankName: newSrv})
    _Client_handler_5._labels = None
    _Client_handler_5._notlabels = None

    def _Client_handler_6(self, newSrv, master):
        print('SETTING NEW TAIL: ', newSrv)
        self.tail_srvs.update({self.bankName: newSrv})
    _Client_handler_6._labels = None
    _Client_handler_6._notlabels = None

def main():
    srvDic = collections.defaultdict(list)
    cliDic = collections.defaultdict(list)
    head_srvs = {}
    tail_srvs = {}
    da.api.config(channel='fifo', handling='all', clock='Lamport')
    flag_srv = False
    flag_cli = False
    flag_req = False
    flag_config = False
    input_srv = []
    input_cli = []
    input_req = []
    config_file = None
    if (len(sys.argv) < 2):
        print('Please input config file!')
        sys.exit()
    else:
        config_file = sys.argv[1]
    fp = open(config_file, 'r')
    for line in fp:
        if line.startswith('//Server'):
            flag_srv = True
            continue
        elif line.startswith('//Client '):
            flag_config = True
            input_str = fp.__next__()
            list_config = parse_config(input_str)
            continue
        elif line.startswith('//Client:'):
            flag_cli = True
            continue
        elif line.startswith('//Request'):
            flag_req = True
            continue
        elif ((flag_srv == True) and (flag_config == False)):
            input_srv.append(line)
        elif ((flag_cli == True) and (flag_req == False)):
            input_cli.append(line)
        elif ((flag_req == True) and (not (line == '\n'))):
            input_req.append(line)
        else:
            pass
    srvList = []
    for string in input_srv:
        srv = parse_server(string)
        srvList.append(srv)
    num_srv = len(input_srv)
    servers = list(da.api.new(Server, num=num_srv))
    bankName_srv = []
    serverIP = []
    startup_delay = []
    life_time = []
    for i in range(num_srv):
        bankName_srv.append(srvList[i][0])
        serverIP.append(srvList[i][1])
        startup_delay.append(srvList[i][2])
        life_time.append(srvList[i][3])
    for i in range(num_srv):
        if ((i == 0) or (not (bankName_srv[i] == bankName_srv[(i - 1)]))):
            prev = None
        else:
            prev = servers[(i - 1)]
        if ((i == (num_srv - 1)) or (not (bankName_srv[i] == bankName_srv[(i + 1)]))):
            next = None
        else:
            next = servers[(i + 1)]
        if (prev == None):
            head_srvs.update({bankName_srv[i]: servers[i]})
        elif (next == None):
            tail_srvs.update({bankName_srv[i]: servers[i]})
        srvDic[bankName_srv[i]].append([servers[i], prev, next, serverIP[i]])
    cliList = []
    for string in input_cli:
        cli = parse_client(string)
        cliList.append(cli)
    num_cli = len(input_cli)
    clients = list(da.api.new(Client, num=num_cli))
    bankName_cli = []
    account_no = []
    clientIP = []
    ifRetrans = list_config[0]
    timeout = list_config[1]
    nRetrans = list_config[2]
    ifRandom = list_config[3]
    for i in range(num_cli):
        bankName_cli.append(cliList[i][0])
        account_no.append(cliList[i][1])
        clientIP.append(cliList[i][2])
    for i in range(num_cli):
        cliDic[bankName_cli[i]].append(clients[i])
    print(cliDic)
    master = da.api.new(Master)
    da.api.setup(master, (srvDic, cliDic))
    da.api.start(master)
    for i in range(num_srv):
        if ((i == 0) or (not (bankName_srv[i] == bankName_srv[(i - 1)]))):
            prev = None
        else:
            prev = servers[(i - 1)]
        if ((i == (num_srv - 1)) or (not (bankName_srv[i] == bankName_srv[(i + 1)]))):
            next = None
        else:
            next = servers[(i + 1)]
        da.api.setup(servers[i], (bankName_srv[i], serverIP[i], startup_delay[i], life_time[i], prev, next, master))
    da.api.start(servers)
    for i in range(num_cli):
        da.api.setup(clients[i], (bankName_cli[i], account_no[i], clientIP[i], input_req, ifRetrans, timeout, nRetrans, ifRandom, master, head_srvs, tail_srvs))
    da.api.start(clients)
