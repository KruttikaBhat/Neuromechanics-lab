import pickle
from classes import *
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import scipy
from scipy.optimize import curve_fit

def logfunc(x, a, b,c):
    return (np.sign(a)*(np.abs(a))**(x)+b)/c

def func(x, a, b):
    return a * (x**b)

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


allAvgMT=[]
allTransMT=[]
totalmt=[]
totalb=[]
totald=[]
file=open("EachTransition/Exp/AllMT/PercentageDrop.txt","w")
file1=open("EachTransition/Exp/Blocks/PercentageDrop.txt","w")
file2=open("EachTransition/Exp/Days/PercentageDrop.txt","w")
dr=[]
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

    rank=[]
    for i in sorted(combi.items(), key=lambda x: x[1], reverse=True):
        if(i[1]!=0):
            rank.append(i)

    #file=open('EachTransition/Person'+str(per+1)+'/lr','w')
    #file.write('Transition; Rate of decay; Learning rate; Drop\n')
    d=[]
    bl=[]
    mt=[]
    #no averaging


    for i in rank:
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
        print(len(x),len(y))
        plt.figure()
        plt.scatter(x,y,label=i[0])
        popt,pcov=scipy.optimize.curve_fit(lambda t,a,b: a*(t**b),  x,  y,p0=[4,-0.05])
        print(popt)
        b=popt[1]
        a=popt[0]
        first=a
        last=a*(x[-1]**b)
        lr=2**b
        diff=(first-last)/first
        mt.append(diff)
        plt.plot(x,func(x,*popt),color='b') #for the exponential fit
        plt.text(0,1.1,'y='+str.format('{0:.4f}',popt[0])+'x^'+str.format('{0:.4f}', popt[1]),fontsize=10) #for the exponential fit
        file.write(i[0]+' = \t'+str.format('{0:.4f}', popt[1])+'\t'+str(lr)+'\t'+str(diff)+'\n')
        plt.legend()
        plt.savefig('EachTransition/Exp/Person'+str(per+1)+'/AllMT/'+str(rank.index(i)+1))
        plt.close()



    #blocks


    for i in rank:
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
        print(len(x),len(y))
        plt.figure()
        plt.scatter(x,y,label=i[0])
        popt,pcov=scipy.optimize.curve_fit(lambda t,a,b: a*(t**b),  x,  y,p0=[4,-0.05])
        print(popt)
        b=popt[1]
        a=popt[0]
        first=a*(x[0]**b)
        last=a*(x[-1]**b)
        lr=2**b
        diff=(first-last)/first
        bl.append(diff)
        plt.plot(x,func(x,*popt),color='b') #for the exponential fit
        plt.text(0,1.1,'y='+str.format('{0:.4f}',popt[0])+'x^'+str.format('{0:.4f}', popt[1]),fontsize=10) #for the exponential fit
        file1.write(i[0]+' = \t'+str.format('{0:.4f}', popt[1])+'\t'+str(lr)+'\t'+str(diff)+'\n')
        plt.legend()
        plt.savefig('EachTransition/Exp/Person'+str(per+1)+'/Blocks/block'+str(rank.index(i)+1))
        plt.close()




    #day wise


    for i in rank:
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
        print(len(x),len(y))
        plt.figure()
        plt.scatter(x,y,label=i[0])
        popt,pcov=scipy.optimize.curve_fit(lambda t,a,b: a*(t**b),  x,  y,p0=[4,-0.05])
        #print(popt)
        b=popt[1]
        a=popt[0]
        first=a
        last=a*(15**b)
        lr=2**b
        diff=(first-last)/first
        d.append(diff)
        plt.plot(x,func(x,*popt),color='b') #for the exponential fit
        plt.text(0,1.1,'y='+str.format('{0:.4f}',popt[0])+'x^'+str.format('{0:.4f}', popt[1]),fontsize=10) #for the exponential fit
        file2.write(i[0]+' = \t'+str.format('{0:.4f}', popt[1])+'\t'+str(lr)+'\t'+str(diff)+'\n')
        plt.legend()
        plt.savefig('EachTransition/Exp/Person'+str(per+1)+'/Days/day'+str(rank.index(i)+1))
        plt.close()




    #file.close()
    #all mt
    totalmt.append(mt)
    x=np.arange(1,len(mt)+1)
    y=np.array(mt)
    plt.figure()
    plt.scatter(x,y)
    p=np.polyfit(x,y,1)
    print(p)
    f = np.poly1d(p)
    plt.plot(x,f(x), 'b-')
    a=popt[1]
    b=popt[0]
    first=f(x[0])
    last=f(x[-1])
    m=(first-last)/(x[0]-x[-1])
    c=f(0)
    plt.text(0.3,0.2,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10) #for the exponential fit

    drop=(first-last)*100
    dr.append(drop)
    #print(str(per+1)+' first:'+str(first)+' last:'+str(last)+' drop:'+str(drop))
    file.write('\n'+str(per+1)+' first:'+str(first)+' last:'+str(last)+' drop:'+str(drop))
    plt.savefig('EachTransition/Exp/AllMT/'+str(per+1))
    plt.close()
    #blocks
    totalb.append(bl)
    x=np.arange(1,len(bl)+1)
    y=np.array(bl)
    plt.figure()
    plt.scatter(x,y)
    p=np.polyfit(x,y,1)
    print(p)
    f = np.poly1d(p)
    plt.plot(x,f(x), 'b-')
    a=popt[1]
    b=popt[0]
    first=f(x[0])
    last=f(x[-1])
    m=(first-last)/(x[0]-x[-1])
    c=f(0)
    plt.text(0.3,0.2,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10) #for the exponential fit

    drop=(first-last)*100
    dr.append(drop)
    #print(str(per+1)+' first:'+str(first)+' last:'+str(last)+' drop:'+str(drop))
    file1.write('\n'+str(per+1)+' first:'+str(first)+' last:'+str(last)+' drop:'+str(drop))
    plt.savefig('EachTransition/Exp/Blocks/'+str(per+1))
    plt.close()

    totald.append(d)
    x=np.arange(1,len(d)+1)
    y=np.array(d)
    plt.figure()
    plt.scatter(x,y)
    p=np.polyfit(x,y,1)
    print(p)
    f = np.poly1d(p)
    plt.plot(x,f(x), 'b-')
    a=popt[1]
    b=popt[0]
    first=f(x[0])
    last=f(x[-1])
    m=(first-last)/(x[0]-x[-1])
    c=f(0)
    plt.text(0.3,0.2,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10) #for the exponential fit

    drop=(first-last)*100
    dr.append(drop)
    #print(str(per+1)+' first:'+str(first)+' last:'+str(last)+' drop:'+str(drop))
    file2.write('\n'+str(per+1)+' first:'+str(first)+' last:'+str(last)+' drop:'+str(drop))
    plt.savefig('EachTransition/Exp/Days/'+str(per+1))
    plt.close()


