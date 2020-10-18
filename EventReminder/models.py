from django.db import models
 
class User(models.Model):
    userName     =      models.CharField(max_length=30,blank=False)
    password     =      models.CharField(max_length = 30,blank=False)
    email        =      models.EmailField(max_length=254,blank=False)
    verifiedUser =      models.BooleanField(default=False,blank=False)

class EventReminder(models.Model):
    userId          =     models.ForeignKey(User, on_delete = models.CASCADE)
    recipientMail   =     models.EmailField(max_length=254,blank=False)
    createdDate     =     models.DateTimeField(blank=False)
    messageDetail   =     models.CharField(max_length = 100,blank=False)
    triggerDateTime =     models.DateTimeField(blank=False)
    EventProgress   =     models.CharField(max_length = 1,blank=False) # P in progress, U untouched , F finish , E error