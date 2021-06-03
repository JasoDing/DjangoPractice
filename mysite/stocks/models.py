from django.db import models
from django.contrib.auth.models import User

# DataBase file here

class Account(models.Model):
    #user = models.ForeignKey(User)
    name = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Stock_lst(models.Model):
    ticker = models.CharField(max_length = 10, null = True)
    fname = models.CharField(max_length = 30, null = True)

    def __str__(self):
        return self.ticker+" - " + self.fname

class Favourite(models.Model):
    userid = models.CharField(max_length = 200, null = True)
    ticker = models.CharField(max_length = 20, null = True)
    fname = models.CharField(max_length = 30, null = True)
    open = models.FloatField(null = True)
    close = models.FloatField(null = True)
    volume = models.IntegerField(null=True)    

class watchlist(models.Model):
    userid = models.CharField(max_length = 200, null = True)
    ticker = models.CharField(max_length = 20, null = True)
    fname = models.CharField(max_length = 30, null = True)
    open = models.FloatField(null = True)
    close = models.FloatField(null = True)
    volume = models.IntegerField(null=True)
    
class RecentStockData(models.Model):
    ticker = models.CharField(max_length = 10, null = True)
    fname = models.CharField(max_length = 30, null = True)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    description = models.TextField()
    open = models.FloatField(null = True)
    high = models.FloatField(null = True)
    low = models.FloatField(null = True)
    close = models.FloatField(null = True)
    volume = models.IntegerField(null=True)

    def __str__(self):
        return self.ticker+" - " + self.date


class Temp_histroy1(models.Model):
    ticker = models.CharField(max_length = 10, null = True)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    close = models.FloatField(null = True)
    high = models.FloatField(null = True)
    low = models.FloatField(null = True)
    open = models.FloatField(null = True)
    volume = models.IntegerField(null=True)

    def __str__(self):
        return self.ticker+" - " + str(self.date)

class contactinfo(models.Model):
    name = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)
    subject = models.CharField(max_length = 200, null = True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject+" - " + self.name
