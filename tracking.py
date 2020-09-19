import cv2
print("Starting")

cap = cv2.VideoCapture(0)
#tracker = cv2.TrackerMOSSE_create()
#tracker = cv2.TrackerMedianFlow_create()
tracker =  cv2.TrackerBoosting_create()
succes, img = cap.read()
bbox=cv2.selectROI("Tracking",img,False)
tracker.init(img,bbox)

def drawBox(img,bbox):
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]),
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(x,y,x*y/255),3,1)

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
    cv2.imshow("Tracking",img)
    if cv2.waitKey(1) & 0xff ==ord('a'):
        break
    if cv2.waitKey(1) & 0xff==ord('t'):
        tracker = cv2.TrackerMOSSE_create()
        bbox = cv2.selectROI("Tracking", img, False)
        tracker.init(img, bbox)