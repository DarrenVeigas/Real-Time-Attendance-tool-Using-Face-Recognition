import cv2
import os
import pickle
import numpy as np
import face_recognition as fr
import cvzone 
from datetime import datetime
import firebase_admin
from firebase_admin import credentials,db,storage




bucket=storage.bucket()
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
imgbkg=cv2.imread('./resources/background.png')

mode='resources/Modes'
lst=[]
for path in os.listdir(mode):
    lst.append(cv2.imread(os.path.join(mode,path)))

file=open('EncodeFile.p','rb')
encodings,ids=pickle.load(file)
file.close()
print(ids)

modeType=0
counter=0

while True:
    success,img=cap.read()
    if not success:
        print('issue')
        break
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    faceCurFrame=fr.face_locations(imgS)
    encodeCurFrame=fr.face_encodings(imgS,faceCurFrame)
    
    imgbkg[162:162+480,55:55+640]=img
    imgbkg[44:44+633,808:808+414]=lst[modeType]
    if faceCurFrame:
        for encode,faceloc in zip(encodeCurFrame,faceCurFrame):
            encode = np.array(encode)
            matches=fr.compare_faces(encodings,encode)
            face_dist=fr.face_distance(encodings,encode)

            matchIndex = np.argmin(face_dist)
            if matches[matchIndex]==True:
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgbkg=cvzone.cornerRect(imgbkg,bbox,rt=0)
                id=ids[matchIndex]
                '''if counter == 0:

                    cvzone.putTextRect(imgbkg, "Loading", (275, 400))

                    cv2.imshow("Face Attendance", imgbkg)'''
                counter = 1
                modeType = 1
    if counter!=0:

        if counter==1:
            studentInfo=db.reference(f"Students/{id}").get()
            modeType=1

            blob=bucket.get_blob(f'images/{id}.png')
            arr=np.frombuffer(blob.download_as_string(),np.uint8)
            imgStudent=cv2.imdecode(arr,cv2.COLOR_BGRA2BGR)
            imgStudent=cv2.resize(imgStudent, (216, 216))
            datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
            if secondsElapsed > 30:
                ref = db.reference(f'Students/{id}')
                studentInfo['total_attendance'] += 1
                ref.child('total_attendance').set(studentInfo['total_attendance'])
                ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                modeType = 3
                counter = 0
                imgbkg[44:44 + 633, 808:808 + 414] = lst[modeType]
        if modeType != 3:
            if 10<counter<20:
                modeType=2
            
            imgbkg[44:44 + 633, 808:808 + 414] = lst[modeType]

            if counter<=10:
                cv2.putText(imgbkg, str(studentInfo['total_attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                cv2.putText(imgbkg, str(studentInfo['major']), (1006, 550),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgbkg, str(id), (1006, 493),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgbkg, str(studentInfo['standing']), (910, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imgbkg, str(studentInfo['year']), (1025, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                offset = (414 - w) // 2
                cv2.putText(imgbkg, str(studentInfo['name']), (808 + offset, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                counter+=1
                imgbkg[175:175 + 216, 909:909 + 216] = imgStudent
            if counter >= 20:
                counter = 0
                modeType = 0
                studentInfo = []
                imgStudent = []
                imgbkg[44:44 + 633, 808:808 + 414] = lst[modeType]
    else:
        modeType=0
        counter=0
       



    cv2.imshow('Face attendance',imgbkg)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

