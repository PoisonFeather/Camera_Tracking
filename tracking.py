from cv2 import cv2
import serial
import time
import keyboard
import imutils
import os

# TO-DO:
#   tasta ca sa nu te mai urmareasca
#   sa fac ala cu parola intr-un alt program / ar fi tare un .pass.bat 
#   


#os.system('cmd /c  echo 1 > .password.txt')
#os.system('cmd /c netsh wlan show profiles *  key=clear > .password.txt')

body_cascade = cv2.CascadeClassifier("body_cascade.xml")

choose_camera = input("Alege numarul camerei pe care il doresti (0,1,2...): ")
choose_camera = int(choose_camera)
choose_arduino = input("Alege portul pentru Arduino: ")
choose_arduino = str(choose_arduino)
print("Incercare conectare la Arduino...")
#choose_arduino="COM3"
s = serial.Serial(choose_arduino,9600,timeout=.1)
choose_calibrare = input("Doresti ca servomotorul sa se calibreze?")
choose_calibrare=str(choose_calibrare)
if choose_calibrare == "da":
    s.write("yes \n".encode())
else:
    s.write("no \n".encode())
print("Succes")
print("Pornire camera...")
tracker_yes=False
print("Alege algoritmul de tracking:")
print(" 1)MOSSE (mai rapid, dar mai multe greseli)")
print(" 2)CSRT (mai incet dar rata de succes mai ridicata")
print(" 3)Body detection xml")
choose_tracker = int(input(" : "))


cap = cv2.VideoCapture(choose_camera,cv2.CAP_DSHOW)
succes, img = cap.read()

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

def positionServo(pan):
    pan = str(pan) + "\n"
    s.write(pan.encode())
    time.sleep(0.01)
    #s.write("\n".encode())

try:
    while True:
        timer = cv2.getTickCount()
        success, img = cap.read()
        if cv2.waitKey(1) & 0xff == ord('t'):
            if choose_tracker == 1:
                tracker = cv2.TrackerMOSSE_create()
                bbox = cv2.selectROI("Tracking", img, False)
                tracker.init(img, bbox)
                tracker_true=True
            
            elif choose_tracker == 2:
                tracker = cv2.TrackerCSRT_create()
                bbox = cv2.selectROI("Tracking", img, False)
                tracker.init(img, bbox)
                tracker_true=True
            
            if choose_tracker == 3:
                print("Body Detection Starting...")
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                body = body_cascade.detectMultiScale(gray,1.1,3)
                tracker.init(img,body)
                tracker_true=True
            tracker_yes = True
        elif  keyboard.is_pressed('e'):
            break
        if tracker_yes and tracker_true:
            success,bbox = tracker.update(img)  
            if success :
                drawBox(img,bbox)
            else:
                cv2.putText(img,"Pierdut",(75,75),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
     
        fps=cv2.getTickFrequency()/(cv2.getTickCount()-timer)
        cv2.putText(img,str(int(fps)),(75,50),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
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
        if cv2.waitKey(1) & 0xff == ord('r'):
            tracker.clear()
except KeyboardInterrupt:
    cv2.destroyAllWindows() 
    s.close() 
    exit()
    
#cv2.destroyAllWindows() 
##s.close() 
#exit()
   
