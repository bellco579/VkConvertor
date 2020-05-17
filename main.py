import glob
import json
import threading
from concurrent.futures import thread

import vk
from apiProcessing import photo, uploadDoc
from commands import commands
from converter import photoConverter
from keyboard import getKeyboard
from messages import Messages
from user import UserProcessing

import vk_requests
import requests
import vk_api

with open('json/config.json', "r") as js_file:
    config = json.load(js_file)
    token = config['token']
vk_session = vk_api.VkApi(token=token)
session = vk.Session()
api = vk.API(session, v=5.8)
id = 1

keyboard = getKeyboard()
Message = Messages(token, keyboard, api=api)


def getVkUser(uid, api, token):
    return api.users.get(access_token=token, user_ids=uid)


def strProcessing(str, user):
    chatHistory = UserProcessing(user.uid).addMsg(str)
    commands(context=chatHistory[-1], command=chatHistory[-2], user=user, message=Message, api=api, token=token,
             lusers=user.linkedUser, luser=str)


def sendDoc(path, title, user):
    attach = uploadDoc(api, token, path, title)
    Message.sendPdfToUser(attach, user.uid)
    is_send = True
    try:
        for id in user.linkedUser:
            is_send = Message.sendPdfToUser(attach, id)
    except:
        is_send = Message.sendPdfToUser(attach, user.linkedUser[0])
    if not is_send:
        Message.sendMessage(
            message="Пользователь {} не находитя в группе".format(getVkUser(uid=user.uid, api=api, token=token)),uid=user.uid)


def convertToPdf(pathList, filename="NoName"):
    return photoConverter(pathList, filename)


def SavePhoto(attachments):
    photosPath = photo().getPhoto(attachments)
    print(photosPath)
    return photosPath


def getUser(uid):
    vk_user = api.users.get(access_token=token, user_ids=uid)[0]
    user = UserProcessing(uid=uid, user=vk_user).getUser()
    return user


def Router(msgId):
    msg = api.messages.getById(access_token=token, message_ids=msgId)["items"][0]
    uid = msg['user_id']
    user = getUser(uid)
    text = msg['body']
    try:

        if text != "":
            strProcessing(text, user)
        print("User send text {}".format(text))
    except:
        pass

    try:
        attachments = msg['attachments']
        photosPath = SavePhoto(attachments)
        docPath = convertToPdf(photosPath, user.lastName)
        if text != "":
            sendDoc(path=docPath, title=text, user=user)
        else:
            sendDoc(path=docPath, title=user.lastName, user=user)
    except Exception as e:
        print(e)


def app():
    from vk_api.longpoll import VkLongPoll, VkEventType

    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            x = threading.Thread(target=Router, args=(event.message_id,))
            x.start()


if __name__ == '__main__':
    app()
