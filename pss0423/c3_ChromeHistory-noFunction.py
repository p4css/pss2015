
# coding: utf-8

import sqlite3
# import urlparse
# import datetime

# ##3.2 Connect to history sqlite file
# conn=sqlite3.connect("History")
conn=sqlite3.connect("../../log_ChromeHistory/History")
cu = conn.cursor()

# ##3.3 執行sql查詢（Send a sql query to cu）
import json
sql = "select visit_count, url from urls order by visit_count;"
cu.execute(sql)
res = cu.fetchall()
print "[COMMAND(num_of_res=%d)]:%s"%(len(res), sql)

# print res[:10]
fout = open("data.json", 'w')
json.dump(res, fout)
fout.close()
fin = open('data.json', 'r')
res = json.load(fin)
print res

for r in sorted(res, reverse=True)[:10]:
    print "%s\t%s"%(r[0], r[1])


# ## 3.4 網址的處理 Combine urls according to their hosts
# * 注意看下面query後的結果，顯然如果是mail.google.com開頭的網址，應該都算進mail.google.com就好，不要有那麼多個不一樣的網址。
#         874	http://mail.google.com/
#         654	https://www.facebook.com/
#         500	http://www.facebook.com/
#         429	https://mail.google.com/
#         407	https://mail.google.com/mail/
#         403	https://mail.google.com/mail/u/0/
#         292	https://mail.google.com/mail/u/0/#label/%5Bntnulib%5D
#         270	http://comic.sfacg.com/
#         255	http://www.yahoo.com.tw/
#         219	http://tw.yahoo.com/
# * 所以我現在希望能夠把前面開頭是mail.google.com的都算成是拜訪同一個網址，並且累計總共拜訪幾次。
# * 相當於要建一個dictionary 把網址前段mapping到出現次數的加總。
# * 而現在的問題是要怎麼把網址斷開？
# 
# ### 3.4.1 string operations
# * 各位是否還記得我們曾經看過一個程式如下，他用sentences.split()把所有的字通通斷開了。
#     1. 把所有的奇怪的字元刪除，包含
#         >!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
#             sentences = sentences.translate(None, string.punctuation)
#     2. 把所有的字轉小寫
#             sentences = sentences.lower()
#     3. 把要輸入的字串依照空白斷開
#             wordlist = sentences.split()
#     4. 用for-each讀取wordlist中的每一個word，看他出現幾次。

# In[13]:

import string
sentences = 'All men have stars, but they are not the same things for different people. For some, who are travelers, the stars are guides. For others they are no more than little lights in the sky. For others, who are scholars, they are problems... But all these stars are silent. You-You alone will have stars as no one else has them... In one of the stars I shall be living. In one of them I shall be laughing. And so it will be as if all the stars will be laughing when you look at the sky at night..You, only you, will have stars that can laugh! And when your sorrow is comforted (time soothes all sorrows) you will be content that you have known me... You will always be my friend. You will want to laugh with me. And you will sometimes open your window, so, for that pleasure... It will be as if, in place of the stars, I had given you a great number of little bells that knew how to laugh'
sentences = sentences.translate(None, string.punctuation)
sentences = sentences.lower()
# print sentences
words = sentences.split()
print words

worddict = {}
for word in words:
    if word not in worddict:
        worddict[word] = 0
#     worddict.setdefault(word, 0)
    worddict[word] += 1
print worddict.items()
## Introduce the split() function


# ### 3.4.2 split the url by "/"

# In[20]:

urlstr = 'https://mail.google.com/mail/u/0/#label/%5Bntnulib%5D'
urlstr = 'http://www.yahoo.com.tw/'
urlseq = urlstr.split('/')
print len(urlseq)
print urlseq[2]
# print urlseq[2]


# In[36]:

urldict = {}
## data[0]: frequency
## data[1]: original url
for data in res:
#     if "mailto" not in data[1]:
    segments = data[1].split('/')
#     if len(segments) > 2:
    try:
        urldict.setdefault(segments[2], 0)
        urldict[segments[2]] += data[0]
    except:
        print "ERROR: %s"%data[1]

resultlist = []
for url, freq in urldict.items():
    resultlist.append([freq, url])

for f, u in sorted(resultlist, reverse=True)[:20]:
    print f, '\t', u
    
#     print "%s\t%s"%(freq, url)
    
