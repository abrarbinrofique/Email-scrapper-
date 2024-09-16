from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Scrapping(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      url=models.URLField()
      scrapping_limit=models.IntegerField(default=0)

   

class History(models.Model):
    url_list=models.CharField(max_length=5000)
    email_list=models.CharField(blank=True,null=True,max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    scrape_time=models.DateTimeField(auto_now_add=True)


