import pickle
from classes import *
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
from sklearn.metrics import r2_score
import math
import scipy
import xlsxwriter
from scipy.optimize import curve_fit

def func1(x, a, b,c):
    return (np.sign(a)*(np.abs(a))**(x)+b)/c

def funclog(x, a):
    return a*np.log(x)


def func(x, a, b):
    return a * (x+b)

def expfunc(x, a, b):
    return a * np.exp(b * x)+c




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


pos={'A':[4,3],'E':[1,1],'I':[3,3],'O':[2,3],'R':[4,1],'N':[2,1],'S':[1,2],'T':[3,1],'H':[4,2]}

#print(pos)

dist={}
for i in letters:
    for j in letters:
        dist[i+j]=math.sqrt((pos[i][0]-pos[j][0])**2 + (pos[i][1]-pos[j][1])**2)


allAvgMT=[]
allTransMT=[]
totalMT=[]
totalBlock=[]
totalDay=[]
rsquareMT=[]
rsquareBlock=[]
rsquareDay=[]
dr=[]
lin=[]
for per in range(8):

    transMT=defaultdict(list)
    start=per
    end=per+1

    combi={}
    for i in range(len(letters)):
        for j in range(len(letters)):
            combi[letters[i]+letters[j]]=0

    for i in proc_data[start:end]:
        for j in i.blocks:
            for k in j.words:
                let=k.letters
                for m,n in zip(let[0:-1],let[1:]):
                    transMT[m+n].append([k.mt[let.index(m)],k.day,k.block])
                    combi[m+n]=combi[m+n]+1
                    #transDT[m+n].append([k.dt[let.index(m)],k.block])

    for i in transMT:
        mx=max(np.array(transMT[i])[:,0])
        for j in transMT[i]:
            j[0]=j[0]/mx
    rank=[]
    for i in sorted(combi.items(), key=lambda x: x[1], reverse=True):
        if(i[1]!=0):
            rank.append(i)

    distRank=[]
    for i in sorted(dist.items(), key=lambda x: x[1], reverse=True):
        if(i[0] in np.array(rank)[:,0]):
            distRank.append([i[0],i[1],combi[i[0]]])
    print(distRank)
    distances=sorted(np.unique(np.array(distRank)[:,1]),reverse=True)
    presDist=distances[0]

    #file=open('EachTransition/Person'+str(per+1)+'/lr','w')
    #file.write('Transition; Rate of decay; Learning rate; Drop\n')
    d=[]
    b=[]
    mt=[]
    #no averaging


    for i in distRank:
        y=np.array(transMT[i[0]])[:,0]
        x=[]
        day=transMT[i[0]][0][1]
        block=transMT[i[0]][0][2]
        temp=((day-1)*12)+block
        count=0
        print(transMT[i[0]])
        for j in range(len(transMT[i[0]])):
            print(day,block)
            if(transMT[i[0]][j][1]==day and transMT[i[0]][j][2]==block):
                count=count+1
                print(j,len(transMT[i[0]])-1)
                if(j==len(transMT[i[0]])-1):
                    for k in range(count):
                        x.append(temp+(k/count))
                    print(x)

            else:
                for k in range(count):
                    x.append(temp+(k/count))
                day=transMT[i[0]][j][1]
                block=transMT[i[0]][j][2]
                temp=((day-1)*12)+block
                count=1
                print(x)
                if(j==len(transMT[i[0]])-1):
                    for k in range(count):
                        x.append(temp+k/count)
                    print(x)

        y=(max(y)-y)/max(y)
        popt,pcov=scipy.optimize.curve_fit(lambda t,a: a*np.log(t),  x,  y)
        #print(popt)
        a=popt[0]
        first=a*np.log(x[0])
        last=a*np.log(x[-1])
        diff=last-first
        if(diff<1):
            mt.append(diff)
        else:
            mt.append(y[-1])


    #blocks


    for i in distRank:
        y=[]
        day=transMT[i[0]][0][1]
        block=transMT[i[0]][0][2]
        temp=(12*(day-1))+block
        sum=0
        count=0
        for j in transMT[i[0]]:
            if(j[1]==day and j[2]==block):
                sum=sum+j[0]
                count=count+1
                if(transMT[i[0]].index(j)==len(transMT[i[0]])-1):
                        y.append([sum/count,temp])
            else:
                y.append([sum/count,temp])
                sum=j[0]
                count=1
                day=j[1]
                block=j[2]
                temp=(12*(day-1))+block

        y=np.array(y)
        x=y[:,1]
        y=y[:,0]
        y=(max(y)-y)/max(y)
        print(len(x),len(y))
        popt,pcov=scipy.optimize.curve_fit(lambda t,a: a*np.log(t),  x,  y)
        #print(popt)
        a=popt[0]
        first=a*np.log(x[0])
        last=a*np.log(x[-1])
        diff=last-first
        if(diff<1):
            b.append(diff)
        else:
            b.append(y[-1])


    #day wise


    for i in distRank:
        y=[]
        day=transMT[i[0]][0][1]
        count=0
        sum=0
        avg=[]
        for j in transMT[i[0]]:
            if(j[1]==day):
                sum=sum+j[0]
                count=count+1
                if(transMT[i[0]].index(j)==len(transMT[i[0]])-1):
                        y.append([sum/count,day])
            else:
                y.append([sum/count,day])
                day=j[1]
                sum=j[0]
                count=1
        y=np.array(y)
        x=y[:,1]
        y=y[:,0]
        y=(max(y)-y)/max(y)
        print(len(x),len(y))

        popt,pcov=scipy.optimize.curve_fit(lambda t,a: a*np.log(t),  x,  y)
        #print(popt)
        a=popt[0]
        first=a*np.log(x[0])
        last=a*np.log(x[-1])
        diff=last-first
        if(diff<1):
            d.append(diff)
        else:
            d.append(y[-1])


    #all mt
    totalMT.append(mt)
    x=np.arange(1,len(mt)+1)
    y=np.array(mt)
    fig=plt.figure()
    fig.suptitle('Improvement as a function of distance; Subject '+str(per+1),fontsize=12)
    plt.scatter(x,y)
    p=np.polyfit(x,y,1)
    print(p)
    f = np.poly1d(p)
    plt.plot(x,f(x), 'b-')
    first=f(x[0])
    last=f(x[-1])
    m=(first-last)/(x[0]-x[-1])
    c=f(0)
    y_actual=y
    y_pred=f(x)
    rsquareMT.append(r2_score(y_actual, y_pred))

    plt.text(10,0.5,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10) #for the exponential fit
    plt.xlabel('Rank')
    plt.ylabel('Improvement')
    plt.savefig('Distance/AllMT/'+str(per+1))
    plt.close()

    #blocks
    totalBlock.append(b)
    x=np.arange(1,len(b)+1)
    y=np.array(b)
    fig=plt.figure()
    fig.suptitle('Improvement as a function of distance; Subject '+str(per+1),fontsize=12)
    plt.scatter(x,y)
    p=np.polyfit(x,y,1)
    print(p)
    f = np.poly1d(p)
    plt.plot(x,f(x), 'b-')
    first=f(x[0])
    last=f(x[-1])
    m=(first-last)/(x[0]-x[-1])
    c=f(0)
    y_actual=y
    y_pred=f(x)
    rsquareBlock.append(r2_score(y_actual, y_pred))

    plt.text(10,0.5,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10) #for the exponential fit
    plt.xlabel('Rank')
    plt.ylabel('Improvement')
    plt.savefig('Distance/Blocks/'+str(per+1))
    plt.close()

    #Days
    totalDay.append(d)
    x=np.arange(1,len(d)+1)
    y=np.array(d)
    fig=plt.figure()
    fig.suptitle('Improvement as a function of distance; Subject '+str(per+1),fontsize=12)
    plt.scatter(x,y)
    p=np.polyfit(x,y,1)
    print(p)
    f = np.poly1d(p)
    plt.plot(x,f(x), 'b-')
    first=f(x[0])
    last=f(x[-1])
    m=(first-last)/(x[0]-x[-1])
    c=f(0)
    y_actual=y
    y_pred=f(x)
    rsquareDay.append(r2_score(y_actual, y_pred))

    plt.text(10,0.5,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10) #for the exponential fit
    plt.xlabel('Rank')
    plt.ylabel('Improvement')
    plt.savefig('Distance/Days/'+str(per+1))
    plt.close()



