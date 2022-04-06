import csv
import matplotlib.pyplot as plt

t1, t2, t3, t4, t5 = [], [], [], [], []

with open('./cloud.csv', 'r') as myfile:
    rows= csv.reader(myfile,delimiter=',')
    for row in rows:
        if(row[0]!=""):
            t1.append(float(row[1])*1e6)
        if(row[1]!=""):
            t2.append(float(row[3])*1e6)
        if(row[2]!=""):
            t3.append(float(row[5])*1e6)
        if(row[3]!=""):
            t4.append(float(row[7])*1e6)
        if(row[4]!=""):
            t5.append(float(row[8])*1e6)

data = [t1, t2, t3, t4, t5]

fig = plt.figure(figsize = (10,7))
ax = fig.add_subplot(111)
ax.boxplot(data)
# fig.title('Thread/Process Context Switch time on 2 Local PCs', fontsize=14)
ax.set_title('Thread Context Switch time in Google Cloud Function', fontsize=16)
# ax.set_xlabel('Benchmarks')
plt.xlabel('Memory', fontsize=16)
plt.ylabel('Time(/us)', fontsize=16)

plt.xticks([1, 2, 3, 4, 5], ['128MB', '256MB', '512MB', '1GB', '2GB'],fontsize=14)
plt.show()