#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = "Ercan Sezdi"
__version__ = 0.2

import cv2
import numpy as np
import os
import configparser
from matplotlib import pyplot as plt


class signLangSave:
    def __init__(self):
        self.conf()
        self.mkdir()
        self.pic_counter()
        self.loop()
    def conf(self):
        self.config = configparser.ConfigParser()
        self.config.read("conf\\data.cfg")
        self.camera = cv2.VideoCapture(3)
        self.kernel = np.ones((6, 6), np.uint8)
        lower_red = np.array([int(x) for x in self.config["veri"]["lower_red"].split(",")])
        upper_red = np.array([int(x) for x in self.config["veri"]["upper_red"].split(",")])
        lower_green = np.array([int(x) for x in self.config["veri"]["lower_green"].split(",")])
        upper_green = np.array([int(x) for x in self.config["veri"]["upper_green"].split(",")])
        lower_blue = np.array([int(x) for x in self.config["veri"]["lower_blue"].split(",")])
        upper_blue = np.array([int(x) for x in self.config["veri"]["upper_blue"].split(",")])
        lower_yellow = np.array([int(x) for x in self.config["veri"]["lower_yellow"].split(",")])
        upper_yellow = np.array([int(x) for x in self.config["veri"]["upper_yellow"].split(",")])
        lower_black = np.array([int(x) for x in self.config["veri"]["lower_black"].split(",")])
        upper_black = np.array([int(x) for x in self.config["veri"]["upper_black"].split(",")])
        self.color_row = ["red", "gre", "blu", "yel", "bla"]
        self.colors = {"red": [lower_red, upper_red], "gre": [lower_green, upper_green],
                       "blu": [lower_blue, upper_blue], "yel": [lower_yellow, upper_yellow],
                       "bla": [lower_black, upper_black]}
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
        if not(os.path.exists("conf/")):
            os.mkdir("conf/")
    def pic_counter(self):
        file_address = os.getcwd()
        files = os.listdir(file_address + "\\proc_pict\\red")
        self.save_num = len(files) + 1
    def loop(self):
        counter = 0
        while True:

            self.ret, self.frame = self.camera.read()
            self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)  # görüntüyü hsv formatına cevirdim
            self.renkFiltresi = cv2.inRange(self.hsv, self.colors[self.color_row[counter]][0],self.colors[self.color_row[counter]][1])
            self.renkFiltresi = cv2.morphologyEx(self.renkFiltresi, cv2.MORPH_CLOSE, self.kernel)  # boşluk doldurma
            self.res = cv2.bitwise_and(self.frame,self.frame,mask=self.renkFiltresi)
            self.result = self.frame.copy()
            self.hand_result = self.result
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

            cv2.putText(self.result,str(self.color_row[counter]), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            cv2.imshow("orjinal image", self.result)

            if cv2.waitKey(1) & 0xFF == ord("s"):
                cv2.imwrite("proc_pict\\" + self.color_row[counter] + "\\" + str(self.save_num) + ".png", self.hand_result)
                print("Image Saved for ", self.color_row[counter])
                counter += 1
                if counter == 5:
                    self.end()
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.end()
    def end(self):
        self.camera.release()
        cv2.destroyAllWindows()

class signLang:
    def __init__(self):
        self.pic_counter()
        self.loop()
    def pic_counter(self):
        file_address = os.getcwd()
        files = os.listdir(file_address + "\\proc_pict\\red")
        self.save_num = len(files) + 1
    def loop(self):
        for folder in ["red","gre","blu","yel","bla"]:
            counter = 1
            array = []
            while counter < self.save_num:
                address = "proc_pict\\" +  folder + "\\" + str(counter) + ".png"

                hist = cv2.calcHist([address], [0, 1, 2], None, [8, 8, 8],
                                    [0, 256, 0, 256, 0, 256])
                hist = cv2.normalize(hist, hist).flatten()
                cv2.compareHist
                counter += 1
            print(array)
if __name__ == "__main__":
    run = signLang()