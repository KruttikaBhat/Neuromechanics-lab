import pickle
from classes import *
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import scipy
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from scipy import stats
import math
import xlsxwriter

def funclog(x, a):
    return a*np.log(x)


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

dt={}
for i in letters:
    for j in letters:
        dt[i+j]=round(math.sqrt((pos[i][0]-pos[j][0])**2 + (pos[i][1]-pos[j][1])**2))




allAvgMT=[]
allTransMT=[]
totalMT=[]
totalBlock=[]
totalDay=[]

dr=[]
lin=[]
rsquareSubjectMT=[]
rsquareSubjectBlock=[]
rsquareSubjectDay=[]
rsquareLinMT=[]
rsquareLinBlock=[]
rsquareLinDay=[]
mtPred=[]
blockPred=[]
dayPred=[]


for per in range(8):
    newMT=[]
    newBlock=[]
    newDay=[]
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
                    transMT[m+n].append([(k.mt[let.index(m)]),k.day,k.block])
                    combi[m+n]=combi[m+n]+1
                    #transDT[m+n].append([k.dt[let.index(m)],k.block])

    rank=[]
    for i in sorted(combi.items(), key=lambda x: x[1], reverse=True):
        if(i[1]!=0):
            rank.append(i)

    distRank=[]
    for i in sorted(dt.items(), key=lambda x: x[1], reverse=True):
        if(i[0] in np.array(rank)[:,0]):
            distRank.append([i[0],i[1],combi[i[0]]])
    """
    for i in transMT:
        for j in transMT[i]:
            j[0]=j[0]*distRank[0][1]
    """
    for i in transMT:
        mx=max(np.array(transMT[i])[:,0])
        for j in transMT[i]:
            j[0]=j[0]/mx

    dMT=[]
    dBlock=[]
    dDay=[]
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


        plt.figure()
        y=(max(y)-y)/max(y)
        plt.scatter(x,y,label=i[0])
        plt.xlabel('Index of Practise')
        plt.ylabel('Movement Time')
        popt,pcov=scipy.optimize.curve_fit(lambda t,a: a*np.log(t),  x,  y)
        #print(popt)
        a=popt[0]
        first=a*np.log(x[0])
        last=a*np.log(x[-1])
        diff=last-first
        if(diff<1):
            dMT.append(diff)
        else:
            dMT.append(y[-1])
        y_actual=y
        y_pred=funclog(x,*popt)
        newMT.append((r2_score(y_actual, y_pred)))
        plt.plot(x,funclog(x,*popt),color='b') #for the exponential fit
        plt.text(100,0.1,'y='+str.format('{0:.4f}',popt[0])+'*log(x)',fontsize=10) #for the exponential fit
        plt.legend()
        plt.savefig('EachTransition/Person'+str(per+1)+'/AllMT/'+str(rank.index(i)+1))
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
        y=(max(y)-y)/max(y)
        print(len(x),len(y))
        plt.figure()
        plt.scatter(x,y,label=i[0])
        popt,pcov=scipy.optimize.curve_fit(lambda t,a: a*np.log(t),  x,  y)
        #print(popt)
        a=popt[0]
        first=a*np.log(x[0])
        last=a*np.log(x[-1])
        diff=last-first
        if(diff<1):
            dBlock.append(diff)
        else:
            dBlock.append(y[-1])
        y_actual=y
        y_pred=funclog(x,*popt)
        newBlock.append(r2_score(y_actual, y_pred))
        plt.plot(x,funclog(x,*popt),color='b') #for the exponential fit
        plt.xlabel('Blocks')
        plt.ylabel('Normalised Movement Time')
        plt.text(50,0,'y='+str.format('{0:.4f}',popt[0])+'log(x)',fontsize=10) #for the exponential fit
        plt.legend()
        plt.savefig('EachTransition/Person'+str(per+1)+'/Blocks/block'+str(rank.index(i)+1))
        plt.close()




    #day wise


    for i in rank:
        y=[]
        day=transMT[i[0]][0][1]
        count=0
        sum=0
        avg=[]
        for j in transMT[i[0]]:
            print(j)
            if(j[1]==day):

                sum=sum+j[0]
                count=count+1
                if(transMT[i[0]].index(j)==len(transMT[i[0]])-1):
                        y.append([sum/count,day])
            else:
                print(sum,count,day)
                y.append([sum/count,day])
                day=j[1]
                sum=j[0]
                count=1
        y=np.array(y)
        x=y[:,1]
        y=y[:,0]
        y=(max(y)-y)/max(y)
        plt.figure()
        plt.scatter(x,y,label=i[0])
        popt,pcov=scipy.optimize.curve_fit(lambda t,a: a*np.log(t),  x,  y)
        #print(popt)
        a=popt[0]
        first=a*np.log(x[0])
        last=a*np.log(x[-1])
        diff=last-first
        if(diff<1):
            dDay.append(diff)
        else:
            dDay.append(y[-1])
        y_actual=y
        y_pred=funclog(x,*popt)
        newDay.append(r2_score(y_actual, y_pred))
        plt.plot(x,funclog(x,*popt),color='b') #for the exponential fit
        plt.text(6,0,'y='+str.format('{0:.4f}',popt[0])+'log(x)',fontsize=10) #for the exponential fit
        plt.legend()
        plt.savefig('EachTransition/Person'+str(per+1)+'/Days/day'+str(rank.index(i)+1))
        plt.close()


    #all MT
    print(dMT)
    x=np.arange(1,len(dMT)+1)
    y=np.array(dMT)
    fig=plt.figure()
    fig.suptitle('Improvement as a function of frequency; Subject '+str(per+1),fontsize=12)
    plt.scatter(x,y)
    p=np.polyfit(x,y,1)
    f = np.poly1d(p)
    plt.plot(x,f(x), 'b-',label="Polyfit")
    y_actual=y
    y_pred=f(x)
    first=f(x[0])
    last=f(x[-1])
    m=(first-last)/(x[0]-x[-1])
    c=f(0)
    plt.xlabel('Rank')
    plt.ylabel('Improvement')
    plt.text(10,0.3,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10) #for the exponential fit
    plt.savefig('EachTransition/MT/'+str(per+1))
    plt.close()
    totalMT.append(dMT)
    rsquareSubjectMT.append(newMT)
    rsquareLinMT.append(r2_score(y_actual, y_pred))
    mtPred.append(f(x))

    #blocks
    print(dBlock)
    x=np.arange(1,len(dBlock)+1)
    y=np.array(dBlock)
    fig=plt.figure()
    fig.suptitle('Improvement as a function of frequency; Subject '+str(per+1),fontsize=12)
    plt.scatter(x,y)
    p=np.polyfit(x,y,1)
    f = np.poly1d(p)
    plt.plot(x,f(x), 'b-',label="Polyfit")
    y_actual=y
    y_pred=f(x)
    first=f(x[0])
    last=f(x[-1])
    m=(first-last)/(x[0]-x[-1])
    c=f(0)
    plt.xlabel('Rank')
    plt.ylabel('Improvement')
    plt.text(10,0.3,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10) #for the exponential fit
    plt.savefig('EachTransition/Blocks/'+str(per+1))
    plt.close()
    totalBlock.append(dBlock)
    rsquareSubjectBlock.append(newBlock)
    rsquareLinBlock.append(r2_score(y_actual, y_pred))
    blockPred.append(f(x))

    #days
    print(dDay)
    x=np.arange(1,len(dDay)+1)
    y=np.array(dDay)
    fig=plt.figure()
    fig.suptitle('Improvement as a function of frequency; Subject '+str(per+1),fontsize=12)
    plt.scatter(x,y)
    p=np.polyfit(x,y,1)
    f = np.poly1d(p)
    plt.plot(x,f(x), 'b-',label="Polyfit")
    y_actual=y
    y_pred=f(x)
    first=f(x[0])
    last=f(x[-1])
    m=(first-last)/(x[0]-x[-1])
    c=f(0)
    plt.xlabel('Rank')
    plt.ylabel('Improvement')
    plt.text(10,0.3,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10) #for the exponential fit
    plt.savefig('EachTransition/Days/'+str(per+1))
    plt.close()
    totalDay.append(dDay)
    rsquareSubjectDay.append(newDay)
    rsquareLinDay.append(r2_score(y_actual, y_pred))
    dayPred.append(f(x))

