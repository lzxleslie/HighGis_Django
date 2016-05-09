#! /usr/bin/python
#-*- coding: UTF-8 -*-

import re
import psycopg2
import datetime, time
# make geometry to XY
from shapely.wkb import loads

def post2table(sql):
	try:
		conn = psycopg2.connect(database="gis_database", user="postgres", password="whu", host="localhost", port="5432")
	except :
		print "unable to connect dataBase"
	cur = conn.cursor()

	resultlist = []
	fieldlist = []
	sql = re.match(r"\((.*)\)", sql)
	if sql:
		sql = str(sql.group(1))
	else:
		print "wrong sql"
		return

	# get the rows from postgis
	cur.execute(sql)
	rows = cur.fetchmany(10)

	# get the field, and add to resultlist
	# i = geometryfield  location
	geomloc = 0
	j = 0
	for des in cur.description:
		if des[0] == 'geom' or des[0] == 'wkb_geometry':
			geomloc = j
		else:
			j = j + 1
		fieldlist.append(des[0])
	resultlist.append(fieldlist)

	for row in rows:
		templist = []
		for i in range(len(cur.description)):
			if type(row[i]) is datetime.date:
				templist.append(str(row[i]))
			elif i == geomloc:
				# tranform hex to lat_lon
				latlon = loads(row[geomloc], hex=True)
				templist.append(str(latlon))
			else:
				templist.append(row[i])
		resultlist.append(templist)
	conn.commit()
	conn.close()
	print resultlist
	return resultlist




if __name__ == '__main__':
	post2table('(select * from fengtao_traj_line_geojson) as traj')
