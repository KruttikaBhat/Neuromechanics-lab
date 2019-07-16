import pickle
from classes import *
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import scipy
from scipy.optimize import curve_fit



def func(x, a,b,c):
    return a*np.log2(b+x)+c

def funclog(x, a,c):
    return a*np.log2(x)+c


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

#all subjects, all mt
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


y=(y[0]-y)/y[0]
x=np.array(x)
y=np.array(y)
plt.figure()
plt.scatter(x,y,label='Top',color='b') #for the exponential fit
popt,pcov=scipy.optimize.curve_fit(lambda t,a,b,c: a*np.log2(b+t)+c,  x,  y, p0=[1,1,0])
print(popt)

plt.plot(x,func(x,*popt),label='Fitted curve top',color='b') #for the exponential fit
plt.text(0,1,'Top = '+str.format('{0:.4f}', popt[0])+'*log('+str.format('{0:.4f}', popt[1])+'+x)+'+str.format('{0:.4f}', popt[2]),fontsize=10) #for the exponential fit

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


y=(y[0]-y)/y[0]
x=np.array(x)
y=np.array(y)

plt.scatter(x,y,label='Bottom',color='g') #for the exponential fit
popt,pcov=scipy.optimize.curve_fit(lambda t,a,b,c: a*np.log2(b+t)+c,  x,  y, p0=[1,1,0])
print(popt)

plt.plot(x,func(x,*popt),label='Fitted curve bottom',color='g') #for the exponential fit
plt.text(4,-2,'Bottom = '+str.format('{0:.4f}', popt[0])+'*log('+str.format('{0:.4f}', popt[1])+'+x)+'+str.format('{0:.4f}', popt[2]),fontsize=10) #for the exponential fit

plt.legend(loc=4)

plt.savefig('correlation_2/Log/Performance/AllMT/AllSubjectsAvg')



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


    y=(y[0]-y)/y[0]
    x=np.array(x)
    y=np.array(y)
    plt.figure()
    plt.scatter(x,y,label='Top',color='b') #for the exponential fit
    popt,pcov=scipy.optimize.curve_fit(lambda t,a,c: a*np.log2(t)+c,  x,  y)#for the exponential fit
    print(popt)

    plt.plot(x,funclog(x,*popt),label='Fitted curve top',color='b') #for the exponential fit
    plt.text(0,1.1,'top 4 = '+str.format('{0:.4f}', popt[0])+'*exp('+str.format('{0:.4f}', popt[1])+'x)',fontsize=10) #for the exponential fit


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


    y=(y[0]-y)/y[0]
    x=np.array(x)
    y=np.array(y)
    plt.scatter(x,y,label='Bottom',color='g') #for the exponential fit

    popt,pcov=scipy.optimize.curve_fit(lambda t,a,c: a*np.log2(t)+c,  x,  y)#for the exponential fit
    print(popt)

    plt.plot(x,funclog(x,*popt),label='Fitted curve bottom',color='g') #for the exponential fit
    plt.text(-1,0,'Bottom 4 = '+str.format('{0:.4f}', popt[0])+'*exp('+str.format('{0:.4f}', popt[1])+'x)',fontsize=10) #for the exponential fit

    plt.legend(loc=4)
    plt.savefig('correlation_2/Log/Performance/AllMT/Person'+str(p+1))
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
    print(len(new))
    top.append([new,d])
    new=[]
    for j in rank2[-4:]:
        for k in range(8):
            allTransMT[k][j[0]]
            for i in allTransMT[k][j[0]]:
                block=((i[1]-1)*12)+i[2]
                print(block,d)
                if(block==d):
                    new.append(i[0])
    print(len(new))
    if(len(new)):
        bottom.append([new,d])

print(np.array(top).shape)
top=np.array(top)
y=[]
x=[]
for i in top:
    print(i)
    y.append(np.mean(i[0]))
    x.append(i[1])

y=(y[0]-y)/y[0]
x=np.array(x)
y=np.array(y)
plt.figure()
plt.scatter(x,y,label='Top',color='b') #for the exponential fit
popt,pcov=scipy.optimize.curve_fit(lambda t,a,b,c: a*np.log2(b+t)+c,  x,  y, p0=[1,1,0])
print(popt)

plt.plot(x,func(x,*popt),label='Fitted curve top',color='b') #for the exponential fit
plt.text(0,1,'Top = '+str.format('{0:.4f}', popt[0])+'*log('+str.format('{0:.4f}', popt[1])+'+x)+'+str.format('{0:.4f}', popt[2]),fontsize=10) #for the exponential fit

y=[]
x=[]
for i in bottom:
    y.append(np.mean(i[0]))
    x.append(i[1])
y=(y[0]-y)/y[0]
x=np.array(x)
y=np.array(y)

plt.scatter(x,y,label='Bottom',color='g') #for the exponential fit

popt,pcov=scipy.optimize.curve_fit(lambda t,a,b,c: a*np.log2(b+t)+c,  x,  y, p0=[1,1,0])
print(popt)

plt.plot(x,func(x,*popt),label='Fitted curve bottom',color='g') #for the exponential fit
plt.text(4,-2,'Bottom = '+str.format('{0:.4f}', popt[0])+'*log('+str.format('{0:.4f}', popt[1])+'+x)+'+str.format('{0:.4f}', popt[2]),fontsize=10) #for the exponential fit

