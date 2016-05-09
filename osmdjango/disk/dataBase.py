#!/usr/bin/python
#-*-coding:utf-8-*-
import psycopg2
import ogr2ogr
import dataProcess
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    conn = psycopg2.connect(database="gis_database", user="postgres", password="whu", host="localhost", port="5432")
except :
    print "unable to connect dataBase"
cur = conn.cursor()
def dataToPostGis(filepath,username,filename):
    staticPath = '/home/whu/projects/osmdjango/'
    filepath = os.path.join(staticPath, filepath)
    if (filename.split('.')[-1]=='xlsx'or filename.split('.')[-1]=='xls'):
        filename=filename.replace('.','_')
        # dataTableName=username+"_"+filename+"_db"
        dataTableName=username+"_"+filename
        cur.execute("drop table IF  EXISTS "+dataTableName)
        # cur.execute('CREATE TABLE IF NOT EXISTS '+dataTableName+'(id serial PRIMARY KEY,geom geometry(Point,4326));')
        cur.execute("create table IF NOT EXISTS "+dataTableName+"(id integer PRIMARY KEY,name varchar,lat numeric,lon numeric,division varchar,geom geometry(Point,3857));")
        data = dataProcess.dataprocess(filepath)
        for i in data:
            i=json.loads(i)
            id=i[u"编号"]
            value={"id":id,"name":i[u"区划"],"lon":i[u"经度"],"lat":i[u"纬度"],"division":i[u"标题"],"geoLon":i[u"经度"],"geoLat":i[u"纬度"]}
            # value=(i[u"经度"],i[u"纬度"])
            # sql=  'INSERT INTO '+dataTableName+'(geom) VALUES(ST_SetSRID(ST_MakePoint(%s, %s), 4326));'
            sql="INSERT INTO "+dataTableName+" VALUES (%(id)s,%(name)s,%(lon)s, %(lat)s, %(division)s,ST_SetSRID(ST_MakePoint(%(geoLon)s, %(geoLat)s), 3857));"
            cur.execute(sql,value)
        conn.commit()
        conn.close()
    elif (filename.split('.')[-1] == 'geojson' or filename.split('.')[-1] == 'json'):
        filename = filename.replace('.', '_')
        dataTableName=username + '_' + filename
        command = "ogr2ogr -f PostgreSQL PG:'dbname=gis_database user=postgres host=localhost password=whu' " + filepath +"  -nln "+ dataTableName +" -overwrite"
        # ogr2ogr.main(["","-f", "PostgreSQL", "PG:'dbname=gis_database user=postgres host=localhost password=whu'", filepath, "-nln", dataTableName, "-overwrite"])
        os.system(command)
    # elif (filename.split('.')[-1] == 'shp'):
    #     filename = filename.replace('.', '_')
    #     dataTableName=username + '_' + filename
    #     command = "ogr2ogr -f PostgreSQL PG:'dbname=gis_database user=postgres host=localhost port=5432 password=whu' " + filepath +"  -nln "+ dataTableName +" -overwrite"
    #     print command
    #     os.system(command)

def postGisToJson(sql):
    cur.execute(sql)
    rows = cur.fetchall()
    index = cur.description
    result = []
    for i in rows:
        row={}
        for j in range(len(index)-1):
            row[index[j][0]]=str(i[j]).encode()
            jsonlist=json.dumps(row,ensure_ascii = False)
        result.append(jsonlist)
    conn.commit()
    cur.close()
    conn.close()
    return result
