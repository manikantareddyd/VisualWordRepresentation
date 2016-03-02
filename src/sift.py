import cv2
from os import listdir
import numpy as np
class SIFT:

    def __init__(self,n):
        self.FeatureVectors = []
        self.imgfiles   = sorted(listdir('../ukbench/full'))[:n]
        self.imageFeat = {}
        self.imageName  = []
        self.extractAll()
    def extractAll(self):
        for imgfile in self.imgfiles:
            self.extract(imgfile)
        return
    def extract(self,imgfile):
        sift = cv2.xfeatures2d.SIFT_create(nfeatures=500)
        img = cv2.imread('../ukbench/full/'+imgfile)
        gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        kp,des = sift.detectAndCompute(gray,None)
        self.imageFeat[str(imgfile)] = np.array(des)
        for j in des:
            self.FeatureVectors.append(j)
            self.imageName.append(imgfile)
        del sift
        del img
        del gray
        del des
        del kp
        return
