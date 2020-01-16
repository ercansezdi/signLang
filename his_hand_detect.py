#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Ercan Sezdi"
__version__ = 0.5
import cv2
import numpy as np
import os
import sys


class signLanguageSave:
    def __init__(self):
        self.choose = "3"
        try:
            while self.choose != "1" and self.choose != "2":
                #self.choose = input()
                self.choose = "1"
                if self.choose != "1" and self.choose != "2":
                    print("Error Wrong Input")
        except:
            print("Error Wrong Input")
            sys.exit()
        try:
            self.camera = cv2.VideoCapture(3)
        except:
            self.camera = cv2.VideoCapture(1)
        self.char = ["A"]
        #self.char = ["A", "B", "C", "D", "W"]
        self.mkdir()

    def mkdir(self):
        if not (os.path.exists("pure_pict")):
            os.mkdir("pure_pict")
        if not (os.path.exists("pure_pict/compare_images")):
            os.mkdir("pure_pict/compare_images")
        if not (os.path.exists("pure_pict/test_images")):
            os.mkdir("pure_pict/test_images")
        if not (os.path.exists("conf/")):
            os.mkdir("conf/")
        for i in self.char:
            if not (os.path.exists("pure_pict/compare_images/" + i)):
                os.mkdir("pure_pict/compare_images/" + i)


    def start(self):
        counter = 0
        #char_counter = len(self.char)
        char_counter = 0
        address = os.getcwd() + "\\pure_pict\\compare_images"
        images = os.listdir(address)
        sizes = {}
        for char in images:
            num_x = address + "\\" + char
            num_x = os.listdir(num_x)
            sizes[char] = num_x
        while True:

            self.ret, self.frame = self.camera.read()
            self.frame_cut = self.frame[150:400, 150:400]
            cv2.imshow("cut-screen", self.frame_cut)
            cv2.putText(self.frame, str(self.char[char_counter-1]) + "-" + str(counter  + 1 + len(sizes[self.char[char_counter-1 ]])), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            cv2.imshow("full-screen", self.frame)


            if cv2.waitKey(1) & 0xFF == ord("s"):
                if self.choose == "1":
                    cv2.imwrite("pure_pict\\compare_images\\" + self.char[char_counter - 1] + "\\rgb_cut_" + self.char[char_counter -1 ] + str(len(sizes[self.char[char_counter -1 ]]) + counter) + ".png", self.frame_cut)
                    try:
                        print("Image Saved", self.char[char_counter-1], counter + int(sizes[self.char[char_counter-1]]))
                    except:
                        print("Image Saved", self.char[char_counter-1], counter  )
                    counter += 1
                    if counter == 15:
                        counter = 0
                        char_counter += 1
                    if char_counter == 5:
                        self.end()
                elif self.choose == "2":
                    cv2.imwrite("pure_pict\\test_images\\" + "\\rgb_full_" + str(counter + len(sizes[self.char[char_counter-1]])) + ".png", self.frame)
                    cv2.imwrite("pure_pict\\test_images\\" + "\\rgb_cut_" + str(counter + len(sizes[self.char[char_counter-1]])) + ".png", self.frame_cut)
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
        if not (os.path.exists("pure_pict")):
            os.mkdir("pure_pict")
        if not (os.path.exists("pure_pict/compare_images")):
            os.mkdir("pure_pict/compare_images")
        if not (os.path.exists("pure_pict/test_images")):
            os.mkdir("pure_pict/test_images")
        if not (os.path.exists("conf/")):
            os.mkdir("conf/")
        for i in self.char:
            if not (os.path.exists("pure_pict/compare_images/" + i)):
                os.mkdir("pure_pict/compare_images/" + i)

    def conf_prog(self):
        if self.choose == "1":
            try:
                self.camera = cv2.VideoCapture(1)
            except:
                self.camera = cv2.VideoCapture(1)
        self.char = ["A", "B", "C", "D"]#, "W"]

    def compare(self):
        address = os.getcwd() + "\\pure_pict\\compare_images\\"
        images_address = os.listdir(address)

        dict = {}
        for i in images_address:
            num_x = address + i
            num_x = os.listdir(num_x)
            dizi = []
            for num in range(0, int(len(num_x))):
                img_1 = cv2.imread(address + "\\" + i + "\\rgb_cut_" + i + str(num) + ".png")

                hsv_base = cv2.cvtColor(img_1, cv2.COLOR_BGR2HSV)
                hist_base = cv2.calcHist([hsv_base], [0, 1], None, [50, 60], [0, 180, 0, 256], accumulate=False)
                cv2.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
                dizi.append(hist_base)

            dict[i] = dizi
        return dict


    def start(self):
        old = "test"
        if self.choose == "1":
            datas = self.compare()
            arry = []
            compare_counter = 5
            while True:
                if len(arry) == compare_counter:
                    arry = []

                self.ret, self.frame = self.camera.read()
                self.frame_cut = self.frame[0:250, 0:250]
                hsv_base = cv2.cvtColor(self.frame_cut, cv2.COLOR_BGR2HSV)

                hist_test = cv2.calcHist([hsv_base], [0, 1], None, [50, 60], [0, 180, 0, 256], accumulate=False)
                cv2.normalize(hist_test, hist_test, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
                arr_1 = []
                arr_2 = []
                for i in self.char:
                    for hist_base in datas[i]:

                        #base_test1 = cv2.compareHist(hist_base, hist_test, 3) # min
                        #base_test2 = cv2.compareHist(hist_base, hist_test, 2) # max
                        base_test3 = cv2.compareHist(hist_base, hist_test, 1) # min
                        #base_test4 = cv2.compareHist(hist_base, hist_test, 0) # max

                        arr_1.append(base_test3)
                        arr_2.append(i)
                if old == str(arr_2[arr_1.index(min(arr_1))]):
                    pass
                else:
                    arry.append(str(arr_2[arr_1.index(min(arr_1))]))
                if len(arry) == compare_counter:
                    sayi = []
                    for i in self.char:
                        sayi.append(arry.count(i))
                    if old != sayi.index(max(sayi)):
                        old = self.char[sayi.index(max(sayi))]
                cv2.putText(self.frame_cut, old, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                            255)
                cv2.imshow("cut-screen", self.frame_cut)
                cv2.imshow("full-screen", self.frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.end()

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
    if choose == "1":
        st = signLanguageSave()
        st.start()
    elif choose == "2":
        st = signLanguageComp()
        st.start()
    else:
        print("Error Wrong Input")
