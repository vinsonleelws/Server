# !/usr/bin/python
# coding:utf-8

import ScenePlayer
import threading
import ProtocolByte
import ServNet


class Scene(object):
    playerList = []

    # GetScenePlayer via id
    def GetScenePlayer(self, id):
        for i in xrange(len(self.playerList)):
            if Scene.playerList[i].id == id:
                return Scene.playerList[i]
        return None

    # Add player
    def AddPlayer(self, id):
        lock = threading.Lock()
        with lock:
            p = ScenePlayer.ScenePlayer()
            p.id = id
            self.playerList.append(p)

    # Delete player
    def DelPlayer(self, id):
        lock = threading.Lock()
        with lock:
            p = self.GetScenePlayer(id)
            if p is not None:
                self.playerList.remove(p)

        protocol = ProtocolByte.ProtocolByte()
        protocol.AddString("PlayerLeave")
        protocol.AddString(id)
        ServNet.servNet.Boradcast(protocol)

    # SendPlayerList
    def SendPlayerList(self, player):
        count = len(self.playerList)
        protocol = ProtocolByte.ProtocolByte()
        protocol.AddString("GetList")
        protocol.AddInt(count)
        for i in xrange(count):
            p = self.playerList[i]
            protocol.AddString(p.id)
            protocol.AddFloat(p.x)
            protocol.AddFloat(p.y)
            protocol.AddFloat(p.z)
            protocol.AddInt(p.score)
        player.Send(protocol)

    # Update information
    def UpdateInfo(self, id, x, y, z, score):
        count = len(self.playerList)
        protocol = ProtocolByte.ProtocolByte()
        p = self.GetScenePlayer(id)
        if p is None:
            return
        p.x = x
        p.y = y
        p.z = z
        p.score = score

# Singleton pattern
scene = Scene()