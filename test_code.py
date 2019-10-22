
import cv2
import numpy as np

class signLang:
    def __init__(self):
        self.camera = cv2.VideoCapture(1)
        self.kernel = np.ones((12, 12), np.uint8)
        self.loop()


    def loop(self):
        while True:
            self.ret, self.frame = self.camera.read()

            self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)  # görüntüyü hsv formatına cevirdim
            altDeger = np.array([35, 140, 60]) #blue
            ustDeger = np.array([255, 255, 180])
            self.renkFiltresi = cv2.inRange(self.hsv, altDeger,ustDeger)  # hsv yi alt ve üst değerlere göre filtreledik
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

            cv2.imshow("orjinal image", self.result)


            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.end()

    def end(self):
        self.camera.release()
        cv2.destroyAllWindows()
if __name__ == "__main__":
    run = signLang()