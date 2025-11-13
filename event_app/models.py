from django.db import models
from django.contrib.auth.models import  User

# Create your models here.

class Event(models.Model):
    title=models.CharField(max_length=250)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    location=models.CharField(max_length=250)
    category=models.ManyToManyField('Category',related_name='events')
    participants=models.ManyToManyField(User,related_name='events',blank=True)

    def __str__(self):
        return self.title


class Asset(models.Model):
    event=models.OneToOneField(Event,on_delete=models.CASCADE,related_name='asset')
    event_image=models.ImageField(upload_to='event_asset/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    last_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event.title

    


class Category(models.Model):
    EVENT_CATEGORIES = [
    ("CONFERENCE", "Conference"),
    ("WORKSHOP", "Workshop"),
    ("WEBINAR", "Webinar"),
    ("MEETUP", "Meetup"),
    ("CONCERT", "Concert"),
    ("FESTIVAL", "Festival"),
    ("SPORTS", "Sports"),
    ("CHARITY", "Charity"),
    ("BUSINESS", "Business"),
    ("BIRTHDAY", "Birthday"),
    ("WEDDING", "Wedding"),
    ]

    
    category_name=models.CharField(max_length=100,choices=EVENT_CATEGORIES,default='CONFERENCE') 
    category_description=models.TextField()

    def __str__(self):
        return self.get_category_name_display()

