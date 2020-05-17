import json

path = "json/links.json"


class User:
    def __init__(self, uid, firstName, lastName, linkedUser):
        self.uid = uid
        self.firstName = firstName
        self.lastName = lastName
        self.linkedUser = linkedUser


class UserProcessing():
    def __init__(self, uid, user=None):
        self.getedUser = user
        self.uid = str(uid)
        self.path = "users/{}.json".format(self.uid)
        self.user = self.Load()

    def Save(self, obj):
        with open(self.path, "w") as js_file:
            json.dump(obj, js_file)

    def Load(self):
        try:
            with open(self.path, "r") as js_file:
                users = json.load(js_file)
                return users
        except Exception as e:
            print(e)
            self.AddUser()

    def AddUser(self):
        self.user = {self.uid: None}
        self.Save(self.user)

    def getLinkedUsers(self):
        try:
            luser = self.user[self.uid]
            return luser
        except:
            self.AddUser()
            return None

    def addLink(self, luid):
        linkedUsers = self.getLinkedUsers()
        if linkedUsers == None:
            self.user[self.uid] = [luid, ]
        else:
            if luid in self.user[self.uid]:
                return
            else:
                self.user[self.uid].append(luid)
        self.Save(self.user)
        print("user {} linked with {}".format(self.uid, luid))

    def deleteLink(self, position):
        rvUser = self.user[self.uid][position]
        del self.user[self.uid][position]
        self.Save(self.user)
        return rvUser

    def addMsg(self, msg):

        try:
            self.user["messages"].append(msg)
        except:
            self.user["messages"] = [None, msg, ]
        self.Save(self.user)
        self.user = self.Load()
        return self.getMsgList()

    def getMsgList(self):

        try:
            return self.user["messages"]
        except:
            return None

    def getUser(self):
        return User(uid=self.uid, firstName=self.getedUser["first_name"], lastName=self.getedUser["last_name"],
                    linkedUser=self.getLinkedUsers())


if __name__ == '__main__':
    UserProcessing(12443).addLink(1223)
