import cv2
import mediapipe as mp
import time

class handDetector():
     def __init__(self, mode=False, maxhands=2, detectionCon=0.5, trackCon=0.5):
          self.mode= mode
          self.maxhands= maxhands
          self.detectionCon= detectionCon
          self.trackCon= trackCon
          self.mphands= mp.solutions.hands
          self.hands= self.mphands.Hands( )
          self.mpdraw=mp.solutions.drawing_utils

     def findhands(self,img,draw=True):
        imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgrgb)
      
        if self.results.multi_hand_landmarks:
            for h1 in self.results.multi_hand_landmarks:
                if draw:
                   self.mpdraw.draw_landmarks( img,h1,self.mphands.HAND_CONNECTIONS) 
        
        return img

     def findposition(self,img,handNo=0,draw=True):
          lmlist=[]
          if self.results.multi_hand_landmarks:
           
                myhand=self.results.multi_hand_landmarks[handNo]
                for id,lm in enumerate(myhand.landmark):
                   h,w,c=img.shape
                   cx,cy=int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                   lmlist.append([id,cx,cy])
                   if draw:
                      cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
          return lmlist
                 
                
               
              
            

def main():
        ptime=0
        ctime=0
        cap=cv2.VideoCapture(0)
        detector=handDetector()
        

        while True: 
           success , img=cap.read()
           img=detector.findhands(img)
           lmlist=detector.findposition(img)
           if len(lmlist)!=0:
             print(lmlist[4])
           ctime=time.time()
           fps=1/(ctime-ptime)
           ptime=ctime
           cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3 )
                

           cv2.imshow("Img",img)
           cv2.waitKey(1)






if __name__== "__main__" :
     main()