from tree import *

class result:
    def __init__(self):
        self.siftDescriptor = SIFT()
        self.vocabTree = VocabTree(self.siftDescriptor,10,1000)
        self.imageDescriptors={}

    def getLeafLabel(self,rootLabel,vector):
        try:
            l=len(adjancency[rootLabel])
            distances={}
            for i in self.vocabTree.adjancency[rootLabel]:
                distances[i]=np.linalg.norm(np.array(vector)-np.array(self.vocabTree.treeMap[i]))
            self.getLeafLabel(min(distances),vector)
        except:
            return rootLabel

    def vectorizer(self,image):
        imageDescriptor = {}
        for i in self.vocabTree.leafLabels:
            imageDescriptor[i]=0
        for featureVector in self.siftDescriptor.imageFeat[image][1]:
            imageDescriptor[self.getLeafLabel('0',featureVector)]+=1
        return imageDescriptor.values()

    def vectorizeAll(self):
        for image in self.siftDescriptor.imgfiles:
            self.imageDescriptors[image]=self.vectorizer(image)

    def extract_4_Matches(self,image):
        distances = {}
        imageVector = np.array(self.imageDescriptors[image])
        imageVector = imageVector/np.linalg.norm(imageVector,ord=1)
        for i in self.siftDescriptor.imgfiles:
            otherVector  = np.array(self.imageDescriptors[i])
            otherVector  = otherVector/np.linalg.norm(otherVector,ord=1)
            distances[i] = np.linalg.norm(imageVector-otherVector,ord=1)
        first=min(distances)
        del distances[first]
        second=min(distances)
        del distances[second]
        third=min(distances)
        del distances[third]
        fourth=min(distances)
        return [first,second,third,fourth]
