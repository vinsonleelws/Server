# !/usr/bin/python
# coding:utf-8

import ServNet
import ProtocolByte
import threading
import os


HOST = '127.0.0.1'
PORT = 1234


def Main():
    while True:
        s = raw_input()
        if s == "quit":
            ServNet.servNet.Close()
            os._exit(0)
        elif s == "print":
            ServNet.servNet.Print()
            print servNet


if __name__ == '__main__':
    root = threading.Thread(target=Main)
    root.start()
    servNet = ServNet.servNet
    servNet.proto = ProtocolByte.ProtocolByte()
    servNet.Start(HOST, PORT)
