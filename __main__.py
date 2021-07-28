import os
from multiprocessing import Process
import numpy as np
import time
import imutils
import cv2
from playsound import playsound

face_d = cv2.CascadeClassifier('haarcascade\haarcascade_frontalface_default.xml')
first_frame = 0
w_size = 1200

mp3file = 'ping.mp3'
cou = 1
ogasdsa = 'n'

def chuongCua() :
    playsound(mp3file)
    print(cou, 'times')
    cou += 1

def run():
    #capture = cv2.VideoCapture('demo.mp4')
    capture = cv2.VideoCapture("rtsp://admin:vietviet@192.168.1.2:554/onvif1", cv2.CAP_FFMPEG)
    
    result, first_frame = capture.read()
    first_frame = imutils.resize(first_frame, width=w_size)
    first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY) 
    first_frame = cv2.GaussianBlur(first_frame, (21, 21), 0)
    take_time = time.time()
    main_emer = 0
    con_emer = time.time()

    while True:
       
        r, img = capture.read()
        img = imutils.resize(img, width=w_size)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        frameDel = cv2.absdiff(first_frame, gray)
        thresh = cv2.threshold(frameDel, 30, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations = 2)

        cv2.imshow("W", frameDel)

        cnts,res = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in cnts:
            if cv2.contourArea(contour) < 10000 :
                continue
            if (time.time() - take_time > 3) :
                cv2.imwrite(str(time.time()) + ".jpg", img)
                take_time = time.time()
            if (time.time() - con_emer > 1) :
                main_emer = 0
            else :
                main_emer += time.time() - con_emer
            con_emer = time.time()
            if main_emer > 10 :
                first_frame = gray
            (x,y,w,h) = cv2.boundingRect(contour)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0), 3)
        cv2.putText(img, str(main_emer), (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 2)     
           
        cv2.imshow("key", img)
        if cv2.waitKey(1) == ord("q"):
            break

if __name__ == '__main__':
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    p = Process(target=run)
    p.start()
    p.join()
