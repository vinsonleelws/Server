# !/usr/bin/python
# coding:utf-8

import PlayerTempData
import DataMgr
import ServNet
import threading
import Scene


class Player(object):
    def __init__(self, id="", conn=None):
        self.id = id
        self.conn = conn
        self.data = None
        self.tempData = PlayerTempData.PlayerTempData()

    # Sends
    def Send(self, proto):
        if self.conn is None:
            return
        ServNet.servNet.Send(self.conn, proto)

    @staticmethod
    def KickOff(id, proto):
        conns = ServNet.servNet.conns
        for i in xrange(len(conns)):
            if conns[i] is None:
                continue
            if not conns[i].isUse:
                continue
            if conns[i].player is None:
                continue
            if conns[i].player.id == id:
                lock = threading.Lock()
                with lock:
                    if proto is not None:
                        conns[i].player.Send(proto)
                    return conns[i].player.Logout()
        return True

    def Logout(self):
        # Handles player event on logout
        ServNet.servNet.handlePlayerEvent.OnLogout(self)
        # Saves player
        if not DataMgr.dataMgr.SavePlayer(self):
            return False
        # Logout
        # Scene.scene.DelPlayer(self.id)
        self.conn.player = None
        self.conn.Close()
        return True
