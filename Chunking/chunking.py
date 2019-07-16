import numpy as np
import pickle
from classes import *
import matplotlib.pyplot as plt
import xlsxwriter

with open("Mean_StdDev/EachWordAllDays.pkl", "rb") as fp:
    uniqueWordsmt=pickle.load(fp)
"""
def generate(x,chunks):
    clusters=[]
    if(chunks==2):
        clusters.append([[x[0],x[1]],[x[2],x[3],x[4]]])
        clusters.append([[x[0],x[1],x[2]],[x[3],x[4]]])
        clusters.append([[x[0]],[x[1],x[2],x[3],x[4]]])
        clusters.append([[x[0],x[1],x[2],x[3]],[x[4]]])

    if(chunks==3):
        clusters.append([[x[0],x[1],x[2]],[x[3]],[x[4]]])
        clusters.append([[x[0]],[x[1],x[2],x[3]],[x[4]]])
        clusters.append([[x[0]],[x[1]],[x[2],x[3],x[4]]])
        clusters.append([[x[0],x[1]],[x[2],x[3]],[x[4]]])
        clusters.append([[x[0],x[1]],[x[2]],[x[3],x[4]]])
        clusters.append([[x[0]],[x[1],x[2]],[x[3],x[4]]])

    if(chunks==4):
        clusters.append([[x[0],x[1]],[x[2]],[x[3]],[x[4]]])
        clusters.append([[x[0]],[x[1],x[2]],[x[3]],[x[4]]])
        clusters.append([[x[0]],[x[1]],[x[2],x[3]],[x[4]]])
        clusters.append([[x[0]],[x[1]],[x[2]],[x[3],x[4]]])

    return clusters


global sdam


def getCluster(x,p,data,mt):
    filter1=[]
    innersum=[]
    outersum=[]
    sdam=0
    for chunks in range(2,5):
        clusters=generate(x,chunks)
        for i in range(len(clusters)):
            outer=[]
            inner=[]
            for j in range(len(clusters[i])):
                if(j!=len(clusters[i])-1):
                    outer.append(clusters[i][j+1][0]-clusters[i][j][-1])
                #print(len(clusters[i][j]))
                if(len(clusters[i][j])!=1):
                    for k in range(len(clusters[i][j])-1):
                        inner.append(clusters[i][j][k+1]-clusters[i][j][k])
            count=0
            print(clusters[i],inner,outer)
            for m in inner:
                for n in outer:
                    print(m,n)
                    if (m<n):
                        count=count+1
            print(count,len(inner)*len(outer)/2)
            if count<=len(inner)*len(outer) and count>=len(inner)*len(outer)/2:
                filter1.append(clusters[i])
                innersum.append(sum(inner))
                outersum.append(sum(outer))
    print('1:',filter1,innersum,outersum)
    filter2=[]
    for i in range(len(filter1)):
        if(innersum[i]/outersum[i]<1):
            print(innersum[i]/outersum[i],filter1[i])
            cluster=filter1[i]
            filter2.append(cluster)
    print('2:',filter2)

    s=[0]*len(filter2)
    ratio=[]


    if p==0:
        for i in range(len(filter2)):
            for j in range(len(filter2[i])):
                m=np.mean(np.array(filter2[i][j]))
                for k in filter2[i][j]:
                    s[i]=s[i]+(k-m)**2

    else:
        mvDiff=(data-np.mean(mt[:p],axis=0))**2
        print(mvDiff)
        for i in range(len(filter2)):
            index=0
            outer=0
            num=len(filter2[i])
            for j in range(num):
                size=len(filter2[i][j])
                index=index+size
                print(index)
                if(index<5):
                    outer=outer+mvDiff[index-1]
            inner=sum(mvDiff)-outer

            print(filter2[i],inner,outer)
            ratio.append(inner/outer)
    if p==0:
        print(s)
        index=s.index(min(s))
    else:
        print(ratio)
        index=ratio.index(min(ratio))
    return filter2[index]






def getCluster(x,p,data):
    fin=[]
    gvf=[]
    check=[]
    global sdam
    if(p==0):
        sdam=0
        mean=np.mean(x)
        for l in x:
            sdam=sdam+(l-mean)**2
    else:
        mvDiff=(data-np.mean(mt[:p],axis=0))**2
        #print(mvDiff)
    for chunks in range(2,5):
        clusters=generate(x,chunks)
        if p==0:
            s=[0]*len(clusters)
            for i in range(len(clusters)):
                for j in range(len(clusters[i])):
                    m=np.mean(np.array(clusters[i][j]))
                    for k in clusters[i][j]:
                        s[i]=s[i]+(k-m)**2
            gvf.append((sdam-min(s))/sdam)
            fin.append(clusters[s.index(min(s))])
        if(p!=0):
            outer=[0]*len(clusters)
            inner=[0]*len(clusters)
            for i in range(len(clusters)):
                index=0
                num=len(clusters)
                for j in range(len(clusters[i])):
                    size=len(clusters[i][j])
                    index=index+size
                    if(index<5):
                        outer[i]=outer[i]+mvDiff[index-1]
                inner[i]=sum(mvDiff)-outer[i]
                outer[i]=outer[i]/(num-1)
                inner[i]=inner[i]/num
            ratio=(np.array(inner)/np.array(outer)).tolist()
            check.append(min(ratio))
            fin.append(clusters[ratio.index(min(ratio))])
    if(p==0):
        index=gvf.index(max(gvf))
    else:
        ratio=(np.array(gvf)/np.array(check)).tolist()
        index=ratio.index(max(ratio))
    print(np.array(fin).size)
    cluster=fin[index]
    return cluster
"""
def getX(mt,p):
    x=[]
    data=mt[p]
    su=0
    x.append(su)
    for i in range(len(data)):
        su=su+data[i]
        x.append(su)
    x=np.array(x)
    return(x,data)


