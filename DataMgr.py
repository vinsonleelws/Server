# !/usr/bin/python
# coding:utf-8

import MySQLdb
import re
import pickle
import PlayerData


class DataMgr(object):
    def __init__(self):
        self.sqlConn = None
        self.cursor = None
        self.Connect()

    def __del__(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.sqlConn:
                self.sqlConn.close()
        except Exception as e:
            print e.message

    def Connect(self):
        self.sqlConn = MySQLdb.connect(host="127.0.0.1",
                                       user="root",
                                       passwd="Oracle6827965",
                                       db="game",
                                       port=3306,
                                       charset='utf8')  # host, user, passwd, db, port, charset
        try:
            self.cursor = self.sqlConn.cursor()
        except MySQLdb.Error, e:
            print "[DataMgr] Connect: " + e.args[1]
            return

    @staticmethod
    def IsSafeStr(s):
        return not re.match(s, r"[-|;|,|\/|\(|\)|\[|\]|\}|\{|%|@|\*|!|\']")

    def CanRegister(self, id):
        # Prevents sql injection
        if not self.IsSafeStr(id):
            return False
        # Query id
        cmd = "select * from user where id='{0}';".format(id)
        try:
            self.cursor.execute(cmd)
            results = self.cursor.fetchall()
            hasRows = bool(len(results))
            return not hasRows
        except Exception as e:
            print "[DataMgr] CanRegister: Unable to fetch data.", e.message
            return False

    def Register(self, id, pw):
        # Prevents sql injection
        if (not self.IsSafeStr(id)) or (not self.IsSafeStr(pw)):
            print "[DataMgr] Register with illegal characters."
            return False

        if not self.CanRegister(id):
            print "[DataMgr] Register: The id has already existed."
            return False

        # Add into sql
        cmd = "insert into user set id ='{0}' ,pw ='{1}';".format(id, pw)
        try:
            self.cursor.execute(cmd)
            return True
        except MySQLdb.Error, e:
            print "[DataMgr] Register: " + e.args[1]
            return False

    def CreatePlayer(self, id):
        # Prevents sql injection
        if not self.IsSafeStr(id):
            return False
        # Serialize
        playerData = PlayerData.PlayerData()
        try:
            byte_data = pickle.dumps(playerData)
        except MySQLdb.Error, e:
            print "[DataMgr] CreatePlayer failed." + e.args[1]
            return False

        # Writes into sql
        cmd = "insert into player values (%s, %s);"
        try:
            self.cursor.execute(cmd, (id, MySQLdb.Binary(byte_data)))
            self.sqlConn.commit()
            return True
        except MySQLdb.Error, e:
            self.sqlConn.rollback()
            print "[DataMgr] CreatePlayer: Can not write into sql. " + e.args[1]
            return False

    def CheckPassWord(self, id, pw):
        # Prevents sql injection
        if (not self.IsSafeStr(id)) or (not self.IsSafeStr(pw)):
            return False

        cmd = "select * from user where id='{0}' and pw='{1}';".format(id, pw)
        try:
            self.cursor.execute(cmd)
            results = self.cursor.fetchall()
            hasRows = bool(len(results))
            return hasRows
        except MySQLdb.Error, e:
            print "[DataMgr] CheckPassWord: sql select failed. " + e.args[1]
            return False

    def GetPlayerData(self, id):
        playerData = None
        # Prevents sql injection
        if not self.IsSafeStr(id):
            return playerData
        # Query
        cmd = "select * from player where id ='{0}';".format(id)
        try:
            self.cursor.execute(cmd)
            results = self.cursor.fetchall()
            if not len(results):
                return playerData
            else:
                self.cursor.execute(cmd)
                results = self.cursor.fetchall()
                # print "[Debug] GetPlayerData - results: ", type(results), results
                buffer = results[0][1]
        except MySQLdb.Error, e:
            print "[DataMgr] GetPlayerData Query" + e.args[1]
            return playerData
        # Deserialize
        try:
            playerData = pickle.loads(buffer)
            return playerData
        except MySQLdb.Error, e:
            print "[DataMgr] GetPlayerData Deserialize" + e.args[1]
            return playerData

    def SavePlayer(self, player):
        id = player.id
        playerData = player.data
        # Serialize
        try:
            byte_data = pickle.dumps(playerData)
        except MySQLdb.Error, e:
            print "[DataMgr] SavePlayer Serialize" + e.args[1]
            return False
        # cmd = "update player SET data='{0}' where id ='{1}';".format(MySQLdb.Binary(byte_data), id)
        cmd = "update player set data='{0}' where \
        id='{1}';".format(MySQLdb.Binary(byte_data.encode('string-escape')), id)
        # print "[Debug] ", cmd
        try:
            self.cursor.execute(cmd)
            self.sqlConn.commit()
            return True
        except MySQLdb.Error, e:
            self.sqlConn.rollback()
            print "[DataMgr] SavePlayer sql update failed. " + e.args[1]
            return False

# Singleton
dataMgr = DataMgr()

# For debug
# dataMgr = DataMgr()
# ret = dataMgr.Register("LWS", "123")
# if ret:
#     print "Register Successfully."
# else:
#     print "Register Failed."
#
# ret = dataMgr.CreatePlayer("LWS")
# if ret:
#     print "CreatePlayer Successfully."
# else:
#     print "CreatePlayer Failed."
#
# pd = dataMgr.GetPlayerData("LWS")
# if pd is not None:
#     print "GetPlayerData Successfully, socre = " + str(pd.score)
# else:
#     print "GetPlayerData Failed."
#
# pd.score += 10
# p = Player()
# p.id = "LWS"
# p.data = pd
# dataMgr.SavePlayer(p)
# pd = dataMgr.GetPlayerData("LWS")
# if pd is not None:
#     print "GetPlayerData Successfully, socre = " + str(pd.score)
# else:
#     print "GetPlayerData Failed."
