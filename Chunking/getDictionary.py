import pickle
from classes import *
import numpy as np


with open("allObjects.pkl", "rb") as fp:
    proc_data = pickle.load(fp)

fp.close()

def sort_name(x):
    return x[0]

total=0
#overall=[]
for i in proc_data:
    unique_words=[]
    print(proc_data.index(i))
    unique_words.append([i.blocks[0].words[0].letters,1])
    for j in i.blocks:
        for k in j.words:
            if(i.blocks.index(j)==0 and j.words.index(k)==0):
                continue
            if k.letters in np.array(unique_words)[:,0].tolist():
                index=np.array(unique_words)[:,0].tolist().index(k.letters)
                unique_words[index][1]=unique_words[index][1]+1
            else:
                unique_words.append([k.letters,1])
    dict=np.array(sorted(unique_words,key=sort_name))
    print(sum(int(x) for x in dict[:,1]))
    tot=sum(int(x) for x in dict[:,1])

    with open("dictionary/"+str(proc_data.index(i)+1)+".txt", 'w') as f:
        f.write("Unique words: "+str(dict.shape[0])+" Total words: "+str(tot)+"\n")
        for item in dict:
            f.write("%s - %s\n" % (item[0],item[1]))
    f.close()

    i.dict=dict
    i.totalWords=tot
    i.uniqueWords=dict.shape[0]

    total=total+i.totalWords
"""
    if(proc_data.index(i)==0):
        overall=list(set(overall) | set(dict[:,0].tolist()))
    else:
        inter=set(overall).intersection(dict[:,0].tolist())
        overall=list(set(overall) | set(inter))
    print(np.array(overall).shape)


    with open("write/write_dictionary_"+str(i+1)+".txt", "wb") as fp:
        pickle.dump(dict, fp)

    fp.close()

print(sorted(overall))

with open("allWords.pkl", "wb") as fp:
    pickle.dump(sorted(overall), fp)
"""
#total words=51558
print("Total="+str(total))
