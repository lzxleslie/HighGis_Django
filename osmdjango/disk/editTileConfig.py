#!/usr/bin/python
#-*-coding:utf-8-*-
#将配置文件作为全局变量便于实时修改
import json

def addLayer2tileConfig(request):
	configFile=open('static/config/tile.cfg')
	config=json.load(configFile)

	if request.user.is_authenticated():
		userXmlFile = request.user.username + ".xml"
		xmlFilePath = "/home/whu/projects/osmdjango/media/upload/style/" + userXmlFile
		config[u'layers'][unicode(request.user.username)] = {}
		config[u'layers'][unicode(request.user.username)] [u"provider"] = {}
		config[u'layers'][unicode(request.user.username)] [u"provider"][u"name"] = u"mapnik"
		config[u'layers'][unicode(request.user.username)] [u"provider"][u"mapfile"] = unicode(xmlFilePath)
		config[u'layers'][unicode(request.user.username)] [u"projection"]= u"spherical mercator"
	else:
		print "user is not authenticated"

	print config
	return config
