import pickle
from classes import *
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import scipy
from scipy.optimize import curve_fit

def func(x, a, b):
    return a * np.exp(b * x)



with open("allObjects.pkl", "rb") as fp:
    proc_data = pickle.load(fp)


letters=['A','E','H','I','N','O','R','S','T']


with open("allWords.pkl","rb") as fp:
    words=pickle.load(fp)

combi2={}
for i in range(len(letters)):
    for j in range(len(letters)):
        combi2[letters[i]+letters[j]]=0

for i in words:
    for m,n in zip(i[0:-1],i[1:]):
        combi2[m+n]=combi2[m+n]+1

rank2=[]
for i in sorted(combi2.items(), key=lambda x: x[1], reverse=True):
    if(i[1]!=0):
        rank2.append(i)


allAvgMT=[]
for per in range(8):

    transMT=defaultdict(list)
    #transDT=defaultdict(list)
    start=per
    end=per+1

    for i in proc_data[start:end]:
        for j in i.blocks:
            for k in j.words:
                let=k.letters
                for m,n in zip(let[0:-1],let[1:]):
                    transMT[m+n].append([k.mt[let.index(m)],k.block,k.day])
                    #transDT[m+n].append([k.dt[let.index(m)],k.block])
    avgMT={}
    for i in transMT:
        #print(transMT[i])
        day=transMT[i][0][2]
        block=((day-1)*12)+transMT[i][0][1]
        preblock=transMT[i][0][1]
        count=0
        sum=0
        avg=[]

        for j in transMT[i]:
            if(((j[2]-1)*12)+j[1]==block):
                sum=sum+j[0]
                count=count+1
                preblock=j[1]
                if(transMT[i].index(j)==len(transMT[i])-1):
                        avg.append([sum/count,((day-1)*12)+preblock])
            else:
                avg.append([sum/count,((day-1)*12)+preblock])
                day=j[2]
                block=((day-1)*12)+j[1]
                sum=j[0]
                count=1
                preblock=j[1]
        avgMT[i]=avg


    allAvgMT.append(avgMT)



#average across blocks for top 4 and bottom 4 for each subject

for i in range(8):
    top=[]
    bottom=[]
    temp=1
    while(temp!=181):
        new=[]
        for j in rank2[:4]:
            mx=max(np.array(allAvgMT[i][j[0]])[:,0])
            for k in allAvgMT[i][j[0]]:
                if(k[1]==temp):
                    new.append(k[0]/allAvgMT[i][j[0]][0][0])
                    break
        if(len(new)):
            top.append([new,temp])

        new=[]
        for j in rank2[-4:]:
            mx=max(np.array(allAvgMT[i][j[0]])[:,0])
            for k in allAvgMT[i][j[0]]:
                if(k[1]==temp):
                    new.append(k[0]/allAvgMT[i][j[0]][0][0])
                    break
        if(len(new)):
            bottom.append([new,temp])

        temp=temp+1

    #print(top)
    x=[]
    y=[]
    yerr=[]
    for t in top:
        y.append(np.mean(t[0]))
        yerr.append(np.std(t[0]))
        x.append(t[1])

    #print(x,y,yerr)
    x=np.array(x)
    y=np.array(y)


    plt.figure()
    plt.errorbar(x,y,yerr, label="top 4")

    x=[]
    y=[]
    yerr=[]
    for b in bottom:
        y.append(np.mean(b[0]))
        yerr.append(np.std(b[0]))
        x.append(b[1])
    x=np.array(x)
    y=np.array(y)
    plt.errorbar(x,y,yerr, label="bottom 4")
    plt.legend(prop={'size': 8})
    #plt.show()
    plt.savefig('correlation_1/ErrorPlots/PerBlock/avgTransitionsPerBlockPerson'+str(i))




#average across blocks for top 4 and bottom 4 across subjects, averaged across subjects then across transitions

top=[]
middle=[]
bottom=[]

temp=1
while(temp!=181):
    avg=[]
    for i in rank2[:4]:
        new=[]
        for j in range(8):
            mx=max(np.array(allAvgMT[j][i[0]])[:,0])
            for k in allAvgMT[j][i[0]]:
                if(k[1]==temp):
                    new.append(k[0]/allAvgMT[j][i[0]][0][0])
                    break
        if(len(new)):
#            print('new:',new)
            avg.append(np.mean(new))
#            print('avg1',avg)
    if(len(avg)):
        top.append([avg,temp])
#        print('avg',avg)


    avg=[]
    for i in rank2[-4:]:
        new=[]
        for j in range(8):
            mx=max(np.array(allAvgMT[j][i[0]])[:,0])
            for k in allAvgMT[j][i[0]]:
                if(k[1]==temp):
                    new.append(k[0]/allAvgMT[j][i[0]][0][0])
                    break
        if(len(new)):
#            print('new:',new)
            avg.append(np.mean(new))
#            print('avg1',avg)
    if(len(avg)):
        bottom.append([avg,temp])
#        print('avg',avg)

    temp=temp+1
x=[]
y=[]
yerr=[]
for t in top:
    y.append(np.mean(t[0]))
    yerr.append(np.std(t[0]))
    x.append(t[1])
#print(x,y,yerr)

x=np.array(x)
y=np.array(y)

plt.figure()
plt.errorbar(x,y,yerr, label="top 4")

x=[]
y=[]
yerr=[]
for b in bottom:
    y.append(np.mean(b[0]))
    yerr.append(np.std(b[0]))
    x.append(b[1])

#print(x,y,yerr)
x=np.array(x)
y=np.array(y)
plt.errorbar(x,y,yerr, label="bottom 4")

plt.savefig('correlation_1/ErrorPlots/PerBlock/avgTransitionsAllSubjectsPerBlock')
#plt.show()
