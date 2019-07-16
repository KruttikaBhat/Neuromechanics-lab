import pickle
from classes import *
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import scipy
from scipy.optimize import curve_fit



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
allTransMT=[]
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
                    transMT[m+n].append([k.mt[let.index(m)],k.day,k.block])
                    transDT[m+n].append([k.dt[let.index(m)],k.day,k.block])

    allTransMT.append(transMT)

#all subjects,all mt

day=1
block=1
index=[]
for i in range(8):
    index.append([0]*4)
count=0
temp=1
br=0
y=[]
x=[]
yerr=[]
while(temp!=181):
    new=[]
    for i in rank2[:4]:
        for p in range(8):
            if(len(allTransMT[p][i[0]])>index[p][rank2.index(i)]):
                j=index[p][rank2.index(i)]
                print(i,allTransMT[p][i[0]][j],day,block)
                if(allTransMT[p][i[0]][j][1]==day and allTransMT[p][i[0]][j][2]==block):
                    new.append(allTransMT[p][i[0]][j][0])
                    index[p][rank2.index(i)]+=1


    if(len(new)):
        y.append(np.mean(new))
        yerr.append(np.std(new))
        count=count+1
        print(y,count)
    else:

        if(count!=0):
            for k in range(count):
                x.append(temp+(k/count))
            print(x)
        temp=temp+1
        if(temp%12==0):
            block=12
            day=int(temp/12)
        else:
            day=int(temp/12)+1
            block=temp%12
        count=0
        print(temp)


y=y/y[0]
x=np.array(x)
y=np.array(y)
plt.figure()
plt.errorbar(x,y,yerr,label='top 4',color='b')

day=1
block=1
index=[]
for i in range(8):
    index.append([0]*4)
count=0
temp=1
br=0
y=[]
x=[]
yerr=[]
while(temp!=181):
    new=[]
    for i in rank2[-4:]:
        for p in range(8):
            if(len(allTransMT[p][i[0]])>index[p][68-rank2.index(i)]):
                j=index[p][68-rank2.index(i)]
                print(i,allTransMT[p][i[0]][j],day,block)
                if(allTransMT[p][i[0]][j][1]==day and allTransMT[p][i[0]][j][2]==block):
                    new.append(allTransMT[p][i[0]][j][0])
                    index[p][68-rank2.index(i)]+=1


    if(len(new)):
        y.append(np.mean(new))
        yerr.append(np.std(new))
        count=count+1
        print(y,count)
    else:

        if(count!=0):
            for k in range(count):
                x.append(temp+(k/count))
            print(x)
        temp=temp+1
        if(temp%12==0):
            block=12
            day=int(temp/12)
        else:
            day=int(temp/12)+1
            block=temp%12
        count=0
        print(temp)


y=y/y[0]
x=np.array(x)
y=np.array(y)
plt.errorbar(x,y,yerr,label='bottom 4',color='g')

plt.legend()

plt.savefig('correlation_2/Exp/ErrorPlots/AllMT/AllSubjectsAvg')



#each subject, all mt

for p in range(8):
    day=1
    block=1
    index=[0,0,0,0]
    count=0
    temp=1
    br=0
    y=[]
    x=[]
    yerr=[]
    while(temp!=181):
        new=[]
        for i in rank2[:4]:
            if(len(allTransMT[p][i[0]])>index[rank2.index(i)]):
                j=index[rank2.index(i)]
                print(i,allTransMT[p][i[0]][j],day,block)
                if(allTransMT[p][i[0]][j][1]==day and allTransMT[p][i[0]][j][2]==block):
                    new.append(allTransMT[p][i[0]][j][0])
                    index[rank2.index(i)]+=1


        if(len(new)):
            y.append(np.mean(new))
            yerr.append(np.std(new))
            count=count+1
            print(y,count)
        else:

            if(count!=0):
                for k in range(count):
                    x.append(temp+(k/count))
                print(x)
            temp=temp+1
            if(temp%12==0):
                block=12
                day=int(temp/12)
            else:
                day=int(temp/12)+1
                block=temp%12
            count=0
            print(temp)


    y=y/y[0]
    x=np.array(x)
    y=np.array(y)
    plt.figure()
    plt.errorbar(x,y,yerr,label='top 4',color='b')

    day=1
    block=1
    index=[0,0,0,0]
    count=0
    temp=1
    br=0
    y=[]
    x=[]
    yerr=[]
    while(temp!=181):
        new=[]
        for i in rank2[-4:]:
            if(len(allTransMT[p][i[0]])>index[68-rank2.index(i)]):
                j=index[68-rank2.index(i)]
                print(i,allTransMT[p][i[0]][j],day,block)
                if(allTransMT[p][i[0]][j][1]==day and allTransMT[p][i[0]][j][2]==block):
                    new.append(allTransMT[p][i[0]][j][0])
                    index[68-rank2.index(i)]+=1


        if(len(new)):
            y.append(np.mean(new))
            yerr.append(np.std(new))
            count=count+1
            print(y,count)
        else:

            if(count!=0):
                for k in range(count):
                    x.append(temp+(k/count))
                print(x)
            temp=temp+1
            if(temp%12==0):
                block=12
                day=int(temp/12)
            else:
                day=int(temp/12)+1
                block=temp%12
            count=0
            print(temp)


    y=y/y[0]
    x=np.array(x)
    y=np.array(y)
    plt.errorbar(x,y,yerr,label='bottom 4',color='g')
    plt.legend()
    plt.savefig('correlation_2/Exp/ErrorPlots/AllMT/Person'+str(p+1))
    plt.close()



