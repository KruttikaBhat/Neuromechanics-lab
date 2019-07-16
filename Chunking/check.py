import pickle
from classes import *
import numpy as np
import xlsxwriter

with open("allObjects.pkl", "rb") as fp:
    proc_data = pickle.load(fp)

fp.close()

with open("Mean_StdDev/allWords.pkl", "rb") as fp:
    words=pickle.load(fp)

fp.close()

"""
#put the movement times, mean and standard deviation of each word of each person into an excel worksheet
#and the mean and stdev of each word across all days across all subjects

with open("Mean_StdDev/EachWordAllDays.pkl", "rb") as fp:
    uniqueWordsmt=pickle.load(fp)

fp.close()


workbook = xlsxwriter.Workbook('Mean_StdDev/PerWord.xlsx')
worksheet=[]
for i in range(1,11):
    worksheet.append(workbook.add_worksheet("Person "+str(i)))

worksheet1=workbook.add_worksheet("AllSubjects")

cell_format1 = workbook.add_format()
cell_format1.set_bold()
cell_format1.set_font_color('blue')

cell_format2 = workbook.add_format()
cell_format2.set_bold()
cell_format2.set_font_color('red')

row=0
col=0
Labels=['Word','Day','MT1','MT2','MT3','MT4']

for i in worksheet:
    i.write_row(row,col,Labels)
row=row+1

for i in uniqueWordsmt:
    row=1
    for j in i:
        worksheet[uniqueWordsmt.index(i)].write(row,col,j.word)
        for (m,n) in zip(j.mts,j.days):
            worksheet[uniqueWordsmt.index(i)].write(row,col+1,n)
            worksheet[uniqueWordsmt.index(i)].write_row(row,col+2,m)
            row=row+1
        worksheet[uniqueWordsmt.index(i)].write(row,col+1,'Mean',cell_format1)
        worksheet[uniqueWordsmt.index(i)].write(row+1,col+1,'Stdev',cell_format2)
        worksheet[uniqueWordsmt.index(i)].write_row(row,col+2,j.mean,cell_format1)
        worksheet[uniqueWordsmt.index(i)].write_row(row+1,col+2,j.stdev,cell_format2)
        row=row+2
row=0
col=0
worksheet1.write_row(row,col,['Word','','MT1','MT2','MT3','MT4'])
row=row+1

for w in words:
    worksheet1.write(row,col,w)
    mvmt=[]
    for i in uniqueWordsmt:
        for j in i[words.index(w)].mts:
            mvmt.append(j)
        print(i[words.index(w)].word)
    print(mvmt)
    mean=np.mean(np.array(mvmt),axis=0)
    stdev=np.std(np.array(mvmt),axis=0)
    print(mean,stdev)
    worksheet1.write_column(row,col+1,['Mean','Stdev'])
    worksheet1.write_row(row,col+2,mean)
    worksheet1.write_row(row+1,col+2,stdev)
    row=row+2


workbook.close()
"""


"""

#for each unique word look at the mean and std dev of mts
#for each word in dictionary. this object is put into a pickle file
wstats=[]

for i in proc_data:
    new_word=[]
    for w in words:
        mtimes=[]
        days=[]
        blocks=[]
        for j in i.blocks:
            for k in j.words:
                #print("k",k.letters)
                if k.letters==w:
                    mtimes.append(k.mt)
                    days.append(k.day)
                    blocks.append(k.block)
        mean=np.mean(np.array(mtimes),axis=0)
        stdev=np.std(np.array(mtimes),axis=0)
        #print(np.array(mtimes))
        #print(mean,stdev)
        new_word.append(wordStats(mtimes,days,blocks,mean,stdev,w))
    wstats.append(new_word)


for i in wstats:
    print(wstats.index(i))
    for j in i:
        print(j.word,j.mean,j.stdev)

with open("Mean_StdDev/EachWordAllDays.pkl","wb") as fp:
    pickle.dump(wstats,fp)

"""


