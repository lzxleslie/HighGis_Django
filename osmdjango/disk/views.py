#!/usr/bin/python
#-*-coding:utf-8-*-
import mapnik
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,render_to_response, redirect
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from disk.models import User_import_data, User
from django.contrib.auth.hashers import make_password
from tile import *
import ModestMaps
from PIL import Image
import json
from editTileConfig import *
import dataProcess
import dataBase
from cartocss2xml import *
import tilelist
from form import *
from post2table import *

TILECONFIG = None

def upload(request):
    table = None
    if request.method == "POST":
        # use forms.Form
        uf = UserForm(request.POST,request.FILES)
        sf = StyleForm(request.POST)
        print "uf is " + str(uf.is_valid())
        print "sf is " + str(sf.is_valid())

        # make formdata ok
        if uf.is_valid():
            userform(uf, request)
        elif sf.is_valid():
            styleform(sf, request)
            table = post2table(sf.cleaned_data['usersql'])

        return table

def tile(request,layer,z,y,x,extension):
    if TILECONFIG == None:
        return
    #pre-edit tileStacheConfig file
    content = getTile(layer,extension,x,y,z,TILECONFIG)
    if extension == 'png':
        response = HttpResponse(content_type="image/png")
        img=Image.open(content)
        img.save(response, 'png')
    else :
        # geojson format
        jsonFile = open(content)
        stmp = json.load(jsonFile)
        response = HttpResponse(json.dumps(stmp, ensure_ascii=False), content_type="application/json")
    return response
def tilelistbyregion(request):
    myData={"padding":0,"bbox":(52.55,13.28,52.46,13.51),"layer":"osm","extension":"png","filename":"","filetype":False}
    zooms=["12","13"]
    fileurllist=tilelist(myData,zooms)
    return HttpResponse(fileurllist)
def main(request):
    if request.user.is_authenticated():
        table = upload(request)

    # global tilestacheFile
    global TILECONFIG
    TILECONFIG = addLayer2tileConfig(request)

    print locals()
    return render(request, 'index.html', locals())
def config_edit(s):
    editTileConfig.config['layers']['user']['provider']['mapfile']=s

def userform(fileform, request):
    username = request.user.username
    userfile = fileform.cleaned_data['userfile']
    user = User_import_data()
    user.username = username
    user.userfile = userfile
    user.save()
    filepath='media/upload/data/'+userfile.name.encode("utf-8")
    dataBase.dataToPostGis(filepath, username,userfile.name.encode("utf-8"))
    # repdata=dataProcess.dataprocess(filepath)

def styleform(styleform, request):
    cartocss = styleform.cleaned_data['userstyle']
    sql = styleform.cleaned_data['usersql']
    cartocss2xml(cartocss, sql, request)

def register(request):
    try:
        if request.method == 'POST':
            regForm = RegisterForm(request.POST)
            if regForm.is_valid():
                # register
                user = User.objects.create(username=regForm.cleaned_data["username"], email=regForm.cleaned_data["email"], password=make_password(regForm.cleaned_data["password"]),)
                user.save()

                # login for redirect
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return HttpResponseRedirect("/main")
            else:
                return render(request, 'failure.html', {'reason': regForm.errors})
        else:
            regForm = RegisterForm()
    except Exception as e:
        print e
    return render(request,'reg.html',locals())

def Login(request):
    # if user logined or not
    if request.user.is_authenticated():
        return render(request, 'index.html', locals())
    try:
        if request.method == "POST":
            login_Form = LoginForm(request.POST)
            if login_Form.is_valid():
                username = login_Form.cleaned_data['username']
                password = login_Form.cleaned_data['password']
                user = authenticate(username = username, password = password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': 'fail to Login'})
                # return render(request, 'index.html', locals())
                return HttpResponseRedirect('/main/')
            else:
                return render(request, 'failure.html', {'reason': login_Form.errors})
        else:
            login_Form = LoginForm()
    except Exception as e:
        print e
    # return render(request, 'login.html', locals())

def Logout(request):
    try:
        logout(request)
    except Exception as e:
        print e
    # return render(request, 'index.html', locals())
    return HttpResponseRedirect('/main/')
