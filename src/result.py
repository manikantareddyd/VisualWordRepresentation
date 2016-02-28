from tree import *
import math
import re
class result:
    def __init__(self,branches,depth):
        self.siftDescriptor = SIFT()
        self.branches=branches
        self.depth=depth
        l=len(self.siftDescriptor.FeatureVectors)
        self.threshold = int(branches**(int(math.log(l,branches))+1)/branches**(depth-1))
        print "Number of Branches:",self.branches
        print "Depth:",self.depth
        print "Threshold:",self.threshold
        self.vocabTree = VocabTree(self.siftDescriptor,self.branches,self.threshold)
        self.imageDescriptors={}
        self.imageFrequency  ={}
        print 'Hi'
        self.descriptorWeights={}
        for i in self.vocabTree.leafLabels:
            self.descriptorWeights[i]=math.log1p(len(self.siftDescriptor.imgfiles)/float(len(self.vocabTree.nodeImages[i])))
        self.allMatches={}
        self.getAllMatches()
        self.allScores={}
        self.getAllScores()
        self.finalResult=self.getFinalScore()



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
        imageFrequency  = {}
        for i in self.vocabTree.leafLabels:
            imageDescriptor[i]=0
            imageFrequency[i]=0
        for featureVector in self.siftDescriptor.imageFeat[image]:
            leaf=self.getLeafLabel(0,featureVector)
            imageDescriptor[leaf]+=1.0*self.descriptorWeights[leaf]
            imageFrequency[leaf]+=1
        self.imageFrequency[image]=imageFrequency
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
            distances[int(re.findall(r'\d+',i)[0])] = float(np.linalg.norm(imageVector-otherVector,ord=1))
        #
        # first=min(distances,key=distances.get)
        # del distances[first]
        # second=min(distances,key=distances.get)
        # del distances[second]
        # third=min(distances,key=distances.get)
        # del distances[third]
        # fourth=min(distances,key=distances.get)
        # print "OOO"
        l=sorted(distances,key=distances.get)[:4]
        # print 'p'
        # print l,'k'
        return l

    def getAllMatches(self):
        self.vectorizeAll()
        for i in self.siftDescriptor.imgfiles:
            self.allMatches[int(re.findall(r'\d+',i)[0])]=self.extract_4_Matches(i)

    def getScore(self,image):
        imageNum = int(re.findall(r'\d+',image)[0])
        matches = self.allMatches[imageNum]
        t=(imageNum/4)*4
        trueMatches = [t,t+1,t+2,t+3]
        score=0
        result=[0,0,0,0]
        for i in range(0,4):
            if matches[i] in trueMatches:
                score+=1
                result[i]+=1
        return score,np.array(result)

    def getAllScores(self):
        for i in self.siftDescriptor.imgfiles:
            self.allScores[i]=self.getScore(i)

    def getFinalScore(self):
        s=np.array([0,0,0,0])
        su=0
        l=len(self.allScores)
        for i in self.allScores:
            su+=self.allScores[i][0]
            s+=self.allScores[i][1]
        return su/(4.0*l),np.ndarray.tolist(s/(1.0*l))
print "lolfgchjbk"
