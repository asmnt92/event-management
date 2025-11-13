from django.shortcuts import render
from event_app.models import Event,Asset, Category
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from event_app.views import is_admin,is_organizer
from django.contrib.auth.models import User
from event_app.models import Event



# Create your views here.

# test view 
# def guest_view(request):
#     from datetime import datetime

#     now = datetime.now()
#     events = Event.objects.prefetch_related('category').filter(
#         Q(date__gt=now.date()) |  
#         Q(date=now.date(), time__gt=now.time())  
#     ).order_by('date', 'time')
#     print(events)
#     print(events.first())
#     context={
#         'event':events.first(),
#         'event2':events.last(),
#         'category':events.first().category.all(),
#         'category2':events.last().category.all()
#     }
#     return render(request,'guest/guest-page.html',context)

# query optimize view 
def guest_view(request):
    now = datetime.now()

    # Filter upcoming events
    events = (
        Event.objects.prefetch_related('category')
        .filter(Q(date__gt=now.date()) | Q(date=now.date(), time__gt=now.time()))
        .order_by('date', 'time')
    )

    # Avoid multiple DB hits
    first_event = events.first()
    last_event = events.last()

    # Prepare categories safely
    category = first_event.category.all() if first_event else []
    category2 = last_event.category.all() if last_event else []

    role='Guest'
    if request.user.is_authenticated:
        if is_admin(request.user):
            role='Admin'
        elif is_organizer(request.user):
            role='Organizer'

  

    context = {
        'event': first_event,
        'event2': last_event,
        'category': category,
        'category2': category2,
        'role':role,
        'page':'guest-page'
    }
    return render(request, 'guest/guest-page.html', context)


def features(request):
    active_count = User.objects.filter(is_active=True).count()
    past_event_count=Event.objects.filter()

    if active_count >= 1_000_000:
        convert_count = f"{active_count/1_000_000:.1f}M+"
    elif active_count >= 1_000:
        convert_count = f"{active_count/1_000:.1f}K+"
    else:
        convert_count = f"{active_count}+"

    role='Guest'
    if request.user.is_authenticated:
        if is_admin(request.user):
            role='Admin'
        elif is_organizer(request.user):
            role='Organizer'

    context={
        'active_count':convert_count,
        'page':'features',
        'role':role,
    }
    return render(request,'guest/features.html',context)





def contact_page(request):

    role='Guest'
    if request.user.is_authenticated:
        if is_admin(request.user):
            role='Admin'
        elif is_organizer(request.user):
            role='Organizer'

    context = {
        'role':role,
        'page':'contact'
    }
    
    return render(request,'guest/contact-page.html',context)