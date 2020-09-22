from cv2 import cv2
import serial
import time
print("starting serial connection ...")
s = serial.Serial('COM4',9600,timeout=.1)
s.open()
print("Starting")
tracker_yes=False
panAngle=90
#s.write(90)
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
succes, img = cap.read()
#tracker = cv2.TrackerMOSSE_create()
#tracker = cv2.TrackerCRST_create()
#bbox=cv2.selectROI("Tracking",img,False)
#tracker.init(img,bbox)

width_camera =int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
window_height,window_width,channels = img.shape


def drawBox(img,bbox):

    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]),
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(x,y,x*y/255),3,1)
    #print(cv2.width)
    mapServoPosition(x)


def mapServoPosition (x):
    global panAngle
    if (x < int((window_width/2)-75)):
        panAngle+=10
        if panAngle >180 :
            panAngle=180
        positionServo(panAngle)
        #print(panAngle)
    if (x > int(window_width/2)+75):
        panAngle-=10
        if panAngle < 10:
            panAngle = 10
        positionServo(panAngle)
        #print(panAngle)
    #time.sleep(.5)
    #panAngle=x
    
    #if (x < (width_camera/2)-75):
     #   panAngle += 10
      #  if panAngle > 170:
       #     panAngle = 170
       # positionServo (panAngle)
       # print(panAngle)
    #if (x > (width_camera/2)+75):
     #   panAngle -= 10
      #  if panAngle < 10:
       #     panAngle = 10
        #positionServo (panAngle)
        #print(panAngle)

    #if x <10:
     #   panAngle=10
    
def positionServo(pan):
    print(s.write(pan))
    


while True:
    timer = cv2.getTickCount()
    success,img=cap.read()
    if tracker_yes:
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
    
    if cv2.waitKey(1) & 0xff== ord('r'):
        s.write(90)
    if cv2.waitKey(1) & 0xff == ord('a'):
        break
    if cv2.waitKey(1) & 0xff== ord('t'):
        tracker = cv2.TrackerMOSSE_create()
        bbox = cv2.selectROI("Tracking", img, False)
        tracker.init(img, bbox)
        tracker_yes=True
cv2.destroyAllWindows()
