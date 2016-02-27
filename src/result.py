from tree import *
import math
class result:
    def __init__(self,s,v):
        self.siftDescriptor = s
        self.vocabTree = v
        self.imageDescriptors={}
        print 'Hi'
        self.descriptorWeights={}
        for i in self.vocabTree.leafLabels:
            self.descriptorWeights[i]=math.log1p(len(self.siftDescriptor.imgfiles)/float(len(self.vocabTree.nodeImages[i])))

    def getLeafLabel(self,rootLabel,vector):
        if(len(self.vocabTree.adjancency[rootLabel])!=0):
            distances={}
            for i in self.vocabTree.adjancency[rootLabel]:
                distances[i]=np.linalg.norm(np.array(vector)-np.array(self.vocabTree.treeMap[i]))
                #print distances[i],i
            # print 'llll'
            # print min(distances,key=distances.get)
            return self.getLeafLabel(min(distances,key=distances.get),vector)
        else:
            #print rootLabel,'hdj'
            return rootLabel

    def vectorizer(self,image):
        imageDescriptor = {}
        for i in self.vocabTree.leafLabels:
            imageDescriptor[i]=0
        for featureVector in self.siftDescriptor.imageFeat[image]:
            leaf=self.getLeafLabel(0,featureVector)
            imageDescriptor[leaf]+=1.0*self.descriptorWeights[leaf]
        return imageDescriptor.values()

    def vectorizeAll(self):
        for image in self.siftDescriptor.imgfiles:
            self.imageDescriptors[image]=self.vectorizer(image)

    def extract_4_Matches(self,image):
        distances = {}
        imageVector = np.array(self.imageDescriptors[image])
        imageVector = imageVector/float(np.linalg.norm(imageVector,ord=1))
        for i in self.siftDescriptor.imgfiles:
            otherVector  = np.array(self.imageDescriptors[i])
            otherVector  = otherVector/float(np.linalg.norm(otherVector,ord=1))
            distances[i] = float(np.linalg.norm(imageVector-otherVector,ord=1))
        first=min(distances,key=distances.get)
        del distances[first]
        second=min(distances,key=distances.get)
        del distances[second]
        third=min(distances,key=distances.get)
        del distances[third]
        fourth=min(distances,key=distances.get)
        return [first,second,third,fourth]

print "lolfgchjbk"
