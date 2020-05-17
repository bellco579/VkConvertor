import json

import requests


class Messages:
    def __init__(self, token,keyboard,api):
        self.token = token
        self.keyboard = keyboard
        self.api = api


    def sendPdfToUser(self, attach, uid ):
        self.api.messages.send(access_token=self.token, user_id=uid, attachment=attach,keyboard=self.keyboard)

    def sendMessage(self,message,uid):
        self.api.messages.send(access_token=self.token, user_id=uid,message=message, keyboard=self.keyboard)

    def sendmsg(self, msg):
        pass

    def sendSuccess(self):
        pass

    def sendError(self,uid):
        self.api.messages.send(access_token=self.token, user_id=uid, message="я не понимаю", keyboard=self.keyboard)
