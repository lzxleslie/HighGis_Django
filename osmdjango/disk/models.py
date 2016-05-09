from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User_import_data(models.Model):
    username = models.CharField(max_length = 100)
    userfile = models.FileField(upload_to = 'upload/data')

    def __unicode__(self):
        return self.username
	

class User(User):
	mobile = models.CharField(max_length = 11, blank = True, null = True, unique = True)

	def __unicode__(self):
		return self.username
