import csv
import matplotlib.pyplot as plt
import numpy as np

t1, t2 = [], []
t3, t4 = [], []
t5, t6 = [], []
t7, t8 = [], []
t9, t10 = [], []

with open('./128fitler.csv', 'r') as myfile:
    rows= csv.reader(myfile,delimiter=',')
    idx = 0
    for row in rows:
        if((idx%2)==0):
            # parse execution time
            tmp = row[0].split()
            exetime = tmp[3]
            t1.append(float(exetime))
        else:
            t2.append((float(row[0])*1e6)/16)
        idx +=1
            # t1.append(float(row[1])*1e6)

with open('./256filter.csv', 'r') as myfile:
    rows= csv.reader(myfile,delimiter=',')
    idx = 0
    for row in rows:
        if((idx%2)==0):
            # parse execution time
            tmp = row[0].split()
            exetime = tmp[3]
            t3.append(float(exetime))
        else:
            t4.append((float(row[0])*1e6)/16)
        idx +=1
with open('./512filter.csv', 'r') as myfile:
    rows= csv.reader(myfile,delimiter=',')
    idx = 0
    for row in rows:
        if((idx%2)==0):
            # parse execution time
            tmp = row[0].split()
            exetime = tmp[3]
            t5.append(float(exetime))
        else:
            t6.append((float(row[0])*1e6)/16)
        idx +=1
with open('./1gfilter.csv', 'r') as myfile:
    rows= csv.reader(myfile,delimiter=',')
    idx = 0
    for row in rows:
        if((idx%2)==0):
            # parse execution time
            tmp = row[0].split()
            exetime = tmp[3]
            t7.append(float(exetime))
        else:
            t8.append((float(row[0])*1e6)/16)
        idx +=1

with open('./2gfilter.csv', 'r') as myfile:
    rows= csv.reader(myfile,delimiter=',')
    idx = 0
    for row in rows:
        if((idx%2)==0):
            # parse execution time
            tmp = row[0].split()
            exetime = tmp[3]
            t9.append(float(exetime))
        else:
            t10.append((float(row[0])*1e6)/16)
        idx +=1

ax = plt.gca()
# ax.set_xlim([xmin, xmax])
ax.set_ylim([min(t10), max(t2)])
# plt.yticks(np.arange(min(t2),max(t2),0.001))
plt.scatter(t1, t2, color='steelblue', label="128MB")
plt.scatter(t3, t4, color='slateblue', label="256MB")
plt.scatter(t5, t6, color='mediumseagreen', label="512MB")
plt.scatter(t7, t8, color='orange', label="1GB")
plt.scatter(t9, t10, color='tomato', label="2GB")

plt.legend(loc="upper left")
plt.title("Thread Context Switch Time vs Function Execution Time")
plt.xlabel('Execution time(/us)', fontsize=11)
plt.ylabel('Context switch time(/us)', fontsize=11)
plt.show()
# data = [t1, t2, t3, t4, t5]

# fig = plt.figure(figsize = (10,7))
# ax = fig.add_subplot(111)
# ax.boxplot(data)
# # fig.title('Thread/Process Context Switch time on 2 Local PCs', fontsize=14)
# ax.set_title('Thread Context Switch time in Google Cloud Function', fontsize=16)
# # ax.set_xlabel('Benchmarks')
# plt.xlabel('Memory', fontsize=16)
# plt.ylabel('Time(/us)', fontsize=16)

# plt.xticks([1, 2, 3, 4, 5], ['128MB', '256MB', '512MB', '1GB', '2GB'],fontsize=14)
# plt.show()