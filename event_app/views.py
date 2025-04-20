from django.shortcuts import render,redirect
from django.http import HttpResponse
from event_app.forms import EventForm,EventCategoryModelForm,ParticipantModelForm
from event_app.models import Event
from django.contrib import messages
from datetime import datetime,timedelta

# Create your views here.
def create_event(request):
    category_form=EventCategoryModelForm()
    event_form=EventForm()

    if request.method =='POST':
        category_form=EventCategoryModelForm(request.POST)
        event_form=EventForm(request.POST)
        
        if category_form.is_valid() and event_form.is_valid():
        
            category= category_form.save()
            event=event_form.save(commit=False)
            event.category=category
            event.save()

            messages.success(request,'Add Event Successfully')
            return redirect('create-event')


    context={
        'category_form':category_form,
        'event_form':event_form,

    }
    return render(request,'register_form/create-event.html',context)


def register_participant(request):
    participant=ParticipantModelForm()

    if request.method=='POST':
        participant=ParticipantModelForm(request.POST)

        if participant.is_valid():
            participant.save()
            messages.success(request,'Registered Successfully')
            return redirect('register-participant')
    context={
        'participant_form':participant,
    }

    return render(request,'register_form/register-participant.html',context)


def home_page(request):
    
    events=Event.objects.filter(date__gt=datetime.now().date()).order_by('date')
    d=datetime.combine(events.first().date,events.first().time)

    d=d-datetime.now()
    context={
        'page':'home',
        'events':events,
        'd':d,
    }
    return render(request,'home_page/home.html',context)