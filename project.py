
import da
PatternExpr_0 = da.pat.TuplePattern([da.pat.ConstantPattern('PING'), da.pat.FreePattern('ping')])
PatternExpr_1 = da.pat.FreePattern('src_id')
PatternExpr_2 = da.pat.TuplePattern([da.pat.ConstantPattern('REQ'), da.pat.FreePattern('req')])
PatternExpr_3 = da.pat.FreePattern('src_id')
PatternExpr_4 = da.pat.TuplePattern([da.pat.ConstantPattern('SYNC'), da.pat.FreePattern('req')])
PatternExpr_5 = da.pat.FreePattern('src_id')
PatternExpr_6 = da.pat.TuplePattern([da.pat.ConstantPattern('SYNC_PROC'), da.pat.TuplePattern([da.pat.FreePattern('reqID'), da.pat.FreePattern('req')])])
PatternExpr_7 = da.pat.FreePattern('src_id')
PatternExpr_8 = da.pat.TuplePattern([da.pat.ConstantPattern('ACK'), da.pat.FreePattern('ack')])
PatternExpr_9 = da.pat.FreePattern('next')
PatternExpr_10 = da.pat.TuplePattern([da.pat.ConstantPattern('srvFail'), da.pat.TuplePattern([da.pat.FreePattern('prev'), da.pat.FreePattern('next')])])
PatternExpr_11 = da.pat.FreePattern('master')
PatternExpr_12 = da.pat.TuplePattern([da.pat.ConstantPattern('extendChain'), da.pat.FreePattern('newSrv')])
PatternExpr_13 = da.pat.FreePattern('master')
PatternExpr_14 = da.pat.TuplePattern([da.pat.ConstantPattern('new_server_join'), da.pat.FreePattern('newprev')])
PatternExpr_15 = da.pat.FreePattern('master')
PatternExpr_16 = da.pat.TuplePattern([da.pat.ConstantPattern('REPLY'), da.pat.FreePattern('reply')])
PatternExpr_17 = da.pat.FreePattern('src_id')
PatternExpr_18 = da.pat.TuplePattern([da.pat.ConstantPattern('newHead'), da.pat.FreePattern('newSrv')])
PatternExpr_19 = da.pat.FreePattern('master')
PatternExpr_20 = da.pat.TuplePattern([da.pat.ConstantPattern('newTail'), da.pat.FreePattern('newSrv')])
PatternExpr_21 = da.pat.FreePattern('master')
PatternExpr_22 = da.pat.TuplePattern([da.pat.ConstantPattern('srvFail'), da.pat.FreePattern('newSrv')])
PatternExpr_23 = da.pat.FreePattern('master')
PatternExpr_24 = da.pat.TuplePattern([da.pat.ConstantPattern('REPLY'), da.pat.FreePattern('reply')])
PatternExpr_25 = da.pat.FreePattern('dst')
PatternExpr_26 = da.pat.FreePattern('rclk')
PatternExpr_28 = da.pat.TuplePattern([da.pat.ConstantPattern('newTail'), da.pat.FreePattern('newSrv')])
PatternExpr_29 = da.pat.FreePattern('master')
PatternExpr_30 = da.pat.FreePattern('rclk')
PatternExpr_32 = da.pat.TuplePattern([da.pat.ConstantPattern('newHead'), da.pat.FreePattern('newSrv')])
PatternExpr_33 = da.pat.FreePattern('master')
PatternExpr_34 = da.pat.FreePattern('rclk')
PatternExpr_36 = da.pat.TuplePattern([da.pat.ConstantPattern('srvFail'), da.pat.FreePattern('newSrv')])
PatternExpr_37 = da.pat.FreePattern('master')
PatternExpr_38 = da.pat.FreePattern('rclk')
PatternExpr_40 = da.pat.TuplePattern([da.pat.ConstantPattern('REPLY'), da.pat.FreePattern('reply')])
PatternExpr_41 = da.pat.FreePattern('dst')
PatternExpr_42 = da.pat.FreePattern('rclk')
PatternExpr_44 = da.pat.TuplePattern([da.pat.ConstantPattern('REPLY'), da.pat.FreePattern('reply')])
PatternExpr_45 = da.pat.FreePattern('dst')
PatternExpr_46 = da.pat.FreePattern('rclk')
import re
import time
import sys
import collections
import logging
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
    time_delay = int(strs[4])
    return [retrans, retrans_interval, retrans_time, ifRandom, time_delay]