"""
#get all movement times and the mean, stdev across all days as well as for each days

workbook = xlsxwriter.Workbook('MovementTimes.xlsx')
worksheet=[]
for i in range(1,11):
    worksheet.append(workbook.add_worksheet("Person "+str(i)))


# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0
Labels=['Day','Block','MT1','MT2','MT3','MT4']

for i in worksheet:
    i.write_row(row,col,Labels)
row=row+1

for i in proc_data:
    row=1
    arr=[]
    for j in i.blocks:
        for k in j.words:
            new_row=[]
            new_row.append(int(i.blocks.index(j)/12)+1)
            new_row.append(i.blocks.index(j)%12+1)
            new_row.append(k.mt[0])
            new_row.append(k.mt[1])
            new_row.append(k.mt[2])
            new_row.append(k.mt[3])
            arr.append(k.mt)
            worksheet[proc_data.index(i)].write_row(row, col,new_row)
            row=row+1
    print(row)
    print(proc_data.index(i))
    print(np.array(arr).shape)
    mtMean=np.mean(np.array(arr),axis=0)
    print("Mean=",mtMean)
    mtStd=np.std(np.array(arr),axis=0)

    worksheet[proc_data.index(i)].write(1,col+7,'All days')
    worksheet[proc_data.index(i)].write_row(0,col+9,Labels[2:])
    worksheet[proc_data.index(i)].write_column(1,col+8,['Mean','Std Deviation'])
    worksheet[proc_data.index(i)].write_row(1,col+9,mtMean) #'=AVERAGE(D2:D4937)'
    worksheet[proc_data.index(i)].write_row(2,col+9,mtStd)


row=4
col=9

for i in proc_data:
    arr=[]
    print(proc_data.index(i))
    for j in i.blocks:
        for k in j.words:
            #print(k.mt)
            arr.append(k.mt)
        if((i.blocks.index(j)+1)%12==0):
            print((i.blocks.index(j)+1)/12)
            print(np.array(arr).shape)
            mtMean=np.mean(np.array(arr),axis=0)
            print("Mean=",mtMean)
            mtStd=np.std(np.array(arr),axis=0)
            print("Standard Deviation=",mtStd)
            arr=[]
            worksheet[proc_data.index(i)].write(row,col-2,'Day '+str(int((i.blocks.index(j)+1)/12)))
            worksheet[proc_data.index(i)].write_column(row,col-1,['Mean','StdDev'])
            worksheet[proc_data.index(i)].write_row(row, col,mtMean)
            worksheet[proc_data.index(i)].write_row(row+1, col,mtStd)
            row=row+4
    row=4


workbook.close()
"""



"""
#for each block and compare day by day 12x15 for each person for each movement time.


workbook = xlsxwriter.Workbook('PerBlock.xlsx')
worksheet=[]
for i in range(1,11):
    worksheet.append(workbook.add_worksheet("Person "+str(i)))

# Start from the first cell. Rows and columns are zero indexed.


for i in proc_data:
    row = 0
    col = 0
    arr=[]
    means=[]
    std=[]
    #print(proc_data.index(i))
    #f.write("\n\nPerson "+str(proc_data.index(i)+1)+":\n")
    for j in i.blocks:
        for k in j.words:
            #print(k.mt)
            arr.append(k.mt)
        #if((i.blocks.index(j)+1)%12==0):
        #print((i.blocks.index(j)+1)/12)
        #print(np.array(arr).shape)
        mtMean=np.mean(np.array(arr),axis=0)
        #print("Mean=",mtMean)
        mtStd=np.std(np.array(arr),axis=0)
        #print("Standard Deviation=",mtStd)

        means.append(mtMean)
        #print(mtMean)
        std.append(mtStd)
    for l in range(4):
        worksheet[proc_data.index(i)].write(row,col,'MT'+str(l+1))
        row=row+1
        for m,n in zip(['Mean', 'Std Dev'],[means,std]):
            worksheet[proc_data.index(i)].write(row,col,m)
            worksheet[proc_data.index(i)].write(row,col+2,'Days')
            worksheet[proc_data.index(i)].write(row+2,col,'Blocks')
            worksheet[proc_data.index(i)].write_row(row+1,col+2,np.arange(1,16))
            worksheet[proc_data.index(i)].write_column(row+2,col+1,np.arange(1,13))
            row=row+2
            #print(means)
            temp=np.array(n)[0::12]
            #print(temp[:,0])
            #print(mt0)
            #for l in temp:
            #    print(l[0])
                #for p in l:
                #    print(p)

            for p in range(12):
                temp=np.array(means)[p::12]
                worksheet[proc_data.index(i)].write_row(row,col+2,temp[:,l].tolist())
                row=row+1
            row=row+2





workbook.close()
#f.close()
"""


