from django.db import models

# Create your models here.

class Event(models.Model):
    name=models.CharField(max_length=250)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    location=models.CharField(max_length=250)
    category=models.ForeignKey('Category',related_name='events',on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return self.name


class Participant(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    events=models.ManyToManyField(Event,related_name='Participants')

    def __str__(self):
        return self.name



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
        return self.category_name

