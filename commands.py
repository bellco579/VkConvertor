from user import UserProcessing


def getVkUser(uid, api, token):
    return api.users.get(access_token=token, user_ids=uid)


def commands(command, context, user, message, api, token, luser=None, lusers=None):
    if command == "Добавить получателя":
        try:
            UserProcessing(uid=user.uid).addLink(int(context))
            vkUser = getVkUser(uid=int(context), api=api, token=token)
            msg = "{} будет получать pdf".format(vkUser[0]['first_name'])
            print(msg)
            message.sendMessage(message=msg, uid=user.uid)
        except:
            pass
            # message.sendError(uid=user.uid)
    if command == "Удалить получателя":
        try:
            rvUser = UserProcessing(uid=user.uid).deleteLink(int(context))
            vkUser = getVkUser(uid=rvUser, api=api, token=token)
            msg = "{} больше не будет получать pdf".format(vkUser[0]['first_name'])
            print(msg)
            message.sendMessage(message=msg, uid=user.uid)
        except:
            pass
            # message.sendError(uid=user.uid)

    if context == "Добавить получателя":
        message.sendMessage(message="отправь id пользователя", uid=user.uid)
    if context == "Удалить получателя":
        s = "Кого? \n отправь цифру\n"
        ex1 = lusers != None
        ex2 = False
        try:
            ex2 = len(lusers) != 0
        except:
            pass
        if ex1 or ex2:
            for i in range(len(lusers)):
                i = int(i)
                luid = int(lusers[i])
                vkUser = getVkUser(uid=luid, api=api, token=token)
                s += "{0} {1}\n".format(i, vkUser[0]['first_name'])
            message.sendMessage(message=s, uid=user.uid)
        else:
            message.sendMessage(message="список пуст", uid=user.uid)

    if context == "Мой id":
        message.sendMessage(message=user.uid, uid=user.uid)

    if context == "Начать":
        ms = "Привет! Теперь ты можешь использовать это приложение для перевода фотографий в pdf.\n\
📎Чтобы отправить свой документ другому человеку, нажми •добавить получателя• и введи его id.\n\
📍Теперь он тоже будет получать твои документы, пока ты его не удалишь: нажми •удалить получателя•, затем выбери цифру.\n\
📌Отправляя фотографии, подпиши сообщение так, как должен называться документ. "
        message.sendMessage(message=ms, uid=user.uid)
