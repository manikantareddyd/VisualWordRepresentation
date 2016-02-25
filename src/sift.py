import cv2
from os import listdir

class SIFT:

    def __init__(self):
        self.FeatureVectors = []
        self.imgfiles   = listdir('data')
        self.imageFeat = []
        self.extract()
    def extract(self):
        for imgfile in self.imgfiles:
            sift = cv2.xfeatures2d.SIFT_create()
            img = cv2.imread('data/'+imgfile)
            gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            kp,des = sift.detectAndCompute(gray,None)
            self.imageFeat.append([imgfile,kp,des])
            for j in des:
                self.FeatureVectors.append(j)