#all subjects, blocks

top=[]
bottom=[]
for d in range(1,181):
    new=[]
    for j in rank2[:4]:
        for k in range(8):
            for i in allTransMT[k][j[0]]:
                block=((i[1]-1)*12)+i[2]
                if(block==d):
                    new.append(i[0])
    #print(len(new))
    top.append([new,d])
    new=[]
    for j in rank2[-4:]:
        for k in range(8):
            allTransMT[k][j[0]]
            for i in allTransMT[k][j[0]]:
                block=((i[1]-1)*12)+i[2]
                #print(block,d)
                if(block==d):
                    new.append(i[0])
    #print(len(new))
    if(len(new)):
        bottom.append([new,d])

#print(np.array(top).shape)
top=np.array(top)
y=[]
x=[]
yerr=[]
for i in top:
    #print(i)
    y.append(np.mean(i[0]))
    yerr.append(np.std(i[0]))
    x.append(i[1])

y=y/y[0]
x=np.array(x)
y=np.array(y)
plt.figure()
plt.errorbar(x,y,yerr,label='top 4',color='b')

y=[]
yerr=[]
x=[]
for i in bottom:
    y.append(np.mean(i[0]))
    yerr.append(np.std(i[0]))
    x.append(i[1])
x=np.array(x)
y=np.array(y)

plt.errorbar(x,y,yerr,label='bottom 4',color='g')
plt.legend()
plt.savefig('correlation_2/Exp/ErrorPlots/PerBlock/AllSubjectsAvg')
plt.close()
#plt.show()



#each subject, blocks

for p in range(8):
    top=[]
    bottom=[]
    for d in range(1,181):
        new=[]
        for j in rank2[:4]:
            for i in allTransMT[p][j[0]]:
                block=((i[1]-1)*12)+i[2]
                if(block==d):
                    new.append(i[0])
        if(len(new)):
            top.append([new,d])
        new=[]
        for j in rank2[-4:]:
            for i in allTransMT[p][j[0]]:
                block=((i[1]-1)*12)+i[2]
                if(block==d):
                    new.append(i[0])

        if(len(new)):
            bottom.append([new,d])
    y=[]
    x=[]
    yerr=[]
    for i in top:
        y.append(np.mean(i[0]))
        x.append(i[1])
        yerr.append(np.std(i[0]))
    y=y/y[0]
    x=np.array(x)
    y=np.array(y)
    #print(x,y)
    plt.figure()
    plt.errorbar(x,y,yerr,label='top 4',color='b')

    y=[]
    x=[]
    yerr=[]
    for i in bottom:
        y.append(np.mean(i[0]))
        yerr.append(np.std(i[0]))
        x.append(i[1])
    y=y/y[0]
    x=np.array(x)
    y=np.array(y)
    plt.errorbar(x,y,yerr,label='bottom 4',color='g')

    plt.legend()
    plt.savefig('correlation_2/Exp/ErrorPlots/PerBlock/Person'+str(p+1))
    #plt.show()




#all subjects, Days

top=[]
bottom=[]
for d in range(1,16):
    new=[]
    for j in rank2[:4]:
        for k in range(8):
            for i in allTransMT[k][j[0]]:
                if(i[1]==d):
                    new.append(i[0])
    #print(len(new))
    top.append(new)
    new=[]
    for j in rank2[-4:]:
        for k in range(8):
            for i in allTransMT[k][j[0]]:
                if(i[1]==d):
                    new.append(i[0])
    #print(len(new))
    bottom.append(new)


y=[]
yerr=[]
for i in top:
    y.append(np.mean(i))
    yerr.append(np.std(i))

y=y/y[0]

x=np.arange(1,len(y)+1)
plt.figure()
plt.errorbar(x,y,yerr,label='top 4',color='b')


y=[]
yerr=[]
for i in bottom:
    y.append(np.mean(i))
    yerr.append(np.std(i))

y=y/y[0]

x=np.arange(len(y))
plt.errorbar(x,y,yerr,label='bottom 4',color='g')
plt.savefig('correlation_2/Exp/ErrorPlots/PerDay/AvgAllSubjects')
#plt.show()

#each subject, Days

for p in range(8):
    top=[]
    bottom=[]
    for d in range(1,16):
        new=[]
        for j in rank2[:4]:
            for i in allTransMT[p][j[0]]:
                if(i[1]==d):
                    new.append(i[0])
        top.append([new,d])
        new=[]
        for j in rank2[-4:]:
            for i in allTransMT[p][j[0]]:
                if(i[1]==d):
                    new.append(i[0])
        #print(len(new))
        if(len(new)):
            bottom.append([new,d])

    y=[]
    yerr=[]
    for t in top:
        y.append(np.mean(t[0]))
        yerr.append(np.std(t[0]))
    x=np.arange(1,len(y)+1)
    y=y/y[0]

    #print(x,y,yerr)
    plt.figure()
    plt.errorbar(x,y,yerr,label='top 4',color='b')

    y=[]
    yerr=[]
    for b in bottom:
        y.append(np.mean(b[0]))
        yerr.append(np.std(b[0]))
    y=y/y[0]
    x=np.arange(1,len(y)+1)
    #print(x,y,yerr)
    plt.errorbar(x,y,yerr,label='bottom 4',color='g')

    plt.savefig('correlation_2/Exp/ErrorPlots/PerDay/Person'+str(p+1))
    #plt.show()
