import cv2
import face_recognition as fr
import os
import pickle
import firebase_admin
from firebase_admin import credentials,db,storage



mode='images'
lst=[]
ids=[]
for path in os.listdir(mode):
    lst.append(cv2.imread(os.path.join(mode,path)))
    ids.append(path[:-4])

    filename=f"{mode}/{path}"
    bucket=storage.bucket()
    blob=bucket.blob(filename)
    blob.upload_from_filename(filename)


def encode(imglst):
    encodings=[]
    for img in imglst:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encodings.append(fr.face_encodings(img)[0])

    return encodings
encodings=encode(lst)
encodingsid=[encodings,ids]
file=open('EncodeFile.p','wb')
pickle.dump(encodingsid,file)
file.close()
