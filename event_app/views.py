from django.shortcuts import render,redirect
from django.http import HttpResponse
from event_app.forms import EventForm,EventCategoryModelForm,AssetForm
from event_app.models import Event,Category
from django.contrib import messages
from datetime import datetime
from django.db.models import Q, Prefetch,Count
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import permission_required,login_required,user_passes_test


# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def check_participant(user,event_id):
    return user.events.filter(id=event_id)

def is_user(user):
    return user.groups.filter(name='User').exists()

@login_required(login_url='users:sign-in')
@permission_required('event_app.add_event',login_url='guest-page')
def create_event(request):
    if Category.objects.exists():
        event_form=EventForm()
        event_image=AssetForm()
        if request.method =='POST':
            event_form=EventForm(request.POST)
            event_image=AssetForm(request.POST,request.FILES)
            
            if  event_form.is_valid() and event_image.is_valid():

                event=event_form.save()
                event_asset=event_image.save(commit=False)
                event_asset.event=event
                event_asset.save()


                messages.success(request,'Add Event Successfully')

        role='Guest'
        if request.user.is_authenticated:
            if is_admin(request.user):
                role='Admin'
            elif is_organizer(request.user):
                role='Organizer'

                
        context={
            'forms':event_form,
            'forms_image':event_image,
            'page':'create-event',
            'role':role

        }
        return render(request,'register_form/create-event.html',context)
    return redirect('create-category')

def check_exits_category(category_name):
    return Category.objects.filter(category_name=category_name).exists()


@login_required(login_url='users:sign-in')
@permission_required('event_app.add_category',login_url='guest-page')
def create_category(request):
    form=EventCategoryModelForm()
    if request.method=='POST':
        form=EventCategoryModelForm(request.POST)
        if form.is_valid():
            category=form.save(commit=False)
            if not check_exits_category(category.category_name):
                category.save()
                messages.success(request,'Add Category Successfully')
                return redirect('create-category')
            messages.error(request,'This category already exits')
    role=''
    if request.user.is_authenticated:
        if is_admin(request.user):
            role='Admin'
        elif is_organizer(request.user):
            role='Organizer'

    context={
        'forms':form,
        'page':'create-category',
        'role':role,

    }
    return render(request,'register_form/create-category.html',context)


@login_required(login_url='users:sign-in')
@permission_required('event_app.change_event',login_url='guest-page')
def edit_event(request,id):
    event=Event.objects.get(id=id)
    print(id)
    print(event)

    event_form=EventForm(instance=event)
    event_image=AssetForm(instance=event.asset)

 
    if request.method =='POST':
        event_form=EventForm(request.POST,instance=event)
        event_image=AssetForm(request.POST,request.FILES,instance=event.asset)
        
        if  event_form.is_valid() and event_image.is_valid():
            event_form.save()
            event_image.save()
            messages.success(request,'Successfully Update Event ')

    role=''
    if request.user.is_authenticated:
        if is_admin(request.user):
            role='Admin'
        elif is_organizer(request.user):
            role='Organizer'

        
    context={
        'forms':event_form,
        'forms_image':event_image,
        'page':'update-event',
        'role':role,

    }
    return render(request,'register_form/create-event.html',context)


@login_required(login_url='users:sign-in')
@permission_required('event_app.delete_event',login_url='guest-page')
def delete_event(request,id):
    Event.objects.get(id=id).delete()
    messages.success(request,f'id-->>{id} Event Delete Successfully')
    return redirect('events')


# for all users/guest
def events(request):
    category_get = request.GET.get('category', 'all')
    search = request.GET.get('search','all')
    now = datetime.now()
    event_categorys = Category.objects.all().only('category_name').distinct()
    events = Event.objects.select_related('asset').prefetch_related(Prefetch('category', queryset=Category.objects.only('category_name')),'participants').annotate(total_participants=Count('participants')).filter(
        Q(date__gt=now.date()) |
        Q(date=now.date() , time__gte=now.time())
    ).order_by('date','time')


    if category_get != 'all':
        events = events.filter(category__category_name=category_get)

    if search != 'all':
        events = events.filter(
            Q(title__icontains=search) |
            Q(category__category_name__icontains=search)
        ).distinct()

    role='Guest'
    if request.user.is_authenticated:
        if is_admin(request.user):
            role='Admin'
        elif is_organizer(request.user):
            role='Organizer'


            
    context = {
        'event_categorys': event_categorys,
        'events': events,
        'page': "events",
        'role':role,
        
    }

    return render(request, 'events/event_list.html', context) #home_page/events

# for all users/guest
def past_events(request):
    category_get = request.GET.get('category', 'all')
    search = request.GET.get('search','all')
    now = datetime.now()
    event_categorys = Category.objects.all().only('category_name').distinct()
    events = Event.objects.select_related('asset').prefetch_related(Prefetch('category', queryset=Category.objects.only('category_name')),'participants').annotate(total_participants=Count('participants')).filter(
        Q(date__lt=now.date()) |
        Q(date=now.date() , time__lte=now.time())
    ).order_by('-date','-time')


    if category_get != 'all':
        events = events.filter(category__category_name=category_get)

    if search != 'all':
        events = events.filter(
            Q(title__icontains=search) |
            Q(category__category_name__icontains=search)
        ).distinct()

    role='Guest'
    if request.user.is_authenticated:
        if is_admin(request.user):
            role='Admin'
        elif is_organizer(request.user):
            role='Organizer'


            
    context = {
        'event_categorys': event_categorys,
        'events': events,
        'page': "past-events",
        'role':role,
        
    }

    return render(request, 'events/event_list.html', context) #home_page/events


@login_required(login_url='users:sign-in')
def chek_or_perticipations(request,event_id):

    event=Event.objects.get(id=event_id)

    if check_participant(request.user,event_id):
        messages.warning(request,'You allready participant in this event')
        return redirect('events')
    event.participants.add(request.user)
    event.save()
    return redirect('events')

@login_required(login_url='Users:sign-in')
@user_passes_test(is_user,login_url='guest-page')
def participate_events(request):

    category_get = request.GET.get('category', 'all')
    search = request.GET.get('search','all')
    now = datetime.now()
    event_categorys = Category.objects.all().only('category_name').distinct()
    events = Event.objects.select_related('asset').prefetch_related(Prefetch('category', queryset=Category.objects.only('category_name')),'participants').annotate(total_participants=Count('participants')).filter(
        Q(participants=request.user),
        Q(date__gt=now.date()) |
        Q(date=now.date() , time__gte=now.time())
    ).order_by('date','time')


    if category_get != 'all':
        events = events.filter(category__category_name=category_get)

    if search != 'all':
        events = events.filter(
            Q(title__icontains=search) |
            Q(category__category_name__icontains=search)
        ).distinct()


            
    context = {
        'event_categorys': event_categorys,
        'events': events,
        'page': "participate",
        'role':'User',
        
    }

    return render(request, 'events/event_list.html', context)
