from django.db import models 
from django.contrib.auth.models import User
from PIL import Image


class Patient_Details(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    auth_token = models.CharField(max_length = 100, blank = True, null= True)
    phone = models.CharField(max_length = 10)
    address = models.TextField()
    zip_code = models.CharField(max_length = 20)
    image = models.ImageField(upload_to ='image/')
    is_link = models.BooleanField(null= True, blank=True)
    date = models.DateTimeField(null= True,blank=True)
    