def parse_server(input_str):
    input_str = input_str.strip()
    input_str = input_str.replace(' ', '')
    str = input_str.split(',')
    bankName = int(str[0])
    serverIP = str[1]
    startup_delay = int(str[2])
    life_time = str[3]
    message_loss = int(str[4])
    return [bankName, serverIP, startup_delay, life_time, message_loss]

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

    def setup(self, srvDic, cliDic, filename, waitList):
        self.srvDic = srvDic
        self.waitList = waitList
        self.cliDic = cliDic
        self.filename = filename
        self.timesheet = {}
        self.srvDict = self.srvDic
        self.cliDict = self.cliDic
        self.filename = self.filename
        self.waitList = self.waitList
        self.filename = self.filename
        self.setup_logfile(self.filename)

    def main(self):
        self.output((('Master  ' + str(self.id)) + '  has started.'))
        self.output(('Server Dictory Stored in Master: ' + str(self.srvDict)))
        self.output(('Client Dictory Stored in Master: ' + str(self.cliDict)))
        self.output(('Server Waitinglist Stored in Master: ' + str(self.waitList)))
        while True:
            _st_label_181 = 0
            self._timer_start()
            while (_st_label_181 == 0):
                _st_label_181 += 1
                if False:
                    pass
                    _st_label_181 += 1
                elif self._timer_expired:
                    self.checkSrv()
                    _st_label_181 += 1
                else:
                    super()._label('_st_label_181', block=True, timeout=5)
                    _st_label_181 -= 1
            else:
                if (_st_label_181 != 2):
                    continue
            if (_st_label_181 != 2):
                break

    def setup_logfile(self, filename):
        rootlog = logging.getLogger('')
        filelvl = logging.INFO
        fh = logging.FileHandler(filename)
        formatter = logging.Formatter('[%(asctime)s]%(name)s: %(message)s')
        fh.setFormatter(formatter)
        fh.setLevel(filelvl)
        rootlog._filelvl = filelvl
        rootlog.addHandler(fh)

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
                self._send(('newHead', newSrv), cli)
            elif (type == 'tail'):
                self._send(('newTail', newSrv), cli)
            elif (type == 'srvFail'):
                self._send(('srvFail', newSrv), cli)

    def updateSrvInfo(self, srv):
        port = srv[0]
        bankName = srv[1]
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
                    self.output('Sending new tail notification to client!')
                elif ((not (prev == None)) and (not (next == None))):
                    self.infoCli(bankName, 'srvFail', None)
                    self.output('Sending server fail notification to client!')
        for item in self.srvDict[bankName]:
            if ((item[0] == prev) or (item[0] == next)):
                self._send(('srvFail', (item[1], item[2])), item[0])
                self.output('Sending server fail notification to server!')
            else:
                pass

    def checkSrv(self):
        cur_ticks = time.time()
        self.output(self.timesheet)
        failedSrv = []
        for key in self.timesheet.keys():
            if ((cur_ticks - self.timesheet.get(key)) > 5):
                self.output((('Master has detected that Server ' + str(key[0])) + ' has failed!'))
                failedSrv.append(key)
        for srv in failedSrv:
            del self.timesheet[srv]
            self.updateSrvInfo(srv)

    def _Master_handler_0(self, ping, src_id):
        cur_ticks = time.time()
        flag = False
        self.output(('Received PING from: ' + str(ping.serverIP)))
        bankname = ping.bankName
        new_tail = None
        for item in self.srvDict[bankname]:
            if (ping.serverIP == item[3]):
                flag = True
                self.timesheet.update({(ping.serverIP, ping.bankName): cur_ticks})
            else:
                pass
        if (flag == False):
            for item in self.waitList:
                if (ping.serverIP == item[4]):
                    new_tail = item
                    self.output((('Server requested extending chain, adding new server ' + str(item[4])) + ' to srvDic'))
                    self.srvDict[item[0]].append([item[1], item[2], item[3], item[4]])
                    self.waitList.remove(item)
                    self.flush_srvDict(bankname)
                    self.timesheet.update({(ping.serverIP, ping.bankName): cur_ticks})
                    self.output(('The current srvDic after chain extension is: ' + str(self.srvDict)))
        if (not (new_tail == None)):
            self.infoCli(bankname, 'tail', new_tail[1])
            for item in self.srvDict[bankname]:
                if (item[2] == new_tail[1]):
                    self._send(('extendChain', item[2]), item[0])
                if (item[0] == new_tail[1]):
                    self._send(('new_server_join', item[1]), item[0])
            self.output('Server notification has been sent')
    _Master_handler_0._labels = None
    _Master_handler_0._notlabels = None

