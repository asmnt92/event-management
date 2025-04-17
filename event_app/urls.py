from django.urls import path
from event_app.views import create_event,register_participant
urlpatterns = [
    path('create-event/',create_event,name='create-event'),
    path('register-participant/',register_participant,name='register-participant'),
    
]
