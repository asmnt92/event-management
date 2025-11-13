from django.urls import path
from event_app.views import create_event,create_category,edit_event,delete_event,events,chek_or_perticipations,past_events,participate_events
urlpatterns = [
    path('create-event/',create_event,name='create-event'),
    path("create-category/",create_category, name="create-category"),
    path('update-event/<int:id>/',edit_event,name='update-event'),
    path('delete-event/<int:id>/',delete_event,name='delete-event'),
    path('events/',events,name='events'),
    path('past-events/',past_events,name='past-events'),
    path('participate-events/',participate_events,name='participate'),
    path('participant-event/<int:event_id>',chek_or_perticipations,name='participant-event'),

    
]