#     print data[0], segments[2]


# ### REVIEW
# * __string__ split
#         str1 = "jirlong hahaha"
#         segs = str1.split()
# * try and except
#         try:
#             #tried block
#         except:
#             # how will you handle the exception? or pass it!!
# * function

# ###3.4.3 combine urls according to the 1st segment of url
# * 下面我們將把/當成切割字串的工具，好獲得網址。
# * 但是你將會遇到一個問題，就是這些資料裡面有兩個資料並非你預期中的資料，這兩個資料是因為使用者從網頁上按了「寄送信件」的按鈕後，系統自動把網頁導引到寄送信件的頁面所產生。
#         mailto:jirlong@ntnu.edu.tw?bcc=96501054@nccu.edu.tw
#         mailto:jackho@ntnu.edu.tw
# * 總之會出錯，你有三種方法處理他
#     1. 知道有這種錯誤，所以排除他！（有mailto在item[0]的通通拿掉），但問題是你怎麼知道有他？
#     2. 偵測如果split()後的結果，長度大於2，代表至少有三個，那我才處理。
#     3. 用try和except。
# * EXPECTED RESULTS
#         ERROR ITEM:mailto:jackho@ntnu.edu.tw
#         ERROR ITEM:mailto:jirlong@ntnu.edu.tw?bcc=96501054@nccu.edu.tw
#         [4674, u'mail.google.com']
#         [3166, u'comic.sfacg.com']
#         [3076, u'www.google.com']
#         [1731, u'www.facebook.com']
#         [1295, u'www.youtube.com']
#         [907, u'moodle.ntnu.edu.tw']
#         [883, u'www.google.com.tw']
#         [764, u'tw.news.yahoo.com']
#         [570, u'coldpic.sfacg.com']
#         [551, u'docs.google.com']

# In[16]:

## combine urls according to the 1st segment of url
url_dict = {}
for item in res:
    urlseg = item[1].split('/')
    url_dict.setdefault(urlseg[2], 0)
    url_dict[urlseg[2]] += item[0]
## But you will encounter an unexpected data entry such as "mailto:jirlong@ntnu.edu.tw?bcc=96501054@nccu.edu.tw"

## swap the column for next step sorting (STORED TO A NEW res_list)
res_list = []

## print the sorted result


# ##3.5 Convert the block of database query to a function
# * 因為下面這兩行常常會用到，不如把它轉成一個「功能性的區塊」，就是function。
#         cu.execute(sql)
#         res=cu.fetchall()
# * y = func(a, b) = sqrt(axa + bxb)
#     * y稱為傳回值 return value
#     * a, b為傳入函式的值。
#     * func(a, b) = sqrt(axa + bxb) 稱為func函式的定義。
# * 函式的定義大致如下
#         ## Define a function
#         def function_name(invalue1, invalue2, invalue3):
#             result1, result2 = 0, 0
#             ## Add some processing here
# 
#             return result1, result2
# * 目前希望的是能夠用下面的方式進行查詢，程式碼會變得比較簡單。
#         res = query("select url,visit_time, from_visit, transition, visit_duration from visits order by id ;") 
#         res = query("SELECT visits.id, visits.visit_time, visits.visit_duration, urls.url FROM visits INNER JOIN urls ON visits.url=urls.id;")
# * 而目前有的送出查詢的程式碼如下
#         cu.execute(sql)
#         res=cu.fetchall()
#         print "[COMMAND(num_of_res=%d)]:%s"%(len(res), sql)      
# 

# In[53]:

## TODO: Define a query function here
def query(sql):
    cu.execute(sql)
    result=cu.fetchall()
    print "[COMMAND(num_of_res=%d)]:%s"%(len(result), sql)
    return result


# In[54]:

## Call a query function
res = query("select visit_count, url from urls order by visit_count;")
print res[:1]


# In[52]:

import numpy
def mydistance(x1, x2, y1, y2):
    return numpy.sqrt((x1-x2)**2 + (y1-y2)**2)
print mydistance(1.3, 5.3, 2.6, 5.6)
alist = sorted(inlist)