plt.legend(loc=4)
plt.savefig('correlation_2/Log/Performance/PerBlock/AllSubjectsAvg')


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
    for i in top:
        y.append(np.mean(i[0]))
        x.append(i[1])
    y=(y[0]-y)/y[0]
    x=np.array(x)
    y=np.array(y)
    print(x,y)
    plt.figure()
    plt.scatter(x,y,label='Top Mean',color='b') #for the exponential fit
    popt,pcov=scipy.optimize.curve_fit(lambda t,a,c: a*np.log2(t)+c,  x,  y)#for the exponential fit
    print(popt)

    plt.plot(x,funclog(x,*popt),label='Fitted curve top',color='b') #for the exponential fit
    plt.text(4,1,'Top = '+str.format('{0:.4f}', popt[0])+'*log(x)+'+str.format('{0:.4f}', popt[1]),fontsize=10) #for the exponential fit

    y=[]
    x=[]
    for i in bottom:
        y.append(np.mean(i[0]))
        x.append(i[1])
    y=(y[0]-y)/y[0]
    x=np.array(x)
    y=np.array(y)

    plt.scatter(x,y,label='Bottom Mean',color='g') #for the exponential fit
    popt,pcov=scipy.optimize.curve_fit(lambda t,a,c: a*np.log2(t)+c,  x,  y)
 #for the exponential fit
    print(popt)

    plt.plot(x,funclog(x,*popt),label='Fitted curve bottom',color='g') #for the exponential fit
    plt.text(4,0,'Bottom = '+str.format('{0:.4f}', popt[0])+'*log(x)+'+str.format('{0:.4f}', popt[1]),fontsize=10) #for the exponential fit


    plt.legend(loc=4)
    plt.savefig('correlation_2/Log/Performance/PerBlock/Person'+str(p+1))


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
    print(len(new))
    top.append(new)
    new=[]
    for j in rank2[-4:]:
        for k in range(8):
            for i in allTransMT[k][j[0]]:
                if(i[1]==d):
                    new.append(i[0])
    print(len(new))
    bottom.append(new)


y=[]
for i in top:
    y.append(np.mean(i))

y=(y[0]-y)/y[0]

x=np.arange(len(y))
plt.figure()

plt.scatter(x,y,label='Top Mean',color='b') #for the exponential fit
popt,pcov=scipy.optimize.curve_fit(lambda t,a,b,c: a*np.log2(b+t)+c,  x,  y, p0=[1,1,0])
#print(popt)

plt.plot(x,func(x,*popt),label='Fitted curve top',color='b') #for the exponential fit
plt.text(0,0.7,'Top = '+str.format('{0:.4f}', popt[0])+'*log('+str.format('{0:.4f}', popt[1])+'+x)+'+str.format('{0:.4f}', popt[2]),fontsize=10) #for the exponential fit

y=[]
for i in bottom:
    y.append(np.mean(i))

y=(y[0]-y)/y[0]

x=np.arange(len(y))

plt.scatter(x,y,label='Bottom Mean',color='g') #for the exponential fit
popt,pcov=scipy.optimize.curve_fit(lambda t,a,b,c: a*np.log2(b+t)+c,  x,  y, p0=[1,1,0])#for the exponential fit
#print(popt)

plt.plot(x,func(x,*popt),label='Fitted curve bottom',color='g') #for the exponential fit
plt.text(4,0.3,'Bottom = '+str.format('{0:.4f}', popt[0])+'*log('+str.format('{0:.4f}', popt[1])+'+x)+'+str.format('{0:.4f}', popt[2]),fontsize=10) #for the exponential fit
plt.legend(loc=4)
plt.savefig('correlation_2/Log/Performance/PerDay/AvgAllSubjects')




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
        print(len(new))
        if(len(new)):
            bottom.append([new,d])

    y=[]
    yerr=[]
    for t in top:
        y.append(np.mean(t[0]))
        yerr.append(np.std(t[0]))
    x=np.arange(1,len(y)+1)
    y=(y[0]-y)/y[0]

    print(x,y,yerr)
    plt.figure()

    plt.scatter(x,y,label='Top Mean',color='b') #for the exponential fit
    popt,pcov=scipy.optimize.curve_fit(lambda t,a,c: a*np.log2(t)+c,  x,  y) #for the exponential fit
    #print(popt)

    plt.plot(x,funclog(x,*popt),label='Fitted curve top',color='b') #for the exponential fit
    plt.text(4,0.1,'Top = '+str.format('{0:.4f}', popt[0])+'*log(x)+'+str.format('{0:.4f}', popt[1]),fontsize=10) #for the exponential fit

    y=[]
    yerr=[]
    for b in bottom:
        y.append(np.mean(b[0]))
        yerr.append(np.std(b[0]))
    y=(y[0]-y)/y[0]
    x=np.arange(1,len(y)+1)
    print(x,y,yerr)

    plt.scatter(x,y,label='Bottom Mean',color='g') #for the exponential fit
    popt,pcov=scipy.optimize.curve_fit(lambda t,a,c: a*np.log2(t)+c,  x,  y) #for the exponential fit
    print(popt)

    plt.plot(x,funclog(x,*popt),label='Fitted curve bottom',color='g') #for the exponential fit
    plt.text(4,0,'Bottom = '+str.format('{0:.4f}', popt[0])+'*log(x)+'+str.format('{0:.4f}', popt[1]),fontsize=10) #for the exponential fit

    plt.legend(prop={'size': 8},loc=4)
    plt.savefig('correlation_2/Log/Performance/PerDay/Person'+str(p+1))
