# coding: utf-8
import urllib2
import json

response = urllib2.urlopen('http://opendata.dot.taipei.gov.tw/opendata/gwjs_cityhall.json')
data = json.load(response)
sbi_list = []
for site in data['retVal']:
    sbi_list.append([int(site['sbi']), site['sna'], site['tot']])
# Print out the outcome
for k, v, i in sorted(sbi_list, reverse=True)[:10]:
    print k, i, v


##------ THE BLOCK TO ACCUMULATE SBI AND TOT ----------
sbi, tot = 0, 0
for site in data['retVal']:
    sbi += int(site['sbi'])
    tot += int(site['tot'])
print sbi, tot
##-----------------------------------------------------


# Open and read a file in your local machine
# 'r' means opening the file for reading, not for writing.
fjson = open('merged_youbike_list.json', 'r')
# load the file as json and convert to the structure formed by dictionary and list
alldata = json.load(fjson)


# In[12]:

## Try to study the data store in alldata

print type(alldata)
# print alldata[0]
print type(alldata[0])
print len(alldata)
print len(alldata[0])


# In[13]:

# print out all timestamp of the first bicycle site
for tdata in alldata[:10]:
    print tdata[0]['mday']


# ## REVIEW: Accumulate sbi

# In[14]:

sbi_list = []
for tdata in alldata:
    sbisum = 0
    for site in tdata:
        sbisum += int(site['sbi'])
    sbi_list.append(sbisum)
print sbi_list[:10]


# ## REVIEW: Appending data to the tail of a list
# * 把資料附加在list尾端

# In[15]:

alist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
blist = []
for a in alist:
    if a%2 == 0:
        blist.append(a)
print blist


# ## VISUALIZATON
# * QUERY "python plot" and get the first result http://matplotlib.org/
# * "MONKEY SEE, MONKEY DO!" Observe from the belows
#     * http://matplotlib.org/examples/lines_bars_and_markers/fill_demo.html
#     * http://matplotlib.org/1.4.1/users/pyplot_tutorial.html
# * The essential parts of most plot function
#     * import a package to plot
#     * Send __list__ to plot()
#     * show() it

# In[16]:

# NOW plot the sbi sequence
get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
plt.plot(sbi_list)
plt.show()
plt.close()


# In[19]:

# Rescale the x-axis to 0~24 hours
# %matplotlib inline
import matplotlib.pyplot as plt
# alist = [1, 3, 2, 4, 1, 3, 2, 4, 1, 3, 1, 3, 2, 3, 2, 4, 2, 4, 1, 3, 24, 1, 3, 24]
xlist = []
for i in range(288):
    ## i/12.0 can rescale the data to 24 hours because each hour has 12 data
    xlist.append(i/12.0)
# plt.plot(sbi_list)
plt.plot(xlist, sbi_list)
plt.show()
# plt.close()


# ## Calculating mean and std of each sites' sbi and plot it!
# * 現在我的目標是計算每一個腳踏車站在一天裡面腳踏車數的平均和標準差，我希望藉此知道，哪些腳踏車站是變化量大的，哪些腳踏車站是變化量小的。最好我還能夠知道，那個腳踏車站一共有多少個腳踏車，這樣我就可以知道，腳踏車數和平均、標準差是否有相關性。要怎麼做？
# * 計算平均和標準差是利用numpy.mean(alist)和numpy.std(alist)
# * 所以我要計算每個站自己的sbi平均和標準差，顯然第一件事是，我要能把每個腳踏車站在這288個時間點內的所有sbi資料存下來。
# * 所以我決定造一個對應，把每個站對應到他的sbi list。

# In[28]:

import numpy
sna2sbis = {}
for tdata in alldata:
    for site in tdata:
        sna2sbis.setdefault(site['sna'], [])
        sna2sbis[site['sna']].append(int(site['sbi']))

totdict = {}
for site in alldata[0]:
    totdict[site['sna']] = int(site['tot'])


# In[23]:

# Build a dictionary mapping sna to a list of sbis of 288 timestamp
sna2sbis = {}
for tdata in alldata:
    for site in tdata:
        sna2sbis.setdefault(site['sna'], [])
        sna2sbis[site['sna']].append(int(site['sbi']))
print len(sna2sbis)
for sna in sna2sbis:
    print sna, sna2sbis[sna]