class Server(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_0', PatternExpr_2, sources=[PatternExpr_3], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_1]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_1', PatternExpr_4, sources=[PatternExpr_5], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_2]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_2', PatternExpr_6, sources=[PatternExpr_7], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_3]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_3', PatternExpr_8, sources=[PatternExpr_9], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_4]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_4', PatternExpr_10, sources=[PatternExpr_11], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_5]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_5', PatternExpr_12, sources=[PatternExpr_13], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_6]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_6', PatternExpr_14, sources=[PatternExpr_15], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_7])])

    def setup(self, bankName, serverIP, startup_delay, life_time, message_loss, prev, next, master, filename):
        self.startup_delay = startup_delay
        self.filename = filename
        self.prev = prev
        self.serverIP = serverIP
        self.master = master
        self.next = next
        self.life_time = life_time
        self.bankName = bankName
        self.message_loss = message_loss
        self.bankName = self.bankName
        self.serverIP = self.serverIP
        self.startup_delay = self.startup_delay
        self.life_time = int(self.life_time)
        self.message_loss = self.message_loss
        self.prev = self.prev
        self.next = self.next
        self.master = self.master
        self.sentTrans = []
        self.procTrans = {}
        self.AccountInfo = {}
        self.filename = self.filename
        self.recTimes = 0
        self.setup_logfile(self.filename)

    def main(self):
        time.sleep(self.startup_delay)
        self.output(((((((((('Server: Bank Name is: ' + str(self.bankName)) + '  Server IP is: ') + str(self.serverIP)) + '  Life time is: ') + str(self.life_time)) + '  Previous server is: ') + str(self.prev)) + '  Next server is: ') + str(self.next)))
        ping = Ping(self.serverIP, self.bankName)
        while True:
            _st_label_349 = 0
            self._timer_start()
            while (_st_label_349 == 0):
                _st_label_349 += 1
                if False:
                    pass
                    _st_label_349 += 1
                elif self._timer_expired:
                    self._send(('PING', ping), self.master)
                    _st_label_349 += 1
                else:
                    super()._label('_st_label_349', block=True, timeout=1)
                    _st_label_349 -= 1
            else:
                if (_st_label_349 != 2):
                    continue
            if (_st_label_349 != 2):
                break

    def setup_logfile(self, filename):
        rootlog = logging.getLogger('')
        filelvl = logging.INFO
        fh = logging.FileHandler(filename)
        formatter = logging.Formatter('[%(asctime)s]%(name)s: %(message)s')
        fh.setFormatter(formatter)
        fh.setLevel(filelvl)
        rootlog._filelvl = filelvl
        rootlog.addHandler(fh)

    def proc_balance(self, ack):
        outcome = Outcome.Processed
        if (self.AccountInfo.get(ack.account_num) == None):
            cur_balance = 0
        else:
            cur_balance = self.AccountInfo[ack.account_num]
        if (not (self.procTrans.get(ack.reqID) == None)):
            if (not (self.procTrans[ack.reqID].reqtype == ack.reqtype)):
                outcome = Outcome.InconsistentWithHistory
            else:
                pass
            new_balance = cur_balance
        elif (ack.reqtype == ReqType.Query):
            new_balance = cur_balance
        elif (ack.reqtype == ReqType.Deposit):
            new_balance = (cur_balance + ack.amount)
        elif (ack.reqtype == ReqType.Withdraw):
            if ((cur_balance - ack.amount) < 0):
                new_balance = cur_balance
                outcome = Outcome.InsufficientFunds
            else:
                new_balance = (cur_balance - ack.amount)
        self.AccountInfo.update({ack.account_num: new_balance})
        return [new_balance, outcome]

    def update_procTrans(self, reqID):
        count_clear = 0
        len_sentTrans = len(self.sentTrans)
        del_list = []
        for i in range(len_sentTrans):
            if (self.sentTrans[i].reqID == reqID):
                req = self.sentTrans[i]
                del_list.append(req)
                if (not (count_clear == 0)):
                    self.output('Using ACK to clear old req ', reqID)
                count_clear += 1
                if (req.reqtype == ReqType.Query):
                    break
                proc_req = self.procTrans.get(req.reqID)
                if (proc_req == None):
                    self.procTrans.update({req.reqID: req})
                    self.output((('Request ' + str(req.reqID)) + ' has been added to processed transaction'))
                elif (req.reqtype == proc_req.reqtype):
                    self.output("Duplicate request, don't add to processed transaction")
                else:
                    self.output("Inconsistent With Histroy request, don't add to processed transaction")
        for i in range(len(del_list)):
            for j in range(len(self.sentTrans)):
                if (del_list[i].reqID == self.sentTrans[j].reqID):
                    self.sentTrans.pop(j)
                    break

    def search_procTrans(self, reqID):
        proc_req = self.procTrans.get(reqID)
        if (proc_req == None):
            return False
        else:
            return True

    def _Server_handler_1(self, src_id, req):
        if (not (src_id == self.prev)):
            self.recTimes += 1
            if ((self.recTimes <= self.message_loss) or (self.message_loss == 0)):
                self.output((('Request ' + str(req.reqID)) + ' from client received! '))
            else:
                self.output(('Packet loss, request ' + str(req.reqID)))
                self.recTimes = 0
                return
        if (self.life_time > 0):
            self.life_time = (self.life_time - 1)
            self.output(('The current life_time is: ' + str(self.life_time)))
        elif (self.life_time == 0):
            self.output((('Server: ' + str(self.serverIP)) + ' has expired!'))
            sys.exit()
        if (not (req.reqtype == ReqType.Query)):
            self.sentTrans.append(req)
            self.output(('Request %s has been added to sent transaction' % req.reqID))
        if (self.next == None):
            ack = Ack(req.reqID, req.reqtype, req.account_num, req.amount)
            result = self.proc_balance(ack)
            new_balance = result[0]
            outcome = result[1]
            reply = Reply(req.reqID, outcome, new_balance)
            search_result = self.search_procTrans(req.reqID)
            self.update_procTrans(req.reqID)
            if ((search_result == False) or ((search_result == True) and (not (outcome == Outcome.Processed)))):
                self._send(('REPLY', reply), req.client_id)
                self.output(((('Reply for Request ' + str(req.reqID)) + ' has been sent to client: ') + str(req.client_id)))
                if (not (req.reqtype == ReqType.Query)):
                    self._send(('ACK', ack), self.prev)
                    self.output((str(ack) + ' has been sent!'))
        else:
            self._send(('REQ', req), self.next)
    _Server_handler_1._labels = None
    _Server_handler_1._notlabels = None

    def _Server_handler_2(self, req, src_id):
        self.output('Synchronization of sentTrans from previous server received! ReqID is ', req.reqID)
        if (not (req.reqtype == ReqType.Query)):
            self.sentTrans.append(req)
            search_result = self.search_procTrans(req.reqID)
            if (search_result == True):
                ack = Ack(req.reqID, req.reqtype, req.account_num, req.amount)
                self._send(('ACK', ack), self.prev)
        self.output(('Request %s has been added to sent transaction' % req.reqID))
        if (not (self.next == None)):
            self._send(('SYNC', req), self.next)
    _Server_handler_2._labels = None
    _Server_handler_2._notlabels = None

    def _Server_handler_3(self, req, reqID, src_id):
        self.output(('Synchronization of procTrans from the old tail ' + str(reqID)))
        if (not (req.reqtype == ReqType.Query)):
            ack = Ack(req.reqID, req.reqtype, req.account_num, req.amount)
            self.sentTrans.append(req)
            result = self.proc_balance(ack)
            self.update_procTrans(reqID)
            self.output(((('Account: ' + str(ack.account_num)) + ' New balance is: ') + str(result[0])))
        if (not (self.next == None)):
            self._send(('SYNC_PROC', (reqID, req)), self.next)
    _Server_handler_3._labels = None
    _Server_handler_3._notlabels = None

    def _Server_handler_4(self, next, ack):
        self.output((str(ack) + ' has been received!'))
        search_result = self.search_procTrans(ack.reqID)
        result = self.proc_balance(ack)
        self.output(((('Account: ' + str(ack.account_num)) + ' New balance is: ') + str(result[0])))
        self.update_procTrans(ack.reqID)
        if ((not (self.prev == None)) and (search_result == False)):
            self._send(('ACK', ack), self.prev)
    _Server_handler_4._labels = None
    _Server_handler_4._notlabels = None

    def _Server_handler_5(self, next, prev, master):
        self.prev = prev
        self.next = next
        self.output((((' Received SrvFail from Master, Setting my prev to: ' + str(self.prev)) + ' and my next to: ') + str(self.next)))
        if (not (self.next == None)):
            for i in range(len(self.sentTrans)):
                req = self.sentTrans[i]
                self.output(('Starting synchronize %s sentTrans to new next server' % req.reqID))
                self._send(('SYNC', req), self.next)
            for (reqID, req) in self.procTrans.items():
                self.output(('Starting synchronize %s procTrans to the new next server ' % reqID))
                self._send(('SYNC_PROC', (reqID, req)), self.next)
        else:
            self.output("I'm the new tail!")
    _Server_handler_5._labels = None
    _Server_handler_5._notlabels = None

    def _Server_handler_6(self, master, newSrv):
        self.output(((str(self.serverIP) + ' Received extendChain from master,setting my next to ') + str(newSrv)))
        self.next = newSrv
        for (reqID, req) in self.procTrans.items():
            self.output(('Starting synchronize %s procTrans to the new tail ' % reqID))
            self._send(('SYNC_PROC', (reqID, req)), self.next)
    _Server_handler_6._labels = None
    _Server_handler_6._notlabels = None

    def _Server_handler_7(self, newprev, master):
        self.output((" I'm the new joined server,setting my prev to " + str(newprev)))
        self.prev = newprev
        self.next = None
    _Server_handler_7._labels = None
    _Server_handler_7._notlabels = None

