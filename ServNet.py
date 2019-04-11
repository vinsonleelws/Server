# !/usr/bin/python
# coding:utf-8

from socket import *
import threading
import struct
from Sys import GetTimeStamp
import Conn
import ProtocolBase
import HandleConnMsg, HandlePlayerEvent, HandlePlayerMsg
import traceback


class ServNet(object):
    # lock = threading.Lock()

    def __init__(self):
        self.listener = None
        self.conns = []
        self.maxConn = 50
        self.timer = threading.Timer(1, self.HandleMainTimer)
        self.heartBeatTime = 180  # 180 (3 minutes)
        self.proto = ProtocolBase.ProtocolBase()
        self.handleConnMsg = HandleConnMsg.HandleConnMsg()
        self.handlePlayerMsg = HandlePlayerMsg.HandlePlayerMsg()
        self.handlePlayerEvent = HandlePlayerEvent.HandlePlayerEvent()

    def NewIndex(self):
        if not self.conns:
            return -1
        for i in xrange(len(self.conns)):
            if self.conns[i] is None:
                self.conns[i] = Conn.Conn()
                return i
            else:
                if self.conns[i].isUse is False:
                    return i
        return -1

    def Start(self, host, port):
        self.timer.start()
        self.conns = [None] * self.maxConn
        # Socket
        self.listener = socket(AF_INET, SOCK_STREAM)
        self.listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        # Bind
        self.listener.bind((host, port))
        # Listen
        self.listener.listen(self.maxConn)
        # Accept
        print "Server Launched Successfully."
        while True:
            newSocket, destAddr = self.listener.accept()
            client = threading.Thread(target=self.AcceptCb, args=(newSocket, destAddr))
            client.start()

    def AcceptCb(self, newSocket, destAddr):
        try:
            index = self.NewIndex()
            if index < 0:
                newSocket.close()
                print "[ServNet] AcceptCb Warning: Too many connections."
            else:
                conn = self.conns[index]
                conn.Init(newSocket)
                conn.address = destAddr[0] + ':' + str(destAddr[1])
                print "Client from [" + conn.address + "]  -  Conn pool ID: " + str(index)
                # Receives
                self.ReceiveCb(conn)
        except Exception as e:
            print "[ServNet] AcceptCb failed. ", e.message

    def Close(self):
        print "Closing ServNet"
        for i in xrange(len(self.conns)):
            if self.conns[i] is None:
                continue
            if not self.conns[i].isUse:
                continue
            lock = threading.Lock()
            with lock:
                self.conns[i].Close()

    def ReceiveCb(self, conn):
        lock = threading.Lock()
        with lock:
            try:
                conn.readBuff = conn.socket.recv(Conn.BUFFER_SIZE)
                count = len(conn.readBuff)
                if count <= 0:
                    print "[ServNet] ReceiveCb: No data received from [" + conn.GetAddress() + "]. Disconnected."
                    conn.Close()
                    return
                conn.buffCount += count
                self.ProcessData(conn)
                # Continues receiving data
                self.ReceiveCb(conn)
            except Exception as e:
                if conn.isUse:
                    print "[ServNet] ReceiveCb Exception. " + conn.GetAddress() + " Disconnected. " + e.message
                    traceback.print_exc()
                    conn.Close()

    def ProcessData(self, conn):
        if conn.buffCount < 4:  # sizeof(Int32)
            return

        conn.lenBytes = conn.readBuff[:4]
        conn.msgLength = struct.unpack('<I', conn.lenBytes)[0]
        if conn.buffCount < conn.msgLength + 4:
            return
        # Handles message
        # data = conn.readBuff[4:].decode('utf-8')
        # print "Received from [" + conn.GetAddress() + "]: " + data
        # if data == "HeatBeat":
        #     conn.lastTickTime = GetTimeStamp()
        # print "[ProcessData] Received from [" + conn.GetAddress() + "]:", repr(conn.readBuff)
        # print "Message from [" + conn.GetAddress() + "]. " + "Length:", conn.msgLength, "  Content:", repr(conn.readBuff[4:])
        protocol = self.proto.Decode(conn.readBuff, 4, conn.msgLength)
        self.HandleMsg(conn, protocol)
        # Cleans up the processed message
        count = conn.buffCount - conn.msgLength - 4
        conn.readBuff = conn.readBuff[4 + conn.msgLength:]
        conn.buffCount = count
        if conn.buffCount > 0:
            self.ProcessData(conn)

    def HandleMsg(self, conn, protoBase):
        name = protoBase.GetName()
        methodName = "Msg" + name
        # print "[HandleMsg] Method name:", methodName
        # Connection protocol distribution
        if (conn.player is None) or (name == "HeatBeat") or (name == "Logout"):
            method = getattr(self.handleConnMsg, methodName, None)
            if method is None:
                print "[ServNet] HandleMsg Warning: 'HandleConnMsg' does not have the method", methodName, "!"
                return
            else:
                # print "Handles connection message from [" + conn.GetAddress() + "].  Protocol: " + name
                method(conn, protoBase)
        else:
        # Player protocol distribution
            method = getattr(self.handlePlayerMsg, methodName, None)
            if method is None:
                print "[ServNet] HandleMsg Warning: HandlePlayerMsg does not have the method", methodName, "!"
                return
            else:
                # print "Handles player message.  id='" + conn.player.id + "'.  Protocol: " + name
                method(conn.player, protoBase)
        # print "[HandleMsg] Receives protocol: " + (name if name else "None")
        # # Handles HeartBeat
        # if name == "HeatBeat":
        #     print "Update heartBeatTime for [" + conn.GetAddress() + "]"
        #     conn.lastTickTime = GetTimeStamp()
        # # Sends back
        # self.Send(conn, protoBase)

    def Send(self, conn, protocol):
        # bytes = bytearray(string, 'utf-8')
        bytes = protocol.Encode()
        length = struct.pack('<I', len(bytes))
        sendBuff = length + bytes
        try:
            # print "[ServNet] Sending back: " + repr(sendBuff)
            print "[ServNet] Sends back protocol (" + protocol.GetName() + ")"
            conn.socket.sendall(sendBuff)
        except Exception as e:
            print "[ServNet] Send Exception. " + conn.GetAddress(), e.message

    def Boradcast(self, protocol):
        """Sends message to every player"""
        for i in xrange(len(self.conns)):
            if self.conns[i] is None:
                continue
            if not self.conns[i].isUse:
                continue
            if self.conns[i].player is None:
                continue
            self.Send(self.conns[i], protocol)

    def HandleMainTimer(self):
        self.HeartBeat()
        self.timer = threading.Timer(1, self.HandleMainTimer)
        self.timer.start()
        # print 'Current number of threads: {}'.format(threading.activeCount())

    def HeartBeat(self):
        # print "[Main Timer Executed]"
        timeNow = GetTimeStamp()

        for i in xrange(len(self.conns)):
            conn = self.conns[i]
            if conn is None:
                continue
            if not conn.isUse:
                continue

            if conn.lastTickTime < timeNow - self.heartBeatTime:
                print "[ServNet] HeartBeat: Disconnection due to heartBeatTime [" + conn.GetAddress()+"]"
                lock = threading.Lock()
                with lock:
                    conn.Close()

    # Prints informationServNet
    def Print(self):
        print "[Server] Login Information:"
        for i in xrange(len(self.conns)):
            conn = self.conns[i]
            if conn is None or not conn.isUse:
                continue
            s = "Connection with [" + conn.GetAddress() + "]. "
            if conn.player is not None:
                s += "Player id='" + conn.player.id + "'."
            print s


servNet = ServNet()