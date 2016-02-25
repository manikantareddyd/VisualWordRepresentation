from sift import *
from treelib import *
import numpy as np
from sklearn.cluster import KMeans

class VocabTree:

    def __init__(self,branches,threshold):
        siftDescriptor = SIFT()
        self.threshold = threshold
        self.branches = branches
        self.adjancency = {}
        self.nodes = 1
        root = (np.array(siftDescriptor.FeatureVectors)).mean(axis=0)
        self.treeMap = {'0':root}
        self.function(0,siftDescriptor.FeatureVectors)

    def function(self, rootLabel, points):
        print rootLabel, len(points)
        if len(points)< self.threshold:
            return
        else:
            model = KMeans(n_clusters = self.branches,n_jobs=3)
            model.fit(points)
            adj = []
            localtree = {}
            for i in model.cluster_centers_:
                self.treeMap[self.nodes]=i
                localtree[tuple(i)]=self.nodes
                adj.append(self.nodes)
                self.nodes = self.nodes + 1
            self.adjancency[rootLabel]=adj
            pointClusters = [[] for i in range(self.branches)]
            for i in range(len(points)):
                pointClusters[model.labels_[i]].append(points[i])
            for i in range(self.branches):
                thisClusterCenter = tuple(model.cluster_centers_[i])
                self.function(localtree[thisClusterCenter],pointClusters[i])
