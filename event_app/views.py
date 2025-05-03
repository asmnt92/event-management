from django.shortcuts import render,redirect
from django.http import HttpResponse
from event_app.forms import EventForm,EventCategoryModelForm,ParticipantModelForm
from event_app.models import Event,Category,Participant
from django.contrib import messages
from datetime import datetime
from django.db.models import Q, Count, Max, Min, Avg

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
        'page':'add-event',

    }
    return render(request,'register_form/create-event.html',context)

def edit_event(request,id):
    event=Event.objects.get(id=id)
    print(id)
    print(event)
    category_form=EventCategoryModelForm(instance=event.category)
    event_form=EventForm(instance=event)

    if request.method =='POST':
        category_form=EventCategoryModelForm(request.POST,instance=event.category)
        event_form=EventForm(request.POST,instance=event)
        
        if category_form.is_valid() and event_form.is_valid():
        
            category= category_form.save()
            event=event_form.save(commit=False)
            event.category=category
            event.save()

            messages.success(request,f'id-->>{id} Event update Successfully')
            return redirect('dashboard')


    context={
        'category_form':category_form,
        'event_form':event_form,
        'page':'update-event',

    }
    return render(request,'register_form/create-event.html',context)

def delete_event(request,id):
    event=Event.objects.get(id=id).delete()
    messages.success(request,f'id-->>{id} Event Delete Successfully')
    return redirect('dashboard')

def register_participant(request):
    participant=ParticipantModelForm()

    if request.method=='POST':
        participant=ParticipantModelForm(request.POST)

        if participant.is_valid():
            participant.save()
            messages.success(request,'Registered Successfully')
            # return redirect('register-participant')
    context={
        'participant_form':participant,
        'page':'Register-participant',
    }

    return render(request,'register_form/register-participant.html',context)


def home_page(request):
    
    events=Event.objects.filter(date__gt=datetime.now().date()).order_by('date')
    if events:
        event=events.first()
        dt=event.date
        dm=event.time
        now=datetime.now()
        if dt> now.date():
            day=dt-now.date()
        hour=abs(dm.hour-now.hour)
        minute=abs(dm.minute-now.minute)
        context={
            'page':'home',
            'events':event,
            'day':day.days,
            'hour':hour,
            'minute':minute, 
            }
        return render(request,'home_page/home.html',context)
    context={
            'page':'home',
            'events':'',
            'day':0,
            'hour':0,
            'minute':0, 
            }
    return render(request,'home_page/home.html',context)

def events(request):
    category_get=request.GET.get('category','all')
    category_search=request.GET.get('search','notfound')
    categorys=Category.objects.all().distinct()
    events=Event.objects.all()
    if category_get != 'all':
        events=Event.objects.filter(category=category_get)        

    if category_search != 'notfound':
        c=Category.objects.filter(category_name__icontains=category_search)
        e=Event.objects.filter(name__icontains=category_search)

        if c and e:
            categorys=c
            events=e
        elif c:
            categorys=c
            events=[]
            for category in categorys:
                for event in category.events:
                    events.append(event)
        elif e:
            events=e
            categorys=[]
            for event in events:
                categorys.append(event.category)
                
            
    context={
        'categorys':categorys,
        'events':events,
        'page':'events'
    }

    return render(request,'home_page/events.html',context)

def dashboard(request):
    search=request.GET.get('search','')
    query=request.GET.get('query','')
    total_p=Participant.objects.all().count()
    events=Event.objects.all().order_by('-date','-time')
    
    upcoming_events=0
    past_events=0
    today_events=[]
    upcom_events=[]
    pasts_events=[]
    now=datetime.now()
    for event in events:
        date=datetime.combine(date=event.date,time=event.time)
        if now>date:
            past_events+=1
            pasts_events.append(event)
        else:
            upcoming_events+=1
            upcom_events.append(event)
        if event.date==now.date() and event.time >= now.time() :
            today_events.append(event)

    count={
        'total_participant':total_p,
        'total_events':len(events),
        'upcomming_events':upcoming_events,
        'past_events':past_events,
        }

    if search :
        events=Event.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
    # upcoming_events=Event.objects.filter(date__gte=d.date()).count()
    # past_events=Event.objects.filter(date__lte=d.date(),time__lt=d.time()).count()

    if query:
        if query=='participan':
            pass
        elif query=='upcomming':
            events=upcom_events
        elif query=='past':
            events=pasts_events
        
    

    context={
        'page':'dashboard',
        'count':count,
        'today_events':today_events,
        'events':events,
    }
    return render(request,'dashboard/dashboard.html',context)