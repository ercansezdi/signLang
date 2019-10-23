"""
    ### Works ###

    renk filtresi uygularken yeşil filtre sari ile karışıyor.
    renk filtresi uygularken mavi filtre çok karıştırıyor.
    renk filtresi uygularken siyah filtre algılaması çok az

"""
__author__ = "Ercan Sezdi"
__version__ = 0.2

import cv2
import numpy as np
import os



class signLang:
    def __init__(self):
        self.camera = cv2.VideoCapture(3)
        self.kernel = np.ones((6, 6), np.uint8)

        lower_red = np.array([161, 155, 84]) # ok
        upper_red = np.array([179, 255, 255]) # ok

        lower_green = np.array([25, 52, 72])
        upper_green = np.array([102, 255, 255])

        lower_blue = np.array([94, 80, 2])
        upper_blue = np.array([126, 255, 255])

        lower_yellow = np.array([22, 60, 200]) # ok
        upper_yellow = np.array([60, 255, 255]) # ok

        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 150, 50])
        self.color_row = ["red","gre","blu","yel","bla"]
        self.colors = {"red": [lower_red, upper_red], "gre": [lower_green, upper_green],
                       "blu": [lower_blue, upper_blue], "yel": [lower_yellow, upper_yellow],
                       "bla": [lower_black, upper_black]}
        self.mkdir()
        self.loop()

    def mkdir(self):
        if not(os.path.exists("proc_pict")):
            os.mkdir("proc_pict")
        if not(os.path.exists("proc_pict/" + str(self.color_row[0]))):
            os.mkdir("proc_pict/" + str(self.color_row[0]))
        if not(os.path.exists("proc_pict/" + str(self.color_row[1]))):
            os.mkdir("proc_pict/" + str(self.color_row[1]))
        if not(os.path.exists("proc_pict/" + str(self.color_row[2]))):
            os.mkdir("proc_pict/" + str(self.color_row[2]))
        if not(os.path.exists("proc_pict/" + str(self.color_row[3]))):
            os.mkdir("proc_pict/" + str(self.color_row[3]))
        if not(os.path.exists("proc_pict/" + str(self.color_row[4]))):
            os.mkdir("proc_pict/" + str(self.color_row[4]))

    def loop(self):
        while True:
            self.ret, self.frame = self.camera.read()
            self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)  # görüntüyü hsv formatına cevirdim
            self.renkFiltresi = cv2.inRange(self.hsv, self.colors[self.color_row[2]][0],self.colors[self.color_row[2]][1])  # hsv yi alt ve üst değerlere göre filtreledik
            self.renkFiltresi = cv2.morphologyEx(self.renkFiltresi, cv2.MORPH_CLOSE, self.kernel)  # boşluk doldurma
            self.res = cv2.bitwise_and(self.frame,self.frame,mask=self.renkFiltresi)
            self.result = self.frame.copy()
            cnts, hierarchy = cv2.findContours(self.renkFiltresi, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            max_genislik = 0
            max_uzunluk = 0
            max_index = -1

            for t in range(len(cnts)):
                cnt = cnts[t]
                x, y, w, h = cv2.boundingRect(cnt)
                if (w > max_genislik and h > max_uzunluk):
                    max_uzunluk = h
                    max_genislik = w
                    max_index = t
            if len(cnts) > 0:

                x, y, w, h = cv2.boundingRect(cnts[max_index])
                cv2.rectangle(self.result, (x, y), (x + w, y + h), (0, 255, 0), 2)
                self.hand_result = self.renkFiltresi[y:y + h, x:x + w]
                cv2.imshow("result", self.hand_result)
            cv2.putText(self.result, "Show " + str(self.color_row[3]), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            cv2.imshow("orjinal image", self.result)


            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.end()

    def end(self):
        self.camera.release()
        cv2.destroyAllWindows()
if __name__ == "__main__":
    run = signLang()