y=np.mean(totalmt,axis=0)
x=np.arange(len(y))
plt.figure()
plt.scatter(x,y)
p=np.polyfit(x,y,1)
#print(p)
f = np.poly1d(p)
plt.plot(x,f(x), 'b-',label="Polyfit")
a=popt[1]
b=popt[0]
first=f(x[0])
last=f(x[-1])
m=(first-last)/(x[0]-x[-1])
c=f(0)
plt.text(0.3,0.2,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10)
drop=(first-last)*100
#print('avg, first:'+str(first)+' last:'+str(last)+' drop:'+str(drop))
file.write('\navg, first:'+str(first)+' last:'+str(last)+' drop:'+str(drop))
file.close()
plt.savefig('EachTransition/Exp/AllMT/AllSubjectsAvg')
plt.close()

y=np.mean(totalb,axis=0)
x=np.arange(len(y))
plt.figure()
plt.scatter(x,y)
p=np.polyfit(x,y,1)
#print(p)
f = np.poly1d(p)
plt.plot(x,f(x), 'b-',label="Polyfit")
a=popt[1]
b=popt[0]
first=f(x[0])
last=f(x[-1])
m=(first-last)/(x[0]-x[-1])
c=f(0)
plt.text(0.3,0.2,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10)
drop=(first-last)*100
#print('avg, first:'+str(first)+' last:'+str(last)+' drop:'+str(drop))
file1.write('\navg, first:'+str(first)+' last:'+str(last)+' drop:'+str(drop))
file1.close()
plt.savefig('EachTransition/Exp/Blocks/AllSubjectsAvg')
plt.close()

y=np.mean(totald,axis=0)
x=np.arange(len(y))
plt.figure()
plt.scatter(x,y)
p=np.polyfit(x,y,1)
#print(p)
f = np.poly1d(p)
plt.plot(x,f(x), 'b-',label="Polyfit")
a=popt[1]
b=popt[0]
first=f(x[0])
last=f(x[-1])
m=(first-last)/(x[0]-x[-1])
c=f(0)
plt.text(0.3,0.2,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10)
drop=(first-last)*100
#print('avg, first:'+str(first)+' last:'+str(last)+' drop:'+str(drop))
file2.write('\navg, first:'+str(first)+' last:'+str(last)+' drop:'+str(drop))
file2.close()
plt.savefig('EachTransition/Exp/Days/AllSubjectsAvg')
plt.close()
