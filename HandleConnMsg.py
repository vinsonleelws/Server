# !/usr/bin/python
# coding:utf-8


import Sys, ProtocolByte, DataMgr, Player, ServNet

class HandleConnMsg(object):

    # HeartBeat protocol
    # Parameters: None
    def MsgHeatBeat(self, conn, protoBase):
        print "[MsgHeatBeat] Received HeatBeat protocol from [" + conn.GetAddress() + "]"
        conn.lastTickTime = Sys.GetTimeStamp()
        print "[MsgHeatBeat] Update heartBeatTime for [" + conn.GetAddress() + "]"

    # Register protocol
    # Parameters: str(id), str(pw)
    # Return protocol: -1(fail), 0(success)
    def MsgRegister(self, conn, protoBase):
        start = 0
        protocol = protoBase
        protoName, start = protocol.GetStringFrom(start)
        id, start = protocol.GetStringFrom(start)
        pw, start = protocol.GetStringFrom(start)
        print "[MsgRegister] Received Register protocol from [" + conn.GetAddress() + "]: id= " + id, " pw= " + pw
        # Constructs return protocol
        protocol = ProtocolByte.ProtocolByte()
        protocol.AddString("Register")
        # Registers
        dataMgr = DataMgr.dataMgr
        if dataMgr.Register(id, pw):
            protocol.AddInt(0)
        else:
            protocol.AddInt(-1)
        # Creates player
        dataMgr.CreatePlayer(id)
        # Sends back
        conn.Send(protocol)

    # Login protocol
    # Parameters: str(id), str(pw)
    # Return protocol: -1(fail), 0(success)
    def MsgLogin(self, conn, protoBase):
        start = 0
        protocol = protoBase
        protoBame, start = protocol.GetStringFrom(start)
        id, start = protocol.GetStringFrom(start)
        pw, start = protocol.GetStringFrom(start)
        print "[MsgLogin] Received Login protocol from [" + conn.GetAddress() + "]. id='" + id +"'", " pw='" + pw + "'."
        # Constructs return protocol
        protocolRet = ProtocolByte.ProtocolByte()
        protocolRet.AddString("Login")
        # Verification
        dataMgr = DataMgr.dataMgr
        if not dataMgr.CheckPassWord(id, pw):
            print "[MsgLogin] Verification failed."
            protocolRet.AddInt(-1)
            conn.Send(protocolRet)
            return
        # Check login
        protocolLogout = ProtocolByte.ProtocolByte()
        protocolLogout.AddString("Logout")
        if not Player.Player().KickOff(id, protocolLogout):
            protocolRet.AddInt(-1)
            conn.Send(protocolRet)
            return
        # Get player data
        playerData = dataMgr.GetPlayerData(id)
        if playerData is None:
            protocolRet.AddInt(-1)
            conn.Send(protocolRet)
            return
        conn.player = Player.Player(id, conn)
        conn.player.data = playerData
        # Triggers event
        ServNet.servNet.handlePlayerEvent.OnLogin(conn.player)
        # Returns
        protocolRet.AddInt(0)
        conn.Send(protocolRet)
        return

    # Logout protocol
    # Parameters: None
    # Return protocol: -1(fail), 0(success)
    def MsgLogout(self, conn, protoBase):
        print "[MsgLogout] Received Logout protocol from [" + conn.GetAddress() + "]."
        protocol = ProtocolByte.ProtocolByte()
        protocol.AddString("Logout")
        protocol.AddInt(0)
        if conn.player is None:
            conn.Send(protocol)
            conn.Close()
        else:
            conn.Send(protocol)
            conn.player.Logout()


# For debug
# handleConnMsg = HandleConnMsg()
# methodName = "MsgHeatBeat"
# method = getattr(handleConnMsg, methodName, None)
# print method
# method("", "")
