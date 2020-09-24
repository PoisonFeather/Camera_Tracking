from cv2 import cv2
import serial
import time
import keyboard
print("starting serial connection ...")
s = serial.Serial('COM4',9600,timeout=1)
#s.open()
print("Starting")
tracker_yes=False
#s.write(90)




cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
succes, img = cap.read()
#tracker = cv2.TrackerMOSSE_create()
#tracker = cv2.TrackerCRST_create()
#bbox=cv2.selectROI("Tracking",img,False)
#tracker.init(img,bbox)t

width_camera =int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
window_height,window_width,channels = img.shape


def drawBox(img,bbox):

    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]),
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(x,y,x*y/255*10),3,1)
    #print(cv2.width)
    mapServoPosition(x,w)


def mapServoPosition (x,w):
    
    if (x+(w/2) < int((window_width/2)-75) and not (x+(w/2) > int((window_width/2)+75))):
        positionServo("+")

    if (x+(w/2) > int((window_width/2)+75) and not (x+(w/2) < int((window_width/2)-75))):
        positionServo("-")
    if(x+(w/2)<int((window_width/2)+75) and x+(w/2)>int((window_width/2)-75)):
        positionServo("ok")
count = 0
write_ok=True
def positionServo(pan):
    global write_ok
    #encoded=0
    #global count
    #byted=bytes([int(pan)])
    #s.write(byted)
    #count=count+1
    #print(byted)
    #if count >= 1 :
     #   time.sleep(0.035)
      #  s.write("".encode())
        #s.write("\\".encode())
       # count=0
    #print(pan.encode())a
    if(pan == "+" or pan=="-" and write_ok==False):
        s.write(pan.encode())
        write_ok=True
        time.sleep(0.25)
    elif pan=="ok" and write_ok==True:
        write_ok=False
        s.write('\n'.encode())
    #time.sleep(0.01)  
    feedback=s.readline().decode('ascii')
    if feedback == "b'1'" or feedback == "b'2'" or  feedback == "ok":
        pass
    #else:
        #print("error")
try:
    while True:
    
        #timer = cv2.getTickCount()
        success, img = cap.read()
        if cv2.waitKey(1) & 0xff == ord('t'):
            tracker = cv2.TrackerKCF_create()
            bbox = cv2.selectROI("Tracking", img, False)
            tracker.init(img, bbox)
            tracker_yes = True
            #s.close()
        elif cv2.waitKey(1) & 0xff == ord('c'):
            break
        if tracker_yes:
            success,bbox = tracker.update(img)  
            if success :
                drawBox(img,bbox)
            else:
                cv2.putText(img,"Lost",(75,75),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
     
    #cv2.imshow("Tracking",img)
    #fps=cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    #cv2.putText(img,str(int(fps)),(75,50),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
        cv2.line(img,(int(window_width/2-75),0),(int(window_width/2-75),int(window_height)),(255,0,75),1)
        cv2.line(img,(int(window_width/2+75),0),(int(window_width/2+75),int(window_height)),(255,0,75),1)
        cv2.imshow("Tracking",img)
        if keyboard.is_pressed('a'):
            s.write("+".encode())
            time.sleep(.1)
            s.write("\n".encode())
        if keyboard.is_pressed('d'):
            s.write("-".encode())
            time.sleep(0.1)
            s.write("\n".encode())
except KeyboardInterrupt:
    cv2.destroyAllWindows() 
    s.close() 
    exit()
    
cv2.destroyAllWindows() 
s.close() 
exit()
   
