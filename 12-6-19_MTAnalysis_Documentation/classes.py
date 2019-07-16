from sklearn.cluster import DBSCAN
import numpy as np

class Name():
    def __init__(self,name):
        self.name=name
        self.blocks=[]
        self.dict=[]
        self.totalWords=0
        for i in range(15):
            for j in range(12):
                self.blocks.append(Block(i,j,name))

"""
class Day():
    def __init__(self,day):
        self.day=day+1
        for i in range(12):
            self.days.append(Block(i))
"""


class Block():
    def __init__(self,day,block,name):
        self.words=[]
        self.data=[]
        f=open("/home/dell/Documents/Neuromechanics lab/code/Timing_data/"+name+"/Day"+str(day+1)+"/Processed_data/data_block_"+str(block+1)+".txt")
        setOfTimings=[line.strip() for line in f]
        f.close()
        for i in setOfTimings:
            [key,dateTime,cTime]=i.split()
            self.data.append(Data(key,cTime))
        #print(setOfTimings)
        #print(len(setOfTimings))



class Data():
    def __init__(self, key,time):
        self.key = key
        self.ctime=time

class Word():
    def __init__(self,letters,day,block,keytimes,lcontroltimes):
        self.day=day
        self.block=block
        self.letters=letters
        self.ct=[float(x)-float(keytimes[0]) for x in keytimes]
        self.lcontroltimes=[float(x)-float(keytimes[0]) for x in lcontroltimes]
        self.mt=np.array(self.ct[1:])-np.array(self.lcontroltimes[:-1])
        self.dt= np.array(self.lcontroltimes)-np.array(self.ct)

    """
        self.chunks=self.getChunks()

    def getChunks(self):
        data=np.reshape(self.times, (len(self.times), 1))
        dbsc = DBSCAN(eps = 1, min_samples = 1).fit(data)
        labels = dbsc.labels_
        core_samples = np.zeros_like(labels, dtype = bool)
        core_samples[dbsc.core_sample_indices_] = True
        print(labels,core_samples)
    """

class wordStats():
    def __init__(self,mts,days,blocks,mean,stdev,word):
        self.mts=mts
        self.days=days
        self.blocks=blocks
        self.mean=mean
        self.stdev=stdev
        self.word=word