#all mt
y=np.mean(totalMT,axis=0)
x=np.arange(1,len(y)+1)
fig=plt.figure()
fig.suptitle('Improvement as a function of frequency; Average of all subjects',fontsize=12)
plt.scatter(x,y)
plt.xlabel('Rank')
plt.ylabel('Improvement')
p=np.polyfit(x,y,1)
f = np.poly1d(p)
plt.plot(x,f(x), 'b-',label="Polyfit")
y_actual=y
y_pred=f(x)
rsquareLinMT.append(r2_score(y_actual, y_pred))
first=f(x[0])
last=f(x[-1])
m=(first-last)/(x[0]-x[-1])
c=f(0)
plt.text(10,0.5,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10)
plt.savefig('EachTransition/MT/AllSubjectsAvg')
plt.close()
#blocks
y=np.mean(totalBlock,axis=0)
x=np.arange(1,len(y)+1)
fig=plt.figure()
fig.suptitle('Improvement as a function of frequency; Average of all subjects',fontsize=12)
plt.scatter(x,y)
plt.xlabel('Rank')
plt.ylabel('Improvement')
p=np.polyfit(x,y,1)
f = np.poly1d(p)
plt.plot(x,f(x), 'b-',label="Polyfit")
y_actual=y
y_pred=f(x)
rsquareLinBlock.append(r2_score(y_actual, y_pred))
first=f(x[0])
last=f(x[-1])
m=(first-last)/(x[0]-x[-1])
c=f(0)
plt.text(10,0.5,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10)
plt.savefig('EachTransition/Blocks/AllSubjectsAvg')
plt.close()
#days
y=np.mean(totalMT,axis=0)
x=np.arange(1,len(y)+1)
fig=plt.figure()
fig.suptitle('Improvement as a function of frequency; Average of all subjects',fontsize=12)
plt.scatter(x,y)
plt.xlabel('Rank')
plt.ylabel('Improvement')
p=np.polyfit(x,y,1)
f = np.poly1d(p)
plt.plot(x,f(x), 'b-',label="Polyfit")
y_actual=y
y_pred=f(x)
rsquareLinDay.append(r2_score(y_actual, y_pred))
first=f(x[0])
last=f(x[-1])
m=(first-last)/(x[0]-x[-1])
c=f(0)
plt.text(10,0.5,'y= '+str.format('{0:.4f}', m)+'x +'+str.format('{0:.4f}', c),fontsize=10)
plt.savefig('EachTransition/Days/AllSubjectsAvg')
plt.close()

