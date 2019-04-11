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

    # Update Information
    def MsgUpdateInfo(self, player, protoBase):
        print "[MsgUpdateInfo] Received UpdateInfo protocol from player '" + player.id + "'."
        # Get values
        start = 0
        protocol = protoBase
        protoName, start = protocol.GetStringFrom(start)
        x, start = protocol.GetFloatFromTo(start)
        y, start = protocol.GetFloatFromTo(start)
        z, start = protocol.GetFloatFromTo(start)
        score = player.data.score
        Scene.scene.UpdateInfo(player.id, x, y, z, score)
        # Broadcast
        protocolRet = ProtocolByte.ProtocolByte()
        protocolRet.AddString("UpdateInfo")
        protocolRet.AddString(player.id)
        protocolRet.AddFloat(x)
        protocolRet.AddFloat(y)
        protocolRet.AddFloat(z)
        protocolRet.AddInt(score)
        # print "To be sent:", repr(protocolRet.GetDesc())
        ServNet.servNet.Boradcast(protocolRet)