class Client(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._ClientReceivedEvent_4 = []
        self._ClientReceivedEvent_5 = []
        self._ClientReceivedEvent_6 = []
        self._ClientReceivedEvent_7 = []
        self._ClientReceivedEvent_8 = []
        self._ClientReceivedEvent_9 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_0', PatternExpr_16, sources=[PatternExpr_17], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_8]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_1', PatternExpr_18, sources=[PatternExpr_19], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_9]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_2', PatternExpr_20, sources=[PatternExpr_21], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_10]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_3', PatternExpr_22, sources=[PatternExpr_23], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_11]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_4', PatternExpr_24, sources=[PatternExpr_25], destinations=None, timestamps=[PatternExpr_26], record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_5', PatternExpr_28, sources=[PatternExpr_29], destinations=None, timestamps=[PatternExpr_30], record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_6', PatternExpr_32, sources=[PatternExpr_33], destinations=None, timestamps=[PatternExpr_34], record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_7', PatternExpr_36, sources=[PatternExpr_37], destinations=None, timestamps=[PatternExpr_38], record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_8', PatternExpr_40, sources=[PatternExpr_41], destinations=None, timestamps=[PatternExpr_42], record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_9', PatternExpr_44, sources=[PatternExpr_45], destinations=None, timestamps=[PatternExpr_46], record_history=True, handlers=[])])

    def setup(self, bankName, account_no, clientIP, input_req, ifRetrans, timeout, nRetrans, ifRandom, time_delay, master, head_srvs, tail_srvs, filename):
        self.ifRetrans = ifRetrans
        self.timeout = timeout
        self.ifRandom = ifRandom
        self.time_delay = time_delay
        self.filename = filename
        self.nRetrans = nRetrans
        self.account_no = account_no
        self.master = master
        self.tail_srvs = tail_srvs
        self.clientIP = clientIP
        self.bankName = bankName
        self.input_req = input_req
        self.head_srvs = head_srvs
        self.bankName = int(self.bankName)
        self.account_no = self.account_no
        self.clientIP = self.clientIP
        self.requests = self.input_req
        self.ifRetrans = self.ifRetrans
        self.timeout = self.timeout
        self.nRetrans = self.nRetrans
        self.ifRandom = self.ifRandom
        self.time_delay = self.time_delay
        self.master = self.master
        self.head_srvs = self.head_srvs
        self.tail_srvs = self.tail_srvs
        self.replyDic = {}
        self.filename = self.filename
        self.setup_logfile(self.filename)

    def main(self):
        self.output(((('Client: Bank Name is: ' + str(self.bankName)) + '  Account number is: ') + str(self.account_no)))
        reqList = self.init_req()
        replyNum = 0
        num_req = len(reqList)
        for i in range(num_req):
            req = reqList[i]
            if (req.reqtype == ReqType.Query):
                dst = self.tail_srvs.get(self.bankName)
            else:
                dst = self.head_srvs.get(self.bankName)
            self.output((('Request ' + str(req.reqID)) + ' has been sent out'))
            time.sleep(self.time_delay)
            clk = self.logical_clock()
            self._send(('REQ', req), dst)
            rclk = reply = dst = None

            def ExistentialOpExpr_4():
                nonlocal rclk, reply, dst
                for (_, (rclk, _, dst), (_ConstantPattern120_, reply)) in self._ClientReceivedEvent_8:
                    if (_ConstantPattern120_ == 'REPLY'):
                        if (rclk > clk):
                            return True
                return False
            _st_label_462 = 0
            self._timer_start()
            while (_st_label_462 == 0):
                _st_label_462 += 1
                if ExistentialOpExpr_4():
                    self.replyDic.update({reply.reqID: reply})
                    continue
                    _st_label_462 += 1
                elif self._timer_expired:
                    self.output((('Client waiting for reply ' + str(req.reqID)) + ' TIMEDOUT!'))
                    self.resend(req)
                    _st_label_462 += 1
                else:
                    super()._label('_st_label_462', block=True, timeout=self.timeout)
                    _st_label_462 -= 1
            else:
                if (_st_label_462 != 2):
                    continue
            if (_st_label_462 != 2):
                break
        while (len(self.replyDic) < num_req):
            clk = self.logical_clock()
            reply = rclk = dst = None

            def ExistentialOpExpr_5():
                nonlocal reply, rclk, dst
                for (_, (rclk, _, dst), (_ConstantPattern134_, reply)) in self._ClientReceivedEvent_9:
                    if (_ConstantPattern134_ == 'REPLY'):
                        if (rclk > clk):
                            return True
                return False
            _st_label_469 = 0
            while (_st_label_469 == 0):
                _st_label_469 += 1
                if ExistentialOpExpr_5():
                    self.replyDic.update({reply.reqID: reply})
                    continue
                    _st_label_469 += 1
                elif self._timer_expired:
                    pass
                    _st_label_469 += 1
                else:
                    super()._label('_st_label_469', block=True)
                    _st_label_469 -= 1
            else:
                if (_st_label_469 != 2):
                    continue
            if (_st_label_469 != 2):
                break
        self.output('All request has been sentout, client exits')

    def setup_logfile(self, filename):
        rootlog = logging.getLogger('')
        filelvl = logging.INFO
        fh = logging.FileHandler(filename)
        formatter = logging.Formatter('[%(asctime)s]%(name)s: %(message)s')
        fh.setFormatter(formatter)
        fh.setLevel(filelvl)
        rootlog._filelvl = filelvl
        rootlog.addHandler(fh)

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
                req = Request(reqID, reqtype, self.account_no, amount, client_id)
                self.output(('Generating randomized request: ' + str(req)))
                reqList.append(req)
        else:
            num_req = len(self.input_req)
            for i in range(num_req):
                strs = parse_req(self.input_req[i])
                if (strs[0].startswith(str(self.bankName)) and (int(strs[2]) == int(self.account_no))):
                    req = Request(strs[0], strs[1], strs[2], strs[3], client_id)
                    reqList.append(req)
                else:
                    pass
        return reqList

    def resend(self, req):
        times = 0
        while True:
            self.output('Start retransmitting Request ', req.reqID)
            time.sleep(self.time_delay)
            clk = self.logical_clock()
            if (req.reqtype == ReqType.Query):
                dst = self.tail_srvs.get(self.bankName)
            else:
                dst = self.head_srvs.get(self.bankName)
            self._send(('REQ', req), dst)
            dst = reply = rclk = None

            def ExistentialOpExpr_0():
                nonlocal dst, reply, rclk
                for (_, (rclk, _, dst), (_ConstantPattern64_, reply)) in self._ClientReceivedEvent_4:
                    if (_ConstantPattern64_ == 'REPLY'):
                        if (rclk > clk):
                            return True
                return False
            rclk = newSrv = master = None

            def ExistentialOpExpr_1():
                nonlocal rclk, newSrv, master
                for (_, (rclk, _, master), (_ConstantPattern78_, newSrv)) in self._ClientReceivedEvent_5:
                    if (_ConstantPattern78_ == 'newTail'):
                        if (rclk > clk):
                            return True
                return False
            master = newSrv = rclk = None

            def ExistentialOpExpr_2():
                nonlocal master, newSrv, rclk
                for (_, (rclk, _, master), (_ConstantPattern92_, newSrv)) in self._ClientReceivedEvent_6:
                    if (_ConstantPattern92_ == 'newHead'):
                        if (rclk > clk):
                            return True
                return False
            master = rclk = newSrv = None

            def ExistentialOpExpr_3():
                nonlocal master, rclk, newSrv
                for (_, (rclk, _, master), (_ConstantPattern106_, newSrv)) in self._ClientReceivedEvent_7:
                    if (_ConstantPattern106_ == 'srvFail'):
                        if (rclk > clk):
                            return True
                return False
            _st_label_436 = 0
            self._timer_start()
            while (_st_label_436 == 0):
                _st_label_436 += 1
                if ExistentialOpExpr_0():
                    break
                    _st_label_436 += 1
                elif ExistentialOpExpr_1():
                    times = 0
                    continue
                    _st_label_436 += 1
                elif ExistentialOpExpr_2():
                    times = 0
                    continue
                    _st_label_436 += 1
                elif ExistentialOpExpr_3():
                    times = 0
                    continue
                    _st_label_436 += 1
                elif self._timer_expired:
                    times += 1
                    if (times == self.nRetrans):
                        self.output(('Retransmit time equals the RetransLimit, stop retransmitting Request ' + str(req.reqID)))
                        break
                    _st_label_436 += 1
                else:
                    super()._label('_st_label_436', block=True, timeout=self.timeout)
                    _st_label_436 -= 1
            else:
                if (_st_label_436 != 2):
                    continue
            if (_st_label_436 != 2):
                break

    def _Client_handler_8(self, src_id, reply):
        self.output(('Reply received from server: ' + str(reply)))
    _Client_handler_8._labels = None
    _Client_handler_8._notlabels = None

    def _Client_handler_9(self, master, newSrv):
        self.output(('Client setting new head: ' + str(newSrv)))
        self.head_srvs.update({self.bankName: newSrv})
    _Client_handler_9._labels = None
    _Client_handler_9._notlabels = None

    def _Client_handler_10(self, newSrv, master):
        self.output(('Client setting new tail: ' + str(newSrv)))
        self.tail_srvs.update({self.bankName: newSrv})
        time.sleep(self.time_delay)
    _Client_handler_10._labels = None
    _Client_handler_10._notlabels = None

    def _Client_handler_11(self, newSrv, master):
        self.output('Client received server fail from Master, starting to sleep.')
        time.sleep(self.time_delay)
    _Client_handler_11._labels = None
    _Client_handler_11._notlabels = None