def getCluster(x,data):
    clusters=[]
    newcluster=[]
    newcluster.append(x[0])
    mean=np.mean(data)
    for i in range(len(data)):
        if(data[i]<mean):
            newcluster.append(x[i+1])
        else:
            clusters.append(newcluster)
            newcluster=[]
            newcluster.append(x[i+1])
    clusters.append(newcluster)
    return clusters

def checksim(data):
    #mean=np.mean(data)
    #print(data)
    count=0
    data=data/sum(data)
    print(data)
    mean=np.mean(data)
    dd=np.sqrt((data-mean)**2)
    print(dd)
    for i in dd:
        if(i<0.1):
            count=count+1
    #print(sum(dd)*100)
    if(count==4):
        return True
    else:
        return False



def getChunks(mt):
    clst=[]
    cum=[]
    maxmean=0
    mtmean=np.mean(mt,axis=0)
    for p in range(len(mt)):
        (x,data)=getX(mt,p)
        #cum.append(x[1:])
        cum.append(data)

        #print(x,cum)
        #sum of squared deviations for array mean
        """
        if(p==0):
            sdam=0
            mean=np.mean(x)
            for l in x:
                sdam=sdam+(l-mean)**2
        else:
            mvDiff=(data-np.mean(mt[:p],axis=0))**2
        fin=[]
        gvf=[]
        check=[]
        """
        #m=np.mean(np.array(data))
        #if(m>maxmean):
        #    maxmean=m
        #diff=sum(np.array(data-m)**2)
        #print(diff)
        count=0
        for i,j in zip(data,mtmean):
            if(i<j):
                count=count+1
        if(count==4 and checksim(data)):
            print(p)
            cluster=[[x[0],x[1],x[2],x[3],x[4]]]
        elif(count==0 and checksim(data)):
            cluster=[[x[0]],[x[1]],[x[2]],[x[3]],[x[4]]]
        else:
            cluster=getCluster(x,data)

        """
        if(diff<0.005):
            #val=np.mean(np.array(x[1:])/np.mean(cum,axis=0))
            #print("v:",val)
            #print(val)
            if(m<maxmean):
                cluster=[[x[0],x[1],x[2],x[3],x[4]]]
            else:
                cluster=[[x[0]],[x[1]],[x[2]],[x[3]],[x[4]]]
        else:
            cluster=getCluster(x,data)
        """
        new=[]
        for k in cluster:
            new.append(len(k))
        clst.append(new)
    print(clst)
    return(clst)



workbook = xlsxwriter.Workbook('Chunks.xlsx')
worksheet=workbook.add_worksheet()
row = 0
col = 0
Labels=['Word','Person 1','Person 2','Person 3','Person 4','Person 5','Person 6','Person 7','Person 8']
worksheet.write_row(row,col,Labels)
row=row+1
maxLen=0
initial=0
for w in range(281):
    row=initial+maxLen+2
    worksheet.write(row,col,uniqueWordsmt[0][w].word)
    maxLen=0
    initial=row
    for p in uniqueWordsmt:
        mt=p[w].mts
        row=initial
        clst=getChunks(mt)
        if len(mt)>maxLen:
            maxLen=len(mt)
        for j in range(len(mt)):
#            print("-".join(str(i) for i in clst[j]))
            worksheet.write(row,col+uniqueWordsmt.index(p)+1,"-".join(str(i) for i in clst[j]))
            row=row+1
workbook.close()
"""
        size=[]
        for i in clst:
            size.append(len(i))
        plt.plot(np.arange(len(size)),size)
        plt.show()
"""
"""
        cum=[]
        for i in mt:
            present=[]
            sum=0
            present.append(sum)
            for j in i:
                sum=sum+j
                present.append(sum)
            cum.append(present)

        #print(cum)
        c=np.array(cum)
        plt.title(p[w].word)
        #plt.subplot(2,5,index)
        #index=index+1
        plt.title("Person "+str(uniqueWordsmt.index(p)))
        plt.plot(np.arange(len(cum)),c[:,0],marker='*')
        plt.plot(np.arange(len(cum)),c[:,1],marker='*')
        plt.plot(np.arange(len(cum)),c[:,2],marker='*')
        plt.plot(np.arange(len(cum)),c[:,3],marker='*')
        plt.plot(np.arange(len(cum)),c[:,4],marker='*')
        plt.grid()
        #plt.xlim(-5,len(cum))
        #plt.ylim(-1,4)
        #for i in range(len(clst)):
        #    plt.text(i-5,-0.2,clst[i],rotation=45)


    plt.show()
"""
