
import scipy.stats as stats
from scipy.stats import shapiro
import csv
import numpy as np
import pylab
import seaborn as sns
import matplotlib.pyplot as plt
from statistics import mean, variance

data = []

with open('./ctx160.csv', 'r') as csvf:
    mycsv = csv.reader(csvf, delimiter=',')
    for row in mycsv:
        data.append(float(row[0]))
#---------------shapiro_wilk-------------
# print(data)
stat, p = shapiro(data)
# if p> 0.05, then it's probably gaussian
print('stat=%.3f, p=%.3f\n' % (stat, p))

# Q-Q plot
# stats.probplot(data, dist="norm", plot=pylab)
# pylab.show()

# histogram
ax = sns.displot(data)
# plt.show()

# CoV
ave = mean(data)
vari = variance(data)
print("CoV: "+str(vari/ave))
