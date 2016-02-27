import cv2
from os import listdir
import numpy as np
class SIFT:

    def __init__(self):
        self.FeatureVectors = []
        self.imgfiles   = listdir('data')
        self.imageFeat = {}
        self.imageName  = []
        self.extract()
    def extract(self):
        for imgfile in self.imgfiles:
            sift = cv2.xfeatures2d.SIFT_create()
            img = cv2.imread('data/'+imgfile)
            gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            kp,des = sift.detectAndCompute(gray,None)
            self.imageFeat[str(imgfile)] = np.array(des)
            for j in des:
                self.FeatureVectors.append(j)
                self.imageName.append(imgfile)
