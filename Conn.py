# !/usr/bin/python
# coding:utf-8

import sys
import socket
import Sys
import ServNet


BUFFER_SIZE = 1024


class Conn(object):

    def __init__(self):
        self.socket = None
        self.readBuff = bytearray(BUFFER_SIZE)
        self.isUse = False
        self.buffCount = None
        self.lenBytes = None
        self.lastTickTime = sys.maxint
        self.msgLength = 0
        self.player = None
        self.address = None

    def Init(self, socket):
        self.socket = socket
        self.isUse = True
        self.buffCount = 0
        self.lenBytes = bytearray(4)  # sizeof(UInt32)
        self.lastTickTime = Sys.GetTimeStamp()
        self.player = None
        self.address = None

    def BuffRemain(self):
        return BUFFER_SIZE - self.buffCount

    def GetAddress(self):
        if not self.isUse:
            return "Can not get address!"
        return self.address

    def Close(self):
        if not self.isUse:
            return
        if self.player is not None:
            print "[Conn] Close: player logout."
            self.player.Logout()
            return
        print "[Disconnected] " + self.GetAddress()
        self.socket.shutdown(socket.SHUT_RDWR)  # further sends and receives are disallowed
        self.socket.close()
        self.isUse = False

    def Send(self, protocol):
        ServNet.servNet.Send(self, protocol)
