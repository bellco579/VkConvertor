import glob
import json

files = glob.glob("D:/Projects/work/testImg/*.*")
import vk_requests
import requests
import vk_api

token = ''
vk_session = vk_api.VkApi(token=token)
import vk

session = vk.Session()
api = vk.API(session, v=5.8)
api.access_token = token
id = 1
from PIL import Image



def create_pdf(imagelist):
    from fpdf import FPDF
    pdf = FPDF()
    # imagelist is the list with all image filenames
    for image in imagelist:
        pdf.add_page()
        pdf.image(image)
    pdf.output("yourfile.pdf", "F")


def getPhoto(url):
    photo = requests.get(url=url)
    # photoObj = photo.content
    file = open("sample_image.png", "wb")
    file.write(photo.content)
    file.close()
    return Image.open("sample_image.png")


def sendPdfToUser(pdf, uid):
    upload_url = api.docs.getMessagesUploadServer(access_token=token, type='doc', peer_id=uid)['upload_url']

    response = requests.post(upload_url, files={'file': open(pdf, 'rb')})
    result = json.loads(response.content)
    file = result['file']

    json1 = api.docs.save(access_token=token,file=file, title=pdf, tags=[])[0]

    owner_id = json1['owner_id']
    photo_id = json1['id']
    attach = 'doc' + str(owner_id) + '_' + str(photo_id)
    messages = api.messages.send(access_token=token,user_id=uid, attachment=attach)


def getPhotoUrls(msgId):
    photos = []
    msg = api.messages.getById(access_token=token, message_ids=msgId)

    uid = msg["items"][0]['user_id']
    for item in msg["items"][0]['attachments']:
        if item['type'] == 'photo':
            photoUrl = item['photo']['photo_1280']
            print(photoUrl)
            immage = getPhoto(photoUrl).convert("RGB")
            photos.append(immage)
    i = photos[0]
    del photos[0]
    user = api.users.get(access_token=token, user_ids=uid)
    fileName = user[0]['first_name'] + user[0]["last_name"] + ".pdf"
    i.save(fileName, save_all=True, append_images=photos)
    sendPdfToUser(fileName, uid)


# print(api)

from vk_api.longpoll import VkLongPoll, VkEventType

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        print(event.attachments)
        getPhotoUrls(event.message_id)

#  if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
# #Слушаем longpoll, если пришло сообщение то:
#      if
