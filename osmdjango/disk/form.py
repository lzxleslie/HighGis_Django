#! /usr/bin/python
#coding:utf-8
from django import forms
from django.conf import settings

# form for register
class RegisterForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"username", "required": "required",}), max_length=50, error_messages={"required": "username can not be null",})
	email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}), max_length=50, error_messages={"required": "email can not be null",})
	password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}), max_length=50, error_messages={"required": "password can not be null",})

# form for login
class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "username", "required": "required",}), max_length=50, error_messages={"required": "username can not be null",})
	password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}), max_length=50, error_messages={"required": "email can not be null",})
	
#form for uploading data
class UserForm(forms.Form):
	userfile = forms.FileField()

#form for  writing cartocss
class StyleForm(forms.Form):
    userstyle = forms.CharField(widget=forms.Textarea)
    usersql = forms.CharField(widget=forms.TextInput)

