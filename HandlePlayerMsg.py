# !/usr/bin/python
# coding:utf-8

import ProtocolByte
import Scene
import ServNet


class HandlePlayerMsg(object):

    # Get Score
    # Return protocol: int(score)
    def MsgGetScore(self, player, protoBase):
        print "[MsgGetScore] Received GetScore protocol from player '" + player.id + "'."
        protocolRet = ProtocolByte.ProtocolByte()
        protocolRet.AddString("GetScore")
        protocolRet.AddInt(player.data.score)
        player.Send(protocolRet)
        print "[MsgGetScore]", player.id, player.data.score

    # Add Score
    def MsgAddScore(self, player, protoBase):
        print "[MsgGetScore] Received AddScore protocol from player '" + player.id + "'."
        start = 0
        protocol = ProtocolByte.ProtocolByte()
        protoName, start = protocol.GetStringFrom(start)
        player.data.score += 1
        print "[MsgAddScore]", player.id, player.data.score

    # Get List
    def MsgGetList(self, player, protoBase):
        print "[MsgGetList] Received GetList protocol from player '" + player.id + "'."
        Scene.scene.SendPlayerList(player)

    # Update Pos
    def MsgUpdatePos(self, player, protoBase):
        print "[MsgUpdateInfo] Received UpdatePos protocol from player '" + player.id + "'."
        # Get values
        start = 0
        protocol = protoBase
        protoName, start = protocol.GetStringFrom(start)
        x, start = protocol.GetFloatFromTo(start)
        y, start = protocol.GetFloatFromTo(start)
        z, start = protocol.GetFloatFromTo(start)
        # score = player.data.score
        player.data.x = x
        player.data.y = y
        player.data.z = z
        Scene.scene.UpdatePos(player.id, x, y, z)
        print x, y, z
        # Broadcast
        protocolRet = ProtocolByte.ProtocolByte()
        protocolRet.AddString("UpdatePos")
        protocolRet.AddString(player.id)
        protocolRet.AddFloat(x)
        protocolRet.AddFloat(y)
        protocolRet.AddFloat(z)
        # print "To be sent:", repr(protocolRet.GetDesc())
        ServNet.servNet.Boradcast(protocolRet)

    # Update Score
    def MsgUpdateScore(self, player, protoBase):
        print "[MsgUpdateScore] Received UpdateScore protocol from player '" + player.id + "'."
        # Get values
        start = 0
        protoName, start = protoBase.GetStringFrom(start)
        score, start = protoBase.GetIntFromTo(start)
        player.data.score = score
        Scene.scene.UpdateScore(player.id, score)

    def MsgUpdateHealth(self, player, protoBase):
        print "[MsgUpdateHealth] Received UpdateHealth protocol from player '" + player.id + "'."
        # Get values
        start = 0
        protoName, start = protoBase.GetStringFrom(start)
        health, start = protoBase.GetFloatFromTo(start)
        player.data.health = health
        Scene.scene.UpdateHealth(player.id, health)

    def MsgUpdateAmmo(self, player, protoBase):
        print "[MsgUpdateAmmo] Received MsgUpdateAmmo protocol from player '" + player.id + "'."
        # Get values
        start = 0
        protoName, start = protoBase.GetStringFrom(start)
        weaponType, start = protoBase.GetStringFrom(start)
        carryingAmmo, start = protoBase.GetIntFromTo(start)
        clipAmmo, start = protoBase.GetIntFromTo(start)
        if weaponType == "Pistol":
            player.data.pistolCarryingAmmo = carryingAmmo
            player.data.pistolClipAmmo = clipAmmo
        elif weaponType == "Rifle":
            player.data.rifleCarryingAmmo = carryingAmmo
            player.data.rifleClipAmmo = clipAmmo
        else:
            print "[Warning] MsgUpdateAmmo: weapon type not found: ", weaponType
        Scene.scene.UpdateAmmo(player.id, weaponType, carryingAmmo, clipAmmo)

    def MsgGetPlayerInfo(self, player, protoBase):
        print "[MsgGetPlayerInfo] Received GetPlayerInfo protocol from player '" + player.id + "'."
        # Returns
        protocol = ProtocolByte.ProtocolByte()
        protocol.AddString("GetPlayerInfo")
        protocol.AddFloat(player.data.health)
        protocol.AddInt(player.data.score)
        protocol.AddInt(player.data.pistolCarryingAmmo)
        protocol.AddInt(player.data.pistolClipAmmo)
        protocol.AddInt(player.data.rifleCarryingAmmo)
        protocol.AddInt(player.data.rifleClipAmmo)
        player.Send(protocol)
