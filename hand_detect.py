
#!/usr/bin/env python
# -*- coding: utf8 -*-

__auther__ = 'Ercan Sezdi'
__version__ = '0.2'
__eposta__ = "ercansezdizero@gmail.com"

import cv2
import numpy as np

class signLang:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.kernel = np.ones((6,6),np.uint8)
        self.test_photo = cv2.imread("data/pokemon_games.png")#"data/pic_1.jpg",0)
        self.red = [[17, 15, 100], [50, 56, 200]]
        self.green = [[40, 40,40], [70, 255,255]]
        self.blue = [[86, 31, 4], [220, 88, 50]]
        self.yellow = [[25, 146, 190], [62, 174, 250]]
        self.color_choice = self.red
        self.loop()

    def loop(self):
        self.choice = "video"
        if self.choice == "video":

            while True:
                self.ret,self.frame = self.camera.read()
                #self.frame = self.frame[0:350,0:350]
                self.hsv = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV) #görüntüyü hsv formatına cevirdim

                altDeger = np.array([0,20,50]) #sarı
                #altDeger = np.array([237,100,0])
                ustDeger = np.array([40,255,255])

                self.renkFiltresi = cv2.inRange(self.hsv,altDeger,ustDeger) # hsv yi alt ve üst değerlere göre filtreledik
                self.renkFiltresi = cv2.morphologyEx(self.renkFiltresi,cv2.MORPH_CLOSE,self.kernel) # boşluk doldurma
                self.result = self.frame.copy()
                cnts , hierarchy = cv2.findContours(self.renkFiltresi,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

                max_genislik = 0
                max_uzunluk =  0
                max_index   = -1

                for t in range(len(cnts)):
                    cnt = cnts[t]
                    x,y,w,h = cv2.boundingRect(cnt)
                    if (w > max_genislik and h > max_uzunluk):
                        max_uzunluk = h
                        max_genislik = w
                        max_index = t


                if len(cnts) > 0 :
                    x,y,w,h = cv2.boundingRect(cnts[max_index])
                    cv2.rectangle(self.result,(x,y),(x+w,y+h),(0,255,0),2)
                    self.hand_result = self.renkFiltresi[y:y+h,x:x+w]

                    #cv2.imshow("hand_result",resized_image)#self.hand_result)


                #cv2.imshow('camera', self.frame)
                #cv2.imshow("Renk Filtresi",self.renkFiltresi)
                #self.result=cv2.resize(result,(100,100))
                #cv2.imshow("Result",self.result)

                if cv2.waitKey(1)&0xFF == ord('q'):
                    self.end()

        elif self.choice == "photo":
            print(self.color_choice[0])
            hsv = cv2.cvtColor(self.test_photo,cv2.COLOR_BGR2HSV)
            lower = np.array(self.color_choice[0])
            upper = np.array(self.color_choice[1])
            result = cv2.inRange(hsv,lower,upper)
            cv2.imshow("Original Image ",self.test_photo)
            cv2.imshow("result",result)

            cv2.waitKey(0)

        else:
            pass



    def end(self):
        #cv2.imwrite("data/one.jpg",self.hand_result)
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run = signLang()
