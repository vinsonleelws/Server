# !/usr/bin/python
# coding:utf-8

from ProtocolBase import ProtocolBase
import struct


class ProtocolByte(ProtocolBase):
    """Supports types of int, float and str"""

    def __init__(self):
        self.bytes = bytearray()

    def Decode(self, readbuff, start, length):
        protocol = ProtocolByte()
        protocol.bytes = readbuff[start: start + length]
        return protocol

    def Encode(self):
        return self.bytes

    def GetName(self):
        return self.GetStringFrom(0)[0]

    def GetDesc(self):
        s = ""
        if self.bytes == b'':
            return s

        # for b in self.bytes:
        #     s += chr(b) + " "
        fmt = str(len(self.bytes)) + 's'
        s = struct.unpack(fmt, self.bytes)[0]
        return s

    def AddString(self, string):
        length = len(string)
        lenBytes = struct.pack('<I', length)
        strBytes = bytearray(string, 'utf-8')
        self.bytes = self.bytes + lenBytes + strBytes

    def GetStringFrom(self, start):
        """Get String from start, then update end"""
        if self.bytes == b'':
            return "", start
        if len(self.bytes) < start + 4:  # 4 bytes (Int32) for message length
            return "", start

        lenBytes = self.bytes[start:start + 4]
        # strLen = eval(str(lenBytes))
        strLen = struct.unpack('<I', lenBytes)[0]  # <I: Little-endian unsigned int
        if len(self.bytes) < start + 4 + strLen:
            return "", start
        b = self.bytes[start + 4:start + 4 + strLen]
        # s = b.decode('utf-8')
        s = str(b)
        end = start + 4 + strLen
        return s, end

    def AddInt(self, num):
        # numBytes = bytearray(str(num), 'utf-8')
        # self.bytes += numBytes
        numBytes = struct.pack('<i', num)
        self.bytes += numBytes

    def GetIntFromTo(self, start):
        if self.bytes == b'':
            return 0, start
        if len(self.bytes) < start + 4:
            return 0, start
        end = start + 4
        bNum = self.bytes[start:start + 4]
        num = struct.unpack('<I', bNum)[0]
        # return int(eval(str(bNum)))
        return int(num), end

    def AddFloat(self, num):
        # numBytes = bytearray(str(num), 'utf-8')
        # self.bytes += numBytes
        numBytes = struct.pack('<f', num)  # d: double 8 bytes, f: float 4 bytes
        self.bytes += numBytes

    def GetFloatFromTo(self, start):
        if self.bytes == b'':
            return 0, start
        if len(self.bytes) < start + 4:  # 4 bytes float
            return 0, start
        end = start + 4
        bNum = self.bytes[start: start + 4]
        num = struct.unpack('<f', bNum)[0]
        # return float(eval(str(bNum)))
        return float(num), end


# For debug
# try:
#     s = b"abc"
#     l = struct.pack('<I', len(s))
#     bytes = bytearray(l + s)
#     p = ProtocolByte()
#     p = p.Decode(bytes, 0, len(bytes))
#     print "p.Encode: ", type(p.Encode()), '  value:', p.Encode()
#     print "p.GetDesc: ", p.GetDesc()
#     print "p.AddString('d')"
#     p.AddString('d')
#     print "p.GetDesc: ", p.GetDesc()
#     print "GetStringFromTo:", p.GetStringFromTo(0, [0])
#     print "p.AddInt(99)"
#     p.AddInt(99)
#     print "p.GetDesc: ", p.GetDesc()
#     print "p.AddFloat(0.1)"
#     p.AddFloat(0.1)
#     print "p.GetDesc: ", p.GetDesc()
#     print "p.GetName:", p.GetName()
#     print "p.GetIntFromTo(0):", p.GetIntFromTo(0)
# except Exception as e:
#     print e.message

# s = b"abc"
# l = struct.pack('<I', len(s))
# bytes = bytearray(l + s)
# p = ProtocolByte()
# p = p.Decode(bytes, 0, len(bytes))
# print "p.Encode: ", type(p.Encode()), '  value:', p.Encode()
# print "p.GetDesc: ", p.GetDesc()
# print "p.AddString('d')"
# p.AddString('d')
# print "p.GetDesc: ", p.GetDesc()
# print "GetStringFromTo:", p.GetStringFrom(0)
# print "p.AddInt(99)"
# p.AddInt(99)
# print "p.GetDesc: ", p.GetDesc()
# print "p.AddFloat(0.1)"
# p.AddFloat(0.1)
# print "p.GetDesc: ", p.GetDesc()
# print "p.GetName:", p.GetName()
# print "p.GetIntFrom(0):", p.GetIntFrom(0)