# ##3.6 Query the visits table by the following sql
# * 用sql browser觀察visits這個表，發現表中的url欄位儲存的不是真正的網址，而只有儲存網址的id。
# * 而這個id，要對應到urls這個資料表的id欄位，才可以查出他所對應到的網址是什麼（urls中的url欄位）。所以要寫一道sql的查詢指令，"INNER JOIN"兩個表（你在這邊不需要知道INNER JOIN是什麼，只要你知道下面這道指令的意思就好了）。
#         SELECT urls.url, visits.visit_time, visits.visit_duration, visits.id, visits.from_visit, visits.transition, visits.segment_id, urls.id FROM visits INNER JOIN urls ON visits.url=urls.id;
# * 如果你想更瞭解SQL指令，可以參閱w3school上的說明。w3school SQL Introduction http://www.w3schools.com/sql/sql_intro.asp。

# In[67]:

## TODO: Modify the following code by use of query function
# cu.execute("SELECT urls.url, visits.visit_time, visits.visit_duration FROM visits INNER JOIN urls ON visits.url=urls.id;")
# res=cu.fetchall()
res = query("SELECT urls.url, visits.visit_time, visits.visit_duration FROM visits INNER JOIN urls ON visits.url=urls.id;")
## TODO: PRINT OUT THE QUERY


for url, t, d in res[:10]:
    segments = url.split('/')
    print t, d, segments[2]
#     print t, d, url


# In[64]:

import json
fvisit = open("visits.json", 'w')
json.dump(res[:1000], fvisit)
fvisit.close()



# In[65]:

import json
fopen = open("visits.json", 'r')
res = json.load(fopen)
print len(res)


# ##3.7 Convert timestamp to readable string
# * 針對這樣的結果，看似有一些手續要處理，第一個，取出網址的前段，第二個，轉換時間成為python讀得懂的格式，不然根本看不懂。
# * 這個看似整數的時間是網路處理時間的方法，為了讓python讀得懂這串數字是什麼，可以使用人家已經寫好的時間函式，把整數timestamp轉換為python datetime的方法可查詢"convert timestamp to datetime python"
#     * 獲得以下結果http://stackoverflow.com/questions/9744775/how-to-convert-integer-timestamp-to-python-datetime
#             >>> import datetime
#             >>> your_timestamp = 1331856000000
#             >>> date = datetime.datetime.fromtimestamp(your_timestamp / 1e3)
# * 因為該整數是以microsecond來累計，所以要除以1000，標準的做法是除以1e3。
# * duration也要轉，
13024375992405427 4763264 www.google.com.tw
13024375995839026 0 mail.google.com
13024375995839026 0 mail.google.com
13024375996831155 0 mail.google.com
13024375996831155 0 accounts.google.com
13024376003875352 118716769 accounts.google.com
13024376004883494 0 mail.google.com
13024376004883494 0 mail.google.com
13024376004883494 0 mail.google.com
13024376006908314 0 mail.google.com
# In[72]:

for url, t, d in res[:10]:
    segments = url.split('/')
    print t, d, segments[2]
t = t/1000000
sec = t%60
print sec


# In[85]:

import urlparse
import datetime

epoch_start = datetime.datetime(1601,1,1) + datetime.timedelta(hours = 8)
# <table style="width:100%">
#   <tr>
#     <td>Jill</td>
#     <td>Smith</td> 
#     <td>50</td>
#   </tr>
# </table>

fhtml = open("table.html", 'w')
fhtml.write(''' <head>
 <style>
 table, th, td {
     border: 1px solid black;
     border-collapse: collapse;
 }
 th, td {
     padding: 5px;
 }
 th {
     text-align: left;
 }
 td:hover
 {
    background-color:yellow
 }
 </style><body>''')
fhtml.write("<table>")
for url, t, d in res[:50]:
    fhtml.write("<tr>")
    # retrieve the first segment of url
    urlhost = urlparse.urlparse(url).netloc
    dt = datetime.timedelta(microseconds = t) ## timestamp
    duration = datetime.timedelta(microseconds = d) ## duration
#     fhtml.write("<td>%s</td><td>%s</td><td>%s</td>"%(epoch_start + dt, duration, urlhost))
    fhtml.write("<td>%s</td>"%(epoch_start + dt))
    fhtml.write("<td>%s</td>"%(duration))
    fhtml.write("<td>%s</td>"%(urlhost))
    fhtml.write("</tr>")

fhtml.write("</table></body>")
fhtml.close()
    # convert integer time stamp to datetime
