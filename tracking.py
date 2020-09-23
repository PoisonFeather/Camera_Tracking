from cv2 import cv2
import serial
import time
print("starting serial connection ...")
s = serial.Serial('COM3',9600,timeout=.1)

print("Starting")
tracker_yes=False
#s.write(90)
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
succes, img = cap.read()
#tracker = cv2.TrackerMOSSE_create()
#tracker = cv2.TrackerCRST_create()
#bbox=cv2.selectROI("Tracking",img,False)a
#tracker.init(img,bbox)

width_camera =int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
window_height,window_width,channels = img.shape


def drawBox(img,bbox):

    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]),
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(x,y,x*y/255*10),3,1)
    #print(cv2.width)
    mapServoPosition(x)


def mapServoPosition (x):
    
    if (x < int((window_width/2)-75)):
        positionServo(str(2))

    if (x > int((window_width/2)+75)):
        positionServo(str(1))
count = 0
def positionServo(pan):
    #encoded=0
    global count
    byted=bytes([int(pan)])
    s.write(byted)

    count=count+1
    time.sleep(0.1)
    print(byted)
    if count >= 2 :
        time.sleep(0.25)
        s.write("".encode())
        count=0
    


while True:
    timer = cv2.getTickCount()
    success,img=cap.read()
    if cv2.waitKey(1) & 0xff == ord('t'):
        tracker = cv2.TrackerMOSSE_create()
        bbox = cv2.selectROI("Tracking", img, False)
        tracker.init(img, bbox)
        tracker_yes = True
    if cv2.waitKey(1) & 0xff == ord('r'):
        s.write(90)
    if cv2.waitKey(1) & 0xff == ord('a'):
        cv2.destroyAllWindows()
        break
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

cv2.destroyAllWindows() 
s.close() 
    

