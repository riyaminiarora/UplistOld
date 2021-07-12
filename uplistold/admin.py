from django.contrib import admin
from . models import Postad,Category,Location,UserProfile,Message
# Register your models here.
admin.site.register(Postad)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(UserProfile)
admin.site.register(Message)