#     print r[1]
#     if r[2] != 0.0:
#         dt = datetime.timedelta(microseconds = r[1]) 
#         duration = datetime.timedelta(microseconds = r[2])
#         print urlhost, epoch_start+dt, duration


# ##3.8 getTime() convert timestamp to python datatime
# * EXPECTED OUTPUT
#         2013-09-23 10:13:12.405427 0:00:04.763264 https://www.google.com.tw/search?q=ma&oq=ma&aqs=chrome..69i57j69i65j0j5j0.361j0&sourceid=chrome&ie=UTF-8
#         2013-09-23 10:13:15.839026 0:00:00 http://mail.google.com/
#         2013-09-23 10:13:15.839026 0:00:00 https://mail.google.com/
#         2013-09-23 10:13:16.831155 0:00:00 https://mail.google.com/mail/
#         2013-09-23 10:13:16.831155 0:00:00 https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1

# In[27]:

## TODO: CONVERT THE PREVIOUS CODE TO A getTime() FUNCTION


# In[84]:

for r in res[:40]:
#     if r[2] != 0.0:
    print getTime(r[1]), getTime(r[2], 'duration'), r[0]


# ##3.9 res to parsed_res: Covert time, duration, host, ...

# In[45]:

cu.execute("SELECT urls.url, visits.visit_time, visits.visit_duration, visits.id, visits.from_visit, visits.transition, visits.segment_id, urls.id FROM visits INNER JOIN urls ON visits.url=urls.id;")
res=cu.fetchall()
parsed_res = []
for item in res:
    urlhost = urlparse.urlparse(item[0]).netloc
    parsed_res.append([urlhost, getTime(item[1]), getTime(item[2], "duration")])


# In[85]:

for v in parsed_res[:30]:
    print "%s\t%s\t%s"%(v[1].strftime('%Y-%m-%d %H:%M:%S'), 
                            v[2].seconds,
                            v[0])


# ##3.10 Merge adjacent visits
# * 由於前述的結果，有太多mail或者talkgadget是相同的服務，我希望前後如果一樣的話，就把他銜接起來。

# In[91]:

print "VISITS BEFORE MERGE:%d"%(len(parsed_res))
merged_visits = []
uniq_url = None
for visit in parsed_res:
    if uniq_url != visit[0]:
        uniq_url = visit[0]
        merged_visits.append([uniq_url, visit[1], visit[1]+visit[2], visit[2]])
    else:
        try:
            merged_visits[-1][2] = visit[1]+visit[2]
            merged_visits[-1][3] = visit[1] - merged_visits[-1][1] + visit[2]
        except:
            print merged_visits[-1]
print "VISITS BEFORE MERGE:%d"%(len(merged_visits))


# In[18]:

for v in merged_visits[:20]:
    print v[1], v[3], v[0]


# ##3.10.1 Filter out unneccesary or Filter in neccesary entry

# In[59]:

def visitfilter(inlist, FILTER=None, DEL=False):
    res = []
    filter_in = ['dropbox', 'dictionary', 'facebook', 'mail', 'youtube', 'toasty', 'comic', 'dm5', 'mobile01']
    filter_out = ['account', 'ftp', 'itc']
    if FILTER == None:
        return inlist
    if FILTER == "Exclude":
        for item in inlist:
            if len([x for x in filter_out if x in item[0]])==0:
                res.append(item)
    if FILTER == "Include":
        for item in inlist:
            if len([x for x in filter_in if x in item[0]])>0:
                res.append(item)
    return res


# In[106]:

filtered_visits = visitfilter(merged_visits, None) ##FILTER = Exclude, Include, or None
print len(filtered_visits)
print "%s\t%-14s\t%s\t%-10s"%('date', 'time', 'duration', 'url')
for r in filtered_visits[:10]:
    print "%s\t%-14s\t%s\t%-10s"%(r[1], r[2],  r[3], r[0])


# ### First try of using Pandas
# * Tutorials http://cloga.info/python/%E6%95%B0%E6%8D%AE%E7%A7%91%E5%AD%A6/2013/09/17/pandas_intro/

# In[94]:

import pandas as pd
df = pd.DataFrame(filtered_visits)
df.head()


# In[98]:

df.describe()


# ##3.11 Convert the time to specified string format

# In[100]:

