import cv2
import face_recognition
import numpy as np
import os
from django.core.files.storage import FileSystemStorage
# from .models import Person


path = '../media/citizens'
images = []
classNames = []
mylist = os.listdir(path)
# print(mylist)

for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown = findEncodings(images)
print(len(encodeListKnown))

# def detect_image_opencv(request):
#     # if request.method == 'POST' and request.FILES['image']:
#     #     myfile = request.FILES['image']
#     #     fs = FileSystemStorage()
#     #     filename = fs.save(myfile.name, myfile)
#     #     uploaded_file_url = fs.url(filename)
#
#     images = []
#     encodings = []
#     names = []
#     files = []
#
#     prsn = Person.objects.all()
#     for img in prsn:
#         images.append(img.name + '_image')
#         print(img)
        # encodings.append(img.name + '_face_encoding')
        # files.append(img.picture)
        # names.append(img.name + ' ' + img.address)
        #
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # encode = face_recognition.face_encodings(img)[0]
        # encodings.append(encode)
        # return encodings
        # images.append(crime.name + '_image')
        # print(images)
        # encodings.append(crime.name + '_face_encoding')
        # files.append(crime.picture)
        # names.append(crime.name + ' ' + crime.address)