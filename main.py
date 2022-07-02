import face_recognition
import cv2
from tkinter import *
import tkinter as tk
from tkinter import ttk



win = Tk()


win.configure(background='cyan')


message = tk.Label(win, text=" UNIVERSITY OF ENGINEERING AND MANAGMANAGEMENT " ,bg="green"  ,fg="yellow"  ,width=50  ,height=2,font=('Times New Roman', 25, 'bold')) 
message.place(x=800, y=760)

message = tk.Label(win, text="ATTENDANCE MANAGEMENT PORTAL" ,bg="yellow"  ,fg="black"  ,width=40  ,height=1,font=('Times New Roman', 35, 'bold underline')) 
message.place(x=400, y=20)





def run_1stcode():
    
    import numpy as np
    import os
    from datetime import datetime
    path = 'Training_images'
    images = []
    classNames = []
    myList = os.listdir(path)
    #print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        #print(classNames)
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList
    
    def markAttendance(name):
        with open('1st period Attendance.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
        
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
                
            if name not in nameList:
                time_now = datetime.now()
                tStr = time_now.strftime('%H:%M:%S')
                dStr = time_now.strftime('%d/%m/%Y')
                f.writelines(f'\n{name},{tStr},{dStr}')
            
                
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')
    
    cap = cv2.VideoCapture(0)
    
    while True:
        success, img = cap.read()
# img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
        # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)

        cv2.imshow('webcam',img)
        if cv2.waitKey(1) == 13:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    
    
    
button1 =  Button(win, text="first period", command=run_1stcode,fg="white"  ,bg="blue"  ,width=20  ,height=2, activebackground = "red" 
                  ,font=('Times New Roman', 15, ' bold '))
button1.pack(side=LEFT, padx=15, pady=20)

button2 =  Button(win, text="second period", command=run_1stcode,fg="white"  ,bg="blue"  ,width=20  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
button2.pack(side=LEFT, padx=175, pady=20)
button3 =  Button(win, text="third period", command=run_1stcode,fg="white"  ,bg="blue"  ,width=20  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
button3.pack(side=LEFT, padx=250, pady=20)
button4 =  Button(win, text="fourth period", command=run_1stcode,fg="white"  ,bg="blue"  ,width=20  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
button4.pack(side=RIGHT, padx=15, pady=20)
win.mainloop()    