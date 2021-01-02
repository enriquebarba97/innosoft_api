from django.db import models

from django.db import models 
from django.contrib.auth.models import AbstractUser 
from django.utils.translation import ugettext_lazy as _ 
from django.conf import settings 
from datetime import date 
class User(AbstractUser):
  class Meta:
    ordering = ['id']
  username = models.CharField(max_length = 50, blank = True, null = True, unique = True) 
  uvus = models.CharField(unique=True, max_length=25)
  email = models.EmailField(_('email address'), blank = True)
  USERNAME_FIELD = 'uvus'
  REQUIRED_FIELDS = ['username', 'first_name','last_name','email','groups'] 
  def __str__(self): 
      return "{}".format(self.uvus) 
