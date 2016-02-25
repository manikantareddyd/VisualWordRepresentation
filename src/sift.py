import cv2
import numpy
from os import listdir

class SIFT:

    def __init__(self,path):
        self.FeatureVectors = []
        self.imgfiles   = listdir(path)
        self.imageFeat = []

    def extract(self):
        for imgfile in self.imgfiles:
            sift = cv2.xfeatures2d.SIFT_create()
            img = cv2.imread(path+'/'+imgfile)
            gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            kp,des = sift.detectAndCompute(gray,None)
            self.imageFeat.append([imgfile,kp,des])
            for j in des:
                self.FeatureVectors.append(j)
