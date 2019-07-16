import pickle
from classes import *
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats.stats import pearsonr

with open("allObjects.pkl", "rb") as fp:
    proc_data = pickle.load(fp)


letters=['A','E','H','I','N','O','R','S','T']

for per in range(8):

    #first generate a dictionary of all possible transitions
    combi={}
    for i in range(len(letters)):
        for j in range(len(letters)):
            combi[letters[i]+letters[j]]=0

    dates_dict = defaultdict(list)
    transMT=defaultdict(list)
    transDT=defaultdict(list)
    start=per
    end=per+1

    for i in proc_data[start:end]:
        for j in i.blocks:
            for k in j.words:
                let=k.letters
                for m,n in zip(let[0:-1],let[1:]):
                    combi[m+n]=combi[m+n]+1
                    transMT[m+n].append([k.mt[let.index(m)],k.day])
                    transDT[m+n].append([k.dt[let.index(m)],k.day])
    avgMT={}
    baseMT={}
    for i in transMT:
        day=transMT[i][0][1]
        count=0
        sum=0
        avg=[]

        for j in transMT[i]:
            if(j[1]==day):
                sum=sum+j[0]
                count=count+1
                if(transMT[i].index(j)==len(transMT[i])-1):
                        avg.append([sum/count,day])
            else:
                avg.append([sum/count,day])

                day=j[1]
                sum=j[0]
                count=1
        #print(avg)
        avgMT[i]=avg

    for i in avgMT:
        baseline=avgMT[i][0][0]
        base=[]
        for j in avgMT[i]:
            base.append([j[0]/baseline,j[1]])
        baseMT[i]=base
    transFre={}
    rank=[]
    avgTransMT={}
    avgTransDT={}
    for i in transMT:
        avgTransMT[i]=np.mean(np.array(transMT[i])[:,0])
    for i in transDT:
        avgTransDT[i]=np.mean(np.array(transDT[i])[:,0])

    for i in sorted(combi.items(), key=lambda x: x[1], reverse=True):
        if(i[1]!=0):
            transFre[i[0]]=i[1]
            rank.append([i,avgTransMT[i[0]],avgTransDT[i[0]]])

    #plotting the mt lines across days
    plt.figure()
    plt.subplot(221)
    for i in rank[:4]:
        arr=np.array(avgMT[i[0][0]])[:,0].tolist()
        plt.plot(np.arange(len(arr)),arr,label=i[0][0])
    plt.legend(prop={'size': 8})
    plt.title('top 4 avg mt')

    plt.subplot(222)
    for i in rank[:4]:
        arr=np.array(baseMT[i[0][0]])[:,0].tolist()
        plt.plot(np.arange(len(arr)),arr,label=i[0][0])
    plt.legend(prop={'size': 8})
    plt.title('top 4 avg mt from first day')

    plt.subplot(223)
    for i in rank[-4:]:
        arr=np.array(avgMT[i[0][0]])[:,0].tolist()
        plt.plot(np.arange(len(arr)),arr,label=i[0][0])
    plt.legend(prop={'size': 8})
    plt.title('least 4 avg mt')

    plt.subplot(224)
    for i in rank[-4:]:
        arr=np.array(baseMT[i[0][0]])[:,0].tolist()
        plt.plot(np.arange(len(arr)),arr,label=i[0][0])
    plt.legend(prop={'size': 8})
    plt.title('least 4 avg mt from first day')

    plt.savefig('MTAcrossDays/Person'+str(per+1))