print filtered_visits[0]
for r in filtered_visits[:20]:
#     print "%s\t%s\t%s\t%s"%(r[0], r[1].isoformat(), r[2].isoformat(), r[3].seconds)
    print "%s\t%s\t%s\t%s"%(r[1].strftime('%Y-%m-%d %H:%M:%S'), r[2].strftime('%Y-%m-%d %H:%M:%S'), r[3].seconds, r[0])


# ## Report as HTML table
# * HTML TABLES http://www.w3schools.com/html/html_tables.asp
# * STEPS
#     1. open an html file and write data into html tables
#     2. using nbviewer [magic display to preview the html results](http://nbviewer.ipython.org/github/ipython/ipython/blob/1.x/examples/notebooks/Part%205%20-%20Rich%20Display%20System.ipynb)
#             from IPython.display import HTML
#             HTML('<iframe src=http://en.mobile.wikipedia.org/?useformat=mobile width=700 height=350></iframe>')
#     3. Apply [CSS style](http://www.w3schools.com/html/tryit.asp?filename=tryhtml_table_headings_left)
#             <head>
#             <style>
#             table, th, td {
#                 border: 1px solid black;
#                 border-collapse: collapse;
#             }
#             th, td {
#                 padding: 5px;
#             }
#             th {
#                 text-align: left;
#             }
#             </style>
# </head>
#     4. Apply [mouse hover (CSS Pseudo class) to change the background color of cell](http://stackoverflow.com/questions/19794433/change-font-color-and-background-in-html-on-mouseover)
#             td:hover
#             {
#                background-color:white
#             }

# In[19]:

ftable = file("visit_table.html", 'w')
## "WRITE SOMETHING INTO FILE"
ftable.write("WRITE SOMETHING INTO FILE")
ftable.close()
from IPython.display import HTML
HTML('<iframe src=visit_table.html width=700 height=350></iframe>')


# ## Report timeline

# In[20]:

def report(vlist, fname):
    fout=file(fname, 'w')
    fout.write('''
<script type="text/javascript" src="https://www.google.com/jsapi?autoload={'modules':[{'name':'visualization',
       'version':'1','packages':['timeline']}]}"></script>
<script type="text/javascript">

google.setOnLoadCallback(drawChart);
function drawChart() {

  var container = document.getElementById('example5.1');
  var chart = new google.visualization.Timeline(container);
  var dataTable = new google.visualization.DataTable();
  dataTable.addColumn({ type: 'string', id: 'Room' });
  dataTable.addColumn({ type: 'string', id: 'Name' });
  dataTable.addColumn({ type: 'date', id: 'Start' });
  dataTable.addColumn({ type: 'date', id: 'End' });
  dataTable.addRows([
    ''')
    for v in vlist:
        fout.write('["%s", "%s", new Date(0,0,0,%d,%d,%d), new Date(0,0,0,%d,%d,%d)],\n'%(v[1].strftime('%Y-%m-%d'), v[0], v[1].hour, v[1].minute, v[1].second, v[2].hour, v[2].minute, v[2].second))
    fout.write('''
        ]);
  var options = {
      colors:['#33ccff', '#ff66cc', '#339933','#ffcc33','#ff0000', '#333333', '#996600'],
    timeline: { rowLabelStyle: {fontName: 'Helvetica', fontSize: 24, color: '#603913' },
                barLabelStyle: { fontName: 'Garamond', fontSize: 14 } }
  };
  chart.draw(dataTable, options);
}
</script>
<div id="example5.1" style="width: 3900px; height: 1000px;"></div>
    ''')
    fout.close()


# ## Query entry during a period...

# In[70]:

def getPeriod(vlist, s, e):
    startTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    endTime = datetime.datetime.strptime(e, "%Y-%m-%d %H:%M:%S")
    rlist=[]
    for v in vlist:
        if startTime < v[1] < endTime:
            if v[1].day != v[2].day:
                dayend = datetime.datetime.strptime(v[1].strftime('%Y-%m-%d')+" 23:59:59", "%Y-%m-%d %H:%M:%S")
                nextday = datetime.datetime.strptime(v[2].strftime('%Y-%m-%d')+" 00:00:00", "%Y-%m-%d %H:%M:%S")
#                 rlist.append([v[0], v[1], dayend, dayend-v[1]])
#                 rlist.append([v[0], nextday, v[2], v[2]-nextday])
            else:
                rlist.append(v)
    return rlist