#saving r-squared values
workbook=xlsxwriter.Workbook('EachTransition/GoF.xlsx')

for w,r1,r2,p in zip(['allMT','Blocks','Days'],[rsquareSubjectMT,rsquareSubjectBlock,rsquareSubjectDay],[rsquareLinMT,rsquareLinBlock,rsquareLinDay],[mtPred,blockPred,dayPred]):
    worksheet=workbook.add_worksheet(w)

    row=0
    col=0
    worksheet.write_row(row,col,'Transition Rank')
    worksheet.write_column(row+1,col,np.arange(1,len(rank2)+1))
    col=col+1
    for i in range(8):
        worksheet.write(row,col,'Subject '+str(i+1))
        worksheet.write_column(row+1,col,np.array(r1)[i,:])
        col=col+1

    col=col+1
    worksheet.write(row,col,'r squared for subject wise improvement plots')
    worksheet.write_column(row+1,col,['Subject 1','Subject 2','Subject 3','Subject 4','Subject 5','Subject 6','Subject 7','Subject 8','Average Across Subjects'])
    worksheet.write_column(row+1,col+1,r2)

    col=col+2
    worksheet.write(row,col,'improvement')
    worksheet.write_column(row+1,col,['Subject 1','Subject 2','Subject 3','Subject 4','Subject 5','Subject 6','Subject 7','Subject 8'])
    worksheet.write(row,col+1,'most frequent')
    worksheet.write(row,col+2,'least frequent')
    worksheet.write_column(row+1,col+1,np.array(p)[:,0])
    worksheet.write_column(row+1,col+2,np.array(p)[:,-1])
    worksheet.write(row+9,col,'Mean')
    worksheet.write(row+10,col,'Std Error')
    worksheet.write(row+9,col+1,np.mean(np.array(p)[:,0]))
    worksheet.write(row+9,col+2,np.mean(np.array(p)[:,-1]))
    worksheet.write(row+10,col+1,np.std(np.array(p)[:,0])/math.sqrt(8))
    worksheet.write(row+10,col+2,np.std(np.array(p)[:,-1])/math.sqrt(8))

workbook.close()
