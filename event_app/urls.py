from django.urls import path
from event_app.views import create_event,edit_event,delete_event,register_participant,home_page,events,dashboard
urlpatterns = [
    path('create-event/',create_event,name='create-event'),
    path('update-event/<int:id>/',edit_event,name='update-event'),
    path('delete-event/<int:id>/',delete_event,name='delete-event'),
    path('register-participant/',register_participant,name='register-participant'),
    path('event-management/',home_page,name='event-management'),
    path('events-show/',events,name='events-show'),
    path('dashboard/',dashboard,name='dashboard'),
    
]
