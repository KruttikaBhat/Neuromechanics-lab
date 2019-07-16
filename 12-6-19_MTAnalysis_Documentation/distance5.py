import pickle
from classes import *
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import math
import scipy
from scipy.optimize import curve_fit
import xlsxwriter


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
        dt[i+j]=math.sqrt((pos[i][0]-pos[j][0])**2 + (pos[i][1]-pos[j][1])**2)


workbook=xlsxwriter.Workbook('Distance/Distance1.xlsx')
worksheet=workbook.add_worksheet('AllMT')
worksheet1=workbook.add_worksheet('Blocks')
worksheet2=workbook.add_worksheet('Days')
row=0
col=0

for per in range(8):

    worksheet.write(row,col,"Person "+str(per+1))
    worksheet1.write(row,col,"Person "+str(per+1))
    worksheet2.write(row,col,"Person "+str(per+1))
    row=row+1
    worksheet.write_row(row,col,['Transition','Distance','Frequency','Improvement'])
    worksheet1.write_row(row,col,['Transition','Distance','Frequency','Improvement'])
    worksheet2.write_row(row,col,['Transition','Distance','Frequency','Improvement'])
    row=row+1
    init=row

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
                    if(dt[m+n]!=0):
                        transMT[m+n].append([(k.mt[let.index(m)]),k.day,k.block])
                        combi[m+n]=combi[m+n]+1
                    #transDT[m+n].append([k.dt[let.index(m)],k.block])

    rank=[]
    for i in sorted(combi.items(), key=lambda x: x[1], reverse=True):
        if(i[1]!=0):
            rank.append(i)

    distRank=[]
    for i in sorted(dt.items(), key=lambda x: x[1], reverse=True):
        if(i[0] in np.array(rank)[:,0] and i[1]!=0):
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
    print(distRank)
    d=[]
    #allmt
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
                        x.append(temp+(k/count))
                    print(x)

        y=(max(y)-y)/max(y)
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

    distances=sorted(np.unique(np.array(distRank)[:,1]),reverse=True)
    print(distances)
    presDist=distances[0]
    trans=[]
    dist=[]
    fre=[]
    imp=[]


    for i in distRank:
        print(i[1],presDist)
        if(float(i[1])==float(presDist)):
            trans.append(i[0])
            dist.append(i[1])
            fre.append(i[2])
            imp.append(d[distRank.index(i)])

            if(i==distRank[-1]):
                newtrans=[n for m,n in sorted(zip(fre,trans))]
                newimp=[n for m,n in sorted(zip(fre,imp))]
                newfre=sorted(fre)
                worksheet.write_column(row,col,newtrans)
                worksheet.write_column(row,col+1,dist)
                worksheet.write_column(row,col+2,newfre)
                worksheet.write_column(row,col+3,newimp)
                row=row+len(newtrans)

        else:

            newtrans=[n for m,n in sorted(zip(fre,trans))]
            newimp=[n for m,n in sorted(zip(fre,imp))]
            newfre=sorted(fre)
            worksheet.write_column(row,col,newtrans)
            worksheet.write_column(row,col+1,dist)
            worksheet.write_column(row,col+2,newfre)
            worksheet.write_column(row,col+3,newimp)
            row=row+len(newtrans)
            trans=[]
            dist=[]
            fre=[]
            imp=[]
            trans.append(i[0])
            dist.append(i[1])
            fre.append(i[2])
            imp.append(d[distRank.index(i)])
            presDist=i[1]

    #Blocks
    row=init
    d=[]
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
            d.append(diff)
        else:
            d.append(y[-1])

    distances=sorted(np.unique(np.array(distRank)[:,1]),reverse=True)
    print(distances)
    presDist=distances[0]
    trans=[]
    dist=[]
    fre=[]
    imp=[]


    for i in distRank:
        print(i[1],presDist)
        if(float(i[1])==float(presDist)):
            trans.append(i[0])
            dist.append(i[1])
            fre.append(i[2])
            imp.append(d[distRank.index(i)])

            if(i==distRank[-1]):
                newtrans=[n for m,n in sorted(zip(fre,trans))]
                newimp=[n for m,n in sorted(zip(fre,imp))]
                newfre=sorted(fre)
                worksheet1.write_column(row,col,newtrans)
                worksheet1.write_column(row,col+1,dist)
                worksheet1.write_column(row,col+2,newfre)
                worksheet1.write_column(row,col+3,newimp)
                row=row+len(newtrans)

        else:

            newtrans=[n for m,n in sorted(zip(fre,trans))]
            newimp=[n for m,n in sorted(zip(fre,imp))]
            newfre=sorted(fre)
            worksheet1.write_column(row,col,newtrans)
            worksheet1.write_column(row,col+1,dist)
            worksheet1.write_column(row,col+2,newfre)
            worksheet1.write_column(row,col+3,newimp)
            row=row+len(newtrans)
            trans=[]
            dist=[]
            fre=[]
            imp=[]
            trans.append(i[0])
            dist.append(i[1])
            fre.append(i[2])
            imp.append(d[distRank.index(i)])
            presDist=i[1]

    #Days
    row=init
    d=[]
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

    distances=sorted(np.unique(np.array(distRank)[:,1]),reverse=True)
    print(distances)
    presDist=distances[0]
    trans=[]
    dist=[]
    fre=[]
    imp=[]


    for i in distRank:
        print(i[1],presDist)
        if(float(i[1])==float(presDist)):
            trans.append(i[0])
            dist.append(i[1])
            fre.append(i[2])
            imp.append(d[distRank.index(i)])

            if(i==distRank[-1]):
                newtrans=[n for m,n in sorted(zip(fre,trans))]
                newimp=[n for m,n in sorted(zip(fre,imp))]
                newfre=sorted(fre)
                worksheet2.write_column(row,col,newtrans)
                worksheet2.write_column(row,col+1,dist)
                worksheet2.write_column(row,col+2,newfre)
                worksheet2.write_column(row,col+3,newimp)
                row=row+len(newtrans)

        else:

            newtrans=[n for m,n in sorted(zip(fre,trans))]
            newimp=[n for m,n in sorted(zip(fre,imp))]
            newfre=sorted(fre)
            worksheet2.write_column(row,col,newtrans)
            worksheet2.write_column(row,col+1,dist)
            worksheet2.write_column(row,col+2,newfre)
            worksheet2.write_column(row,col+3,newimp)
            row=row+len(newtrans)
            trans=[]
            dist=[]
            fre=[]
            imp=[]
            trans.append(i[0])
            dist.append(i[1])
            fre.append(i[2])
            imp.append(d[distRank.index(i)])
            presDist=i[1]


    row=row+2

workbook.close()
