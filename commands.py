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
    if command == "Удалить получателя":
        try:
            rvUser = UserProcessing(uid=user.uid).deleteLink(int(context))
            vkUser = getVkUser(uid=rvUser,api=api,token=token)
            msg = "{} больше не будет получать pdf".format(vkUser[0]['first_name'])
            print(msg)
            message.sendMessage(message=msg, uid=user.uid)
        except:
            pass

    if context == "Добавить получателя":
        message.sendMessage(message="отправь id пользователя", uid=user.uid)
    if context == "Удалить получателя":
        s = "Кого? \n"
        for i in range(len(lusers)):
            i = int(i)
            luid = int(lusers[i])
            vkUser = getVkUser(uid=luid, api=api, token=token)
            s += "{0} {1}\n".format(i, vkUser[0]['first_name'])
        message.sendMessage(message=s, uid=user.uid)

    if context == "Мой id":
        message.sendMessage(message=user.uid, uid=user.uid)
