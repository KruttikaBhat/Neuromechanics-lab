import pickle
from classes import *


Names=["Niraj","Satish","Ravi","hari","Allwyn","Ramakrishna","Ann","k"]

proc_data=[]
for i in Names:
    proc_data.append(Name(i))



with open("allWords.pkl", "rb") as fp:
    words = pickle.load(fp)
#print(words)

for i in proc_data:
    for j in i.blocks:
        count=0
        letters=[]
        keytimes=[]
        lcontroltimes=[]
        for k in range(len(j.data)):
            #print(count,j.data[k].key,j.data[k].ctime)
            #print(k,j.data[k].key,j.data[k].ctime,len(j.data[k].key))
            if(count<5 and count>0 and j.data[k].key=="LCONTROL" and k<len(j.data)-1 and j.data[k+1].key!="LCONTROL"):
                lcontroltimes.append(j.data[k].ctime)

            elif(j.data[k].key=="SPACE" or j.data[k].key=="LWIN" or j.data[k].key=="BACK"\
                 or (j.data[k].key=="LCONTROL" and k<len(j.data)-1 and j.data[k+1].key=="LCONTROL")):
                count=0
                letters=[]
                keytimes=[]
                lcontroltimes=[]

            else:
                if(count==0 and len(j.data[k].key)==1 and\
                  (k==0 or (j.data[k-2].key=="SPACE" and j.data[k-1].key=="LCONTROL")) and\
                   k<len(j.data)-1 and j.data[k+1].key=="LCONTROL"):
                    count=1
                    letters.append(j.data[k].key)
                    keytimes.append(j.data[k].ctime)
                elif(count<5 and count>0 and len(j.data[k-2].key)==1 and\
                     len(j.data[k].key)==1 and k<len(j.data)-1 and j.data[k+1].key=="LCONTROL"):
                    count=count+1
                    letters.append(j.data[k].key)
                    keytimes.append(j.data[k].ctime)
                    print(proc_data.index(i)+1,i.blocks.index(j)+1,k)
                    print(count,letters,keytimes,lcontroltimes)
                    if(count==5 and k<len(j.data)-2 and j.data[k+1].key=="LCONTROL" and j.data[k+2].key=="SPACE"):
                        if("".join(letters) in words):
                            block=i.blocks.index(j)%12+1
                            day=int(i.blocks.index(j)/12)+1
                            lcontroltimes.append(j.data[k+1].ctime)
                            j.words.append(Word("".join(letters),day,block,keytimes,lcontroltimes))
                            #print("added")

                elif(k<len(j.data)-1 and j.data[k].key!="LCONTROL" and j.data[k+1].key!="LCONTROL"):
                    #print("to zero")
                    count=0
                    letters=[]
                    keytimes=[]
                    lcontroltimes=[]



for i in proc_data[0:1]:
    print(proc_data.index(i))
    for j in i.blocks[:3]:
        print(i.blocks.index(j))
        for k in j.words:
            print(k.letters,k.ct,k.lcontroltimes,k.mt,k.dt)


with open("allObjects.pkl", "wb") as fp:
    pickle.dump(proc_data, fp,protocol=2)