#         if v[1] > v[2]:
#             print v[1].day, v[2].day, v[1].strftime('%Y-%m-%d %H:%M:%S'), v[2].strftime('%Y-%m-%d %H:%M:%S')
#         else:


# In[107]:

rlist = getPeriod(merged_visits, "2013-12-01 00:00:00", "2015-01-01 00:00:00")
for r in rlist:
    print r
report(rlist, "viz.html")


# In[108]:

HTML('<iframe src=viz.html width=700 height=350></iframe>')


# # Reference
def getTime(timestamp, pivot="time"):
    newtime = str(timestamp)
    stripped1 = newtime.strip(' (),L')
    ms = int(stripped1)
    delta = datetime.timedelta(microseconds = ms)
    epoch_start = datetime.datetime(1601,1,1) + datetime.timedelta(hours = 8)
    if pivot=="duration":
        return delta
    else:
        return epoch_start + delta# Query a table
# def show_table(cu, name="%"):
#     sql="SELECT * FROM sqlite_master WHERE type='table' and name like '%s';"%(name)
#     return query(cu, sql)
# tb = show_table(cu) # return all table
# tb = show_table(cu, 'urls') # return table with name like urlsdef get_transition(transition):
    code = 0xff
    transition = code & transition

    flag=""
    if transition==0:
        flag = "CLICK_LINK"     ##"LINK: User reached page by clicking a link on another page"
    elif transition==1:
        flag = "TYPE_URL"       ##"TYPED: User typed page in URL bar"
    elif transition==2:
        flag = "AUTO_BOOKMARK"  ##"AUTO BOOKMARK: User got to this page through a suggestion in the UI"
    elif transition==3:
        flag = "AUTO_SUBFRAME"  ##"AUTO SUBFRAME: Content automatically loaded in a non-toplevel frame"
    elif transition==4:
        flag = "MANU_SUBFRAME"  ##"MANUAL SUBFRAME: Subframe navigation explicitly requested by the user"
    elif transition==5:
        flag = "GENERATED"      ##"GENERATED: User typed page in the URL bar and selected an entry that did not look like a URL"
    elif transition==6:
        flag = "START PAGE"     ##"START PAGE: Page was specified in the command line or is the start page"
    elif transition==7:
        flag = "FORM SUBMIT"    ##"FORM SUBMIT: User filled out values in a form and submitted it"
    elif transition==8:
        flag = "RELOAD"         ##"RELOAD: User reloaded the page"
    elif transition==9:
        flag = "KEYWORD"        ##"KEYWORD: URL generated from a replaceable keyword other than the default search provider"
    elif transition==10:
        flag = "KEYWORD GENERATED"  ##"KEYWORD GENERATED: Visit was generated by a keyword"
    else:
        flag = "UNKNOW"          ##"Unable to understand the transition value. Check, something is horribly wrong here :"
    return flag# def top_n_url2(cu, n=None, sql="select url,visit_count from urls order by url ;"):
#     res = query(cu, sql)
#     uniq_res = {}
#     for item in res:
# #         urlseg = item[0].split('/')
# #         print urlseg[2]
#         urlhost = urlparse.urlparse(item[0]).netloc   # for getting host from url
#         uniq_res.setdefault(urlhost, 0)
#         uniq_res[urlhost] += item[1]
#     res_list = uniq_res.items()
#     res_list.sort(key=lambda x:x[1],reverse=True)
#     for r in res_list[:10]:
#         print r
#     return res_list[:n]
# res = top_n_url2(cu, 10)ftable = file("visit_table.html", 'w')
ftable.write('''<html><body>
<style>
td:hover
{
   background-color:yellow
}
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
}
th {
    text-align: left;
}
</style>
<table>
''')
for r in filtered_visits[:20]:
    ftable.write('''<tr>''')
    ftable.write('''<td>%s</td>'''%(r[1].strftime('%Y-%m-%d %H:%M:%S')))
    ftable.write('''<td>%s</td>'''%(r[2].strftime('%Y-%m-%d %H:%M:%S')))
    ftable.write('''<td>%s</td>'''%(r[3].seconds))
    ftable.write('''<td>%s</td>'''%(r[0]))
    ftable.write('''</tr>''')
ftable.write('''</table></body></html>''')
ftable.close()
from IPython.display import HTML
HTML('<iframe src=visit_table.html width=700 height=350></iframe>')