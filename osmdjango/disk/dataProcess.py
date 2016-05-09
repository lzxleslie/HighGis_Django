#!/usr/bin/python  
#-*-coding:utf-8-*- 
import csv
import json
import  xdrlib ,sys
import xlrd

reload(sys)
sys.setdefaultencoding('utf-8')
def excel_table_byindex(file= 'dt.xlsx',colnameindex=0,by_index=0):
    try:
        data = xlrd.open_workbook(file)
    except Exception,e:
        print str(e)    
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    for rownum in range(1,nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i].encode('utf-8')] = row[i] 
        jsonlist=json.dumps(app,ensure_ascii = False)
        list.append(jsonlist)
    return list
def csvToJson(filepath):
    out = None;

    with open( filepath, 'r') as csvFile:
        #Note this reads the first line as the keys we can add specific keys with:
        #csv.DictReader( csvFile, fieldnames=<LIST HERE>, restkey=None, restval=None, )
        csvDict = csv.DictReader( csvFile, restkey=None, restval=None, )
        out = [obj for obj in csvDict]

    if out:
        return json.dumps( out );
    else:
        print "Error creating csv dict!"

def geojsonTo(filepath):
    jsonFile = open(filepath)
    stem = json.load(jsonFile)
    return json.dumps(stem, ensure_ascii=False)
        
def dataprocess(filepath):
    data=None
    if(filepath.split('.')[-1]=='csv'):
        data=csvToJson(filepath)
    elif(filepath.split('.')[-1]=='xlsx'or filepath.split('.')[-1]=='xls'):
        data=excel_table_byindex(filepath)
    elif(filepath.split('.')[-1] == 'geojson' or filepath.split('.')[-1] == 'json'):
        data = geojsonTo(filepath)
    return data