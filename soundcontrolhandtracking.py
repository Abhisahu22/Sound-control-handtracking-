import cv2
import time
import numpy as np
import handtrackingmodule as htm
import math
import osascript
#from ctypes import cast ,POINTER
#from ctypes import CLSCTX_ALL
#from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
cap=cv2.VideoCapture(0)
ptime=0
detector=htm.handDetector(detectionCon=0.7)

#devices = AudioUtilities.GetSpeakers()
#interface = devices.Activate(
#IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
#print(volume.GetVolumeRange())
#volume.SetMasterVolumeLevel(-20.0, None)
#target_volume = 
vol = "set volume output volume " + str(50)
print(osascript.osascript(vol))


volu=0




while True:
    success , img=cap.read()
    img=detector.findhands(img)
    lmlist=detector.findposition(img,draw=False)
    if len(lmlist)!=0:
       #print(lmlist[4])
       x1,y1=lmlist[4][1],lmlist[4][2]
       x2,y2=lmlist[8][1],lmlist[8][2]
       c1,c2=(x1+x2)//2,(y1+y2)//2
       cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED )
       cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED )
       cv2.line(img,(x1,y1),(x2,y2), (255,0,255),3)
       cv2.circle(img,(c1,c2),15,(255,0,255),cv2.FILLED )
       length=math.hypot(x2-x1,y2-y1)
       if length<60:
           cv2.circle(img,(c1,c2),15,(0,255,0),cv2.FILLED )
       volu=np.interp(length,[60,600],[0,100])
       volubar=np.interp(length,[60,600],[400,150])
       print(volu)
       target_volume=volu
       vol = "set volume output volume " + str(volu)
       osascript.osascript(vol)
       cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
       cv2.rectangle(img,(50,int(volubar)),(85,400),(0,255,0),cv2.FILLED)
       

       #print(length)
      







    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),1 )
    cv2.imshow("Img",img)
    cv2.waitKey(1)