'''
Created on 2017年5月25日

@author: moonlit
'''
import cv2

cap = cv2.VideoCapture(0)

while True:
    _, image = cap.read()

#     image = cv2.imread("d:/1c5d0004f5d810150dac.jpg")
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Image Title",image)
    face_cascade = cv2.CascadeClassifier("D:\BossSensor\haarcascades\haarcascades/haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(
                                            gray,
                                            scaleFactor = 1.15,
                                            minNeighbors = 5,
                                            minSize = (5,5)
    #                                         flags = cv2.cv.CV_HAAR_SCALE_IMAGE
                                          )
    # cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))
    print("发现{0}个人脸!".format(len(faces)) )
    for(x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+w),(0,255,0),2)
        
    cv2.imshow("Find Faces!",image)
    cv2.waitKey(100)