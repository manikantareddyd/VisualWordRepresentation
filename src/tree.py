from sift import *
import numpy as np
from sklearn.cluster import KMeans

class VocabTree:

    def __init__(self,siftDescriptor,branches,threshold):
        self.threshold = threshold
        self.branches = branches
        self.adjancency = {}
        self.nodes = 1
        self.nodeImages = {}
        self.leafLabels=[]
        root = (np.array(siftDescriptor.FeatureVectors)).mean(axis=0)
        self.treeMap = {0:root} #Stores a map from node number to FeatureVector(Centroid)
        self.treeGenerator(0,siftDescriptor.FeatureVectors,siftDescriptor.imageName)

    def treeGenerator(self, rootLabel, points,names):
        # rootLabel is label of root
        # points is list of Feature Vectors
        # names is the name of the image corresponding Feature vector is in
        # print rootLabel, len(points)
        if len(points) < self.threshold:
            self.adjancency[rootLabel]=[]
            if rootLabel not in self.leafLabels:
                self.leafLabels.append(rootLabel)
            return
        else:
            localModel = KMeans(n_clusters = self.branches,n_jobs=4)
            localModel.fit(points)
            adj = []
            localTree = {}
            for i in localModel.cluster_centers_:
                self.treeMap[self.nodes]=i
                self.nodeImages[self.nodes]=[] # A map for node and the Images It has
                localTree[tuple(i)]=self.nodes
                adj.append(self.nodes)
                self.nodes = self.nodes + 1
            self.adjancency[rootLabel]=adj
            localClusterPoints = [[] for i in range(self.branches)]
            localClusterImgNames = [[] for i in range(self.branches)]
            # A local array to store which FV is in which cluster
            for i in range(len(points)):
                localClusterPoints[localModel.labels_[i]].append(points[i])
                localClusterImgNames[localModel.labels_[i]].append(names[i])
                if names[i] not in self.nodeImages[localTree[tuple(localModel.cluster_centers_[localModel.labels_[i]])]]:
                     self.nodeImages[localTree[tuple(localModel.cluster_centers_[localModel.labels_[i]])]].append(names[i])
            for i in range(self.branches):
                thisClusterCenter = tuple(localModel.cluster_centers_[i])
                self.treeGenerator(localTree[thisClusterCenter],localClusterPoints[i],localClusterImgNames[i])