# In[24]:

for sna in sna2sbis:
    plt.plot(xlist, sna2sbis[sna])


# In[39]:

# Build a dictionary mapping sna to tot(total number of bicycles there)
sna2tot = {}
for site in alldata[0]:
    sna2tot[site['sna']] =  int(site['tot'])
print len(sna2tot)


# ## Ploting as scatter
# * http://matplotlib.org/examples/shapes_and_collections/scatter_demo.html
#         import numpy as np
#         import matplotlib.pyplot as plt
#         N = 50
#         x = np.random.rand(N)
#         y = np.random.rand(N)
#         colors = np.random.rand(N)
#         area = np.pi * (15 * np.random.rand(N))**2 # 0 to 15 point radiuses
#
#         plt.scatter(x, y, s=area, c=colors, alpha=0.5)
#         plt.show()

# In[31]:

import numpy
meanlist = [] # each site's mean of sbi from 288 timestamps
stdlist = [] # each site's std of sbi from 288 timestamps
totlist = [] # each site's total number of parking slots
# colors = []
labels = []
for sna in sna2sbis:
    meanlist.append(numpy.mean(sna2sbis[sna]))
    stdlist.append(numpy.std(sna2sbis[sna]))
    totlist.append(totdict[sna]**2/10)
#     colors.append('#6666FF')
    labels.append(sna)
plt.scatter(meanlist, stdlist, s=totlist, c='blue', alpha=0.2)
plt.show()
plt.close()


# In[44]:

from matplotlib.font_manager import FontProperties
# font = FontProperties(fname=r"/library/Fonts/Microsoft/PMingLiU.ttf", size=12)
font = FontProperties(fname=r"data/PMingLiU.ttf", size=12)
fig = plt.figure(1, figsize=(16, 9) ,  facecolor='w')
plt.scatter(meanlist, stdlist, s=totlist, c='blue', alpha=0.1)
for x, y, l in zip(meanlist, stdlist, labels):
    plt.annotate(
        l, # the label
        xy=(x, y), # plot the lobel at (x, y)
        xytext=(0, -10), #
        textcoords='offset points',
        ha='center', # horizontal alignment
        va='top',  # vertical alignment
        fontproperties=font)

# plt.annotate(
#     u"這是我畫的圖", # the label
#     xy=(0, 10), # plot the lobel at (x, y)
#     xytext=(0, -100), #
#     textcoords='offset points',
#     ha='center', # horizontal alignment
#     va='top',  # vertical alignment
#     fontproperties=font)

plt.show()
plt.close()


# ## calculating pearson correlation among them
# * http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html

# In[47]:

import scipy
from scipy import stats
p = scipy.stats.pearsonr(meanlist, stdlist)
print p


# In[45]:

import scipy
from scipy import stats
r, p = scipy.stats.pearsonr(x, y)
print "%.4f\t%.4f"%(r, p)
r, p = scipy.stats.pearsonr(x, area)
print "%.4f\t%.4f"%(r, p)
r, p = scipy.stats.pearsonr(y, area)
print "%.4f\t%.4f"%(r, p)
# print r, p = scipy.stats.pearsonr(x, y)


# ## Python unicode support
# * http://python.ez2learn.com/basic/unicode.html

# In[51]:

# print sna2sbis.items()[0]
print sna2sbis[u'丹鳳派出所']


# ## Reshape the list

# In[62]:

A = sna2sbis[u'丹鳳派出所']
for i, d in enumerate(numpy.reshape(A, (-1, 12))):
    print i, d


# ## Define functional block

# In[69]:

def site_query(sitename):
    A = sna2sbis[sitename]
    for i, d in enumerate(numpy.reshape(A, (-1, 12))):
        print i, d


# In[70]:

site_query(u'國立政治大學')


# In[72]:

site_query(u'羅斯福新生南路口')


# In[73]:

# for sna in sna2sbis:
#     print sna


# In[74]:

site_query(u'臺大資訊大樓')


# In[75]:

site_query(u'捷運科技大樓站')


# # Case: Chrome history
# * 這個案例的目的是為了讓你
#     1. 複習以更熟悉dictionary、list的操作
#     2. 處理程式中的時間
#     3. 處理程式中的文字
#     4. 了解程式和網頁間的關係，並進行視覺化
