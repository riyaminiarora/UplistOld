from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Location(models.Model):
    location_name=models.CharField(max_length=100)

    def __str__(self):
        return self.location_name

class Category(models.Model):
    cat_name=models.CharField(max_length=150,null=True,blank=True)
    cat_image=models.ImageField(upload_to="images/cat_images/",null=True,
            blank=True,help_text="Please upload png and jpg images")

    def __str__(self):
        return self.cat_name



class UserProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to="images/profile/",null=True,blank=True,default="images/profile/default.png")
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    phone_no =models.IntegerField(null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    info=models.CharField(max_length=400,null=True,blank=True)

    def __str__(self):
        return str(self.user)

class Postad(models.Model):
    ad_title=models.CharField(max_length=200,null=True,blank=True)
    ad_desc=models.CharField(max_length=500)
    ad_location=models.ForeignKey(Location,blank=True,null=True,on_delete=models.CASCADE)
    ad_category=models.ForeignKey(Category,blank=True,null=True,on_delete=models.CASCADE)
    ad_price=models.IntegerField(null=True,blank=True)
    ad_postedby=models.ForeignKey(User,on_delete=models.CASCADE)
    ad_image1=models.ImageField(upload_to="images/ad_images/",null=True,blank=True)
    ad_image2=models.ImageField(upload_to="images/ad_images/",null=True,blank=True)
    ad_image3 = models.ImageField(upload_to="images/ad_images/", null=True, blank=True)
    ad_postedon=models.DateTimeField(default=datetime.now)
    ad_phoneno=models.BigIntegerField(null=True,blank=True)
    ad_status=models.IntegerField(null=True,blank=True,default=1)

    def __str__(self):
        return self.ad_title

class Message(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    reciever=models.ForeignKey(User,on_delete=models.CASCADE,related_name="reciever")
    ad_id=models.ForeignKey(Postad,on_delete=models.CASCADE,related_name="sender")
    sub=models.CharField(max_length=200,blank=True,null=True)
    msg=models.CharField(max_length=500,blank=True,null=True)
    posted_date=models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.msg
