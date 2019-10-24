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
        self.camera = cv2.VideoCapture(3)
        self.char = ["A","B","C","D","E"]
    def start(self):
        counter = 0
        char_counter = 0
        while True:
            self.ret, self.frame = self.camera.read()
            self.gray = cv2.cvtColor(self.frame[0:250,0:250], cv2.COLOR_BGR2GRAY)
            cv2.imshow("result1",self.gray)
            cv2.imshow("result2",self.frame)

            if cv2.waitKey(1) & 0xFF == ord("s"):
                if self.choose == "1":
                    cv2.imwrite("pure_pict\\compare_images\\" + self.char[char_counter] + "\\rgb_" + self.char[char_counter] + str(counter) + ".png",self.frame)
                    cv2.imwrite("pure_pict\\compare_images\\" + self.char[char_counter] + "\\gray_" + self.char[char_counter] + str(counter) + ".png",self.gray)

                    print("Image Saved",self.char[char_counter] , counter +1 )
                    counter += 1
                    if counter == 2:
                        counter = 0
                        char_counter += 1
                    if char_counter == 5:
                        self.end()
                elif self.choose == "2":
                    cv2.imwrite("pure_pict\\test_images\\" +  "\\rgb_" +  str(counter) + ".png", self.frame)
                    cv2.imwrite("pure_pict\\test_images\\" +  "\\gray_" + str(counter) + ".png", self.gray)
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
            self.camera = cv2.VideoCapture(3)
        self.char = ["A","B","C","D","E"]
        self.choose_proceses = ["video_compare_images","images_compare_images"]

    def start(self):
        if self.choose == "1":
            while True:
                self.ret, self.frame = self.camera.read()
                self.gray = cv2.cvtColor(self.frame[0:250, 0:250], cv2.COLOR_BGR2GRAY)
                cv2.imshow("result1", self.gray)
                cv2.imshow("result2", self.frame)



                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.end()
        elif self.choose == "2":
            pass
        else:
            pass
    def end(self):
        self.camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    st = signLanguageSave()
    st.start()