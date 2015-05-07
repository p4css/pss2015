
# coding: utf-8


import sqlite3
# import urlparse
# import datetime


conn=sqlite3.connect("History")
# conn=sqlite3.connect("../../log_ChromeHistory/History")
cu = conn.cursor()


def query(sql):
    cu.execute(sql)
    result=cu.fetchall()
    print "[COMMAND(num_of_res=%d)]:%s"%(len(result), sql)
    return result


res = query("select visit_count, url from urls order by visit_count;")
print res[:1]

#import numpy
#def mydistance(x1, x2, y1, y2):
#    return numpy.sqrt((x1-x2)**2 + (y1-y2)**2)
#print mydistance(1.3, 5.3, 2.6, 5.6)
#alist = sorted(inlist)
## ##3.6 Query the visits table by the following sql
## * 用sql browser觀察visits這個表，發現表中的url欄位儲存的不是真正的網址，而只有儲存網址的id。
## * 而這個id，要對應到urls這個資料表的id欄位，才可以查出他所對應到的網址是什麼（urls中的url欄位）。所以要寫一道sql的查詢指令，"INNER JOIN"兩個表（你在這邊不需要知道INNER JOIN是什麼，只要你知道下面這道指令的意思就好了）。
##         SELECT urls.url, visits.visit_time, visits.visit_duration, visits.id, visits.from_visit, visits.transition, visits.segment_id, urls.id FROM visits INNER JOIN urls ON visits.url=urls.id;
## * 如果你想更瞭解SQL指令，可以參閱w3school上的說明。w3school SQL Introduction http://www.w3schools.com/sql/sql_intro.asp。
#
## In[16]:
#
### TODO: Modify the following code by use of query function
## cu.execute("SELECT urls.url, visits.visit_time, visits.visit_duration FROM visits INNER JOIN urls ON visits.url=urls.id;")
## res=cu.fetchall()
#res = query("SELECT urls.url, visits.visit_time, visits.visit_duration FROM visits INNER JOIN urls ON visits.url=urls.id;")
#for url, t, d in res[:10]:
#    segments = url.split('/')
#    print t, d, segments[2]
#
#
## ##3.7 Convert timestamp to readable string
## * 針對這樣的結果，看似有一些手續要處理，第一個，取出網址的前段，第二個，轉換時間成為python讀得懂的格式，不然根本看不懂。
## * 這個看似整數的時間是網路處理時間的方法，為了讓python讀得懂這串數字是什麼，可以使用人家已經寫好的時間函式，把整數timestamp轉換為python datetime的方法可查詢"convert timestamp to datetime python"
##     * 獲得以下結果http://stackoverflow.com/questions/9744775/how-to-convert-integer-timestamp-to-python-datetime
##             >>> import datetime
##             >>> your_timestamp = 1331856000000
##             >>> date = datetime.datetime.fromtimestamp(your_timestamp / 1e3)
## * 因為該整數是以microsecond來累計，所以要除以1000，標準的做法是除以1e3。
## * duration也要轉，
#
## ## Report as HTML table
## * HTML TABLES http://www.w3schools.com/html/html_tables.asp
## * STEPS
##     1. open an html file and write data into html tables
##     2. using nbviewer [magic display to preview the html results](http://nbviewer.ipython.org/github/ipython/ipython/blob/1.x/examples/notebooks/Part%205%20-%20Rich%20Display%20System.ipynb)
##             from IPython.display import HTML
##             HTML('<iframe src=http://en.mobile.wikipedia.org/?useformat=mobile width=700 height=350></iframe>')
##     3. Apply [CSS style](http://www.w3schools.com/html/tryit.asp?filename=tryhtml_table_headings_left)
##             <head>
##             <style>
##             table, th, td {
##                 border: 1px solid black;
##                 border-collapse: collapse;
##             }
##             th, td {
##                 padding: 5px;
##             }
##             th {
##                 text-align: left;
##             }
##             </style>
## </head>
##     4. Apply [mouse hover (CSS Pseudo class) to change the background color of cell](http://stackoverflow.com/questions/19794433/change-font-color-and-background-in-html-on-mouseover)
##             td:hover
##             {
##                background-color:white
##             }
#
## In[20]:
#
#import urlparse
#import datetime
#
#
#epoch_start = datetime.datetime(1601,1,1) + datetime.timedelta(hours = 8)
#fhtml = open("table.html", 'w')
#fhtml.write(''' <head><link rel=stylesheet type="text/css" href="table.css"></head>
# <body><table>''')
#for url, t, d in res[:20]:
#    fhtml.write("<tr>")
#    urlhost = urlparse.urlparse(url).netloc # retrieve the first segment of url
#    dt = datetime.timedelta(microseconds = t) ## timestamp
#    duration = datetime.timedelta(microseconds = d) ## duration
#    fhtml.write("<td>%s</td>"%(epoch_start + dt))
#    fhtml.write("<td>%s</td>"%(duration))
#    fhtml.write("<td>%s</td>"%(urlhost))
#    fhtml.write("</tr>")
#fhtml.write("</table></body>")
#fhtml.close()
#from IPython.display import HTML
#HTML('<iframe src=table.html width=1024 height=568></iframe>')
#
#
## ##3.8 getTime() convert timestamp to python datatime
## * EXPECTED OUTPUT
##         2013-09-23 10:13:12.405427 0:00:04.763264 https://www.google.com.tw/search?q=ma&oq=ma&aqs=chrome..69i57j69i65j0j5j0.361j0&sourceid=chrome&ie=UTF-8
##         2013-09-23 10:13:15.839026 0:00:00 http://mail.google.com/
##         2013-09-23 10:13:15.839026 0:00:00 https://mail.google.com/
##         2013-09-23 10:13:16.831155 0:00:00 https://mail.google.com/mail/
##         2013-09-23 10:13:16.831155 0:00:00 https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1
#
## In[35]:
#
#def getTime(t, prop="duration"): # t:timestamp, prop:properties
#    epoch_start = datetime.datetime(1601,1,1) + datetime.timedelta(hours = 8)
#    dt = datetime.timedelta(microseconds = t)
#    if prop == "time":
#        return epoch_start + dt
#    return dt
#
#for url, t1, d1 in res[:10]:
#    print getTime(t1, "time").strftime('%Y/%m/%d %H:%M:%S'), getTime(d1).seconds, urlparse.urlparse(url).netloc
#
### Create a getTime() Convert the timestamp and duration
## getTime(t, 'time') --> convert to timestamp
## getTime(t, 'duration') --> convert to duration
## timestamp = epoch_start + dt
## duration = dt
## urlhost = urlparse.urlparse(url).netloc
#
#
## ##3.9 parsed_res = parsed_res(res)
## * 原本每一筆資料為[str(url), int(timestamp), int(duration)]
##         "SELECT urls.url, visits.visit_time, visits.visit_duration FROM visits INNER JOIN urls ON visits.url=urls.id;"
## * 我現在希望把它儲存為[str(urlhost), datetime(start_time), datetime(end_time), datetime(duration)]變成四個值。
#
## In[42]:
#
#parsed_res = []
#for item in res: #url, timestamp, duraiton
#    urlhost = urlparse.urlparse(item[0]).netloc
#    start_time = getTime(item[1], "time")
#    duration = getTime(item[2])
#    end_time = start_time + duration
#    parsed_res.append([urlhost, start_time, end_time, duration])
#
## function, original res to parsed res
## parsed_res = []
## for item in res:
##     urlhost = urlparse.urlparse(item[0]).netloc
##     parsed_res.append([urlhost, getTime(item[1]), getTime(item[2], "duration")])
#
#
## In[41]:
#
### Print parsed_res in specified format or in seconds
#for item in parsed_res[:30]:
#    print "%s\t%s\t%s\t%s"%(item[1].strftime('%Y-%m-%d %H:%M:%S'),
#                            item[2].strftime('%Y-%m-%d %H:%M:%S'),
#                            item[3].seconds,
#                            item[0])
#
#
## ##3.10 Merge adjacent visits
## * 由於前述的結果，有太多mail或者talkgadget是相同的服務，我希望前後如果一樣的話，就把他銜接起來。
#
## In[54]:
#
#print "VISITS BEFORE MERGE:%d"%(len(parsed_res))
#merged_visits = []
#uniq_url = None
#for visit in parsed_res: #urlhost, stime, etime, duration
#    if uniq_url != visit[0]:
#        uniq_url = visit[0]
#        merged_visits.append([uniq_url, visit[1], visit[2], visit[3]])
#    else:
#        if visit[1] - merged_visits[-1][2] > getTime(300000000):
#            merged_visits.append([uniq_url, visit[1], visit[2], visit[3]])
#        else:
#            try:
#                merged_visits[-1][2] = visit[2]
#                merged_visits[-1][3] = visit[2] - merged_visits[-1][1]
#            except:
#                print merged_visits[-1]
#print "VISITS BEFORE MERGE:%d"%(len(merged_visits))
#
#
## In[51]:
#
#print "VISITS BEFORE MERGE:%d"%(len(parsed_res))
#merged_visits = []
#uniq_url = None
#for visit in parsed_res: #urlhost, stime, etime, duration
#    if uniq_url != visit[0]:
#        uniq_url = visit[0]
#        merged_visits.append([uniq_url, visit[1], visit[2], visit[3]])
#    else:
#        try:
#            merged_visits[-1][2] = visit[2]
#            merged_visits[-1][3] = visit[2] - merged_visits[-1][1]
#        except:
#            print merged_visits[-1]
#print "VISITS BEFORE MERGE:%d"%(len(merged_visits))
#
#
## In[55]:
#
#for v in merged_visits[:20]:
#    print v[1], v[3].seconds, v[0]
#
#
## ##3.10.1 Filter in neccesary entry
## * 有了merged_visits後，我現在希望的是只留下某些我所要觀察的項目，例如我只想觀察使用者使用facebook、mail、youtube的情形，那要怎麼抓出來？
## * 所以我現在要把merged_visits轉成filtered_visits。
#
## In[58]:
#
#filtered_visits = []
#filter_in = ['dropbox', 'dictionary', 'facebook', 'mail', 'youtube', 'comic', 'dm5', 'mobile01']
#for row in merged_visits:
##     counter = 0
##     for word in filter_in:
##         if word in row[0]:
##             counter += 1
##     if counter > 0:
##         filtered_visits.append(row)
#    if len([word for word in filter_in if word in row[0]])>0: ## LIST COMPREHENSION
#        filtered_visits.append(row)
## for item in inlist:
##     if len([x for x in filter_in if x in item[0]])>0:
##         res.append(item)
#
#
## In[61]:
#
#print len(filtered_visits)
#print "%s\t%-14s\t%s\t%-10s"%('date', 'time', 'duration', 'url')
#
### how to print date only?
#for r in filtered_visits[:30]:
#    print "%s\t%-14s\t%s\t%-10s"%(r[1], r[2],  r[3], r[0])
#
#
## ### First try of using Pandas
## * Tutorials http://cloga.info/python/%E6%95%B0%E6%8D%AE%E7%A7%91%E5%AD%A6/2013/09/17/pandas_intro/
#
## In[63]:
#
#import pandas as pd
## df = pd.DataFrame(filtered_visits)
#df = pd.DataFrame(merged_visits) ## convert list to pandas dataframe format
#df.head() ## print the first 5 data for example
#
#
## In[65]:
#
#df.describe()
#
#
## ##3.11 Convert the time to specified string format
#
## In[67]:
#
## print filtered_visits[0]
#for r in filtered_visits[:20]:
##     print "%s\t%s\t%s\t%s"%(r[0], r[1].isoformat(), r[2].isoformat(), r[3].seconds)
#    print "%s\t%s\t%s\t%s"%(r[1].strftime('%Y-%m-%d %H:%M:%S'), r[2].strftime('%Y-%m-%d %H:%M:%S'), r[3].seconds, r[0])
#
#
## In[6]:
#
### Save the result to a filtered_table.html and display it!!
## ftable = file("visit_table.html", 'w')
## ## "WRITE SOMETHING INTO FILE"
## ftable.write("WRITE SOMETHING INTO FILE")
## ftable.close()
## HTML('<iframe src=visit_table.html width=700 height=350></iframe>')
#
#
## ## Report timeline
#
## In[69]:
#
#def report(vlist, fname):
#    fout=file(fname, 'w')
#    fout.write('''
#<script type="text/javascript" src="https://www.google.com/jsapi?autoload={'modules':[{'name':'visualization',
#       'version':'1','packages':['timeline']}]}"></script>
#<script type="text/javascript">
#
#google.setOnLoadCallback(drawChart);
#function drawChart() {
#
#  var container = document.getElementById('example5.1');
#  var chart = new google.visualization.Timeline(container);
#  var dataTable = new google.visualization.DataTable();
#  dataTable.addColumn({ type: 'string', id: 'Room' });
#  dataTable.addColumn({ type: 'string', id: 'Name' });
#  dataTable.addColumn({ type: 'date', id: 'Start' });
#  dataTable.addColumn({ type: 'date', id: 'End' });
#  dataTable.addRows([
#    ''')
#    for v in vlist:
#        fout.write('["%s", "%s", new Date(0,0,0,%d,%d,%d), new Date(0,0,0,%d,%d,%d)],\n'%(v[1].strftime('%Y-%m-%d'), v[0], v[1].hour, v[1].minute, v[1].second, v[2].hour, v[2].minute, v[2].second))
#    fout.write('''
#        ]);
#  var options = {
#      colors:['#33ccff', '#ff66cc', '#339933','#ffcc33','#ff0000', '#333333', '#996600'],
#    timeline: { rowLabelStyle: {fontName: 'Helvetica', fontSize: 24, color: '#603913' },
#                barLabelStyle: { fontName: 'Garamond', fontSize: 14 } }
#  };
#  chart.draw(dataTable, options);
#}
#</script>
#<div id="example5.1" style="width: 3900px; height: 1000px;"></div>
#    ''')
#    fout.close()
#
#
## In[73]:
#
#report(filtered_visits[120:320], "viz.html")
#HTML('<iframe src=viz.html width=700 height=350></iframe>')
#
#
## # Reference
#def getTime(timestamp, pivot="time"):
#    newtime = str(timestamp)
#    stripped1 = newtime.strip(' (),L')
#    ms = int(stripped1)
#    delta = datetime.timedelta(microseconds = ms)
#    epoch_start = datetime.datetime(1601,1,1) + datetime.timedelta(hours = 8)
#    if pivot=="duration":
#        return delta
#    else:
#        return epoch_start + delta# Query a table
## def show_table(cu, name="%"):
##     sql="SELECT * FROM sqlite_master WHERE type='table' and name like '%s';"%(name)
##     return query(cu, sql)
## tb = show_table(cu) # return all table
## tb = show_table(cu, 'urls') # return table with name like urlsdef get_transition(transition):
#    code = 0xff
#    transition = code & transition
#
#    flag=""
#    if transition==0:
#        flag = "CLICK_LINK"     ##"LINK: User reached page by clicking a link on another page"
#    elif transition==1:
#        flag = "TYPE_URL"       ##"TYPED: User typed page in URL bar"
#    elif transition==2:
#        flag = "AUTO_BOOKMARK"  ##"AUTO BOOKMARK: User got to this page through a suggestion in the UI"
#    elif transition==3:
#        flag = "AUTO_SUBFRAME"  ##"AUTO SUBFRAME: Content automatically loaded in a non-toplevel frame"
#    elif transition==4:
#        flag = "MANU_SUBFRAME"  ##"MANUAL SUBFRAME: Subframe navigation explicitly requested by the user"
#    elif transition==5:
#        flag = "GENERATED"      ##"GENERATED: User typed page in the URL bar and selected an entry that did not look like a URL"
#    elif transition==6:
#        flag = "START PAGE"     ##"START PAGE: Page was specified in the command line or is the start page"
#    elif transition==7:
#        flag = "FORM SUBMIT"    ##"FORM SUBMIT: User filled out values in a form and submitted it"
#    elif transition==8:
#        flag = "RELOAD"         ##"RELOAD: User reloaded the page"
#    elif transition==9:
#        flag = "KEYWORD"        ##"KEYWORD: URL generated from a replaceable keyword other than the default search provider"
#    elif transition==10:
#        flag = "KEYWORD GENERATED"  ##"KEYWORD GENERATED: Visit was generated by a keyword"
#    else:
#        flag = "UNKNOW"          ##"Unable to understand the transition value. Check, something is horribly wrong here :"
#    return flag# def top_n_url2(cu, n=None, sql="select url,visit_count from urls order by url ;"):
##     res = query(cu, sql)
##     uniq_res = {}
##     for item in res:
## #         urlseg = item[0].split('/')
## #         print urlseg[2]
##         urlhost = urlparse.urlparse(item[0]).netloc   # for getting host from url
##         uniq_res.setdefault(urlhost, 0)
##         uniq_res[urlhost] += item[1]
##     res_list = uniq_res.items()
##     res_list.sort(key=lambda x:x[1],reverse=True)
##     for r in res_list[:10]:
##         print r
##     return res_list[:n]
## res = top_n_url2(cu, 10)ftable = file("visit_table.html", 'w')
#ftable.write('''<html><body>
#<style>
#td:hover
#{
#   background-color:yellow
#}
#table, th, td {
#    border: 1px solid black;
#    border-collapse: collapse;
#}
#th, td {
#    padding: 5px;
#}
#th {
#    text-align: left;
#}
#</style>
#<table>
#''')
#for r in filtered_visits[:20]:
#    ftable.write('''<tr>''')
#    ftable.write('''<td>%s</td>'''%(r[1].strftime('%Y-%m-%d %H:%M:%S')))
#    ftable.write('''<td>%s</td>'''%(r[2].strftime('%Y-%m-%d %H:%M:%S')))
#    ftable.write('''<td>%s</td>'''%(r[3].seconds))
#    ftable.write('''<td>%s</td>'''%(r[0]))
#    ftable.write('''</tr>''')
#ftable.write('''</table></body></html>''')
#ftable.close()
#from IPython.display import HTML
#HTML('<iframe src=visit_table.html width=700 height=350></iframe>')# import json
## fvisit = open("visits.json", 'w')
## json.dump(res[:1000], fvisit)
## fvisit.close()
## fopen = open("visits.json", 'r')
## res = json.load(fopen)
## print len(res)def getPeriod(vlist, s, e):
#    startTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
#    endTime = datetime.datetime.strptime(e, "%Y-%m-%d %H:%M:%S")
#    rlist=[]
#    for v in vlist:
#        if startTime < v[1] < endTime:
#            if v[1].day != v[2].day:
#                dayend = datetime.datetime.strptime(v[1].strftime('%Y-%m-%d')+" 23:59:59", "%Y-%m-%d %H:%M:%S")
#                nextday = datetime.datetime.strptime(v[2].strftime('%Y-%m-%d')+" 00:00:00", "%Y-%m-%d %H:%M:%S")
##                 rlist.append([v[0], v[1], dayend, dayend-v[1]])
##                 rlist.append([v[0], nextday, v[2], v[2]-nextday])
#            else:
#                rlist.append(v)
#    return rlist
##         if v[1] > v[2]:
##             print v[1].day, v[2].day, v[1].strftime('%Y-%m-%d %H:%M:%S'), v[2].strftime('%Y-%m-%d %H:%M:%S')
##         else:
