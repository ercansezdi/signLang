#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = "Ercan Sezdi"

import cv2
import numpy as np
import os
import sys
class signLanguageSave:
    def __init__(self):
        self.choose = "3"
        try:
            while self.choose != "1" and self.choose != "2":
                print("""
                       1 - > Save compare images 
                       2 - > Save test images 
                       """)
                print(">>",end="")
                self.choose = input()
                if self.choose != "1" and self.choose != "2":
                    print("Error Wrong Input")
        except:
            print("Error Wrong Input")
            sys.exit()
        self.conf_prog()
        self.mkdir()

    def mkdir(self):
        if not(os.path.exists("pure_pict")):
            os.mkdir("pure_pict")
        if not(os.path.exists("pure_pict/compare_images")):
            os.mkdir("pure_pict/compare_images")
        if not(os.path.exists("pure_pict/test_images")):
            os.mkdir("pure_pict/test_images")
        if not(os.path.exists("conf/")):
            os.mkdir("conf/")
        for i in self.char:
            if not (os.path.exists("pure_pict/compare_images/"+ i)):
                os.mkdir("pure_pict/compare_images/" + i)
    def conf_prog(self):
        try:
            self.camera = cv2.VideoCapture(3)
        except:
            self.camera = cv2.VideoCapture(1)
        self.char = ["A","B","C","D","W"]
    def start(self):
        counter = 0
        char_counter = 0
        while True:
            self.ret, self.frame = self.camera.read()
            self.gray = cv2.cvtColor(self.frame[0:250,0:250], cv2.COLOR_BGR2GRAY)
            self.frame_cut = self.frame[0:250,0:250]
            cv2.imshow("cut-screen",self.frame_cut)
            cv2.imshow("full-screen",self.frame)

            if cv2.waitKey(1) & 0xFF == ord("s"):
                if self.choose == "1":
                    cv2.imwrite("pure_pict\\compare_images\\" + self.char[char_counter] + "\\rgb_full_" + self.char[char_counter] + str(counter) + ".png",self.frame)
                    cv2.imwrite("pure_pict\\compare_images\\" + self.char[char_counter] + "\\rgb_cut_" + self.char[char_counter] + str(counter) + ".png",self.frame_cut)

                    print("Image Saved",self.char[char_counter] , counter +1 )
                    counter += 1
                    if counter == 2:
                        counter = 0
                        char_counter += 1
                    if char_counter == 5:
                        self.end()
                elif self.choose == "2":
                    cv2.imwrite("pure_pict\\test_images\\" +  "\\rgb_full_" +  str(counter) + ".png", self.frame)
                    cv2.imwrite("pure_pict\\test_images\\" +  "\\rgb_cut_" + str(counter) + ".png", self.frame_cut)
                    print("Image Saved")
                    self.end()
                else:
                    pass

    def end(self):
        self.camera.release()
        cv2.destroyAllWindows()

class signLanguageComp:
    def __init__(self):
        self.choose = "3"
        try:
            while self.choose != "1" and self.choose != "2":
                print("""
                1 - > Video compare images
                2 - > Image compare images
                """)
                print(">>", end="")
                self.choose = input()
                #self.choose = "1"
                if self.choose != "1" and self.choose != "2":
                    print("Error Wrong Input")
        except:
            print("Error Wrong Input")
            sys.exit()

        self.conf_prog()
        self.mkdir()

    def mkdir(self):
        if not(os.path.exists("pure_pict")):
            os.mkdir("pure_pict")
        if not(os.path.exists("pure_pict/compare_images")):
            os.mkdir("pure_pict/compare_images")
        if not(os.path.exists("pure_pict/test_images")):
            os.mkdir("pure_pict/test_images")
        if not(os.path.exists("conf/")):
            os.mkdir("conf/")
        for i in self.char:
            if not (os.path.exists("pure_pict/compare_images/"+ i)):
                os.mkdir("pure_pict/compare_images/" + i)
    def conf_prog(self):
        if self.choose == "1":
            try:
                self.camera = cv2.VideoCapture(3)
            except:
                self.camera = cv2.VideoCapture(1)
        self.char = ["A","B","C","D","W"]
        self.choose_proceses = ["video_compare_images","images_compare_images"]

    def start(self):
        if self.choose == "1":
            old = False
            while True:

                self.ret, self.frame = self.camera.read()
                self.gray = cv2.cvtColor(self.frame[0:250, 0:250], cv2.COLOR_BGR2GRAY)
                self.frame_cut = self.frame[0:250, 0:250]
                cv2.imshow("cut-screen", self.frame_cut)
                cv2.imshow("full-screen", self.frame)
                img_1 = self.frame_cut
                address = os.getcwd() + "\\pure_pict\\compare_images"
                images = os.listdir(address)
                arr = []

                for char in images:
                    img_2 = cv2.imread(address + "\\" + char + "\\rgb_cut_" + char + "0.png")

                    hsv_base = cv2.cvtColor(img_1, cv2.COLOR_BGR2HSV)
                    hsv_test1 = cv2.cvtColor(img_2, cv2.COLOR_BGR2HSV)

                    hist_base = cv2.calcHist([hsv_base], [0, 1], None, [50, 60], [0, 180, 0, 256], accumulate=False)
                    cv2.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
                    hist_test1 = cv2.calcHist([hsv_test1], [0, 1], None, [50, 60], [0, 180, 0, 256], accumulate=False)
                    cv2.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

                    base_test1 = cv2.compareHist(hist_base, hist_test1, 3)

                    arr.append(base_test1)
                if old == self.char[arr.index(min(arr))]:
                    pass
                else:
                    old = self.char[arr.index(min(arr))]
                    print("------", old, "------")

                cv2.putText(self.frame_cut, old, (0, 0), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)


                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.end()
        elif self.choose == "2":
            img_1 = cv2.imread("pure_pict\\test_images\\rgb_cut_0.png")
            address = os.getcwd() + "\\pure_pict\\compare_images"
            images = os.listdir(address)
            arr = []
            for char in images:
                img_2 = cv2.imread(address + "\\" + char + "\\rgb_cut_" + char + "1.png")

                hsv_base = cv2.cvtColor(img_1, cv2.COLOR_BGR2HSV)
                hsv_test1 = cv2.cvtColor(img_2, cv2.COLOR_BGR2HSV)

                hist_base = cv2.calcHist([hsv_base], [0, 1], None, [50, 60], [0, 180, 0, 256], accumulate=False)
                cv2.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
                hist_test1 = cv2.calcHist([hsv_test1], [0, 1], None, [50, 60], [0, 180, 0, 256], accumulate=False)
                cv2.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

                base_test1 = cv2.compareHist(hist_base, hist_test1, 3)
                print('Main - {} = {} '.format(char,base_test1))
                arr.append(base_test1)
            print("--------------",self.char[arr.index(max(arr))],"--------------")
        else:
            pass
    def end(self):
        self.camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    print("""
                    1 - > Save
                    2 - > Compare
                    """)
    print(">>", end="")
    choose = input()
    #choose = "2"
    if choose == "1":
        st = signLanguageSave()
        st.start()
    elif choose == "2":
        st = signLanguageComp()
        st.start()
    else:
        print("Error Wrong Input")