"""


#for all blocks in each day. write to a text file
f=open("Mean_StdDev/EachDayAllBlocks.txt","w")

f.write("The mean and standard deviation of the 4 movement times are taken across all blocks in each day for each person irrespective of the word.\n")
for i in proc_data:
    arr=[]
    print(proc_data.index(i))
    f.write("\n\nPerson "+str(proc_data.index(i)+1)+":\n")
    for j in i.blocks:
        for k in j.words:
            #print(k.mt)
            arr.append(k.mt)
        if((i.blocks.index(j)+1)%12==0):
            print((i.blocks.index(j)+1)/12)
            print(np.array(arr).shape)
            mtMean=np.mean(np.array(arr),axis=0)
            print("Mean=",mtMean)
            mtStd=np.std(np.array(arr),axis=0)
            print("Standard Deviation=",mtStd)
            arr=[]
            f.write("\nDay "+str(int((i.blocks.index(j)+1)/12))+":\n")
            f.write("Mean:"+" mt1="+str.format('{0:.4f}',mtMean[0])+" mt2="+str.format('{0:.4f}',mtMean[1])+" mt3="+str.format('{0:.4f}',mtMean[2])+" mt4="+str.format('{0:.4f}',mtMean[3])+"\n")
            f.write("Standard Dev:"+" mt1="+str.format('{0:.4f}',mtStd[0])+" mt2="+str.format('{0:.4f}',mtStd[1])+" mt3="+str.format('{0:.4f}',mtStd[2])+" mt4="+str.format('{0:.4f}',mtStd[3])+"\n")



f.close()

"""

"""
#each person, all days, write to a text file

f=open("Mean_StdDev/AllDays.txt","w")

f.write("The mean and standard deviation of the 4 movement times are taken across all days for each person irrespective of word.\n")
for i in proc_data:
    arr=[]
    for j in i.blocks:
        for k in j.words:
            #print(k.mt)
            arr.append(k.mt)
    print(proc_data.index(i))
    print(np.array(arr).shape)
    mtMean=np.mean(np.array(arr),axis=0)
    print("Mean=",mtMean)
    mtStd=np.std(np.array(arr),axis=0)
    print("Standard Deviation=",mtStd)
    f.write("\n\nPerson "+str(proc_data.index(i)+1)+":\n")
    f.write("Mean:"+" mt1="+str.format('{0:.4f}',mtMean[0])+" mt2="+str.format('{0:.4f}',mtMean[1])+" mt3="+str.format('{0:.4f}',mtMean[2])+" mt4="+str.format('{0:.4f}',mtMean[3])+"\n\n")
    f.write("Standard Dev:"+" mt1="+str.format('{0:.4f}',mtStd[0])+" mt2="+str.format('{0:.4f}',mtStd[1])+" mt3="+str.format('{0:.4f}',mtStd[2])+" mt4="+str.format('{0:.4f}',mtStd[3])+"\n")

f.close()
"""