y=np.mean(totalMT,axis=0)
x=np.arange(len(y))
fig=plt.figure()
fig.suptitle('Improvement as a function of distance; Average of all subjects',fontsize=12)
plt.scatter(x,y)
p=np.polyfit(x,y,1)
#print(p)
f = np.poly1d(p)
plt.plot(x,f(x), 'b-',label="Polyfit")

first=f(x[0])
last=f(x[-1])
m=(first-last)/(x[0]-x[-1])
c=f(0)
y_actual=y
y_pred=f(x)
rsquareMT.append(r2_score(y_actual, y_pred))
plt.text(10,0.5,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10)
plt.xlabel('Rank')
plt.ylabel('Improvement')
drop=(first-last)/first
plt.savefig('Distance/AllMT/AllSubjectsAvg')
plt.close()

y=np.mean(totalBlock,axis=0)
x=np.arange(len(y))
fig=plt.figure()
fig.suptitle('Improvement as a function of distance; Average of all subjects',fontsize=12)
plt.scatter(x,y)
p=np.polyfit(x,y,1)
#print(p)
f = np.poly1d(p)
plt.plot(x,f(x), 'b-',label="Polyfit")

first=f(x[0])
last=f(x[-1])
m=(first-last)/(x[0]-x[-1])
c=f(0)
y_actual=y
y_pred=f(x)
rsquareBlock.append(r2_score(y_actual, y_pred))
plt.text(10,0.5,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10)
plt.xlabel('Rank')
plt.ylabel('Improvement')
drop=(first-last)/first
plt.savefig('Distance/Blocks/AllSubjectsAvg')
plt.close()

