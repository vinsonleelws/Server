# !/usr/bin/python
# coding:utf-8

from abc import ABCMeta, abstractmethod


class ProtocolBase(object):
    # __metaclass__ = ABCMeta

    @abstractmethod
    def Decode(self, readbuff, start, length):
        return ProtocolBase()

    @abstractmethod
    def Encode(self):
        return []

    @abstractmethod
    def GetName(self):
        return ""

    @abstractmethod
    def GetDesc(self):
        return ""
