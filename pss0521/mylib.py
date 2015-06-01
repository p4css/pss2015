import xlrd
def XLS2List(fname, sheetname):
    outlist = []
    bk = xlrd.open_workbook(fname)
    try:
        sh = bk.sheet_by_name(sheetname)
    except:
        print "no sheet in %s named data" % fname
    print "nrows %d, ncols %d" % (sh.nrows, sh.ncols)
    if sh.ncols==1:
        for rownum in range(sh.nrows):
            outlist.append(sh.cell_value(rownum, 0))
    else:
        for rownum in range(sh.nrows):
            temp = []
            for colnum in range(sh.ncols):
                temp.append(sh.cell_value(rownum, colnum))
            outlist.append(temp)
    return outlist