import csv
import matplotlib.pyplot as plt

t1, t2, t3, t4, t5 = [], [], [], [], []

with open('./local_pc.csv', 'r') as myfile:
    rows= csv.reader(myfile,delimiter=',')
    for row in rows:
        if(row[0]!=""):
            t1.append(float(row[0]))
        if(row[1]!=""):
            t2.append(float(row[1]))
        if(row[2]!=""):
            t3.append(float(row[2]))
        if(row[3]!=""):
            t4.append(float(row[3]))
        if(row[4]!=""):
            t5.append(float(row[4]))

data = [t1, t2, t3, t4, t5]

fig = plt.figure(figsize = (10,7))
ax = fig.add_subplot(111)
ax.boxplot(data)
# fig.title('Thread/Process Context Switch time on 2 Local PCs', fontsize=14)
ax.set_title('Thread/Process Context Switch time on 2 Local PCs', fontsize=16)
# ax.set_xlabel('Benchmarks')
plt.xlabel('Benchmarks', fontsize=16)
plt.ylabel('Time(/us)', fontsize=16)

plt.xticks([1, 2, 3, 4, 5], ['ThreadpingC', 'ThreadCondC', 'ThreadpingP', 'Lmbench', 'ProcRing'],fontsize=14)
plt.show()
