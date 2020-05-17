import json

import requests

from repositories import downloadPhoto


class photo:
    def getUrl(self, item):
        phtoUrl = ""
        try:
            photoUrl = item['photo']['photo_1280']
            print("hight quality")
        except:
            try:
                photoUrl = item['photo']['photo_807']
                print("meddle quality")
            except:
                photoUrl = item['photo']['photo_604']
                print("low quality")
        return photoUrl

    def getPhoto(self, attachments):
        photos_path = []
        for item in attachments:
            if item['type'] == 'photo':
                photoUrl = self.getUrl(item)
                print(photoUrl)
                path = downloadPhoto(photoUrl)
                photos_path.append(path)
        return photos_path

def uploadDoc(api,token,path,title):
    maratik = 313941939
    upload_url = api.docs.getMessagesUploadServer(access_token=token, type='doc', peer_id=maratik)['upload_url']

    response = requests.post(upload_url, files={'file': open(path, 'rb')})
    result = json.loads(response.content)
    file = result['file']

    json1 = api.docs.save(access_token=token, file=file, title=title, tags=[])[0]

    owner_id = json1['owner_id']
    photo_id = json1['id']
    attach = 'doc' + str(owner_id) + '_' + str(photo_id)
    return attach