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
        player.Send(protocol)

    # Update pos
    def UpdatePos(self, id, x, y, z):
        p = self.GetScenePlayer(id)
        if p is None:
            return
        p.x = x
        p.y = y
        p.z = z

    # Update score
    def UpdateScore(self, id, score):
        p = self.GetScenePlayer(id)
        if p is None:
            return
        p.score = score

    # Update health
    def UpdateHealth(self, id, health):
        p = self.GetScenePlayer(id)
        if p is None:
            return
        p.health = health

    # Update ammo
    def UpdateAmmo(self, id, weaponType, carryingAmmo, clipAmmo):
        p = self.GetScenePlayer(id)
        if p is None:
            return
        if weaponType == "Pistol":
            p.pistolCarryingAmmo = carryingAmmo
            p.pistolClipAmmo = clipAmmo
        elif weaponType == "Rifle":
            p.rifleCarryingAmmo = carryingAmmo
            p.rifleClipAmmo = clipAmmo
        else:
            print "[Warning] Scene.UpdateAmmo: weapon type not found: ", weaponType


# Singleton pattern
scene = Scene()