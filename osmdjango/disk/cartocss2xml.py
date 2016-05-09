#!/usr/bin/python
#-*-coding:utf-8-*-
import commands
import os
def cartocss2xml(cartocss, sql, request):
	#get the username who logined
	#actually, request has the username
	if request.user.is_authenticated():
		username = request.user.username

	userXmlFile = username + ".xml"

	# replace space
	cartocss = cartocss.replace(' ', '')
	cartocss = cartocss.replace('\n', '')
	cartocss = cartocss.replace('\r', '')

	staticPath = '/home/whu/projects/osmdjango/'
	filepath = os.path.join(staticPath, "media/cartocssMaker/app.js")
	newfilepath = os.path.join(staticPath,"media/cartocssMaker/cartocss2xml.js")

	# add cartocss style
	start = " var style = " +"'"+ cartocss +"'" + ";" + "\n"
	# define xml - file's name
	start = start + "var userXmlFile = " + "'"+userXmlFile + "'"+';' + "\n"
	# add sql
	start = start + " var sql = " +"'"+ sql +"'" + ";" + "\n"

	try:
		f = open(filepath, "r+")
	except :
		print "js file is not found"
		return
	content = f.read()
	style_pos = content.find("var style")
	f.close()
	if style_pos != -1:
		content = content[:style_pos] + start + content[style_pos+9:]
		f = open(newfilepath, "w+")
		f.write(content)
		f.close()
	try:
		res = commands.getoutput('node /home/whu/projects/osmdjango/media/cartocssMaker/cartocss2xml.js')
		print res
	except Exception, e:
		print e
