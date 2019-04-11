# !/usr/bin/python
# coding:utf-8

import Scene


class HandlePlayerEvent(object):

    def OnLogin(self, player):
        Scene.scene.AddPlayer(player.id)

    def OnLogout(self, player):
        Scene.scene.DelPlayer(player.id)