y=np.mean(totalDay,axis=0)
x=np.arange(len(y))
fig=plt.figure()
fig.suptitle('Improvement as a function of distance; Average of all subjects',fontsize=12)
plt.scatter(x,y)
p=np.polyfit(x,y,1)
#print(p)
f = np.poly1d(p)
plt.plot(x,f(x), 'b-',label="Polyfit")

first=f(x[0])
last=f(x[-1])
m=(first-last)/(x[0]-x[-1])
c=f(0)
y_actual=y
y_pred=f(x)
rsquareDay.append(r2_score(y_actual, y_pred))
plt.text(10,0.5,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10)
plt.xlabel('Rank')
plt.ylabel('Improvement')
drop=(first-last)/first
plt.savefig('Distance/Days/AllSubjectsAvg')
plt.close()

workbook=xlsxwriter.Workbook('Distance/GoF.xlsx')
worksheet=workbook.add_worksheet()
row=0
col=0
worksheet.write(row,col+1,'AllMT')
worksheet.write(row,col+2,'Across Blocks')
worksheet.write(row,col+3,'Across Days')
worksheet.write_column(row+1,col,['Subject 1','Subject 2','Subject 3','Subject 4','Subject 5','Subject 6','Subject 7','Subject 8','Average Across Subjects'])
worksheet.write_column(row+1,col+1,rsquareMT)
worksheet.write_column(row+1,col+2,rsquareBlock)
worksheet.write_column(row+1,col+3,rsquareDay)
workbook.close()
