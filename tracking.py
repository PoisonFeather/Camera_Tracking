from cv2 import cv2
import serial
import time
s = serial.Serial('COM4',9600,timeout=5)
print("Starting")

cap = cv2.VideoCapture(0)
succes, img = cap.read()
time.sleep(1)

tracker = cv2.TrackerMOSSE_create()
#tracker = cv2.TrackerCRST_create()

bbox=cv2.selectROI("Tracking",img,False)
tracker.init(img,bbox)
#panAngle=90
width_camera =int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
window_height,window_width,channels = img.shape
def drawBox(img,bbox):
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]),
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(x,y,x*y/255),3,1)
    #print(cv2.width)
    mapServoPosition(x)


def mapServoPosition (x):
    panAngle=x
    if (x < (width_camera/2)-75):
        panAngle += 10
        if panAngle > 320:
            panAngle = 320
        positionServo (panAngle)
        print(panAngle)
    if (x > (width_camera/2)+75):
        panAngle -= 10
        if panAngle < 10:
            panAngle = 10
        positionServo (panAngle)
        print(panAngle)

    if x <10:
        pan=10
    
def positionServo(pan):
    s.write(pan)



while True:
    timer = cv2.getTickCount()
    success,img=cap.read()
    success,bbox = tracker.update(img)  
    if success :
        drawBox(img,bbox)
    else:
        cv2.putText(img,"Lost",(75,75),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
        
    #cv2.imshow("Tracking",img)
    fps=cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(img,str(int(fps)),(75,50),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
    cv2.line(img,(int(window_width/2-75),0),(int(window_width/2-75),int(window_height)),(255,0,75),2)
    cv2.line(img,(int(window_width/2+75),0),(int(window_width/2+75),int(window_height)),(255,0,75),2)
    cv2.imshow("Tracking",img)
    if cv2.waitKey(1) & 0xff ==ord('a'):
        break
    if cv2.waitKey(1) & 0xff==ord('t'):
        tracker = cv2.TrackerMOSSE_create()
        bbox = cv2.selectROI("Tracking", img, False)
        tracker.init(img, bbox)
