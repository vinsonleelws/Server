# !/usr/bin/python
# coding:utf-8

from ProtocolBase import ProtocolBase


class ProtocolStr(ProtocolBase):

    def __init__(self):
        self.s = ""

    def Decode(self, readbuff, start, length):
        protocol = ProtocolStr()
        buff = readbuff[start: start + length]
        protocol.s = buff.decode('utf-8')
        return protocol

    def Encode(self):
        # b = self.s.encode('utf-8')
        strBytes = bytearray(self.s, 'utf-8')
        return strBytes

    def GetName(self):
        if len(self.s) == 0:
            return ""
        else:
            return self.s.split(',')[0]

    def GetDesc(self):
        return self.s


# For debug
# p = ProtocolStr()
# p = p.Decode("abc", 0, 3)
# print 'p.Encode():', type(p.Encode()), '  value:', p.Encode()
# print p.GetName()
# print p.GetDesc()