def main():
    srvDic = collections.defaultdict(list)
    cliDic = collections.defaultdict(list)
    waitList = []
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
    message_loss = []
    for i in range(num_srv):
        bankName_srv.append(srvList[i][0])
        serverIP.append(srvList[i][1])
        startup_delay.append(srvList[i][2])
        life_time.append(srvList[i][3])
        message_loss.append(srvList[i][4])
    for i in range(num_srv):
        if ((i == 0) or (not (bankName_srv[i] == bankName_srv[(i - 1)]))):
            prev = None
        else:
            prev = servers[(i - 1)]
        if ((i == (num_srv - 1)) or (not (bankName_srv[i] == bankName_srv[(i + 1)])) or (not (startup_delay[(i + 1)] == 0))):
            next = None
        else:
            next = servers[(i + 1)]
        if ((prev == None) and (startup_delay[i] == 0)):
            head_srvs.update({bankName_srv[i]: servers[i]})
        elif ((next == None) and (startup_delay[i] == 0)):
            tail_srvs.update({bankName_srv[i]: servers[i]})
        if (startup_delay[i] == 0):
            srvDic[bankName_srv[i]].append([servers[i], prev, next, serverIP[i]])
        else:
            waitList.append([bankName_srv[i], servers[i], prev, next, serverIP[i]])
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
    time_delay = list_config[4]
    for i in range(num_cli):
        bankName_cli.append(cliList[i][0])
        account_no.append(cliList[i][1])
        clientIP.append(cliList[i][2])
    for i in range(num_cli):
        cliDic[bankName_cli[i]].append(clients[i])
    filename_master = './master_log'
    filename_server = './server/server_log'
    filename_client = './client/client_log'
    master = da.api.new(Master)
    da.api.setup(master, (srvDic, cliDic, filename_master, waitList))
    da.api.start(master)
    for i in range(num_srv):
        server_name = (filename_server + str((i + 1)))
        if ((i == 0) or (not (bankName_srv[i] == bankName_srv[(i - 1)]))):
            prev = None
        else:
            prev = servers[(i - 1)]
        if ((i == (num_srv - 1)) or (not (bankName_srv[i] == bankName_srv[(i + 1)])) or (not (startup_delay[(i + 1)] == 0))):
            next = None
        else:
            next = servers[(i + 1)]
        da.api.setup(servers[i], (bankName_srv[i], serverIP[i], startup_delay[i], life_time[i], message_loss[i], prev, next, master, server_name))
    da.api.start(servers)
    for i in range(num_cli):
        client_name = (filename_client + str((i + 1)))
        da.api.setup(clients[i], (bankName_cli[i], account_no[i], clientIP[i], input_req, ifRetrans, timeout, nRetrans, ifRandom, time_delay, master, head_srvs, tail_srvs, client_name))
    da.api.start(clients)
