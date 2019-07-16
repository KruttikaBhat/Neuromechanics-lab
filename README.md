# Neuromechanics-lab
Worked under Dr. Varadhan SKM as part of the Neuromechanics lab in IIT Madras.  
<br>
Initially worked on identifying chunking patterns in the timing data collected as part of a thesis which analyzed finger thumb opposition movements in motor sequence learning. Analysis was done with the raw data. Various clustering algorithms were studied and employed such as K-means and DBSCAN. These are not present here.  
<br>
As these methods work better with multi-dimensional data, an algorithm for identifying chunks was written which looked at identifying a threshold for chunking. This is found in the folder Chunking.  
<br>
After multiple discussions, the problem statement shifted to answering various questions in the data such as how the frequency of practise, distance required for a movement and the combination of frequency and distance will effect improvement in task performance.  
<br>
To answer these questions, I looked specifically at the movement times and improvement in performance with practise by fitting a logarithmic curve to the data and using an improvement metric to compare improvement between different frequencies, transitions and subjects. This is found in the folder 12-6-19_MTAnalysis_Documentation.  
<br>
All programs for this data analysis were written in Python. The work was done independently under the guidance of the afore mentioned professor as well as the PhD student on whose data the analysis was performed. The work is still in progress. 
