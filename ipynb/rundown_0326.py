
# coding: utf-8

# # REVIEW
# ## What you have known
# * All list operations: creating, accessing, methods for list including len(), enumerate(), append(), sorted()
# * All dictionary operations: 
# 
# ## Skils
# * for-each in for-each to access a __two dimensional__ list 
# 
# ## Case study
# * Short questions: Couting fruits, validating Y/M/D
# * Youbike
#     * 計算總腳踏車數
#     * 計算每個行政區的腳踏車數
#     * 計算總腳踏車數的變化
#     * 繪製總腳踏車數的變化的曲線圖
#     * 找出哪個腳踏車站有大幅度的曲線變化
#     * 判斷每個腳踏車站的全滿時刻
# * NEXT CASE STUDIES
#     * Chrome History
#     * Twitter API and nytime API
#     * Crawling news from ettoday
#     * Parsing news of apple news

# # Revewing list

# In[2]:

alist = [1, 3, 5, 7, 9]
blist = [12, 44, 6, 18, 10]
print len(alist)
print sorted(blist)
print enumerate(alist)
for b in blist:
    alist.append(b)
for i, a in enumerate(alist):
    print i, a


# In[3]:

# OTHER LIST FUNCTIONS LIST EXTENSION 
alist.extend(blist) # merge two lists
alist = alist + blist # also be able to merge two lists
print alist


# ## Create a new empty list
# 

# In[4]:

import urllib2
import json
response = urllib2.urlopen('http://opendata.dot.taipei.gov.tw/opendata/gwjs_cityhall.json')
data = json.load(response)
# initialize a list
sbi_list = [] 

for site in data['retVal']:
    sbi_list.append([int(site['sbi']), site['sna'], site['tot']])

# Print out the outcome
for k, v, i in sorted(sbi_list, reverse=True)[1:-1]:
    print k, i, v
# for site in data['retVal']:
#     sbi_list.append([int(site['sbi']), site['sna']])
# for k, v in sorted(sbi_list, reverse=True):
#     print k, v


# # Reviewing Dictionary

# In[5]:

#Accessing dictionary
adict = {1:2}
adict[3]=4
adict[5]=6
adict[7]=8
adict[9]=10
print adict
print adict.items()
print adict.keys()
print adict.values()
print len(adict)


# In[6]:

print list(adict)
print [[k, v] for k, v in adict.items()]


# In[7]:

for a in adict:
    print a, adict[a]
for b, value in adict.items():
    print b, value


# In[8]:

# Create a dictionary mapping sitename to other data
sitedict = {}


# #Youbike(cont.)
# * 目前你應該已經知道如何印出list/dictionary中的資料，且能夠操作（加總）其中的資料。
# * 可是我們要這資料的目的，通常不僅是要知道現在他有多少腳踏車，通常希望能夠知道，在一天內的車輛數變化（所有、每個站台），包含變化的趨勢、變化量、平均台數等等。這時候你會需要把所有的資料抓下來，並且處理。底下為一個已經處理完的資料。

# In[9]:

## list operations - append
alist = [1, 3, 2, 4, 5, 6, 7, 8, 1, 2, 3, 4, 2, 4, 2]
b = []
for a in alist:
    if a%2 == 0:
        b.append(a)
print b 


# ## Convert data structure
# * 目前的資料結構是，一個list裡面，包含著288筆循序資料。每一筆資料是某個時間的全台北市腳踏車資料。
# * 目前你會的事情是，加總某一筆資料裡面全台北市未借出的腳踏車數量和總停車格數。
# * 現在我想解決的問題是，在這288個時間點內，全台北市用車的比例（SBI/TOT）。

# In[10]:

import urllib2
import json
response = urllib2.urlopen('http://opendata.dot.taipei.gov.tw/opendata/gwjs_cityhall.json')
data = json.load(response)


##------ THE BLOCK TO ACCUMULATE SBI AND TOT ----------
sbi, tot = 0, 0
for site in data['retVal']:
    sbi += int(site['sbi'])
    tot += int(site['tot'])
print sbi, tot
##-----------------------------------------------------


# ## Read content of json
# * 開啟檔案的函式：__file_name = open(FILE_PATH, MODE)__
#     * FILE_PATH為所要開啟檔案的路徑
#     * MODE可能是r、w、a、r+等諸模式 (See [file mode](https://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files))
# * __json.load(file_name)__
#     * 將所獲取的json檔案（無論是線上或者是本地端電腦），轉換為python可以使用者的dictionary或list。

# In[11]:

import json # You don't need to import it again, because you have imported it in the previous code.

# Open and read a file in your local machine
# 'r' means opening the file for reading, not for writing.
fjson = open('data/merged_youbike_list.json', 'r')
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


# In[1]:

# Rescale the x-axis to 0~24 hours
# %matplotlib inline
import matplotlib.pyplot as plt
alist = [1, 3, 2, 4, 1, 3, 2, 4, 1, 3, 1, 3, 2, 3, 2, 4, 2, 4, 1, 3, 24, 1, 3, 24]
# xlist = []
# for i in range(288):
#     ## i/12.0 can rescale the data to 24 hours because each hour has 12 data
#     xlist.append(i/12.0)
plt.plot(alist)
# plt.plot(xlist, sbi_list)
plt.show()
# plt.close()


# ## Calculating mean and std of each sites' sbi and plot it!
# * 現在我的目標是計算每一個腳踏車站在一天裡面腳踏車數的平均和標準差，我希望藉此知道，哪些腳踏車站是變化量大的，哪些腳踏車站是變化量小的。最好我還能夠知道，那個腳踏車站一共有多少個腳踏車，這樣我就可以知道，腳踏車數和平均、標準差是否有相關性。要怎麼做？
# * 計算平均和標準差是利用numpy.mean(alist)和numpy.std(alist)
# * 所以我要計算每個站自己的sbi平均和標準差，顯然第一件事是，我要能把每個腳踏車站在這288個時間點內的所有sbi資料存下來。
# * 所以我決定造一個對應，把每個站對應到他的sbi list。

# In[37]:

import numpy
sna2sbis = {}
for tdata in alldata:
    for site in tdata:
        sna2sbis.setdefault(site['sna'], [])
        sna2sbis[site['sna']].append(int(site['sbi']))

totdict = {}
for site in alldata[0]:
    totdict[site['sna']] = int(site['tot'])


# In[40]:

# Build a dictionary mapping sna to a list of sbis of 288 timestamp
sna2sbis = {}
for tdata in alldata:
    for site in tdata:
        sna2sbis.setdefault(site['sna'], [])
        sna2sbis[site['sna']].append(int(site['sbi']))
print len(sna2sbis)


# In[41]:

for sna in sna2sbis:
    plt.plot(sna2sbis[sna])


# In[ ]:




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

# In[54]:

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


# In[53]:

from matplotlib.font_manager import FontProperties
# font = FontProperties(fname=r"/library/Fonts/Microsoft/PMingLiU.ttf", size=12)
font = FontProperties(fname=r"data/PMingLiU.ttf", size=12)
fig = plt.figure(1,figsize=(16, 9) ,  facecolor='w')
plt.scatter(meanlist, stdlist, s=totlist, c='blue', alpha=0.1)
for x, y, l in zip(meanlist, stdlist, labels):
    plt.annotate(
        l,
        xy=(x, y),
        xytext=(0, -10),
        textcoords='offset points',
        ha='center',
        va='top', 
        fontproperties=font)
plt.show()
plt.close()


# ## calculating pearson correlation among them
# * http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html

# In[26]:

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

# In[60]:

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
