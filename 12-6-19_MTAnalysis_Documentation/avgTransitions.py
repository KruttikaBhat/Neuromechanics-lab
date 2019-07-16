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
    transDT=defaultdict(list)
    start=per
    end=per+1

    for i in proc_data[start:end]:
        for j in i.blocks:
            for k in j.words:
                let=k.letters
                for m,n in zip(let[0:-1],let[1:]):
                    transMT[m+n].append([k.mt[let.index(m)],k.day])
                    transDT[m+n].append([k.dt[let.index(m)],k.day])

    avgMT={}
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
    allAvgMT.append(avgMT)
#plotting mean and stdev of top 4 and bottom 4 for each subject

for i in range(8):
    top=[]
    middle=[]
    bottom=[]
    for j in range(15):

        new=[]
        for k in rank2[:4]:
            mx=max(np.array(allAvgMT[i][k[0]])[:,0])
            if(len(allAvgMT[i][k[0]])>j):
                new.append(allAvgMT[i][k[0]][j][0]/allAvgMT[i][k[0]][0][0])
        if(len(new)):
            top.append(new)


        new=[]
        for k in rank2[14:18]:
            if(len(allAvgMT[i][k[0]])>j):
                new.append(allAvgMT[i][k[0]][j][0]/allAvgMT[i][k[0]][0][0])
        if(len(new)):
            middle.append(new)


        new=[]
        for k in rank2[-4:]:
            mx=max(np.array(allAvgMT[i][k[0]])[:,0])
            if(len(allAvgMT[i][k[0]])>j):
                new.append(allAvgMT[i][k[0]][j][0]/allAvgMT[i][k[0]][0][0])
        if(len(new)):
            bottom.append(new)
            #print(new)

    y=[]
    yerr=[]
    for t in top:
        y.append(np.mean(t))
        yerr.append(np.std(t))
    x=np.arange(1,len(y)+1)

    #print(x,y,yerr)
    plt.figure()
    plt.errorbar(x,y,yerr, label="top 4")

    y=[]
    yerr=[]
    for b in bottom:
        y.append(np.mean(b))
        yerr.append(np.std(b))
    x=np.arange(1,len(y)+1)
    #print(x,y,yerr)
    plt.errorbar(x,y,yerr, label="bottom 4")
    plt.legend(prop={'size': 8})
    plt.savefig('correlation_1/ErrorPlots/PerDay/avgTransitionsPerson'+str(i+1))

#plotting avg and stdev across all subjects to4 and bottom4
#averaging across subjects then across transitions

top=[]
middle=[]
bottom=[]
for i in range(15):
    new=[]
    avg=[]
    for j in rank2[:4]:
        for k in range(8):
            mx=max(np.array(allAvgMT[k][j[0]])[:,0])
            if(len(allAvgMT[k][j[0]])>i):
                new.append(allAvgMT[k][j[0]][i][0]/allAvgMT[k][j[0]][0][0])
        if(len(new)):
            avg.append(np.mean(new))
            new=[]
    top.append(avg)



    new=[]
    avg=[]
    for j in rank2[-4:]:
        for k in range(8):
            mx=max(np.array(allAvgMT[k][j[0]])[:,0])
            if(len(allAvgMT[k][j[0]])>i):
                new.append(allAvgMT[k][j[0]][i][0]/allAvgMT[k][j[0]][0][0])
        if(len(new)):
            avg.append(np.mean(new))
            new=[]
    bottom.append(avg)


y=[]
yerr=[]
for t in top:
    y.append(np.mean(t))
    yerr.append(np.std(t))
x=np.arange(1,len(y)+1)
#print(top,x,y,yerr)
y=y/y[0]
plt.figure()
plt.errorbar(x,y,yerr, label="top 4") #for the error bars


y=[]
yerr=[]
for b in bottom:
    y.append(np.mean(b))
    yerr.append(np.std(b))
x=np.arange(1,len(y)+1)
print(x,y,yerr)
y=y/y[0]
plt.errorbar(x,y,yerr, label="bottom 4") #for the error bars

plt.legend(prop={'size': 8})

#plt.savefig("correlation/avgTransitionsAllSubjects") #for only the errorbars
plt.savefig("correlation_1/ErrorPlots/PerDay/avgTransitionsAllSubjects0") #for the exponential fit
#plt.show()
